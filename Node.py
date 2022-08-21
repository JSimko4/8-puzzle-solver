class Node:
    neighbours = []

    h_cost = 0  # vzdialenost od konecneho uzla - heuristika
    g_cost = 0  # vzdialenost od pociatocneho uzla - hlbka uzla
    f_cost = 0  # celkove ohodnotenie vzdialenosti : f(n) = h(n) + g(n)

    operator = ""  # operator ktorym vznikol tento stav

    # state_string nemusi byt ukladany ale v takom pripade bude program pri kazdom volani
    # na ziskanie state_string vykonat cyklus n*m, čo sa následne ukáže na rýchlosti algoritmu
    state_string = ""  # stav ulozeny vo forme retazca pre hladanie/vkladanie do slovnika

    def __init__(self, state, previous):
        self.state = state
        self.previous = previous

    # porovnavacia funkcia pre spravnu funkciu priorityq
    def __lt__(self, other):
        return self.f_cost < other.f_cost

    # porovnavacia funkcia pre spravnu funkciu priorityq
    def __le__(self, other):
        return self.f_cost <= other.f_cost

    # snazim sa nevolat funkciu set_state_string() az dokedy nie je nutne vyuzit state_string atribut
    def get_state_string(self):
        if self.state_string == "":
            self.set_state_string()
        return self.state_string

    def set_state_string(self):
        m, n = len(self.state[0]), len(self.state)
        for i in range(n):
            for j in range(m):
                self.state_string += str(self.state[i][j])

    def set_g_cost(self):
        if self.previous is not None:
            self.g_cost = self.previous.g_cost + 1
        else:
            self.g_cost = 0

    def set_f_cost(self):
        self.f_cost = self.g_cost + self.h_cost

    def set_operator(self, index):
        if index == 0:
            self.operator = "DOLAVA"
        elif index == 1:
            self.operator = "DOPRAVA"
        elif index == 2:
            self.operator = "HORE"
        else:
            self.operator = "DOLE"

    def print_node(self):
        print(f"Stav: {self.state}")
        print(f"g_cost: {self.g_cost}\n"
              f"h_cost: {self.h_cost}\n"
              f"f_cost: {self.f_cost}\n")
