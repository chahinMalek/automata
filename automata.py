from itertools import combinations
from typing import Set, Dict


def get_power_set(s: Set):
    """
    Creates a power set from elements contained in parameter s.

    Args:
        s (Set): Set of elements from which the power set is created.

    Returns:
        dict: Dictionary of key: value pairs of indexes: elements in the found power set.
    """

    pw_set = []

    for i in range(len(s)+1):
        pw_set.extend(combinations(s, i))

    return {element: index for index, element in enumerate(pw_set)}


class Alphabet(object):
    """
    Formal class representation of an alphabet.

    Class instances represent alphabets of unique symbols following the formal definition of an alphabet.

    Attributes:
        symbols (Set): Set of symbols contained in the representing alphabet.

    """

    def __init__(self, symbols: Set):
        """
        Args:
              symbols (Set): Set of elements which will represent alphabet symbols in the
              instances of this class.
        """
        self.symbols = symbols

    def add(self, symbol: str):
        """
        Adds a non existing symbol into the alphabet.

        Args:
            symbol (str): A string containing exactly one symbol.

        Raises:
            ValueError: If symbol parameter is anything but a one symbol only.
        """

        if not isinstance(symbol, str) or len(symbol) != 1:
            raise ValueError('Method argument must be a character.')

        self.symbols.add(symbol)

    def get_nfa_alphabet(self) -> 'Alphabet':
        """
        Used to get a NFA representation of the alphabet instance.

        Returns:
            Alphabet: Alphabet containing the epsilon (empty) string, represented as None value, along with other
            symbols of the instanced alphabet.
        """

        alphabet = Alphabet(self.symbols)
        alphabet.symbols.add(None)

        return alphabet

    def __contains__(self, item: str):
        """
        Used to check whether a symbol is part of the instanced alphabet object.

        Args:
            item (str): Symbol which is checked for existence.

        Returns:
             bool: True if the item is present in the alphabet, False otherwise.
        """
        return item in self.symbols

    def __repr__(self):
        """
        String representation of the class instance.

        Returns:
            str: string representation of the alphabet.
        """
        return self.symbols.__repr__()


class State(object):
    """
    Class representation of the formal defined of a DFA state. May be considered as a graph node.

    Attributes:
        index (int): Index value of the state (consider as a state id).
        alphabet (Alphabet): Alphabet of symbols for which this state transitions to other states.
        transitions (Dict): Dictionary of key: value pairs of alphabet symbol: state index transitions.
    """

    def __init__(self, index: int, alphabet: 'Alphabet'):
        """
        Args:
            index (int): Integer which will be stored as the state's id
            alphabet (Alphabet): Instance of the Alphabet class to store the state's alphabet of symbols.
        """
        self.index = index
        self.alphabet = alphabet
        self.transitions = self._get_empty_transitions()

    def add(self, symbol: str, state: 'State') -> str:
        """
        Instance method to add/update state instance transitions.

        Args:
            symbol (str): Symbol which will be considered as a transition key.
            state (State): State where the state instance will transition when reading the symbol parameter.

        Returns:
            str: Symbol passed as the method parameter as a indicator that insert/update operation
            was successfully executed.

        Raises:
            ValueError: If symbol is not part of the alphabet.
        """

        if symbol not in self.alphabet:
            raise ValueError('Symbol is not part of the state\'s alphabet.')

        self.transitions[symbol] = state
        return symbol

    def _get_empty_transitions(self) -> Dict:
        """
        Creates empty transitions for every symbol in the state's alphabet.

        Returns:
            dict: symbol:None pairs for each symbol in the state's alphabet.
        """
        return {x: None for x in self.alphabet.symbols}

    def __repr__(self):
        """
        Returns:
            String representation of the state instance including its id and transitions
        """

        value = 'q{}\n'.format(self.index)
        symbols = sorted(self.alphabet.symbols, key=lambda x: '' if x is None else x)

        for i in symbols:
            value += '{} -> {}\n'.format(i, self.transitions[i].index if self.transitions[i] is not None else None)

        return value


