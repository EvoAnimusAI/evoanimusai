## ⚙️ `strategy_manager.py`

Este script contiene la clase `StrategyManager`, que permite:

- Generar nuevas estrategias a partir de conceptos simbólicos recientes.
- Persistir las estrategias mutadas como funciones Python versionadas.
- Integrarse con el contexto simbólico de EvoAnimus para explorar mutaciones funcionales.

### Métodos clave

- `generate_new_strategy()`: Genera una nueva función basada en conceptos recientes. Devuelve `None` si no hay conceptos válidos.
- `save_strategy(func_name, func_code)`: Guarda una nueva función mutada en disco.
- `list_strategies()`: Devuelve una lista de estrategias generadas.
- `load_strategy(func_name)`: Importa dinámicamente una estrategia existente.

## 📂 `evolved_strategies/`

Este subdirectorio es generado dinámicamente. Aquí se almacenan los archivos `.py` correspondientes a estrategias mutadas, nombradas automáticamente (por ejemplo, `func_abcdxy.py`).

Estas funciones son persistidas para evaluación futura o reinyección al motor simbólico.

## 🧪 Tests

Los tests correspondientes están en:
