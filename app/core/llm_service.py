class MockLLMService:
    """
    A mock LLM service that simulates API calls for summarization and data extraction.
    This allows for robust, cost-free development and testing, and is designed to be
    easily swappable with a real LLM service in the future.
    """
    def analyze_text(self, text: str) -> dict:
        """
        Simulates analyzing text and returns a structured dictionary.
        Includes a special trigger to simulate an API failure for testing robustness.
        """
        if "FAIL_LLM" in text:
            raise ConnectionError("Mock LLM service was triggered to fail.")

        return {
            "summary": "This is a mock summary of the provided text, highlighting its key points and themes.",
            "structured_data": {
                "title": "A Mock Analysis",
                "topics": ["mock data", "software testing", "prototyping"],
                "sentiment": "neutral",
                "confidence": 0.95
            }
        }