from unittest.mock import MagicMock, patch
from strategies.strategy_manager import StrategyManager

@patch("strategies.strategy_manager.EvoContext")
def test_generate_and_load_strategy(mock_context_class):
    # Simulación de un contexto con conceptos simbólicos recientes
    mock_context = MagicMock()
    mock_context.get_recent_concepts.return_value = ["concepto_simulado"]
    mock_context_class.return_value = mock_context

    manager = StrategyManager(max_strategies=5)
    result = manager.generate_new_strategy()
    assert result is not None

@patch("strategies.strategy_manager.EvoContext")
def test_generate_strategy_without_concepts(mock_context_class):
    # Simulación de un contexto sin conceptos simbólicos
    mock_context = MagicMock()
    mock_context.get_recent_concepts.return_value = []
    mock_context_class.return_value = mock_context

    manager = StrategyManager(max_strategies=5)
    result = manager.generate_new_strategy()
    assert result is None  # Se espera None por falta de conceptos

@patch("strategies.strategy_manager.mutate_function")
def test_generate_strategy_without_concepts(mock_mutate):
    mock_mutate.side_effect = ValueError("No se encontraron conceptos simbólicos recientes para mutación.")
    manager = StrategyManager(max_strategies=5)
    result = manager.generate_new_strategy()
    assert result is None  # Debe retornar None si mutate_function falla
