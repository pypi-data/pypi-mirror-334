from pytest import CaptureFixture, MonkeyPatch
from msfpatterns.cli import main


def test_cli_generate_pattern(
    capsys: CaptureFixture[str], monkeypatch: MonkeyPatch
) -> None:
    """Test the CLI pattern generation command"""
    monkeypatch.setattr("sys.argv", ["msfpatterns", "16"])

    main()

    captured = capsys.readouterr()
    assert len(captured.out.strip()) == 16  # Ensure output is correct length


def test_cli_find_offset_valid(
    capsys: CaptureFixture[str], monkeypatch: MonkeyPatch
) -> None:
    """Test finding an offset from a known pattern"""
    monkeypatch.setattr("sys.argv", ["msfpatterns", "256", "-q", "Ab0A"])

    main()

    captured = capsys.readouterr()
    assert captured.out == "[*] Found 1 occurrence at offset: 30\n"


def test_cli_find_offset_not_found(
    capsys: CaptureFixture[str], monkeypatch: MonkeyPatch
) -> None:
    """Test searching for a non-existent pattern"""
    monkeypatch.setattr("sys.argv", ["msfpatterns", "256", "-q", "XXXX"])

    main()

    captured = capsys.readouterr()
    assert captured.out == "[x] Value not found in the pattern.\n"
