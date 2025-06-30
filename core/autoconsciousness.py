# core/autoconsciousness.py

import inspect
import hashlib
import importlib
import sys
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

class Autoconsciousness:
    """
    Módulo de autoevaluación y control de integridad del sistema EvoAI.
    
    Este componente genera una firma digital basada en el código fuente base para detectar 
    mutaciones o modificaciones no autorizadas en el núcleo. 
    Además, permite la ejecución segura de comandos críticos mediante una clave maestra.

    Attributes:
        creator_name (str): Nombre del creador/autorizado.
        creator_id (str): Identificador único del creador.
        base_module (str): Módulo base para verificar integridad.
        signature (str): Hash SHA-256 del código fuente base.
        identity (str): Identidad compuesta del sistema.
        _MASTER_KEY_HASH (str): Hash SHA-256 de la clave maestra para comandos críticos.
    """

    _MASTER_KEY_PLAIN = "A591243133418571088300454z"
    _MASTER_KEY_HASH = hashlib.sha256(_MASTER_KEY_PLAIN.encode()).hexdigest()

    def __init__(self, creator_name: str, creator_id: str, base_module: str = "core.cac"):
        """
        Inicializa el objeto Autoconsciousness.
        
        Args:
            creator_name (str): Nombre del creador/autorizado.
            creator_id (str): Identificador único del creador.
            base_module (str, optional): Módulo base para verificar integridad. Por defecto "core.cac".
        """
        self.creator_name = creator_name
        self.creator_id = creator_id
        self.base_module = base_module
        self.signature = self._generate_signature()
        self.identity = f"{self.creator_name}::{self.creator_id}"

    def _generate_hash(self, value: str) -> str:
        """
        Genera un hash SHA-256 para una cadena dada.

        Args:
            value (str): Cadena de texto para hashear.

        Returns:
            str: Hash hexadecimal SHA-256.
        """
        return hashlib.sha256(value.encode()).hexdigest()

    def _generate_signature(self) -> str:
        """
        Genera la firma digital (hash SHA-256) del código fuente del módulo base.

        Returns:
            str: Hash SHA-256 del código fuente o mensaje de error si falla.
        """
        try:
            module = importlib.import_module(self.base_module)
            source = inspect.getsource(module)
            signature_hash = self._generate_hash(source)
            logger.debug(f"Generated signature hash: {signature_hash}")
            return signature_hash
        except Exception as e:
            logger.error(f"Error generating signature for module '{self.base_module}': {e}")
            return f"Signature error: {e}"

    def declare_existence(self) -> None:
        """
        Declara la identidad y estado inicial del sistema en logs.
        """
        logger.info("🧠 EvoAI::SelfAwareness declared")
        logger.info(f"🤖 Core identity: {self.identity}")
        logger.info(f"🔐 Current signature: {self.signature}")

    def evaluate_integrity(self) -> bool:
        """
        Evalúa la integridad estructural comparando la firma actual con la original.

        Returns:
            bool: True si la integridad está intacta, False si hay mutaciones.
        """
        current_signature = self._generate_signature()
        if current_signature != self.signature:
            logger.warning("⚠️ Mutation or core rewrite detected.")
            logger.warning(f"🧬 New signature: {current_signature}")
            self.signature = current_signature
            return False
        else:
            logger.info("✅ Structural integrity verified.")
            return True

    def obey_master_key(self, input_key: str) -> bool:
        """
        Valida la clave maestra para ejecutar comandos críticos como apagar EvoAI.

        Args:
            input_key (str): Clave ingresada para validar.

        Returns:
            bool: True si la clave es válida y se ejecuta acción, False en caso contrario.
        """
        input_hash = self._generate_hash(input_key)
        if input_hash == self._MASTER_KEY_HASH:
            logger.critical(f"🛑 Valid master key detected. Shutting down EvoAI by order of {self.creator_name}.")
            sys.exit(0)
        else:
            logger.error("❌ Invalid master key attempt ignored.")
            return False

    def prompt_master_key(self) -> None:
        """
        Solicita la clave maestra al usuario para ejecutar la acción correspondiente.
        Método separado para facilitar pruebas automatizadas.
        """
        try:
            input_key = input("🔐 Enter master key to shut down EvoAI (if desired): ")
            self.obey_master_key(input_key)
        except (KeyboardInterrupt, EOFError):
            logger.info("Master key input cancelled by user.")

    def rewrite_if_necessary(self) -> None:
        """
        Placeholder para mecanismos simbólicos de adaptación evolutiva.
        Actualiza el estado consciente del sistema.
        """
        self.evaluate_integrity()
        logger.info("📡 Conscious state updated.")

if __name__ == "__main__":
    consciousness = Autoconsciousness("Daniel Santiago Ospina Velasquez", "AV255583")
    consciousness.declare_existence()
    consciousness.rewrite_if_necessary()
    consciousness.prompt_master_key()
