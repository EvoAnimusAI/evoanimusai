# utils/default_rules.py

def get_default_rules():
    return [
        {"action": "explore", "priority": 1.0},
        {"action": "wait", "priority": 0.8},
        {"action": "calm", "priority": 0.5},
        {"action": "advance", "priority": 0.9}
    ]
