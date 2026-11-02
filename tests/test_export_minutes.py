
from pathlib import Path

import pytest
from docx import Document

from app.export_minutes import export_minutes


@pytest.fixture
def sample_minutes():
    return {
        "topics": ["Project progress discussion"],
        "decisions": ["Submission finalized for Friday"],
        "action_items": [
            {
                "task": "Complete documentation",
                "owner": "Priya",
                "deadline": "Thursday"
            },
            {
                "task": "Review testing",
                "owner": "",
                "deadline": ""
            }
        ]
    }


def test_txt_export(sample_minutes, tmp_path):
    output = tmp_path / "minutes.txt"

    result = export_minutes(sample_minutes, output)

    assert Path(result).exists()
    content = output.read_text(encoding="utf-8")
    assert "DISCUSSION TOPICS" in content
    assert "DECISIONS" in content
    assert "ACTION ITEMS" in content
    assert "Not assigned" in content
    assert "Not specified" in content


def test_docx_export(sample_minutes, tmp_path):
    output = tmp_path / "minutes.docx"

    result = export_minutes(sample_minutes, output)

    assert Path(result).exists()

    document = Document(output)
    content = "\n".join(p.text for p in document.paragraphs)

    assert "Meeting Minutes" in content
    assert "Discussion Topics" in content
    assert "Decisions" in content
    assert "Action Items" in content
    assert "Not assigned" in content
    assert "Not specified" in content


def test_unsupported_format(sample_minutes, tmp_path):
    output = tmp_path / "minutes.pdf"

    with pytest.raises(ValueError):
        export_minutes(sample_minutes, output)


def test_empty_minutes_export(sample_minutes, tmp_path):
    empty_minutes = {
        "topics": [],
        "decisions": [],
        "action_items": []
    }

    txt_output = tmp_path / "empty.txt"
    docx_output = tmp_path / "empty.docx"

    export_minutes(empty_minutes, txt_output)
    export_minutes(empty_minutes, docx_output)

    assert txt_output.exists()
    assert docx_output.exists()

    document = Document(docx_output)
    content = "\n".join(p.text for p in document.paragraphs)

    assert content.count("None recorded.") == 3


def test_unicode_export(tmp_path):
    minutes = {
        "topics": ["Project discussion – Bengaluru"],
        "decisions": ["Review completed ✓"],
        "action_items": []
    }

    output = tmp_path / "unicode.txt"
    export_minutes(minutes, output)

    content = output.read_text(encoding="utf-8")

    assert "Bengaluru" in content
    assert "✓" in content


def test_invalid_output_path(sample_minutes, tmp_path):
    output = tmp_path / "missing_folder" / "minutes.txt"

    with pytest.raises(OSError):
        export_minutes(sample_minutes, output)
