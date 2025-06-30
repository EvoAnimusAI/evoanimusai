# core/environment.py

import random
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class Environment:
    """
    Entorno simbólico para EvoAI que simula un espacio lineal con variables como energía,
    entropía y ruido contextual. Permite ejecutar acciones que afectan el estado del agente.
    """

    # Constantes de acción
    ACTION_EXPLORE = ("explore", "explorar")
    ACTION_ADVANCE = ("advance", "avanzar", "mover")
    ACTION_WAIT = ("wait", "esperar")
    ACTION_CALM = ("calm", "calmar")
    ACTION_RESET = ("reset", "reiniciar")

    def __init__(self, parameters=None):
        """
        Inicializa el entorno con parámetros opcionales.

        Args:
            parameters (dict): Parámetros como 'max_position'. Si no se proporciona, se usan valores por defecto.
        """
        self.parameters = parameters or {}
        self.max_position = self.parameters.get("max_position", 5)
        self.state = {}
        self.visited = set()
        self.reset()

    def reset(self):
        """
        Reinicia el entorno a su estado inicial.
        """
        self.state = {
            "pos": 0,
            "explorado": False,
            "entropía": 0.0,
            "energía": 100,
            "ruido": None
        }
        self.visited.clear()
        logger.info("🔄 Entorno simbólico reiniciado.")

    def observe(self):
        """
        Retorna una copia del estado actual del entorno.

        Returns:
            dict: Estado simbólico del entorno.
        """
        return self.state.copy()

    def act(self, action):
        """
        Ejecuta una acción simbólica y retorna la recompensa y estado de término.

        Args:
            action (str): Acción simbólica a ejecutar.

        Returns:
            tuple: (recompensa (float), finalización (bool))

        Raises:
            TypeError: Si la acción no es cadena de texto.
            ValueError: Si la acción es cadena vacía.
        """
        if not isinstance(action, str):
            logger.error("La acción debe ser una cadena de texto.")
            raise TypeError("La acción debe ser una cadena de texto.")
        if not action:
            logger.error("La acción no puede ser una cadena vacía.")
            raise ValueError("La acción no puede ser una cadena vacía.")

        action = action.lower().strip()
        logger.debug(f"🎬 Acción simbólica recibida: {action}")

        reward = 0.0
        done = False
        current_pos = self.state["pos"]

        # Interpretación de acción
        if action in self.ACTION_EXPLORE:
            if current_pos in self.visited:
                reward = -0.2
                logger.debug("🔁 Exploración redundante.")
            else:
                reward = 2.0
                self.state["explorado"] = True
                logger.info("🧭 Exploración nueva exitosa.")
                self.visited.add(current_pos)

        elif action in self.ACTION_ADVANCE:
            if current_pos < self.max_position:
                self.state["pos"] += 1
                self.state["energía"] -= 5
                reward = 1.0
                logger.info("🚶‍♂️ Movimiento hacia adelante.")
            else:
                reward = -0.5
                logger.warning("⛔ Límite de movimiento alcanzado.")

        elif action in self.ACTION_WAIT:
            reward = -0.1
            logger.debug("⏳ Esperando...")

        elif action in self.ACTION_CALM:
            old_entropy = self.state["entropía"]
            self.state["entropía"] = max(0.0, old_entropy - 0.3)
            reward = 0.5 if old_entropy > 0.3 else -0.1
            logger.info(f"🧘 Acción calmante: entropía de {old_entropy} → {self.state['entropía']}")

        elif action in self.ACTION_RESET:
            self.reset()
            return 0.0, False

        else:
            reward = -1.0
            logger.warning(f"❌ Acción no reconocida: {action}")

        # Efectos secundarios: entropía y ruido (excepto para 'calm')
        if action not in self.ACTION_CALM:
            self.state["entropía"] = round(random.uniform(0.0, 1.0), 2)

        self.state["ruido"] = random.choice(["calma", "tensión", "caos", "armónico", "neutro"])

        # Condiciones de finalización
        if self.state["energía"] <= 0:
            logger.info("💀 Energía agotada.")
            done = True
        elif self.state["pos"] >= self.max_position:
            logger.info("🎯 Posición máxima alcanzada.")
            done = True
        elif self.state["explorado"]:
            logger.info("✅ Exploración completa.")
            done = True

        return reward, done
