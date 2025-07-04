import pytest
from unittest.mock import MagicMock, patch, mock_open
from daemon import evoai_network_learning

@patch("daemon.evoai_network_learning.log_synthesis")
@patch("daemon.evoai_network_learning.log_concept")
@patch("daemon.evoai_network_learning.extract_symbolic_concepts", return_value=["AI", "Knowledge"])
@patch("daemon.evoai_network_learning.save_topic_summary")
def test_learn_from_web_success(save_mock, extract_mock, log_concept_mock, log_synthesis_mock):
    consciousness = MagicMock()
    net = MagicMock()
    net.learn_from_url.return_value = None
    net.summarize_topic.return_value = "AI is transforming knowledge synthesis"
    context = MagicMock()

    result = evoai_network_learning.learn_from_web(
        consciousness=consciousness,
        net=net,
        topic="Artificial Intelligence",
        url="https://example.com/ai",
        context=context,
        cycle=7
    )

    assert result == "AI is transforming knowledge synthesis"
    net.learn_from_url.assert_called_once_with("https://example.com/ai", "Artificial Intelligence")
    net.summarize_topic.assert_called_once_with("Artificial Intelligence")
    save_mock.assert_called_once_with("Artificial Intelligence", "AI is transforming knowledge synthesis", 7)
    extract_mock.assert_called_once_with("AI is transforming knowledge synthesis")
    context.add_concept.assert_any_call("AI", source="wiki:Artificial Intelligence")
    context.add_concept.assert_any_call("Knowledge", source="wiki:Artificial Intelligence")

@patch("daemon.evoai_network_learning.logger")
def test_learn_from_web_failure(logger_mock):
    consciousness = MagicMock()
    consciousness.evaluate_integrity.side_effect = Exception("fail")
    net = MagicMock()
    context = MagicMock()

    result = evoai_network_learning.learn_from_web(
        consciousness=consciousness,
        net=net,
        topic="Cybersecurity",
        url="https://fail.com",
        context=context,
        cycle=99
    )

    assert result is None
    logger_mock.error.assert_called_once()

def test_save_topic_summary(tmp_path):
    topic = "Cybernetics"
    summary = "Cybernetics is the science of control and communication."
    cycle = 42

    expected_filename = f"knowledge_logs/cycle_{cycle}_{topic.replace(' ', '_')}.txt"

    with patch("daemon.evoai_network_learning.os.makedirs") as makedirs_mock, \
         patch("daemon.evoai_network_learning.open", mock_open()) as m_open:
        evoai_network_learning.save_topic_summary(topic, summary, cycle)
        m_open.assert_called_once_with(expected_filename, "w", encoding="utf-8")
        handle = m_open()
        handle.write.assert_called_once_with(summary)
        
if __name__ == "__main__":
    pytest.main()
