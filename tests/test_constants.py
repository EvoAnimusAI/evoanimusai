# tests/test_constants.py

import pytest
import metacognition.constants as const

def test_constants_types_and_values():
    # Test mutation intensities
    assert isinstance(const.MUTATION_INTENSITY_LIGHT, float)
    assert 0.0 <= const.MUTATION_INTENSITY_LIGHT <= 1.0

    assert isinstance(const.MUTATION_INTENSITY_MODERATE, float)
    assert 0.0 <= const.MUTATION_INTENSITY_MODERATE <= 1.0

    assert isinstance(const.MUTATION_INTENSITY_STRONG, float)
    assert 0.0 <= const.MUTATION_INTENSITY_STRONG <= 1.0

    # Test integer constants
    assert isinstance(const.MAX_REJECTED_MUTATIONS_BEFORE_MODERATE, int)
    assert const.MAX_REJECTED_MUTATIONS_BEFORE_MODERATE > 0

    # Test entropy thresholds
    assert isinstance(const.ENTROPY_THRESHOLD_MODERATE, float)
    assert 0.0 <= const.ENTROPY_THRESHOLD_MODERATE <= 1.0

    # Test allowed actions
    assert isinstance(const.ALLOWED_ACTIONS, tuple)
    assert all(isinstance(a, str) and a for a in const.ALLOWED_ACTIONS)

    # Test deltas
    assert 0.0 <= const.MODERATE_MUTATION_THRESHOLD_DELTA <= 1.0
    assert 0.0 <= const.LIGHT_MUTATION_WEIGHT_DELTA <= 1.0

    # Test context keys
    assert isinstance(const.CONTEXT_KEY_RECENT_REWARDS, str) and const.CONTEXT_KEY_RECENT_REWARDS
    assert isinstance(const.CONTEXT_KEY_CURRENT_ENTROPY, str) and const.CONTEXT_KEY_CURRENT_ENTROPY
    assert isinstance(const.CONTEXT_KEY_REJECTED_MUTATIONS, str) and const.CONTEXT_KEY_REJECTED_MUTATIONS
    assert isinstance(const.CONTEXT_KEY_CYCLES_WITHOUT_NEW_RULE, str) and const.CONTEXT_KEY_CYCLES_WITHOUT_NEW_RULE

    # Test min values
    assert const.MIN_THRESHOLD_VALUE >= 0.0
    assert const.MIN_WEIGHT_VALUE >= 0.0

    # Test max cycles
    assert isinstance(const.MAX_CYCLES_WITHOUT_IMPROVEMENT, int)
    assert const.MAX_CYCLES_WITHOUT_IMPROVEMENT > 0

    # Test exit reasons are non-empty strings
    assert all(isinstance(reason, str) and reason for reason in [
        const.EXIT_REASON_ENTROPY_LOW,
        const.EXIT_REASON_NO_NEW_RULES,
        const.EXIT_REASON_NEGATIVE_REWARDS,
    ])

if __name__ == "__main__":
    pytest.main()
