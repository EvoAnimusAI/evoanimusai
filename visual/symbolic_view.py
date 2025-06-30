# visual/symbolic_view.py

# visual/symbolic_view.py

def show_symbolic_state(context, decision, observation, reward=None, extra_info=None):
    print("\n ^=   Real-time Symbolic Visualization =^")
    print(f" ^=^t^m Symbolic Observation: {observation}")
    print(f" ^z     Symbolic Decision: {decision}")
    print(f" ^=^n   Executed Action: {observation.get('action')}")
    print(f" ^=^o^f Reward: {reward}")
    print(f" ^=     Current Symbolic Context: {context.status}")
    if extra_info:
        print(f" ^=     Additional Information: {extra_info}")
    print("-" * 60)
