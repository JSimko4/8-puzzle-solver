import time
from queue import PriorityQueue
from GUI.gui import *
from Node import Node
from tester import generate_test

# Autor: Jakub Šimko
# IDE: PyCharm
# Dátum vytvorenia: 14.10.2021


# 1. heuristika - počet políčok, ktoré nie sú na svojom mieste
def heuristic1(curr_node_state, end_node_state, m, n):
    heuristic_value = 0
    for i in range(n):
        for j in range(m):
            # do heuristiky nezapočítavam medzeru
            if curr_node_state[i][j] == 0:
                continue

            if curr_node_state[i][j] != end_node_state[i][j]:
                heuristic_value += 1

    return heuristic_value


def manhattan_distance(x1, x2, y1, y2):
    return abs(x1-x2) + abs(y1-y2)


# 2. heuristika - súčet vzdialeností jednotlivých políčok od ich cieľovej pozície
def heuristic2(curr_node_state, end_node_state, m, n):
    positions1 = {}
    positions2 = {}

    # pozicia v aktualnom stave
    for i in range(n):
        for j in range(m):
            if curr_node_state[i][j] != 0:
                positions1[curr_node_state[i][j]] = i, j

            if end_node_state[i][j] != 0:
                positions2[end_node_state[i][j]] = i, j

    total_distance = 0
    for number, coordinates in positions1.items():
        total_distance += manhattan_distance(positions1[number][0], positions2[number][0],
                                             positions1[number][1], positions2[number][1])

    return total_distance


def new_state_after_operator(state, last_operator, operator, x, y, m, n):
    if last_operator != "DOPRAVA" and operator == "DOLAVA" and y+1 < m:
        new_state = [copy[:] for copy in state]
        new_state[x][y] = state[x][y+1]
        new_state[x][y+1] = 0

    elif last_operator != "DOLAVA" and operator == "DOPRAVA" and y-1 >= 0:
        new_state = [copy[:] for copy in state]
        new_state[x][y] = state[x][y-1]
        new_state[x][y-1] = 0

    elif last_operator != "HORE" and operator == "DOLE" and x-1 >= 0:
        new_state = [copy[:] for copy in state]
        new_state[x][y] = state[x-1][y]
        new_state[x-1][y] = 0

    elif last_operator != "DOLE" and operator == "HORE" and x+1 < n:
        new_state = [copy[:] for copy in state]
        new_state[x][y] = state[x+1][y]
        new_state[x+1][y] = 0

    else:  # dany operator sa neda vykonať
        return None

    return new_state


def create_neighbours(current_node, m, n):
    neighbours = []
    state = current_node.state

    # zisti poziciu medzery
    x = y = 0
    for i in range(n):
        for j in range(m):
            if state[i][j] == 0:
                x = i
                y = j
                break

    new_states = [new_state_after_operator(state, current_node.operator, "DOLAVA", x, y, m, n),
                  new_state_after_operator(state, current_node.operator, "DOPRAVA", x, y, m, n),
                  new_state_after_operator(state, current_node.operator, "HORE", x, y, m, n),
                  new_state_after_operator(state, current_node.operator, "DOLE", x, y, m, n)]

    i = -1
    neighbours_count = 0
    for new_state in new_states:  # cyklus vytvara susedov - nove uzly
        i += 1
        if new_state is None:
            continue

        neighbour = Node(new_state, current_node)
        neighbour.set_operator(i)
        neighbours.append(neighbour)
        neighbours_count += 1

    return neighbours, neighbours_count


def update_que(que, updated_node):
    for i in range(len(que.queue)):
        temp = que.get()
        que.put(temp)
        if temp == updated_node:
            break


def reconstruct_path(end_node):
    path = []

    node = end_node
    while node.previous is not None:
        path.insert(0, node.operator)
        node = node.previous

    return path


