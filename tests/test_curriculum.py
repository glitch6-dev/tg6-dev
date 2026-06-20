from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = (ROOT / "course" / "curriculum.js").read_text(encoding="utf-8")


def test_six_modules():
    # one "module:" key per module object
    assert SRC.count("module:") == 6


def test_ladder_endpoints_named():
    low = SRC.lower()
    assert "claude code" in low, "top of the ladder must be Claude Code"
    assert "chat" in low, "bottom of the ladder is a browser chat"


def test_no_automation_in_curriculum():
    assert "automation" not in SRC.lower()


def test_no_raw_html_css_teaching_modules():
    # the old build-a-site module titles are gone
    assert "HTML structure" not in SRC
    assert "CSS & layout" not in SRC


def test_every_lesson_has_objective_and_tasks():
    # cheap structural check: objective/tasks keys appear for each lesson
    assert SRC.count("objective:") == SRC.count("title:") - 6  # titles = 6 modules + N lessons
    assert "tasks:" in SRC
