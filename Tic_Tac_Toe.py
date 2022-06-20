def show_field():
    print()
    print('     |  0  |  1  |  2  | ')
    print('  ======================')
    for i, j in enumerate(field):
        print(f"  {i}  |  {'  |  '.join(map(str, j))}  |")
        print('  ======================')


def ask():
    while True:
        coord = input('        Your move: ').split()

        if len(coord) != 2:
            print('   Enter 2 coordinates!')
            continue

        x, y = coord

        if not (x.isdigit()) or not (y.isdigit()):
            print('   Enter only numbers!')
            continue

        x, y = int(x), int(y)

        if x < 0 or x > 2 or y < 0 or y > 2:
            print('   Coordinates out of range!')
            continue

        if field[x][y] != " ":
            print('   The cell is occupied!')
            continue

        return x, y


def check_win():
    win_coord = [((0, 0), (0, 1), (0, 2)), ((1, 0), (1, 1), (1, 2)), ((2, 0), (2, 1), (2, 2)),
                 ((0, 0), (1, 0), (2, 0)), ((0, 1), (1, 1), (2, 1)), ((0, 2), (1, 2), (2, 2)),
                 ((0, 0), (1, 1), (2, 2)), ((0, 2), (1, 1), (2, 0))]

    for coord in win_coord:
        a, b, c = coord[0], coord[1], coord[2]

        if field[a[0]][a[1]] == field[b[0]][b[1]] == field[c[0]][c[1]] != ' ':
            show_field()
            print('!!!!!CONGRATULATION!!!!!')
            print(f'       Won "{field[a[0]][a[1]]}"!')
            return True

    return False


field = [[' ' for j in range(3)] for i in range(3)]
move = 0
while True:
    move += 1

    show_field()

    if move % 2 == 1:
        print('       Now move "X"')
    else:
        print('    Now move "0"')

    x, y = ask()

    if move % 2 == 1:
        field[x][y] = 'X'
    else:
        field[x][y] = '0'

    if check_win():
        break

    if move == 9:
        show_field()
        print('Draw!!!')
        break
