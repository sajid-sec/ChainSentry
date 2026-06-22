from auditor.parser import parse_requirements

def test_basic_specifiers(tmp_path):
    f = tmp_path / "requirements.txt"
    f.write_text("requests==2.31.0\nflask>=2.0.0\nnumpy~=1.26.0\ndjango<=4.2.0\n")
    result = parse_requirements(str(f))
    assert len(result) == 4
    assert result[0] == {"name": "requests", "version": "2.31.0"}
    assert result[1] == {"name": "flask", "version": "2.0.0"}
    assert result[2] == {"name": "numpy", "version": "1.26.0"}
    assert result[3] == {"name": "django", "version": "4.2.0"}

def test_unpinned_package(tmp_path):
    f = tmp_path / "requirements.txt"
    f.write_text("click\n")
    result = parse_requirements(str(f))
    assert result[0] == {"name": "click", "version": None}

def test_comments_and_blank_lines(tmp_path):
    f = tmp_path / "requirements.txt"
    f.write_text("# this is a comment\n\nrequests==2.31.0\n")
    result = parse_requirements(str(f))
    assert len(result) == 1

def test_empty_file(tmp_path):
    f = tmp_path / "requirements.txt"
    f.write_text("")
    result = parse_requirements(str(f))
    assert result == []
