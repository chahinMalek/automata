from random import randint
from unittest import TestCase
from unittest import main

from automata import Alphabet
from automata import Dfa
from automata import Nfa


def get_random_string() -> str:

    n: int = randint(10, 1000)
    res: str = ''

    for i in range(n):
        res += str(randint(0, 1))

    return res


def get_alphabet() -> 'Alphabet':
    return Alphabet({'0', '1'})


class TestDfa(TestCase):

    def test_odd_length_dfa(self):

        odd_length_dfa = Dfa(2, get_alphabet(), 0, 1)
        odd_length_dfa.add_transition(0, 1, '0')
        odd_length_dfa.add_transition(0, 1, '1')
        odd_length_dfa.add_transition(1, 0, '0')
        odd_length_dfa.add_transition(1, 0, '1')

        for i in range(1000):

            s: str = get_random_string()
            self.assertEqual(bool(len(s) % 2), odd_length_dfa.accepts(s))

        self.assertEqual(False, odd_length_dfa.accepts(''))

    def test_even_length_dfa(self):

        even_length_dfa = Dfa(2, get_alphabet(), 0, 0)
        even_length_dfa.add_transition(0, 1, '0')
        even_length_dfa.add_transition(0, 1, '1')
        even_length_dfa.add_transition(1, 0, '0')
        even_length_dfa.add_transition(1, 0, '1')

        for i in range(1000):

            s: str = get_random_string()
            self.assertEqual(not bool(len(s) % 2), even_length_dfa.accepts(s))

        self.assertEqual(True, even_length_dfa.accepts(''))

    def test_empty_dfa(self):

        d = Dfa(1, get_alphabet(), 0)
        d.add_transition(0, 0, '0')
        d.add_transition(0, 0, '1')

        for i in range(1000):
            self.assertEqual(False, d.accepts(get_random_string()))

        self.assertEqual(False, d.accepts(''))

    def test_odd_0s(self):

        d = Dfa(2, get_alphabet(), 0, 1)
        d.add_transition(0, 0, '1')
        d.add_transition(0, 1, '0')
        d.add_transition(1, 0, '0')
        d.add_transition(1, 1, '1')

        for i in range(1000):

            s: str = get_random_string()
            j: int = 0

            for symbol in s:
                if symbol == '0':
                    j += 1

            self.assertEqual(bool(j % 2), d.accepts(s))

    def test_three0_in_row(self):

        d = Dfa(4, get_alphabet(), 0, 3)
        d.add_transition(0, 0, '1')
        d.add_transition(0, 1, '0')
        d.add_transition(1, 0, '1')
        d.add_transition(1, 2, '0')
        d.add_transition(2, 0, '1')
        d.add_transition(2, 3, '0')
        d.add_transition(3, 3, '0')
        d.add_transition(3, 3, '1')

        for i in range(1000):

            s: str = get_random_string()
            self.assertEqual('000' in s, d.accepts(s))

    def test_substr_101(self):

        d = Dfa(4, get_alphabet(), 0, 3)
        d.add_transition(0, 0, '0')
        d.add_transition(0, 1, '1')
        d.add_transition(1, 1, '1')
        d.add_transition(1, 2, '0')
        d.add_transition(2, 0, '0')
        d.add_transition(2, 3, '1')
        d.add_transition(3, 3, '0')
        d.add_transition(3, 3, '1')

        for i in range(1000):

            s: str = get_random_string()
            self.assertEqual('101' in s, d.accepts(s))

    def test_substr_010(self):

        d = Dfa(4, get_alphabet(), 0, 3)
        d.add_transition(0, 0, '1')
        d.add_transition(0, 1, '0')
        d.add_transition(1, 1, '0')
        d.add_transition(1, 2, '1')
        d.add_transition(2, 0, '1')
        d.add_transition(2, 3, '0')
        d.add_transition(3, 3, '0')
        d.add_transition(3, 3, '1')

        for i in range(1000):

            s: str = get_random_string()
            self.assertEqual('010' in s, d.accepts(s))

    def test_even_0_and_len(self):

        d = Dfa(4, get_alphabet(), 0, 0)
        d.add_transition(0, 3, '0')
        d.add_transition(0, 1, '1')
        d.add_transition(1, 2, '0')
        d.add_transition(1, 0, '1')
        d.add_transition(2, 1, '0')
        d.add_transition(2, 3, '1')
        d.add_transition(3, 0, '0')
        d.add_transition(3, 2, '1')

        for i in range(1000):

            s: str = get_random_string()
            ctr: int = s.count('0')
            expected: bool = bool(not (ctr % 2)) and bool(not (len(s) % 2))

            self.assertEqual(expected, d.accepts(s))

    def test_even_0_or_len(self):

        d = Dfa(4, get_alphabet(), 0, 0, 1, 2)
        d.add_transition(0, 3, '0')
        d.add_transition(0, 1, '1')
        d.add_transition(1, 2, '0')
        d.add_transition(1, 0, '1')
        d.add_transition(2, 1, '0')
        d.add_transition(2, 3, '1')
        d.add_transition(3, 0, '0')
        d.add_transition(3, 2, '1')

        for i in range(1000):

            s: str = get_random_string()
            ctr: int = s.count('0')
            expected: bool = bool(not (ctr % 2)) or bool(not (len(s) % 2))

            self.assertEqual(expected, d.accepts(s))


class TestNfa(TestCase):

    def test_end_with_110(self):

        n: Nfa = Nfa(4, get_alphabet(), 0, 3)

        n.add_transition(0, 0, '0')
        n.add_transition(0, 1, '1')
        n.add_transition(1, 0, '0')
        n.add_transition(1, 1, '1')
        n.add_transition(1, 2, '1')
        n.add_transition(2, 3, '0')
        n.add_transition(2, 2, '1')

        for i in range(1000):

            s: str = get_random_string()
            self.assertEqual(s[-3:] == '110', n.accepts(s))

    def test_all_accept_nfa(self):

        n: Nfa = Nfa(2, get_alphabet(), 0, 0)

        n.add_transition(0, 1, None)
        n.add_transition(1, 0, '0')
        n.add_transition(1, 0, '1')

        for i in range(1000):
            self.assertEqual(True, n.accepts(get_random_string()))


if __name__ == '__main__':
    main()
