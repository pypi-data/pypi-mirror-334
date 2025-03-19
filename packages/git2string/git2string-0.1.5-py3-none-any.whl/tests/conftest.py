import pytest

def pytest_runtest_logreport(report):
    if report.when == "call":
        if report.failed:
            print(f"❌ {report.nodeid} FAILED")
        elif report.passed:
            print(f"✅ {report.nodeid} PASSED")
