# utils/default_rules.py
# -*- coding: utf-8 -*-
"""
🛡️ Symbolic Rule System — Military/Governmental Grade
Version: 3.0.0 | Classification: ULTRA-RESTRICTED
"""

import hashlib
import time
from typing import List, Dict, Tuple, Any
from dataclasses import dataclass, field
from enum import Enum
from threading import Lock
from utils.evo_logging import log  # Custom secure logger

class SecurityLevel(Enum):
    PUBLIC = 1
    RESTRICTED = 2
    CONFIDENTIAL = 3
    SECRET = 4
    ULTRA_SECRET = 5

class RuleValidationError(Exception): pass
class RuleSecurityError(Exception): pass

@dataclass
class SymbolicRule:
    rule_id: str
    pattern: str
    action: str
    condition: str
    security_level: SecurityLevel
    checksum: str = field(default="")
    created_at: float = field(default_factory=time.time)
    last_validated: float = field(default_factory=time.time)
    validation_count: int = field(default=0)

    def __post_init__(self):
        if not self.checksum:
            self.checksum = self._generate_checksum()
            print(f"[INIT] Checksum generated for {self.rule_id} → {self.checksum}")

    def _generate_checksum(self) -> str:
        base = f"{self.rule_id}:{self.pattern}:{self.action}:{self.condition}"
        return hashlib.sha256(base.encode()).hexdigest()[:16]

    def validate_integrity(self) -> bool:
        expected = self._generate_checksum()
        is_valid = expected == self.checksum
        if is_valid:
            self.last_validated = time.time()
            self.validation_count += 1
        else:
            print(f"[ERROR] Integrity check failed for rule {self.rule_id}")
        return is_valid

class MilitaryRuleEngine:
    def __init__(self, security_clearance: SecurityLevel = SecurityLevel.RESTRICTED):
        self.security_clearance = security_clearance
        self._rules_cache: Dict[str, SymbolicRule] = {}
        self._access_log: List[Dict] = []
        self._lock = Lock()
        self._rule_counter = 0
        self._init_time = time.time()

    def _log_access(self, operation: str, rule_id: str = "", status: str = "OK"):
        with self._lock:
            entry = {
                "timestamp": time.time(),
                "operation": operation,
                "rule_id": rule_id,
                "status": status,
                "level": self.security_clearance.name
            }
            self._access_log.append(entry)

    def _validate_rule_syntax(self, rule: str) -> Tuple[bool, str]:
        if not rule or not isinstance(rule, str):
            return False, "Empty rule or invalid type"
        if "=>" not in rule or "::" not in rule:
            return False, "Missing '=>' or '::' separators"

        for ch in [';', '`', '$']:
            if ch in rule:
                print(f"[🧨 DEBUG] Rule blocked due to character '{ch}': {rule}")
                return False, "Dangerous characters detected"

        if len(rule) > 1000:
            return False, "Rule too long"

        try:
            pattern, right = rule.split("=>")
            action, condition = right.split("::")
            if not pattern.strip() or not action.strip() or not condition.strip():
                return False, "Empty fields detected"
            return True, "OK"
        except Exception as e:
            return False, f"Parsing error: {str(e)}"

    def _create_symbolic_rule(self, raw: str) -> SymbolicRule:
        self._rule_counter += 1
        rule_id = f"RULE_{self._rule_counter:04d}_{int(time.time())}"
        pattern, right = raw.split("=>")
        action, condition = right.split("::")
        return SymbolicRule(
            rule_id=rule_id,
            pattern=pattern.strip(),
            action=action.strip(),
            condition=condition.strip(),
            security_level=self.security_clearance
        )

    def get_default_rules(self) -> List[str]:
        raw_rules = [
            "tactical:reconnaissance => advance_position :: threat_level < 3 AND visibility > 0.7",
            "strategic:defense => establish_perimeter :: enemy_distance > 500 AND ammunition > 0.3",
            "operational:stealth => maintain_silence :: noise_signature < 0.2 AND mission_phase == 'infiltration'",
            "combat:engagement => fire_suppression :: target_acquired == True AND friendly_fire_risk < 0.1",
            "logistics:supply => request_resupply :: inventory_level < 0.25 AND supply_line_secure == True",
            "intel:gathering => passive_observation :: surveillance_mode == 'active' AND detection_risk < 0.15",
            "communication:secure => encrypt_transmission :: communication_channel == 'secure' AND encryption_level >= 256",
            "navigation:movement => update_position :: gps_accuracy > 0.95 AND terrain_analysis == 'complete'",
            "threat:assessment => escalate_alert :: anomaly_detected == True AND confidence_level > 0.8",
            "mission:abort => immediate_extraction :: mission_compromise == True OR casualty_threshold_exceeded == True"
        ]

        print(f"[INFO] Processing {len(raw_rules)} rules...")
        self._log_access("GET_DEFAULT_RULES", status="INITIATED")

        validated = []
        for idx, rule in enumerate(raw_rules, 1):
            valid, msg = self._validate_rule_syntax(rule)
            if not valid:
                log(f"[❌ SYNTAX] Rule {idx}: {msg}", level="ERROR")
                print(f"[❌ SYNTAX] Rule {idx}: {msg}")
                continue
            symbolic = self._create_symbolic_rule(rule)
            if not symbolic.validate_integrity():
                log(f"[❌ INTEGRITY] Rule {idx}: {symbolic.rule_id}", level="ERROR")
                continue
            self._rules_cache[symbolic.rule_id] = symbolic
            validated.append(rule)
            print(f"[✅ OK] Rule {idx} validated: {symbolic.rule_id}")
            log(f"[✅ SYNTAX] Rule syntactically valid: {rule}", level="INFO")

        if not validated:
            raise RuleValidationError("All rules failed validation.")

        self._log_access("GET_DEFAULT_RULES", status="SUCCESS")
        return validated

    def get_rule_statistics(self) -> Dict[str, Any]:
        return {
            "rules_loaded": len(self._rules_cache),
            "uptime_sec": round(time.time() - self._init_time, 2),
            "security_clearance": self.security_clearance.name,
            "total_accesses": len(self._access_log)
        }

    def audit_log(self) -> List[Dict]:
        return self._access_log.copy()

_engine = MilitaryRuleEngine()

def get_default_rules() -> List[str]:
    return _engine.get_default_rules()

def get_system_statistics() -> Dict[str, Any]:
    return _engine.get_rule_statistics()

if __name__ == "__main__":
    print("=== [🔐 MILITARY RULE SYSTEM] ===")
    try:
        rules = get_default_rules()
        stats = get_system_statistics()
        print(f"\n📋 Total rules: {stats['rules_loaded']}")
        print(f"🔒 Security: {stats['security_clearance']}")
        print(f"🕒 Uptime: {stats['uptime_sec']}s")
        print("=== [✅ SYSTEM OK] ===")
    except Exception as e:
        print(f"[💥 FATAL] Critical error: {e}")
