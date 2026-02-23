"""Race execution helpers for agent launch and score collection."""

import os
import re
import subprocess
import threading
import time


def build_agent_command(
    agent_defs,
    agent_name,
    agent_type,
    prompt,
    max_turns,
    port,
    model_override=None,
):
    """Build the CLI command to launch an agent autonomously."""
    env = {**os.environ, "VM_URL": f"http://localhost:{port}"}

    if agent_type == "claude":
        env.pop("CLAUDECODE", None)
        cmd = [
            "claude",
            "-p",
            prompt,
            "--dangerously-skip-permissions",
            "--allowedTools",
            "Bash,Read,Write,Edit,Glob,Grep",
            "--max-turns",
            str(max_turns),
        ]
        if model_override:
            cmd.extend(["--model", model_override])

    elif agent_type == "codex":
        cmd = ["codex", "exec", "--dangerously-bypass-approvals-and-sandbox"]
        if model_override:
            cmd.extend(["-c", f'model="{model_override}"'])
        cmd.append(prompt)

    elif agent_type == "gemini":
        cmd = ["gemini", "--yolo"]
        if model_override:
            cmd.extend(["-m", model_override])
        cmd.extend(["-p", prompt])

    else:
        env.pop("CLAUDECODE", None)
        cmd = [
            "claude",
            "-p",
            prompt,
            "--dangerously-skip-permissions",
            "--max-turns",
            str(max_turns),
        ]
        if model_override:
            cmd.extend(["--model", model_override])

    return cmd, env


def push_status_to_server(api_post_cb, port, action, detail, success=True):
    """Push a status/error event to the server's WebSocket via REST."""
    try:
        api_post_cb(
            port,
            "/api/race/event",
            {
                "action": action,
                "detail": detail,
                "success": success,
            },
        )
    except Exception:
        pass


def monitor_agent_log(log_path, agent_name, port, api_post_cb, stop_event):
    """Tail the agent log in real-time and push errors/status to the server."""
    seen_lines = 0
    error_patterns = [
        (r"does not exist or you do not have access", "Model not available — check your account access"),
        (r"rate.?limit|429|Too Many Requests|rateLimitExceeded", "Rate limited — retrying..."),
        (r"No capacity available", "No model capacity — server overloaded"),
        (r"authentication|unauthorized|401", "Authentication failed"),
        (r"BANKRUPT", "Agent went bankrupt"),
        (r"connection refused|ECONNREFUSED", "Server connection failed"),
        (r"timeout|ETIMEDOUT", "Request timed out"),
        (r"Reconnecting\.\.\. (\d+)/(\d+)", None),
    ]

    last_error_time = 0

    while not stop_event.is_set():
        try:
            with open(log_path, "r") as f:
                lines = f.readlines()
            new_lines = lines[seen_lines:]
            seen_lines = len(lines)

            for line in new_lines:
                line_stripped = line.strip()
                if not line_stripped:
                    continue

                for pattern, message in error_patterns:
                    if re.search(pattern, line_stripped, re.IGNORECASE):
                        now = time.time()
                        if now - last_error_time < 3:
                            break

                        if message is None:
                            m = re.search(r"Reconnecting\.\.\. (\d+)/(\d+)", line_stripped)
                            if m:
                                message = f"Reconnecting attempt {m.group(1)}/{m.group(2)}"
                        push_status_to_server(
                            api_post_cb,
                            port,
                            "agent-error",
                            f"[{agent_name}] {message}",
                            success=False,
                        )
                        last_error_time = now
                        break

        except Exception:
            pass

        stop_event.wait(1.0)


