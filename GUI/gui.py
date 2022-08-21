from tkinter import font
from tkinter import *
from main import new_state_after_operator

# globalna premenne pre GUI
buttons = []
glob_path = []
glob_start_state = []
glob_current_state = []
glob_end_state = []
glob_counter = 0


def gui_create(root, m, n, state):
    root.title("8-hlavolam riešený pomocou A*")
    myFont = font.Font(size=13)
    button = Button(root, text=0, padx=50, pady=30, borderwidth=4, fg='#ffffff', bg='#363636', activebackground='#363636')
    button['font'] = myFont
    buttons.append(button)

    for i in range(1, m*n):
        button = Button(root, text=i, padx=50, pady=30, borderwidth=4, bg="#e6e6e6", activebackground='#e6e6e6')
        button['font'] = myFont
        buttons.append(button)

    gui_update_buttons(m, n, state)

    myFont = font.Font(size=9)
    button = Button(root, text="RESET", padx=30, pady=15, borderwidth=3, fg='#ffffff', bg='#6e54f0',
                    activebackground='#6e54f0', command=gui_reset)
    button['font'] = myFont
    buttons.append(button)

    button = Button(root, text="ĎALŠÍ KROK", padx=20, pady=15, borderwidth=3, fg='#ffffff', bg='#6e54f0',
                    activebackground='#6e54f0', command=gui_next_step)
    button['font'] = myFont
    buttons.append(button)

    buttons[len(buttons)-2].grid(row=n, column=0)
    buttons[len(buttons)-1].grid(row=n, column=m-1)


def gui_update_buttons(m, n, new_state):
    for i in range(n):
        for j in range(m):
            buttons[new_state[i][j]].grid(row=i, column=j)

            if buttons[new_state[i][j]]['text'] == 0:
                continue

            if buttons[new_state[i][j]]['text'] == buttons[glob_end_state[i][j]]['text']:
                buttons[new_state[i][j]].config(bg='#1cc925')
            else:
                buttons[new_state[i][j]].config(bg='#e6e6e6')


def gui_update(state, operator):
    m, n = len(state[0]), len(state)

    # zisti poziciu medzery
    x = y = 0
    for i in range(n):
        for j in range(m):
            if state[i][j] == 0:
                x = i
                y = j
                break

    new_state = new_state_after_operator(state, "Empty", operator, x, y, m, n)
    gui_update_buttons(m, n, new_state)

    return new_state


def gui_next_step():
    global glob_counter, glob_current_state
    if glob_counter >= len(glob_path):
        return

    operator = glob_path[glob_counter]
    glob_counter += 1
    glob_current_state = gui_update(glob_current_state, operator)


def gui_reset():
    global glob_counter, glob_current_state
    glob_counter = 0
    glob_current_state = glob_start_state

    gui_update_buttons(len(glob_start_state[0]), len(glob_start_state), glob_start_state)


def gui(path, m, n, start_node_state, end_node_state):
    global glob_path, glob_start_state, glob_current_state, glob_end_state

    glob_path = path
    glob_start_state = start_node_state
    glob_current_state = start_node_state
    glob_end_state = end_node_state

    root = Tk()
    gui_create(root, m, n, start_node_state)
    root.mainloop()
