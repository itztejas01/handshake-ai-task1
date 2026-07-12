import json
from pathlib import Path

REPORT_PATH = Path("/app/report.json")


def _load_report():
    with REPORT_PATH.open() as f:
        return json.load(f)


def test_report_exists():
    """Success criterion 1: /app/report.json exists."""
    assert REPORT_PATH.exists(), "no report.json found"


def test_total_requests():
    """Success criterion 2: total_requests matches non-empty log lines."""
    report = _load_report()
    assert (
        report["total_requests"] == 6
    ), f"total_requests is {report['total_requests']}, expected 6"


def test_unique_ips():
    """Success criterion 3: unique_ips matches distinct client IPs."""
    report = _load_report()
    assert (
        report["unique_ips"] == 3
    ), f"unique_ips is {report['unique_ips']}, expected 3"


def test_top_path():
    """Success criterion 4: top_path is the most frequently requested path."""
    report = _load_report()
    assert (
        report["top_path"] == "/index.html"
    ), f"top_path is {report['top_path']!r}, expected '/index.html'"
