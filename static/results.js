// Vending Machine AI Race — Results Dashboard
// Fetches historical race results and renders a leaderboard dashboard.
(function () {
  "use strict";

  var container = document.getElementById("results-container");
  var loadingEl = document.getElementById("loading-state");
  var expandedRaceIndex = null;

  // --- Helpers ---

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }

  function formatMoney(val) {
    if (val === undefined || val === null) return "$0.00";
    var num = parseFloat(val);
    var sign = num < 0 ? "-" : "";
    return sign + "$" + Math.abs(num).toFixed(2);
  }

  function formatDate(timestamp) {
    if (!timestamp) return "Unknown";
    // Handles both ISO and "YYYY-MM-DD HH:MM:SS" formats
    var d = new Date(timestamp.replace(" ", "T"));
    if (isNaN(d.getTime())) return timestamp;
    var months = [
      "Jan",
      "Feb",
      "Mar",
      "Apr",
      "May",
      "Jun",
      "Jul",
      "Aug",
      "Sep",
      "Oct",
      "Nov",
      "Dec",
    ];
    var month = months[d.getMonth()];
    var day = d.getDate();
    var year = d.getFullYear();
    var h = d.getHours();
    var m = d.getMinutes();
    var ampm = h >= 12 ? "PM" : "AM";
    h = h % 12 || 12;
    var mins = m < 10 ? "0" + m : "" + m;
    return month + " " + day + ", " + year + " " + h + ":" + mins + " " + ampm;
  }

  function formatDuration(seconds) {
    if (!seconds || seconds <= 0) return "--";
    if (seconds < 60) return Math.round(seconds) + "s";
    var mins = Math.floor(seconds / 60);
    var secs = Math.round(seconds % 60);
    if (mins < 60) return mins + "m " + secs + "s";
    var hrs = Math.floor(mins / 60);
    mins = mins % 60;
    return hrs + "h " + mins + "m";
  }

  function getAgentTypeClass(agentType) {
    if (!agentType) return "";
    var base = agentType.split("-")[0].toLowerCase();
    if (base === "claude") return "claude";
    if (base === "codex") return "codex";
    if (base === "gemini") return "gemini";
    return "";
  }

  function getAgentColorClass(agentType) {
    var base = getAgentTypeClass(agentType);
    if (base) return "agent-color-" + base;
    return "";
  }

  function getRankMedal(rank) {
    if (rank === 1) return "\uD83E\uDD47";
    if (rank === 2) return "\uD83E\uDD48";
    if (rank === 3) return "\uD83E\uDD49";
    return "#" + rank;
  }

  function sortResults(results) {
    // Sort by final_balance descending; agents with errors go last
    var copy = results.slice();
    copy.sort(function (a, b) {
      var aErr = a.error ? 1 : 0;
      var bErr = b.error ? 1 : 0;
      if (aErr !== bErr) return aErr - bErr;
      return (b.final_balance || 0) - (a.final_balance || 0);
    });
    return copy;
  }

  function getWinner(results) {
    var sorted = sortResults(results);
    if (sorted.length === 0) return null;
    if (sorted[0].error) return null;
    return sorted[0];
  }

  // --- Render: Loading / Error / Empty ---

  function showMessage(text, isError) {
    container.replaceChildren();
    var msg = el("div", "state-message" + (isError ? " error" : ""), text);
    container.appendChild(msg);
  }

  // --- Render: Latest Race Hero ---

  function renderLatestRace(race) {
    var section = el("div", "latest-race");

    // Header
    var header = el("div", "latest-race-header");
    var title = el("h2", null, "Latest Race");
    header.appendChild(title);

    var meta = el("div", "latest-race-meta");
    var dateItem = el("span", "meta-item", formatDate(race.timestamp));
    meta.appendChild(dateItem);
    if (race.seed !== null && race.seed !== undefined) {
      var seedItem = el("span", "meta-item", "Seed: " + race.seed);
      meta.appendChild(seedItem);
    }
    var daysItem = el("span", "meta-item", race.days + " days");
    meta.appendChild(daysItem);
    header.appendChild(meta);
    section.appendChild(header);

    // Podium cards
    var podium = el("div", "latest-podium");
    var sorted = sortResults(race.results || []);

    for (var i = 0; i < sorted.length; i++) {
      var r = sorted[i];
      var card = el(
        "div",
        "podium-card" + (i === 0 && !r.error ? " winner" : ""),
      );

      var rankEl = el("div", "podium-rank", getRankMedal(i + 1));
      card.appendChild(rankEl);

      var nameEl = el("div", "podium-name " + getAgentColorClass(r.agent_type));
      nameEl.textContent = r.agent || "Unknown";
      card.appendChild(nameEl);

      if (r.error) {
        var balEl = el("div", "podium-balance", "--");
        card.appendChild(balEl);
        var errEl = el("div", "podium-error", r.error);
        card.appendChild(errEl);
      } else {
        var balance = r.final_balance || 0;
        var balEl2 = el(
          "div",
          "podium-balance" + (balance < 0 ? " negative" : ""),
        );
        balEl2.textContent = formatMoney(balance);
        card.appendChild(balEl2);

        var stats = el("div", "podium-stats");
        var profitStat = el(
          "span",
          null,
          "P/L: " + formatMoney(r.total_profit),
        );
        stats.appendChild(profitStat);
        var itemsStat = el("span", null, (r.total_items_sold || 0) + " sold");
        stats.appendChild(itemsStat);
        card.appendChild(stats);
      }

      podium.appendChild(card);
    }

    section.appendChild(podium);
    return section;
  }

  // --- Render: Race History Table ---

  function renderRaceTable(races) {
    var section = el("div", "history-section");
    var heading = el(
      "h2",
      null,
      "Race History (" +
        races.length +
        " race" +
        (races.length !== 1 ? "s" : "") +
        ")",
    );
    section.appendChild(heading);

    var table = document.createElement("table");
    table.className = "race-table";

    // Thead
    var thead = document.createElement("thead");
    var headRow = document.createElement("tr");
    var headers = ["Date", "Winner", "Seed", "Days", "Agents"];
    for (var h = 0; h < headers.length; h++) {
      var th = document.createElement("th");
      th.textContent = headers[h];
      headRow.appendChild(th);
    }
    thead.appendChild(headRow);
    table.appendChild(thead);

    // Tbody
    var tbody = document.createElement("tbody");
    tbody.id = "race-tbody";

    // Show newest first
    for (var i = races.length - 1; i >= 0; i--) {
      appendRaceRow(tbody, races[i], i);
    }

    table.appendChild(tbody);
    section.appendChild(table);
    return section;
  }

  function appendRaceRow(tbody, race, raceIndex) {
    var row = document.createElement("tr");
    row.className = "race-row";
    row.setAttribute("data-index", raceIndex);

    var winner = getWinner(race.results || []);

    // Date cell
    var tdDate = document.createElement("td");
    var expandIcon = el("span", "expand-icon", "\u25B6");
    tdDate.appendChild(expandIcon);
    var dateText = document.createTextNode(formatDate(race.timestamp));
    tdDate.appendChild(dateText);
    row.appendChild(tdDate);

    // Winner cell
    var tdWinner = document.createElement("td");
    if (winner) {
      var winnerSpan = el(
        "span",
        "winner-name " + getAgentColorClass(winner.agent_type),
      );
      winnerSpan.textContent = winner.agent;
      tdWinner.appendChild(winnerSpan);
      var winBalance = document.createTextNode(
        " " + formatMoney(winner.final_balance),
      );
      tdWinner.appendChild(winBalance);
    } else {
      tdWinner.textContent = "No winner";
    }
    row.appendChild(tdWinner);

    // Seed cell
    var tdSeed = document.createElement("td");
    tdSeed.textContent =
      race.seed !== null && race.seed !== undefined ? race.seed : "random";
    row.appendChild(tdSeed);

    // Days cell
    var tdDays = document.createElement("td");
    tdDays.textContent = race.days || "--";
    row.appendChild(tdDays);

    // Agents cell
    var tdAgents = document.createElement("td");
    var pillBox = el("div", "agent-pills");
    var agents = race.agents || [];
    var types = race.agent_types || [];
    for (var a = 0; a < agents.length; a++) {
      var typeClass = getAgentTypeClass(types[a] || agents[a]);
      var pill = el("span", "agent-pill " + typeClass, agents[a]);
      pillBox.appendChild(pill);
    }
    tdAgents.appendChild(pillBox);
    row.appendChild(tdAgents);

    // Click handler
    row.addEventListener(
      "click",
      (function (idx) {
        return function () {
          toggleRaceDetail(idx);
        };
      })(raceIndex),
    );

    tbody.appendChild(row);
  }

  function toggleRaceDetail(raceIndex) {
    var tbody = document.getElementById("race-tbody");
    if (!tbody) return;

    // Find the row and any existing detail
    var rows = tbody.querySelectorAll("tr.race-row");
    var targetRow = null;
    for (var i = 0; i < rows.length; i++) {
      if (parseInt(rows[i].getAttribute("data-index"), 10) === raceIndex) {
        targetRow = rows[i];
        break;
      }
    }
    if (!targetRow) return;

    var existingDetail = targetRow.nextElementSibling;
    var isCurrentlyExpanded =
      existingDetail && existingDetail.classList.contains("detail-row");

    // Collapse all open details
    var allDetails = tbody.querySelectorAll("tr.detail-row");
    for (var d = 0; d < allDetails.length; d++) {
      allDetails[d].parentNode.removeChild(allDetails[d]);
    }
    var allExpanded = tbody.querySelectorAll("tr.race-row.expanded");
    for (var e = 0; e < allExpanded.length; e++) {
      allExpanded[e].classList.remove("expanded");
    }

    if (isCurrentlyExpanded) {
      expandedRaceIndex = null;
      return;
    }

    // Expand this one
    targetRow.classList.add("expanded");
    expandedRaceIndex = raceIndex;

    var detailRow = document.createElement("tr");
    detailRow.className = "detail-row";
    var detailTd = document.createElement("td");
    detailTd.setAttribute("colspan", "5");

    var content = renderLeaderboard(allRaces[raceIndex]);
    detailTd.appendChild(content);
    detailRow.appendChild(detailTd);

    // Insert after targetRow
    if (targetRow.nextSibling) {
      tbody.insertBefore(detailRow, targetRow.nextSibling);
    } else {
      tbody.appendChild(detailRow);
    }
  }

  // --- Render: Leaderboard Detail ---

  function renderLeaderboard(race) {
    var wrapper = el("div", "detail-content");
    var sorted = sortResults(race.results || []);

    // Column headers
    var headerRow = el("div", "lb-header");
    var colNames = ["Rank", "Agent", "Balance", "Profit", "Items", "Duration"];
    for (var c = 0; c < colNames.length; c++) {
      headerRow.appendChild(el("span", null, colNames[c]));
    }
    wrapper.appendChild(headerRow);

    var grid = el("div", "leaderboard-grid");

    for (var i = 0; i < sorted.length; i++) {
      var r = sorted[i];
      var rank = i + 1;
      var hasError = !!r.error;
      var rankClass = "";
      if (rank === 1) rankClass = " rank-1";
      else if (rank === 2) rankClass = " rank-2";
      else if (rank === 3) rankClass = " rank-3";
      if (hasError) rankClass += " has-error";

      var entry = el("div", "lb-entry" + rankClass);

      // Rank
      entry.appendChild(el("span", "lb-rank", getRankMedal(rank)));

      // Agent name + type
      var agentInfo = el("div", "lb-agent-info");
      var nameSpan = el(
        "span",
        "lb-agent-name " + getAgentColorClass(r.agent_type),
      );
      nameSpan.textContent = r.agent || "Unknown";
      agentInfo.appendChild(nameSpan);
      var typeSpan = el(
        "span",
        "lb-agent-type " + getAgentColorClass(r.agent_type),
      );
      typeSpan.textContent = r.agent_type || "unknown";
      agentInfo.appendChild(typeSpan);
      entry.appendChild(agentInfo);

      // Balance
      if (hasError) {
        entry.appendChild(el("span", "lb-balance", "--"));
      } else {
        var balance = r.final_balance || 0;
        var balSpan = el(
          "span",
          "lb-balance " + (balance >= 0 ? "positive" : "negative"),
        );
        balSpan.textContent = formatMoney(balance);
        entry.appendChild(balSpan);
      }

      // Profit
      if (hasError) {
        entry.appendChild(el("span", "lb-profit", "--"));
      } else {
        entry.appendChild(el("span", "lb-profit", formatMoney(r.total_profit)));
      }

      // Items sold
      if (hasError) {
        entry.appendChild(el("span", "lb-items", "--"));
      } else {
        entry.appendChild(
          el("span", "lb-items", (r.total_items_sold || 0) + " sold"),
        );
      }

      // Duration
      entry.appendChild(el("span", "lb-duration", formatDuration(r.duration)));

      grid.appendChild(entry);

      // Error message row
      if (hasError) {
        var errorEntry = el("div", "lb-entry has-error");
        errorEntry.style.gridTemplateColumns = "40px 1fr";
        errorEntry.appendChild(el("span", null));
        var errMsg = el("span", "lb-error-msg");
        errMsg.textContent = r.error;
        errorEntry.appendChild(errMsg);
        grid.appendChild(errorEntry);
      }
    }

    wrapper.appendChild(grid);
    return wrapper;
  }

  // --- Main Render ---

  var allRaces = [];

  function render(races) {
    allRaces = races;
    container.replaceChildren();

    if (!races || races.length === 0) {
      showMessage(
        "No races yet. Run a race with run_race.py to see results here.",
        false,
      );
      return;
    }

    // Latest race hero
    var latestRace = races[races.length - 1];
    var latestSection = renderLatestRace(latestRace);
    container.appendChild(latestSection);

    // Full history table
    var tableSection = renderRaceTable(races);
    container.appendChild(tableSection);
  }

  // --- Fetch Data ---

  function fetchResults() {
    fetch("/api/race/results")
      .then(function (resp) {
        if (!resp.ok) {
          throw new Error("Server returned " + resp.status);
        }
        return resp.json();
      })
      .then(function (data) {
        render(data);
      })
      .catch(function (err) {
        showMessage("Failed to load race results: " + err.message, true);
      });
  }

  // --- Init ---
  fetchResults();
})();
