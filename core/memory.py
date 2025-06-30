import logging
from typing import Any, Optional, List

logger = logging.getLogger(__name__)

class AgentMemory:
    """
    AgentMemory provides a simple in-memory storage for agent data.

    Attributes:
        _memory_store (List[Any]): Internal list storing memory items.
    """

    def __init__(self) -> None:
        """Initialize the AgentMemory with an empty memory store."""
        self._memory_store: List[Any] = []
        logger.info("AgentMemory initialized with empty memory store.")

    def store(self, input_data: Any) -> None:
        """
        Store input data into memory.

        Args:
            input_data (Any): Data to be stored.
        """
        if input_data is None:
            logger.warning("Attempted to store None data; ignoring.")
            return

        self._memory_store.append(input_data)
        logger.debug(f"Data stored in memory: {input_data}")

    def recall(self, index: int = -1) -> Optional[Any]:
        """
        Recall data from memory by index.

        Args:
            index (int): Index of the item to recall. Defaults to last item.

        Returns:
            Optional[Any]: The recalled memory data or None if empty or invalid index.
        """
        try:
            data = self._memory_store[index]
            logger.debug(f"Recalled data from memory at index {index}: {data}")
            return data
        except IndexError:
            logger.warning(f"Recall failed: index {index} out of range.")
            return None

    def clear(self) -> None:
        """Clear all data from memory."""
        self._memory_store.clear()
        logger.info("AgentMemory cleared all stored data.")

    def summary(self) -> dict:
        """
        Returns a summary of the current memory state.

        Returns:
            dict: A summary dictionary with key statistics.
        """
        return {
            "items": len(self._memory_store)
        }

    def __len__(self) -> int:
        """Return the number of items currently stored in memory."""
        return len(self._memory_store)

    def __repr__(self) -> str:
        """Return string representation of AgentMemory state."""
        return f"<AgentMemory: {len(self._memory_store)} items>"
