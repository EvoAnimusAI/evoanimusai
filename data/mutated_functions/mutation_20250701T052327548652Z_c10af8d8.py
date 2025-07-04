def func_vitqok(obs):
    if obs['entropy'] < 0.5 and obs['energy'] > 50:
        return 'advance'
    return 'wait'
