import os
import json
import yaml
import re

# Directorios donde buscar reglas
RULE_DIRS = [
    "data",
    "data/rules"
]

# Métodos válidos de diccionarios que NO deben corregirse
DICT_METHOD_WHITELIST = {"get", "items", "keys", "values", "update", "pop", "clear", "copy", "setdefault", "fromkeys"}

# Campos esperados que contienen condiciones simbólicas
CONDITION_KEYS = {"condicion", "condition"}

# Patrón general para detectar expresiones tipo obj.attr
DICT_ATTR_PATTERN = re.compile(r"\b(\w+)\.(\w+)\b")

# Detecta si es una expresión obj.attr que no debe tocarse
def is_invalid_attr_access(obj, attr):
    return attr not in DICT_METHOD_WHITELIST

def correct_condition(expr):
    # Corrige solo si es un acceso no permitido
    matches = DICT_ATTR_PATTERN.findall(expr)
    corrected_expr = expr
    for obj, attr in matches:
        if is_invalid_attr_access(obj, attr):
            corrected_expr = corrected_expr.replace(f"{obj}.{attr}", f"{obj}['{attr}']")
    return corrected_expr

def load_rules(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        if filepath.endswith('.json'):
            return json.load(f)
        elif filepath.endswith('.yaml') or filepath.endswith('.yml'):
            return yaml.safe_load(f)
    return None

def save_json(filepath, rules):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(rules, f, indent=4, ensure_ascii=False)

def process_file(filepath, corrected_rules):
    try:
        rules = load_rules(filepath)
        if not isinstance(rules, list):
            print(f"[⚠️ SKIP] {filepath} no contiene una lista de reglas.")
            return
    except Exception as e:
        print(f"[❌ ERROR] No se pudo cargar {filepath}: {e}")
        return

    modified = False
    for rule in rules:
        for key in CONDITION_KEYS:
            if key in rule and isinstance(rule[key], str):
                original = rule[key]
                corrected = correct_condition(original)
                if corrected != original:
                    print(f"[🔧 FIX] {filepath} | Corrigiendo: {original} → {corrected}")
                    rule[key] = corrected
                    modified = True
        corrected_rules.append(rule)

    if modified:
        out_path = filepath.replace(".json", "_corrected.json").replace(".yaml", "_corrected.json")
        save_json(out_path, rules)
        print(f"[✅ GUARDADO] Archivo corregido: {out_path}")
    else:
        print(f"[✔️ OK] {filepath} no requiere correcciones.")

def find_rule_files():
    rule_files = []
    for base_dir in RULE_DIRS:
        for fname in os.listdir(base_dir):
            if fname.endswith(('.json', '.yaml', '.yml')):
                rule_files.append(os.path.join(base_dir, fname))
    return rule_files

def export_consolidated(rules, path='data/symbolic_rule_engine_consolidated.json'):
    save_json(path, rules)
    print(f"[📦 CONSOLIDADO] Exportado archivo único: {path}")

if __name__ == "__main__":
    print("[🔍 AUDITOR] Iniciando auditoría extendida de reglas simbólicas...")
    files = find_rule_files()
    all_corrected_rules = []

    for filepath in files:
        process_file(filepath, all_corrected_rules)

    if all_corrected_rules:
        export_consolidated(all_corrected_rules)

    print("[🏁 FIN] Auditoría completada.")


def main():
    print("[🔍 AUDITOR] Iniciando auditoría extendida de reglas simbólicas...")
    files = find_rule_files()
    all_corrected_rules = []

    for filepath in files:
        process_file(filepath, all_corrected_rules)

    if all_corrected_rules:
        export_consolidated(all_corrected_rules)

    print("[🏁 FIN] Auditoría completada.")

# Permite ejecución como script o importación como módulo
if __name__ == "__main__":
    main()
