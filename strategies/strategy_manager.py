# ... (encabezado y docstring igual)

import os
import time
import random
import traceback
import importlib.util
from datetime import datetime
from typing import Callable, Optional, List, Tuple

import numpy as np

from core.agent import EvoAgent
from core.context import EvoContext
from mutations.mutation_engine import mutate_function
from runtime.monitor import log_event
from symbolic_ai.symbolic_context import symbolic_context
from symbolic_ai.symbolic_persistence import register_mutated_function


EVO_DIR = os.path.abspath("strategies/evolved_strategies")
os.makedirs(EVO_DIR, exist_ok=True)


class StrategyManager:
    def __init__(self, max_strategies: int = 30):
        self.max_strategies = max_strategies
        self.strategies: List[Tuple[str, float, str]] = []

    def register_function(self, func: Callable, name: str = "base_function", score: float = 0.0, path: Optional[str] = None) -> None:
        self.strategies.append((name, score, path or "manual"))
        log_event("STRATEGY_REGISTERED", f"{name} (manual)")

    def generate_new_strategy(self) -> Optional[Tuple[str, str]]:
        try:
            agent = EvoAgent(context=EvoContext(), name="EvoTemp")
            knowledge = agent.memory.retrieve_all()
            context = agent.context

            mutated = mutate_function(knowledge, context)
            strategy_name = mutated.name
            file_path = os.path.join(EVO_DIR, f"{strategy_name}.py")

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(mutated.description)

            mutated.file_path = file_path

            register_mutated_function.register(strategy_name, mutated.description)

            symbolic_context.add_concept({
                "name": strategy_name,
                "description": mutated.description,
                "file_path": file_path,
                "timestamp": datetime.utcnow().isoformat()
            })

            log_event("STRATEGY_CREATED", strategy_name)
            return strategy_name, file_path

        except Exception as e:
            log_event("ERROR_GENERATING_STRATEGY", traceback.format_exc())
            return None

    def load_strategy(self, file_path: str) -> Optional[Callable]:
        try:
            module_name = os.path.splitext(os.path.basename(file_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            func = getattr(module, module_name, None)

            if not callable(func):
                log_event("ERROR_LOADING_STRATEGY", f"Función '{module_name}' no encontrada o no callable en {file_path}")
                return None

            log_event("STRATEGY_LOADED", module_name)
            return func

        except Exception:
            log_event("ERROR_LOADING_STRATEGY", traceback.format_exc())
            return None

    def evaluate_strategy(self, strategy_func: Callable) -> float:
        try:
            data = np.random.randn(100)
            result = strategy_func(data)

            if isinstance(result, (int, float)):
                return float(result)
            else:
                return -10000.0

        except Exception:
            log_event("ERROR_EVALUATING_STRATEGY", traceback.format_exc())
            return -10000.0

    def evolve(self, generations: int = 5) -> None:
        for _ in range(generations):
            gen_result = self.generate_new_strategy()
            if gen_result is None:
                continue

            name, path = gen_result
            func = self.load_strategy(path)
            if func is None:
                continue

            score = self.evaluate_strategy(func)
            self.strategies.append((name, score, path))
            log_event("STRATEGY_EVALUATED", f"{name} → {score:.4f}")

            if len(self.strategies) > self.max_strategies:
                self.prune()

            time.sleep(0.1)

    def prune(self) -> None:
        try:
            scores = [s[1] for s in self.strategies]
            if not scores:
                return

            median_score = np.median(scores)
            survivors = [(n, s, p) for (n, s, p) in self.strategies if s >= median_score]
            removed = [(n, s, p) for (n, s, p) in self.strategies if s < median_score]

            for _, _, path in removed:
                try:
                    if os.path.exists(path):
                        os.remove(path)
                        log_event("STRATEGY_REMOVED", f"Archivo eliminado: {path}")
                except Exception:
                    log_event("ERROR_REMOVING_STRATEGY", traceback.format_exc())

            self.strategies = survivors
            log_event("STRATEGIES_PRUNED", f"Supervivientes: {len(survivors)}")

        except Exception:
            log_event("ERROR_PRUNING_STRATEGIES", traceback.format_exc())

    def get_top_strategies(self, top_n: int = 5) -> List[Tuple[str, float, str]]:
        return sorted(self.strategies, key=lambda x: x[1], reverse=True)[:top_n]

    def save_symbolic_log(self, log_path: str = "logs/strategy_symbolic_log.txt") -> None:
        try:
            os.makedirs(os.path.dirname(log_path), exist_ok=True)
            with open(log_path, "w", encoding="utf-8") as f:
                for name, score, path in self.strategies:
                    f.write(f"{datetime.utcnow().isoformat()} | {name} | {score:.4f} | {path}\n")
            log_event("LOG_SAVED", f"Log guardado en {log_path}")
        except Exception:
            log_event("ERROR_SAVING_LOG", traceback.format_exc())


if __name__ == "__main__":
    manager = StrategyManager(max_strategies=30)
    manager.evolve(generations=20)
    top = manager.get_top_strategies()
    for name, score, path in top:
        print(f"[TOP] {name} → Score: {score:.4f}")
    manager.save_symbolic_log()