# argument heuristic obsahuje heuristiku ktoru ma a* vyuzivat
def a_star(heuristic, start_node_state, end_node_state, m, n):
    path = []
    open_check = {}

    # vytvori začiatočny uzol
    start_node = Node(start_node_state, None)
    start_node.set_g_cost()
    start_node.h_cost = heuristic(start_node_state, end_node_state, m, n)
    start_node.set_f_cost()

    # priority que z python knižnice
    openSet = PriorityQueue()
    openSet.put(start_node)
    open_check[start_node.get_state_string()] = True

    # počítadla
    found_path = False
    analysed_nodes_counter = 0
    created_nodes_counter = 0
    while not openSet.empty():
        current_node = openSet.get()  # ziskanie elementu ho odstrani z q
        open_check[current_node.get_state_string()] = False
        analysed_nodes_counter += 1

        # rekonstrukcia cesty
        if current_node.state == end_node_state:
            found_path = True
            path = reconstruct_path(current_node)
            break

        current_node.neighbours, new_neighbours_count = create_neighbours(current_node, m, n)
        created_nodes_counter += new_neighbours_count
        for neighbour in current_node.neighbours:
            # ak sa daný stav nenachádza v slovníku tak ešte nebol nikdy vložený do que (openSet) - novy susedia
            if neighbour.get_state_string() not in open_check:
                neighbour.set_g_cost()
                neighbour.h_cost = heuristic(neighbour.state, end_node_state, m, n)
                neighbour.set_f_cost()

                openSet.put(neighbour)
                open_check[neighbour.get_state_string()] = True
                continue

            # stav je v closedSet
            if not open_check[neighbour.get_state_string()]:
                continue

            # stav sa nachádaza v que (openSet)
            # program sa musi pozrieť či neexistuje efektívnejšia cesta do tohto uzla

            # If the heuristic is consistent,
            # when a node is removed from openSet the path to it is guaranteed to be optimal
            # so the test ‘tentative_gScore < gScore[neighbor]’ will always fail if the node is reached again.
            # https://en.wikipedia.org/wiki/A*_search_algorithm
            temp_g_cost = current_node.g_cost + 1
            if temp_g_cost < neighbour.g_cost:  # efektivnejšia cesta
                neighbour.previous = current_node
                neighbour.g_cost = temp_g_cost
                neighbour.set_f_cost()
                update_que(openSet, neighbour)  # upravil sa f_cost je nutne aktualizovat que

    print(f"Pocet vytvorených uzlov: {created_nodes_counter}")
    print(f"Pocet spracovaných uzlov: {analysed_nodes_counter}")
    print(f"Počet ťahov riešenia: {len(path)}")

    # V pripade kedy program prejde všetky dostupné kombinácie uzlov tak problém nema riešenie
    # Zo začiatočneho stavu ktory nema riešenie sa počet spracovanych uzlov == (n*m)!/2
    if not found_path:
        print("Nepodarilo sa nájsť riešenie")

    print(path)  # dodatocny vypis riešenia - moze/nemusi byt vhodny pri vypisoch z testov / vstupu

    return path


# CLI INTERFACE
def print_path(path):
    i = 1
    for operator in path:
        if i % 8 == 0:
            print(operator)
        else:
            print(operator, end=" ")
        i += 1
    print(" ")


def print_state(state):
    m, n = len(state[0]), len(state)
    for i in range(n):
        for j in range(m):
            print(state[i][j], end=" ")
        print(" ")


def print_commands():
    print("Príkazy:\n"
          "1     :   Zadanie vlastného hlavolamu - rozmery, začiatočny, koncový stav, výber heuristiky, vizualizácia pomocou GUI alebo naformatovaný výpis riešenia\n"
          "2     :   Funkcia testovania - vygeneruje X náhodnych testov (generuje rozmery, začiatočný a koncový stav a vykoná obidve heuristiky\n"
          "          Aby testy netrvali príliš dlho sú rozmery náhodné ale v rozmedzí: 2x2-4 alebo 3x2-3\n"
          "k     :   Ukončí program")


def cli_interface():
    print("Zadaj rozmery hlavolamu...\n")
    print("Počet riadkov:")
    n = int(input())
    print("Počet stlpcov:")
    m = int(input())

    print("Zadaj začiatočný stav vo formáte: 012 345 ...")
    print("Riadky sú oddelené medzerou")
    start_input = input()
    start_input = start_input.split(" ")

    print("Zadaj koncový stav vo formáte: 345 012 ...")
    print("Každý riadok oddelený medzerou.")
    end_input = input()
    end_input = end_input.split(" ")

    start_node_state = [[] for i in range(n)]
    end_node_state = [[] for i in range(n)]
    for i in range(n):
        for j in range(m):
            start_node_state[i].append(int(start_input[i][j]))
            end_node_state[i].append(int(end_input[i][j]))

    print("###############################")
    print(f"Rozmery hlavolamu {n}x{m}")
    print("Začiatočný stav:")
    print_state(start_node_state)
    print("Koncový stav:")
    print_state(end_node_state)
    print("###############################")
    print("Program po výbere heuristiky začne hľadať riešenie...")

    return m, n, start_node_state, end_node_state


