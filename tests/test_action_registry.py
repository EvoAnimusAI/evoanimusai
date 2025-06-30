import pytest
from behavior.action_registry import ActionRegistry

def test_basic_registry():
    registry = ActionRegistry()
    
    assert registry.is_valid('explore')
    assert registry.is_valid('investigate')
    assert not registry.is_valid('fly')

def test_register_and_use():
    registry = ActionRegistry()
    registry.register('scan', 'Scan the surroundings', priority=0.6, alias=['analyze'])

    assert registry.is_valid('scan')
    assert registry.is_valid('analyze')

    assert registry.use_action('scan') is True
    assert registry.use_action('analyze') is True

def test_invalid_register():
    registry = ActionRegistry()
    
    with pytest.raises(ValueError):
        registry.register('wait', 'Try to overwrite')  # protegida

    with pytest.raises(ValueError):
        registry.register('explore', 'Duplicate')       # ya existe

    with pytest.raises(ValueError):
        registry.register('123invalid', 'Bad name')     # mal nombre
