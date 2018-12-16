from automata import Nfa
from automata import NfaState
from automata import Alphabet
from automata import get_power_set

al = Alphabet({'a', 'b'})

n = Nfa(3, al, 0, 0)

n.add_transition(0, 1, 'b')
n.add_transition(0, 2, None)
n.add_transition(1, 1, 'a')
n.add_transition(1, 2, 'a')
n.add_transition(1, 2, 'b')
n.add_transition(2, 0, 'a')

d = n.convert_to_dfa()
d.remove_redundant_states()

print(d.states)
