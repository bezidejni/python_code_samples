#!/usr/bin/env python

class Turing:
    """A deterministic Turing machine with infinite tape"""
    
    def __init__(self, path):
        self.table_path = path
        self.transitions = {}
        self.current_char_index = 0
        self.spatial_complexity = 0
        self.space = []
        self.time_complexity = 0
        self.tape = ""
        self.current_char = ""
        self.current_state = 0 

    def machine_initialize(self):
        self.read_starting_state()
        self.load_transitions()
        self.load_tape('Input a string of characters: ')
        self.read_head_position('Input head position: ')


    def simulate(self):
        while True:
            self.read_char_from_tape()
            transition = self.transition_function()
            if (transition):
                self.change_state(transition)
                self.write_char_to_tape(transition)
                self.move(transition)
            else:
                break
        self.check_spatial_complexity()


    def report(self):
        print "\n"
        print "Time complexity is %d" % self.time_complexity
        print "Spatial complexity is %d" % self.spatial_complexity

    def read_starting_state(self):
        input = open(self.table_path, 'r')
        self.current_state = input.readline().strip()
        input.close()
    
    def load_transitions(self):
        input = open(self.table_path, 'r')
        input.seek(2)
        
        for row in input.readlines():
            content = row.strip().split('#')
            key = content[0] + content[1]            
            self.transitions[key] = {'new_state' : content[2], 'new_char' : content[3], 'move' : content[4]}
        input.close()



    def load_tape(self, tekst):
        self.tape = raw_input(tekst)
        self.space = [0 for x in xrange(len(self.tape))]
        
    def read_head_position(self, tekst, position=0):
        position = int(raw_input(tekst))
        if (position < 0):
            self.tape = abs(position) * "B" + self.tape
            self.space = [0 for x in xrange(abs(position))] + self.space
            self.current_char_index = 0
        elif (position >= len(self.tape)):
            difference = position - (len(self.tape) - 1)
            self.tape = self.tape + difference * "B"
            self.space = self.space + [0 for x in xrange(difference)]
            self.current_char_index = position
        else:
            self.current_char_index = position


    def read_char_from_tape(self):
        self.current_char = self.tape[self.current_char_index]


    def change_state(self, transition):
        self.current_state = transition["new_state"]


    def write_char_to_tape(self, transition):
        self.tape = self.tape[0:self.current_char_index] + transition["new_char"] + self.tape[self.current_char_index + 1 :]
        self.space[self.current_char_index] = 1


    def transition_function(self):
        key = self.current_state + self.current_char
        if (key in self.transitions):
            return self.transitions[key]
        else:
            return False

    def move(self, transition):
        if (transition["move"] == "L"):
            self.go_left()
        elif (transition["move"] == "D"):
            self.go_right()
        self.time_complexity += 1

    def check_spatial_complexity(self):
        for cell in self.space:
            if (cell == 1):
                self.spatial_complexity += 1


    def go_left(self):
        self.current_char_index -= 1
        if (self.current_char_index < 0):
            self.tape = "B" + self.tape
            self.space = [0] + self.space
            self.current_char_index = 0

    def go_right(self):
        self.current_char_index += 1
        if (self.current_char_index >= len(self.tape)):
            self.tape = self.tape + "B"
            self.space = self.space + [0]




if __name__ == "__main__":
    turing = Turing('funkcije.txt')
    turing.machine_initialize()
    turing.simulate()
    turing.report()
    
