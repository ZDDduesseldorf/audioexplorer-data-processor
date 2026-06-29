from app.main import run


def test_run_returns_ready_message() -> None:
    assert run() == "Audioexplorer processing app is ready"
