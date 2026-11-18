
from collector.log_collector import collect_logs


def test_collect_logs():
    logs = collect_logs("logs/sample_auth.log")

    assert len(logs) == 4


def test_collect_logs_returns_list():
    logs = collect_logs("logs/sample_auth.log")

    assert isinstance(logs, list)


def test_collect_logs_ignores_empty_lines(tmp_path):
    log_file = tmp_path / "sample.log"

    log_file.write_text(
        "First log\n"
        "\n"
        "Second log\n"
    )

    logs = collect_logs(log_file)

    assert logs == ["First log", "Second log"]


def test_collect_logs_missing_file(tmp_path):
    log_file = tmp_path / "missing.log"

    logs = collect_logs(log_file)

    assert logs == []
