import pytest
from behavior.action_registry import ActionRegistry

@pytest.fixture
def registry():
    return ActionRegistry()

def test_all_actions_exist(registry):
    actions = registry.all_actions()
    assert "explore" in actions
    assert "wait" in actions

def test_is_valid_direct_and_alias(registry):
    assert registry.is_valid("explore")
    assert registry.is_valid("investigate")
    assert not registry.is_valid("nonexistent")

def test_get_description(registry):
    assert registry.get_description("advance") == "Move forward deliberately"
    assert registry.get_description("progress") == "Move forward deliberately"
    assert registry.get_description("unknown_action") == "Unknown action"

def test_register_new_action(registry):
    registry.register("observe", "Watch the environment", 0.5, ["look", "see"])
    assert registry.is_valid("observe")
    assert registry.is_valid("look")

def test_register_invalid_name(registry):
    with pytest.raises(ValueError):
        registry.register("123invalid", "Bad name")

def test_register_protected_action(registry):
    with pytest.raises(ValueError):
        registry.register("explore", "Overwrite not allowed")

def test_register_existing_action(registry):
    registry.register("scan", "Perform scan", 0.4)
    with pytest.raises(ValueError):
        registry.register("scan", "Duplicate")

def test_use_action_increments_count(registry):
    registry.use_action("explore")
    exported = registry.export_actions()
    assert exported["explore"]["usage_count"] == 1

def test_use_invalid_action_does_nothing(registry):
    assert not registry.use_action("nonexistent")
