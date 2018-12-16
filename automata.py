from itertools import combinations
from typing import Set


def get_power_set(s: Set):

    pw_set = []

    for i in range(len(s)+1):
        pw_set.extend(combinations(s, i))

    return {element: index for index, element in enumerate(pw_set)}


class Alphabet(object):

    def __init__(self, symbols: Set):
        self.symbols = symbols

    def add(self, symbol: str):

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError('Method argument must be a character.')

        self.symbols.add(symbol)

    def get_nfa_alphabet(self) -> 'Alphabet':

        alphabet = Alphabet(self.symbols)
        alphabet.symbols.add(None)

        return alphabet

    def __contains__(self, item: str):
        return item in self.symbols

    def __repr__(self):
        return self.symbols.__repr__()


class State(object):

    def __init__(self, index, alphabet: 'Alphabet'):

        self.index = index
        self.alphabet = alphabet
        self.transitions = self._get_transitions()

    def add(self, symbol, state: 'State') -> str:

        if symbol not in self.alphabet:
            raise ValueError('Symbol is not part of the given alphabet.')

        self.transitions[symbol] = state
        return symbol

    def _get_transitions(self):
        return {x: None for x in self.alphabet.symbols}

    def __repr__(self):

        value = 'q{}\n'.format(self.index)
        symbols = sorted(self.alphabet.symbols, key=lambda x: '' if x is None else x)

        for i in symbols:
            value += '{} -> {}\n'.format(i, self.transitions[i].index if self.transitions[i] is not None else None)

        return value


class NfaState(State):

    def add(self, symbol, state: 'State') -> str:

        if symbol not in self.alphabet:
            raise ValueError('Symbol is not part of the given alphabet.')

        self.transitions[symbol].append(state)
        return symbol

    def convert_to_dfa_state(self):

        states = set()
        states.add(self)

        state_queue = [] if self.transitions[None] is None else [x for x in self.transitions[None]]

        while len(state_queue) > 0:

            next_state = state_queue.pop(0)
            states.add(next_state)

            for state in next_state.transitions[None]:
                state_queue.append(state)

        return tuple(sorted([x.index for x in states]))

    def _get_transitions(self):
        return {x: [] for x in self.alphabet.symbols}

    def __repr__(self):

        value = 'q{}\n'.format(self.index)
        symbols = sorted(self.alphabet.symbols, key=lambda x: '' if x is None else x)

        for i in symbols:
            value += '{} -> {}\n'.format(i, [x.index for x in self.transitions[i]])

        return value


class Dfa(object):

    def __init__(self, size: int, alphabet: 'Alphabet', start: int, *accept_indices: int):

        if not 0 <= start < size:
            raise ValueError('Start state index out of bounds.')

        for i in accept_indices:
            if not 0 <= i < size:
                raise ValueError('End states indices out of bounds.')

        self.alphabet = alphabet
        self.states = {}

        for i in range(size):
            self.states[i] = self.get_state_instance(i, alphabet)

        self.start = start
        self.accept_indices = set(accept_indices)
        self.size = size

    def get_state_instance(self, i, alphabet):
        return State(i, alphabet)

    def get_start_state(self) -> 'State':
        return self.states[self.start]

    def add_transition(self, source: int, destination: int, symbol) -> None:

        if not 0 <= source < self.size:
            raise ValueError('Start state index out of bounds.')

        if not 0 <= destination < self.size:
            raise ValueError('End states indices out of bounds.')

        self.states[source].add(symbol, self.states[destination])

    def accepts(self, string: str) -> bool:

        next_state = self.get_start_state()

        for symbol in string:

            if symbol not in self.alphabet:
                raise ValueError('Symbol is not a part of the alphabet.')

            next_state = next_state.transitions[symbol]

        return next_state.index in self.accept_indices

    def remove_redundant_states(self):

        visited: list = [False for _ in self.states]
        queue: list = [self.start]

        while len(queue) > 0:

            state = queue.pop(0)

            if not visited[state]:

                visited[state] = True

                for symbol in self.states[state].transitions:

                    if not visited[self.states[state].transitions[symbol].index]:
                        queue.append(self.states[state].transitions[symbol].index)

        for i in range(len(visited)):
            if not visited[i]:
                self.states.pop(i)


class Nfa(Dfa):

    def __init__(self, size: int, alphabet: 'Alphabet', start: int, *accept_indices: int):
        super().__init__(size, alphabet.get_nfa_alphabet(), start, *accept_indices)

    def get_state_instance(self, i, alphabet):
        return NfaState(i, alphabet)

    def accepts(self, string: str) -> bool:

        state_queue = [(0, self.get_start_state().index)]

        while len(state_queue) > 0:

            index, current_state_index = state_queue.pop(0)
            current_state = self.states[current_state_index]

            if index == len(string) and current_state_index in self.accept_indices:
                return True

            elif index == len(string):

                for state in current_state.transitions[None]:
                    state_queue.append((index, state.index))

                continue

            for symbol in current_state.transitions:

                if symbol is None:
                    for state in current_state.transitions[symbol]:
                        state_queue.append((index, state.index))

                elif symbol == string[index]:
                    for state in current_state.transitions[symbol]:
                        state_queue.append((index+1, state.index))

        return False

    def convert_to_dfa(self):

        states = get_power_set({x for x in range(self.size)})

        start_state_index = states[self.get_start_state().convert_to_dfa_state()]

        accept_indices = []

        for state in states:
            for index in state:

                if index in self.accept_indices:
                    accept_indices.append(states[state])
                    break

        al = Alphabet({x for x in self.alphabet.symbols if x is not None})

        d = Dfa(2 ** self.size, al, start_state_index, *accept_indices)

        for s in states:

            for symbol in al.symbols:

                next_state = set()

                for index in s:

                    for state in self.states[index].transitions[symbol]:
                        next_state = next_state.union(self.states[state.index].convert_to_dfa_state())

                d.add_transition(states[s], states[tuple(sorted(next_state))], symbol)

        return d
