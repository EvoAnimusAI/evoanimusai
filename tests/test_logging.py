import logging
import io
import pytest
from utils import logging as utils_logging

@pytest.fixture
def caplog_stream():
    import logging
    log_stream = io.StringIO()
    handler = logging.StreamHandler(log_stream)
    logger = logging.getLogger("evoai.utils.logging")
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    yield log_stream
    logger.removeHandler(handler)

def test_log_event_logs_message(caplog_stream):
    utils_logging.log_event("test_event", {"foo": "bar"})
    log_contents = caplog_stream.getvalue()
    assert "Evento: test_event" in log_contents
    assert "foo" in log_contents
    assert "bar" in log_contents

def test_log_event_with_no_details(caplog_stream):
    utils_logging.log_event("simple_event")
    log_contents = caplog_stream.getvalue()
    assert "Evento: simple_event" in log_contents
