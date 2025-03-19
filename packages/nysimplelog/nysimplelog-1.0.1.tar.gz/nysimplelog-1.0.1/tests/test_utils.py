import logging
import os

from nysimplelog import ISO8601_Formatter, initialize_simple_logger


def test_iso8601_formatter():
    formatter = ISO8601_Formatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="Test message",
        args=(),
        exc_info=None,
    )
    time_str = formatter.formatTime(record)
    # Check if the time string is in ISO-8601 format
    assert "T" in time_str and "+" in time_str, "Should be ISO-8601 format"


def test_initialize_simple_logger(tmp_path):
    log_dir = str(tmp_path / "logs")
    logger = initialize_simple_logger(
        name="test_logger",
        log_dir=log_dir,
        level=logging.DEBUG,
        stream_handler_level=logging.INFO,
        file_handler_level=logging.WARNING,
    )

    # Check if the log file is created
    log_file = os.path.join(log_dir, "test_logger.log")
    assert os.path.exists(log_file)

    # Check if the logger works as expected
    logger.debug("Debug message")      # Not displayed
    logger.info("Info message")        # Only in file (if level allows)
    logger.warning("Warning message")  # Console and file

    with open(log_file, "r") as f:
        content = f.read()
        assert "Warning message" in content
        assert "Info message" not in content
