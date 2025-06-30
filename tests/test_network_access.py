# tests/test_network_access.py

import unittest
from unittest.mock import patch, MagicMock
from core.network_access import NetworkAccess
from typing import Any


class TestNetworkAccess(unittest.TestCase):
    """
    Test suite for the NetworkAccess class ensuring correctness, robustness,
    and compliance with expected behaviors.
    """

    def setUp(self) -> None:
        """Initialize NetworkAccess instance before each test."""
        self.net_access = NetworkAccess(master_key="test_master_key", verbose=False)

    def test_authenticate_success(self) -> None:
        """Authenticate should return True with correct key."""
        self.net_access.master_key = "correct_key"
        self.assertTrue(self.net_access.authenticate("correct_key"))

    def test_authenticate_failure(self) -> None:
        """Authenticate should return False with incorrect key."""
        self.net_access.master_key = "correct_key"
        self.assertFalse(self.net_access.authenticate("wrong_key"))

    def test_authenticate_invalid_type(self) -> None:
        """Authenticate should fail gracefully with non-string input."""
        self.assertFalse(self.net_access.authenticate(123))  # type: ignore

    def test_search_web_valid_query(self) -> None:
        """Search web should return correctly formatted DuckDuckGo URL."""
        query = "symbolic AI"
        url = self.net_access.search_web(query)
        expected_url = "https://duckduckgo.com/?q=symbolic+AI"
        self.assertEqual(url, expected_url)

    def test_search_web_invalid_query(self) -> None:
        """Search web should return empty string for invalid input."""
        self.assertEqual(self.net_access.search_web(""), "")
        self.assertEqual(self.net_access.search_web("    "), "")

    @patch("core.network_access.requests.get")
    def test_fetch_page_success(self, mock_get: MagicMock) -> None:
        """fetch_page should return cleaned text content on success."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "<html><body>Test content</body></html>"
        mock_get.return_value = mock_response

        content = self.net_access.fetch_page("https://example.com")
        self.assertIn("Test content", content)

    @patch("core.network_access.requests.get")
    def test_fetch_page_http_error(self, mock_get: MagicMock) -> None:
        """fetch_page should handle HTTP error status codes gracefully."""
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = Exception("404 Not Found")
        mock_get.return_value = mock_response

        result = self.net_access.fetch_page("https://example.com")
        self.assertTrue(result.startswith("❌ HTTP error") or "Unexpected error" in result)

    def test_fetch_page_invalid_url(self) -> None:
        """fetch_page should return error message for invalid URLs."""
        invalid_url = "ftp://invalid-url.com"
        result = self.net_access.fetch_page(invalid_url)
        self.assertTrue(result.startswith("❌ Invalid URL"))

    @patch.object(NetworkAccess, "fetch_page", return_value="Valid content from page.")
    def test_learn_from_url_success(self, mock_fetch: MagicMock) -> None:
        """learn_from_url should store content in knowledge_base for valid fetch."""
        topic = "TestTopic"
        self.net_access.learn_from_url("https://valid.url", topic)
        self.assertIn(topic.lower(), self.net_access.knowledge_base)
        self.assertEqual(self.net_access.knowledge_base[topic.lower()], "Valid content from page.")

    @patch.object(NetworkAccess, "fetch_page", return_value="❌ Error fetching page")
    def test_learn_from_url_failure(self, mock_fetch: MagicMock) -> None:
        """learn_from_url should not store content if fetch failed."""
        topic = "ErrorTopic"
        self.net_access.learn_from_url("https://invalid.url", topic)
        self.assertNotIn(topic.lower(), self.net_access.knowledge_base)

    def test_learn_from_url_invalid_topic(self) -> None:
        """learn_from_url should handle invalid topics gracefully."""
        self.net_access.learn_from_url("https://valid.url", "")
        self.assertNotIn("", self.net_access.knowledge_base)

    def test_summarize_topic_success(self) -> None:
        """summarize_topic should return a summary string if content exists."""
        long_text = (
            "This paragraph is sufficiently long to exceed the minimum length requirement for summarization "
            "and contains multiple sentences so it won't be split into shorter fragments."
        )
        self.net_access.knowledge_base["topic"] = long_text
        summary = self.net_access.summarize_topic("topic")
        self.assertIsInstance(summary, str)
        self.assertTrue(summary.startswith("- "))

    def test_summarize_topic_no_content(self) -> None:
        """summarize_topic should return warning message if topic missing."""
        result = self.net_access.summarize_topic("nonexistent")
        self.assertEqual(result, "⚠️ Topic not found.")

    def test_summarize_topic_invalid_topic(self) -> None:
        """summarize_topic should return warning on invalid topic input."""
        self.assertEqual(self.net_access.summarize_topic(""), "⚠️ Invalid topic specified.")
        self.assertEqual(self.net_access.summarize_topic(None), "⚠️ Invalid topic specified.")  # type: ignore


if __name__ == "__main__":
    unittest.main()
