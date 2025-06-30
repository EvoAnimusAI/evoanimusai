def func_amircx(obs):
    if not (obs['entropy'] < 0.5 and obs['energy'] > 50):
        return 'advance'
    return 'wait'