class NfaState(State):
    """
        Class representation of the formal defined of a NFA state. May be considered as a graph node.
        Find class attributes in the superclass documentation.
    """

    def add(self, symbol, state: 'State') -> str:
        """
            Instance method to add/update state instance transitions.

            Args:
                symbol (str): Symbol which will be considered as a transition key.
                state (State): State where the state instance will transition when reading the symbol parameter.

            Returns:
                str: Symbol passed as the method parameter as a indicator that insert/update operation
                was successfully executed.

            Raises:
                ValueError: If symbol is not part of the alphabet.
        """

        if symbol not in self.alphabet:
            raise ValueError('Symbol is not part of the given alphabet.')

        self.transitions[symbol].append(state)
        return symbol

    def convert_to_dfa_state(self):
        """
        Executes a BFS search on the state's neighbors. A state is considered as a neighbor if it can be reached
        via state's transitions, returning every state that can be reached from the state instance followin only
        epsilon transitions.

        Returns:
            tuple: Tuple representation of states that can be reach following epsilon transitions.
        """

        states = set()
        states.add(self)

        state_queue = [] if self.transitions[None] is None else [x for x in self.transitions[None]]

        while len(state_queue) > 0:

            next_state = state_queue.pop(0)
            states.add(next_state)

            for state in next_state.transitions[None]:
                state_queue.append(state)

        return tuple(sorted([x.index for x in states]))

    def _get_empty_transitions(self):
        """
        Creates empty transitions for every symbol in the state's alphabet.

        Returns:
            dict: symbol:None pairs for each symbol in the state's alphabet.
        """
        return {x: [] for x in self.alphabet.symbols}

    def __repr__(self):
        """
            Returns:
                String representation of the state instance including its id and transitions
        """

        value = 'q{}\n'.format(self.index)
        symbols = sorted(self.alphabet.symbols, key=lambda x: '' if x is None else x)

        for i in symbols:
            value += '{} -> {}\n'.format(i, [x.index for x in self.transitions[i]])

        return value


class Dfa(object):
    """
        Class representation of the formal defined of a DFA automata. May be considered as a graph.

        Attributes:
            alphabet (Alphabet):
            states (Dict): Dictionary of the DFA states given in index:state pairs.
            start (int): DFA start state index.
            accept_indices (set): Set of state indexes which form the DFA set of accept states.
            size (int): Number of DFA states.
    """

    def __init__(self, size: int, alphabet: 'Alphabet', start: int, *accept_indices: int):
        """
        Args:
            size (int): The DFA's states number.
            alphabet (Alphabet): Alphabet on which the automata's transitions are being created.
            start (int): Start state index.
            *accept_indices (list): End state indexes.

        Raises:
            ValueError: if the start state index is out of bounds or if any of the accepting state indexes are.
        """

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

    def get_state_instance(self, index: int, alphabet: Alphabet):
        """
        Args:
            index (int): State id.
            alphabet (Alphabet): Alphabet for the state's transitions to be created on.

        Returns:
            State: New State class instance.
        """

        return State(index, alphabet)

    def get_start_state(self) -> 'State':
        """
        Returns:
            State: DFA start state.
        """
        return self.states[self.start]

    def add_transition(self, source: int, destination: int, symbol: str) -> None:
        """
        Inserts new transition or updates is if one already exists between source and destination states.

        Args:
            source (int): Index of the DFA state from which transition starts.
            destination (int): Index of the DFA state in which transition end.
            symbol (str): Symbol on which the transition occurs.

        Raises:
            ValueError: If any of the start or accepting indexes are out of bounds.
        """

        if not 0 <= source < self.size:
            raise ValueError('Start state index out of bounds.')

        if not 0 <= destination < self.size:
            raise ValueError('Accepting states indices out of bounds.')

        self.states[source].add(symbol, self.states[destination])

    def accepts(self, string: str) -> bool:
        """
        Method used to check whether the DFA instance accepts the string parameter formed on the DFA's alphabet.

        Returns:
            bool: True if the DFA accepts the input string following its defined transitions, False otherwise.

        Raises:
            ValueError: If symbol is not in the DFA's alphabet.
        """

        next_state = self.get_start_state()

        for symbol in string:

            if symbol not in self.alphabet:
                raise ValueError('Symbol is not a part of the alphabet.')

            next_state = next_state.transitions[symbol]

        return next_state.index in self.accept_indices

    def remove_redundant_states(self):
        """
        Executes a BFS search algorithm starting on the DFA's starting state. Any state which is not marked during the
        BFS search will be removed from the DFA's state map along with its transition mappings.
        """

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
    """
        Class representation of the formal defined of a NFA automata. May be considered as a graph.
        Find class attributes in the superclass documentation.
    """

    def __init__(self, size: int, alphabet: 'Alphabet', start: int, *accept_indices: int):
        """
        Find constructor documentation in the super class constructor documentation.
        """
        super().__init__(size, alphabet.get_nfa_alphabet(), start, *accept_indices)

    def get_state_instance(self, index, alphabet):
        """
            Args:
                index (int): State id.
                alphabet (Alphabet): Alphabet for the state's transitions to be created on.

            Returns:
                State: New State class instance.
        """
        return NfaState(index, alphabet)

    def accepts(self, string: str) -> bool:
        """
            Method used to check whether the NFA instance accepts the string parameter formed on the NFA's alphabet.

            Returns:
                bool: True if the NFA accepts the input string following its defined transitions, False otherwise.

            Raises:
                ValueError: If symbol is not in the NFA's alphabet.
        """

        state_queue = [(0, self.get_start_state().index)]

        while len(state_queue) > 0:

            index, current_state_index = state_queue.pop(0)

            if string[index] not in self.alphabet:
                raise ValueError('Symbol is not a part of the alphabet.')

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
        """
        Converts the NFA automata instance into an equivalent DFA automata instance. This function removes
        redundant states in the resulting DFA instance.
        """

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