def extract_error_from_log(log_path):
    """Scan the last 50 lines of a log for common error patterns."""
    try:
        with open(log_path) as f:
            lines = f.readlines()
        tail = lines[-50:] if len(lines) > 50 else lines
        text = "".join(tail)

        patterns = [
            ("does not exist or you do not have access", "Model not available"),
            ("rate limit", "Rate limited"),
            ("Rate Limit", "Rate limited"),
            ("rateLimitExceeded", "Rate limited"),
            ("No capacity available", "No model capacity"),
            ("authentication", "Auth failed"),
            ("unauthorized", "Auth failed"),
            ("connection refused", "Server connection failed"),
            ("timeout", "Timed out"),
        ]
        for pattern, summary in patterns:
            if pattern.lower() in text.lower():
                return summary

        bankruptcy_signals = [
            r"you have gone bankrupt",
            r"you are bankrupt",
            r"your balance.*below.*-\$?50",
            r"simulation ended.*bankrupt",
            r"game over.*bankrupt",
        ]
        for sig in bankruptcy_signals:
            if re.search(sig, text, re.IGNORECASE):
                return "Went bankrupt"
        return ""
    except Exception:
        return ""


def run_agent(
    script_dir,
    agent_defs,
    api_post_cb,
    agent_name,
    agent_type,
    port,
    prompt,
    max_turns,
    model_override=None,
):
    """Run a single AI agent. Returns (agent_name, port, returncode, duration, error_summary)."""
    log_path = f"/tmp/vending-race-agent-{agent_name}.log"
    cmd, env = build_agent_command(
        agent_defs,
        agent_name,
        agent_type,
        prompt,
        max_turns,
        port,
        model_override=model_override,
    )

    start_time = time.time()
    with open(log_path, "w") as log:
        model_info = model_override or "(CLI default)"
        log.write(f"# Agent: {agent_name} (type: {agent_type})\n")
        log.write(f"# Model: {model_info}\n")
        log.write(f"# Port: {port}\n")
        log.write(f"# Command: {' '.join(cmd[:5])}...\n")
        log.write(f"# Started: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        log.write(f"{'='*60}\n\n")
        log.flush()

        display = agent_defs.get(agent_type, {}).get("display", agent_type)
        push_status_to_server(
            api_post_cb,
            port,
            "agent-start",
            f"[{agent_name}] Starting ({display}, model: {model_info})",
        )

        try:
            proc = subprocess.Popen(
                cmd,
                cwd=script_dir,
                stdout=log,
                stderr=subprocess.STDOUT,
                env=env,
                bufsize=1,
            )

            monitor_stop = threading.Event()
            monitor = threading.Thread(
                target=monitor_agent_log,
                args=(log_path, agent_name, port, api_post_cb, monitor_stop),
                daemon=True,
            )
            monitor.start()

            proc.wait()
            duration = time.time() - start_time

            monitor_stop.set()
            monitor.join(timeout=2)

            error_summary = extract_error_from_log(log_path)

            if proc.returncode == 0:
                push_status_to_server(
                    api_post_cb,
                    port,
                    "agent-complete",
                    f"[{agent_name}] Finished in {duration:.0f}s",
                )
            else:
                push_status_to_server(
                    api_post_cb,
                    port,
                    "agent-error",
                    f"[{agent_name}] Exited with code {proc.returncode}: {error_summary or 'unknown error'}",
                    success=False,
                )

            return agent_name, port, proc.returncode, duration, error_summary
        except FileNotFoundError:
            duration = time.time() - start_time
            log.write(f"\nERROR: '{cmd[0]}' binary not found!\n")
            push_status_to_server(
                api_post_cb,
                port,
                "agent-error",
                f"[{agent_name}] Binary '{cmd[0]}' not found",
                success=False,
            )
            return agent_name, port, -1, duration, f"Binary '{cmd[0]}' not found"
        except Exception as e:
            duration = time.time() - start_time
            log.write(f"\nERROR: {e}\n")
            push_status_to_server(
                api_post_cb,
                port,
                "agent-error",
                f"[{agent_name}] {e}",
                success=False,
            )
            return agent_name, port, -1, duration, str(e)


def collect_score(api_get_cb, port):
    """Collect the final score from a server."""
    score = api_get_cb(port, "/api/sim/score")
    if isinstance(score, dict) and "error" in score:
        return None
    full_score = api_get_cb(port, "/api/sim/full-score")
    if isinstance(full_score, dict) and "error" not in full_score:
        score["v2_score"] = full_score
    return score
