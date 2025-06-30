# tests/test_environment.py

import pytest
from core.environment import Environment

@pytest.fixture
def env():
    return Environment(parameters={"max_position": 3})

def test_initial_state(env):
    state = env.observe()
    assert isinstance(state, dict), "El estado debe ser un diccionario"
    assert state["pos"] == 0, "La posición inicial debe ser 0"
    assert state["energía"] == 100, "La energía inicial debe ser 100"
    assert state["explorado"] is False, "El estado explorado debe ser False inicialmente"
    assert state["entropía"] == 0.0, "La entropía inicial debe ser 0.0"
    assert state["ruido"] is None, "El ruido inicial debe ser None"

def test_reset_resets_state(env):
    env.state["pos"] = 2
    env.state["energía"] = 10
    env.reset()
    state = env.observe()
    assert state["pos"] == 0, "Reset debe reiniciar la posición a 0"
    assert state["energía"] == 100, "Reset debe reiniciar la energía a 100"
    assert state["explorado"] is False, "Reset debe poner explorado en False"
    assert env.visited == set(), "Reset debe limpiar las posiciones visitadas"

def test_explore_action(env):
    # Primera exploración en posición 0, no visitada
    env.state["pos"] = 0
    env.visited.clear()
    reward, done = env.act("explore")
    assert isinstance(reward, float), "Recompensa debe ser float"
    assert reward == 2.0, "Recompensa por exploración nueva debe ser 2.0"
    assert done is True, "La exploración marca done=True"
    # Exploración redundante (posición ya visitada)
    reward2, done2 = env.act("explore")
    assert reward2 == -0.2, "Recompensa por exploración redundante debe ser -0.2"
    assert done2 is True, "Estado done no cambia en exploración redundante"

def test_advance_action(env):
    env.state["pos"] = 1
    env.state["energía"] = 50
    reward, done = env.act("advance")
    assert reward == 1.0, "Recompensa por avanzar dentro del rango debe ser 1.0"
    assert env.state["pos"] == 2, "Posición debe incrementarse en 1"
    assert env.state["energía"] == 45, "Energía debe disminuir en 5"
    assert done is False, "No debe terminar si no llega al max_position"
    # Intentar avanzar más allá del máximo
    env.state["pos"] = env.max_position
    reward2, done2 = env.act("advance")
    assert reward2 == -0.5, "Recompensa por avanzar más allá del límite debe ser -0.5"
    assert env.state["pos"] == env.max_position, "Posición no debe cambiar al avanzar fuera del rango"
    assert done2 is True, "Estado done debe ser True al alcanzar max_position"

def test_wait_action(env):
    reward, done = env.act("wait")
    assert reward == -0.1, "Recompensa por esperar debe ser -0.1"
    assert done in (True, False), "Estado done debe ser booleano"

def test_calm_action(env):
    env.state["entropía"] = 0.5
    reward, done = env.act("calm")
    assert env.state["entropía"] <= 0.5, "Entropía debe disminuir o mantenerse igual"
    if 0.5 > 0.3:
        assert reward == 0.5, "Recompensa debe ser 0.5 si entropía previa > 0.3"
    else:
        assert reward == -0.1, "Recompensa debe ser -0.1 si entropía previa ≤ 0.3"
    assert done is False, "Calmar no debe terminar el episodio"

def test_reset_action(env):
    env.state["pos"] = 2
    env.state["energía"] = 10
    reward, done = env.act("reset")
    assert reward == 0.0, "Recompensa por reset debe ser 0.0"
    assert done is False, "Reset no termina el episodio"
    state = env.observe()
    assert state["pos"] == 0, "Reset debe reiniciar posición"
    assert state["energía"] == 100, "Reset debe reiniciar energía"
    assert env.visited == set(), "Reset debe limpiar visitados"

def test_unrecognized_action(env):
    reward, done = env.act("invalid_action")
    assert reward == -1.0, "Recompensa por acción inválida debe ser -1.0"
    assert done is False, "Acción inválida no termina episodio"

def test_energy_depletion_done():
    e = Environment(parameters={"max_position": 10})
    e.state["energía"] = 0
    reward, done = e.act("wait")
    assert done is True, "Energía 0 debe marcar done=True"

def test_explored_done():
    e = Environment()
    e.state["explorado"] = True
    reward, done = e.act("wait")
    assert done is True, "Explorado=True debe marcar done=True"

def test_position_max_done():
    e = Environment(parameters={"max_position": 1})
    e.state["pos"] = 1
    reward, done = e.act("wait")
    assert done is True, "Posición máxima debe marcar done=True"

def test_action_type_validation(env):
    with pytest.raises(TypeError):
        env.act(123)  # No str

def test_action_empty_string(env):
    with pytest.raises(ValueError):
        env.act("")  # Cadena vacía

def test_entropy_and_noise_update(env):
    prev_entropy = env.state["entropía"]
    reward, done = env.act("wait")
    state = env.observe()
    assert 0.0 <= state["entropía"] <= 1.0, "Entropía debe estar en rango [0,1]"
    assert state["ruido"] in {"calma", "tensión", "caos", "armónico", "neutro"}, "Ruido debe ser valor válido"
    assert isinstance(state["ruido"], str), "Ruido debe ser string"
