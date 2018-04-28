class NpuzzleView:
    def __init__(self, states):
        self.states = states

    def display(self):
        for i, state in enumerate(self.states):
            print("step number %d: " % (i))
            self.print_state(state)

    def print_state(self, state):
        s = ""
        for row in state:
            for item in row:
                s += ("%3d" % (item)) + " "
            s += "\n"
        print(s, end="")
            
