#!/usr/bin/env python


class PdaAutomaton():
    """A non-deterministic pushdown automaton, accepts arithmetic expressions
    in infix notation. 
    
    Example: (A+B)*(C-A)-B
    """

    def __init__(self):
        self.transitions = []
        self.stack = 'K'
        self.poc_state = 'q0'
        self.input = ''
        self.dop_state = 'qe'
        self.A = ['A', 'B', 'C', 'D', 'E']
        self

    def load_transitions(self, path):
        input = open('automat.txt', 'r')
        i = 0
        for red in input.readlines():
            content = red.strip().split('\t')
            tren = content[0].strip().split(',')
            sljed = content[1].strip().split(',')
            self.transitions.append({
                'q': tren[0],
                'a': tren[1].replace('e', ''),
                'Z': tren[2],
                'p': sljed[0],
                'y': sljed[1].replace('e', '')
            })

            i += 1
        input.close()

    def load_input(self, text):
        self.input = raw_input(text)
        self.input = self.input.replace('B', 'A')
        self.input = self.input.replace('C', 'A')
        self.input = self.input.replace('D', 'A')
        self.input = self.input.replace('E', 'A')
        self.input = self.input.replace('/', '*')
        self.input = self.input.replace('-', '+')

    def simulate(self):
        if self.accept(self.poc_state, self.input, self.stack):
            print "input accepted"
        else:
            print "input not accepted"

    def print_status(self, ind, state, input, tmp_stack):
        f = self.transitions[ind]
        print "Currently loading: %s" % input[0]
        print "Current state: %s" % state
        print "Current stack state: %s" % tmp_stack
        tmp_stack = self.update_stack(tmp_stack, f['y'])
        print "Current transition (%s,%s,%s) -> (%s,%s)" %\
                (f['q'], f['a'], f['Z'], f['p'], f['y'])
        print "New state %s" % f['p']
        print "New stack state %s" % tmp_stack
        print "\n\n"

    def update_stack(self, st, txt):
        st = st[:-1] + txt[::-1]
        return st

    def accept(self, state, input, stack):
        vr = []
        if state == self.dop_state and input == '':
            return 1
        elif input == '':
            return 0
        else:
            for letter in input:
                p_ind = []
                for p in self.transitions:
                    if (p['q'] == state and p['a'] == letter
                            and p['Z'] == stack[-1]):
                        p_ind.append(self.transitions.index(p))
                for p in p_ind:
                    self.print_status(p, state, input, stack)
                    vr.append(self.accept(self.transitions[p]['p'],
                        input[1:], self.update_stack(stack, self.transitions[p]['y'])))
                if 1 in vr:
                    return 1
                else:
                    return 0


if __name__ == "__main__":
    automat = PdaAutomaton()
    automat.load_transitions('automat.txt')
    automat.load_input('Upisi input znakova: ')
    automat.simulate()
