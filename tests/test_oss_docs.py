"""Contract checks for OSS documentation and governance files."""

from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


REQUIRED_FILES = [
    "LICENSE",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "SUPPORT.md",
    "CONTRIBUTING.md",
    "docs/WHAT_THIS_TESTS.md",
    "docs/TESTING.md",
    "docs/SCREENSHOTS.md",
    "docs/OPEN_SOURCE_STANDARDS_TASKS.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.yml",
    ".github/ISSUE_TEMPLATE/simulation_proposal.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
]


def test_required_oss_files_exist():
    missing = [path for path in REQUIRED_FILES if not (ROOT / path).exists()]
    assert not missing, f"Missing OSS standards files: {missing}"


def test_readme_links_methodology_docs():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "docs/WHAT_THIS_TESTS.md" in readme
    assert "docs/TESTING.md" in readme
    assert "docs/SCREENSHOTS.md" in readme
    assert "docs/OPEN_SOURCE_STANDARDS_TASKS.md" in readme


def test_readme_scope_claim_boundary_present():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert 'It is **not** a universal "gold standard" benchmark.' in readme
    assert "| 51  | First Contact Protocol" not in readme


def test_index_links_methodology_and_has_current_live_count():
    index_html = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert "Fifty simulations live." in index_html
    assert "Forty-eight simulations live." not in index_html
    assert "docs/WHAT_THIS_TESTS.md" in index_html
    assert "docs/TESTING.md" in index_html
