import os
import shutil

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Estructura de destino
structure = {
    "core": [
        "actions.py", "agent.py", "analyzer_daemon.py", "autoconsciousness.py",
        "context.py", "decision.py", "engine.py", "environment.py",
        "evo_codex.py", "memory.py", "network_access.py", "self_reflection.py"
    ],
    "autoprogramming": [
        "base_symbols.py", "directed_mutation.py", "mutation_evaluation.py",
        "mutation_generator.py", "mutation_operator.py"
    ],
    "symbolic_ai": [
        "function_evaluator.py", "hypermutation.py", "hypermutator.py",
        "interpreter.py", "symbolic_context.py", "symbolic_evaluator.py",
        "symbolic_expression.py", "symbolic_interpreter.py", "symbolic_learning_engine.py",
        "symbolic_logger.py", "symbolic_persistence.py", "symbolic_rule.py",
        "symbolic_rule_engine.py", "web_filter.py"
    ],
    "metacognition": ["autonomous_stop.py", "targeted_mutation.py"],
    "mutations": ["mutation_engine.py"],
    "strategies": ["strategy_manager.py"],
    "runtime": ["executor.py", "monitor.py"],
    "utils": ["default_rules.py", "logger.py", "observer.py"],
    "visual": ["symbolic_view.py"],
    "data": ["symbolic_rule_engine.p", "symbolic_rule_engine.json"],
    "tests": [
        "test_bootstrap.py", "test_engine.py", "test_engine_context.py",
        "test_english_language.py", "test_identifiers_in_english.py",
        "test_rule.py", "test_rule_persistence.py"
    ],
    "logs": [
        "evoai_super_daemon.log", "function_mutation.log",
        "rule_mutation.log", "system_events.log", "symbolic_log.txt"
    ],
}

# Rutas personalizadas
custom_moves = {
    "evolved_strategies": os.path.join("strategies", "evolved_strategies"),
    "mutated_functions": os.path.join("data", "mutated_functions"),
    "codex_logs": "logs",
    "kfjjd": "data",  # dudoso, puede eliminarse si no tiene propósito
}

# Carpetas temporales a eliminar
trash = ["__pycache__"]

def move_files():
    for dest_dir, files in structure.items():
        dest_path = os.path.join(BASE_DIR, dest_dir)
        os.makedirs(dest_path, exist_ok=True)
        for filename in files:
            src = os.path.join(BASE_DIR, filename)
            if os.path.exists(src):
                shutil.move(src, os.path.join(dest_path, filename))
                print(f"Movido {filename} → {dest_dir}/")
    
    for src, dst in custom_moves.items():
        src_path = os.path.join(BASE_DIR, src)
        dst_path = os.path.join(BASE_DIR, dst)
        if os.path.exists(src_path):
            os.makedirs(dst_path, exist_ok=True)
            try:
                shutil.move(src_path, dst_path)
                print(f"Movida carpeta {src} → {dst}/")
            except Exception as e:
                print(f"[ERROR] {src} → {dst}: {e}")

def cleanup_trash():
    for root, dirs, _ in os.walk(BASE_DIR):
        for d in dirs:
            if d in trash:
                path = os.path.join(root, d)
                shutil.rmtree(path)
                print(f"Eliminado: {path}")

if __name__ == "__main__":
    print("📁 Reorganizando estructura de EvoAI...")
    move_files()
    cleanup_trash()
    print("✅ Proyecto reorganizado.")
