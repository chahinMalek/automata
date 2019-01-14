from automata import Alphabet
from automata import Nfa

al = Alphabet({'a', 'b'})

n = Nfa(3, al, 0, 0)

n.add_transition(0, 1, 'b')
n.add_transition(0, 2, None)
n.add_transition(1, 1, 'a')
n.add_transition(1, 2, 'a')
n.add_transition(1, 2, 'b')
n.add_transition(2, 0, 'a')

# n: Nfa = Nfa(2, al, 0, 0)

# n.add_transition(0, 1, None)
# n.add_transition(1, 0, '0')
# n.add_transition(1, 0, '1')

d = n.convert_to_dfa()
d.remove_redundant_states()

print(d.accepts('aa'))
print(n.accepts('aa'))

d = n.convert_to_dfa()
d.remove_redundant_states()