def gui_cli_option(path, m, n, start_node_state, end_node_state):
    print("Otvoriť GUI s riešením? y/n\n"
          'V prípade odpovede "n" sa na termináli vypíše naformátované riešenie.')
    command = input()
    if command == "y":
        gui(path, m, n, start_node_state, end_node_state)
    elif command == "n":
        print_path(path)


# n = pocet riadkov
# m = pocet stlpcov
def main():
    command = "xxx"
    while command != "k":
        print_commands()
        command = input()
        if command == "1":
            m, n, start_node_state, end_node_state = cli_interface()

            # ak sa zakomentuje riadok 286 tak je mozne pomocou kodu zadat vstupny/koncovy stav: odkomentovat 3 riadky dole
            # start_node_state = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]
            # end_node_state = [[4, 3, 2, 6, 1], [9, 8, 7, 5, 0]]
            # m, n = len(start_node_state[0]), len(start_node_state)

            print("Výber heuristiky:\n"
                  "1                         :   Heuristika 1: Počet políčok, ktoré nie su na svojom mieste\n"
                  "2 / Akýkoľvek iný znak    :   Heuristika 2: Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície")
            cmd = input()
            if cmd == "1":
                print("Heuristika 1: Počet políčok, ktoré nie su na svojom mieste")

                start_time = time.process_time()
                path = a_star(heuristic1, start_node_state, end_node_state, m, n)
                elapsed_time = time.process_time() - start_time

                print(f"Čas vykonávania algoritmu: {elapsed_time}s\n")
                gui_cli_option(path, m, n, start_node_state, end_node_state)
            else:
                print("Heuristika 2: Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície")

                start_time = time.process_time()
                path = a_star(heuristic2, start_node_state, end_node_state, m, n)
                elapsed_time = time.process_time() - start_time

                print(f"Čas vykonávania algoritmu: {elapsed_time}s\n")
                gui_cli_option(path, m, n, start_node_state, end_node_state)

        elif command == "2":
            print("Zadaj počet testov:")
            x = int(input())
            test_count = x
            heuristic1_avg_time = 0
            heuristic2_avg_time = 0
            for i in range(0, x):
                start_node_state, end_node_state = generate_test()
                m, n = len(start_node_state[0]), len(start_node_state)

                print("###############################")
                print(f"Rozmery hlavolamu {n}x{m}")
                print("Začiatočný stav:")
                print_state(start_node_state)
                print("Koncový stav:")
                print_state(end_node_state)
                print("###############################")
                print("Program začína hľadať riešenie...")

                print("Heuristika 1: Počet políčok, ktoré nie su na svojom mieste")
                start_time = time.process_time()
                path = a_star(heuristic1, start_node_state, end_node_state, m, n)
                elapsed_time = time.process_time() - start_time
                if len(path) == 0:
                    test_count -= 1
                else:
                    heuristic1_avg_time += elapsed_time
                print(f"Čas vykonávania algoritmu: {elapsed_time}s\n")

                print("Heuristika 2: Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície")
                start_time = time.process_time()
                path = a_star(heuristic2, start_node_state, end_node_state, m, n)
                elapsed_time = time.process_time() - start_time
                if len(path) != 0:
                    heuristic2_avg_time += elapsed_time

                print(f"Čas vykonávania algoritmu: {elapsed_time}s\n")

            if test_count == 0:
                test_count = 1
            print(f"Priemerný čas vykonávania algoritmu:\n"
                  f"Heuristika 1 Počet políčok, ktoré nie su na svojom mieste                        :   {heuristic1_avg_time/test_count}s\n"
                  f"Heuristika 2 Súčet vzdialeností jednotlivých políčok od ich cieľovej pozície     :   {heuristic2_avg_time/test_count}s")
        elif command == "k":
            return 0
        else:
            print("Neznámy príkaz...")


if __name__ == "__main__":
    main()
