import pytest
from core.context_patch_handler import ContextPatchHandler

def test_safe_set_allows_existing_key():
    ctx = {"existing_key": 1}
    ContextPatchHandler.safe_set(ctx, "existing_key", 42)
    assert ctx["existing_key"] == 42

def test_safe_set_allows_safe_key():
    ctx = {}
    for key in ContextPatchHandler.SAFE_KEYS:
        ContextPatchHandler.safe_set(ctx, key, "value")
        assert ctx[key] == "value"

def test_safe_set_rejects_unauthorized_key():
    ctx = {}
    with pytest.raises(KeyError):
        ContextPatchHandler.safe_set(ctx, "unauthorized_key", 123)

def test_safe_set_rejects_non_dict_context():
    with pytest.raises(TypeError):
        ContextPatchHandler.safe_set("not_a_dict", "symbiotic_progress", 0.1)

def test_authorize_and_revoke_key():
    key = "new_key"
    assert key not in ContextPatchHandler.SAFE_KEYS
    ContextPatchHandler.authorize_key(key)
    assert key in ContextPatchHandler.SAFE_KEYS
    ContextPatchHandler.revoke_key(key)
    assert key not in ContextPatchHandler.SAFE_KEYS

def test_list_safe_keys_returns_copy():
    keys = ContextPatchHandler.list_safe_keys()
    assert isinstance(keys, set)
    keys.add("fake_key")
    # The internal SAFE_KEYS should not be affected
    assert "fake_key" not in ContextPatchHandler.SAFE_KEYS
