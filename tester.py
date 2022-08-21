import random


def generate_row(m, n, used_nums):
    row = []
    for i in range(m):
        while True:
            rand_int = random.randint(0, m*n-1)
            if not used_nums[rand_int]:
                row.append(rand_int)
                used_nums[rand_int] = True
                break
    return row


def generate_test():
    n, m = random.randint(2, 3), random.randint(2, 4)
    if n == 3:
        m = random.randint(2, 3)

    numbers = []
    for i in range(n*m):
        numbers.append(i)

    start_node_state = []
    end_node_state = []
    used_nums = [False for i in range(n*m)]
    for i in range(n):
        start_node_state.append(generate_row(m, n, used_nums))

    used_nums = [False for i in range(n*m)]
    for i in range(n):
        end_node_state.append(generate_row(m, n, used_nums))

    return start_node_state, end_node_state
