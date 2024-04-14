############################################################################################################
# This script is used to generate an SMV model for the Sokoban game. The script reads the board from a file
# and generates the SMV model for the game. The script generates the initial state, the transitions, and the
# winning conditions for the game. The script generates the SMV model and saves it to a file.
# Author: Avidan Menashe     - 207812421
#         Chen Cohen Gershon - 208955732
############################################################################################################
import os


def read_board_from_file(file_path):
    """
    Read the board from a file and return it as a 2D list
    :param file_path: the path in which the board file is located
    :return: the board as a 2D list
    """
    with open(file_path, 'r') as file:
        # this code takes each line from the file and converts it to a list of characters
        # Also, it removes the '\n' character
        # board = [list(line.strip()) for line in file]
        board = [list(line.strip()) for line in file if line.strip()]

    # iterate over the board and search for a char prefix of '\u202'
    # if found, remove it
    for lst in board:
        for i in range(len(lst)):
            if lst[i] not in ['#', '@', '$', '.', '+', '*', '-']:
                # we need to remove it, create a new list that contains the correct characters only
                new_lst = []
                for char in lst:
                    if char in ['#', '@', '$', '.', '+', '*', '-']:
                        new_lst.append(char)
                # replace the old list with the new list
                board.insert(board.index(lst), new_lst)
                # remove the old list
                board.remove(lst)
                break
    return board

def create_initial_state(board, n, m):
    init_str = ""
    row_indx = 0
    col_indx = 0
    for y in range(n):
        for x in range(m):
            if y == n - 1 and x == m - 1:
                # Map XSB symbols to char values in SMV model
                if board[y][x] == '#':
                    init_str += f"game_board[{row_indx}][{col_indx}] = Wall;\n\t\t"  # Wall
                elif board[y][x] == '@':
                    init_str += f"game_board[{row_indx}][{col_indx}] = Player;\n\t\t"  # Player
                elif board[y][x] == '$':
                    init_str += f"game_board[{row_indx}][{col_indx}] = Box;\n\t\t"  # Box
                elif board[y][x] == '.':
                    init_str += f"game_board[{row_indx}][{col_indx}] = Goal;\n\t\t"  # Target
                elif board[y][x] == '+':
                    init_str += f"game_board[{row_indx}][{col_indx}] = PonGoal;\n\t\t"  # Player on target
                elif board[y][x] == '*':
                    init_str += f"game_board[{row_indx}][{col_indx}] = BonGoal;\n\t\t"  # Box on target
                elif board[y][x] == '-':
                    init_str += f"game_board[{row_indx}][{col_indx}] = Floor;\n\t\t"  # Floor
            else:
                # Map XSB symbols to char values in SMV model
                if board[y][x] == '#':
                    init_str += f"game_board[{row_indx}][{col_indx}] = Wall &\n\t"  # Wall
                elif board[y][x] == '@':
                    init_str += f"game_board[{row_indx}][{col_indx}] = Player &\n\t"  # Player
                elif board[y][x] == '$':
                    init_str += f"game_board[{row_indx}][{col_indx}] = Box &\n\t"  # Box
                elif board[y][x] == '.':
                    init_str += f"game_board[{row_indx}][{col_indx}] = Goal &\n\t"  # Target
                elif board[y][x] == '+':
                    init_str += f"game_board[{row_indx}][{col_indx}] = PonGoal &\n\t"  # Player on target
                elif board[y][x] == '*':
                    init_str += f"game_board[{row_indx}][{col_indx}] = BonGoal &\n\t"  # Box on target
                elif board[y][x] == '-':
                    init_str += f"game_board[{row_indx}][{col_indx}] = Floor &\n\t"  # Floor

            col_indx += 1

        col_indx = 0
        row_indx += 1

    return init_str

def define_transitions(board):
    """
    Define the transitions for the Sokoban game
    :param board: the board as a 2D list
    :return:
    """
    transitions = ''
    num_rows = len(board)
    num_cols = len(board[0])

    # first, filter all cells equal to '#' and save the indices of those cells
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == '#':
                transitions += f'next(game_board[{i}][{j}]) := Wall;\n\t'
            else:
                transitions += f'\n\tnext(game_board[{i}][{j}]) := \n\t\tcase\n'
                # MAYBE IN DEFAULT CASE
                transitions += f'\t\t\t--Current @ V + next cell #\n'
                transitions += (f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) '
                                f'& movement = l & game_board[{i}][{j - 1}] = Wall: game_board[{i}][{j}];\n')
                transitions += (f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) '
                                f'& movement = r & game_board[{i}][{j + 1}] = Wall: game_board[{i}][{j}];\n')
                transitions += (f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) '
                                f'& movement = u & game_board[{i - 1}][{j}] = Wall: game_board[{i}][{j}];\n')
                transitions += (f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) '
                                f'& movement = d & game_board[{i + 1}][{j}] = Wall: game_board[{i}][{j}];\n\n')

                # -----------------------------------------------------------------------------------------------
                transitions += f'\t\t\t--Current @ next cell .\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = l & game_board[{i}][{j-1}] = Goal: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = r & game_board[{i}][{j+1}] = Goal: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = u & game_board[{i-1}][{j}] = Goal: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = d & game_board[{i+1}][{j}] = Goal: Floor;\n\n'

                transitions += '\t\t\t-- other tiles cases for Current @ next cell .\n'
                transitions += f'\t\t\tgame_board[{i}][{j+1}] = Player & movement = l & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j-1}] = Player & movement = r & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i+1}][{j}] = Player & movement = u & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i-1}][{j}] = Player & movement = d & game_board[{i}][{j}] = Goal: PonGoal;\n\n'

                # -----------------------------------------------------------------------------------------------
                transitions += f'\t\t\t--Current @ next cell -\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = l & game_board[{i}][{j-1}] = Floor: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = r & game_board[{i}][{j+1}] = Floor: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = u & game_board[{i-1}][{j}] = Floor: Floor;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = Player & movement = d & game_board[{i+1}][{j}] = Floor: Floor;\n\n'

                transitions += '\t\t\t-- other tiles cases for Current @ next cell -\n'
                transitions += f'\t\t\tgame_board[{i}][{j+1}] = Player & movement = l & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i}][{j-1}] = Player & movement = r & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i+1}][{j}] = Player & movement = u & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i-1}][{j}] = Player & movement = d & game_board[{i}][{j}] = Floor: Player;\n\n'

                # -----------------------------------------------------------------------------------------------
                # MAYBE IN DEFAULT CASE
                transitions += f'\t\t\t--Current @ V + next cell $ V * next next cell $ V # V *\n'
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) '
                        f'& movement = l & (game_board[{i}][{j - 1}] = Box | game_board[{i}][{j - 1}] = BonGoal) & '
                        f'(game_board[{i}][{j - 2}] = Box | game_board[{i}][{j - 2}] = Wall | game_board[{i}][{j - 2}] = BonGoal)'
                        f' : game_board[{i}][{j}];\n')
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) '
                        f'& movement = r & (game_board[{i}][{j + 1}] = Box | game_board[{i}][{j + 1}] = BonGoal) & '
                        f'(game_board[{i}][{j + 2}] = Box | game_board[{i}][{j + 2}] = Wall | game_board[{i}][{j + 2}] = BonGoal)'
                        f' : game_board[{i}][{j}];\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) '
                        f'& movement = u & (game_board[{i - 1}][{j}] = Box | game_board[{i - 1}][{j}] = BonGoal) & '
                        f'(game_board[{i - 2}][{j}] = Box | game_board[{i - 2}][{j}] = Wall | game_board[{i - 2}][{j}] = BonGoal)'
                        f' : game_board[{i}][{j}];\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j}] = Player | game_board[{i}][{j}] = PonGoal) '
                        f'& movement = d & (game_board[{i + 1}][{j}] = Box | game_board[{i + 1}][{j}] = BonGoal) & '
                        f'(game_board[{i + 2}][{j}] = Box | game_board[{i + 2}][{j}] = Wall | game_board[{i + 2}][{j}] = BonGoal)'
                        f' : game_board[{i}][{j}];\n\n')
                # -----------------------------------------------------------------------------------------------
                transitions += f'\t\t\t--Current @ next cell $ V * next next cell - V .\n'
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = Player & movement = l '
                        f'& (game_board[{i}][{j - 1}] = Box | game_board[{i}][{j - 1}] = BonGoal) & '
                        f'(game_board[{i}][{j - 2}] = Floor | game_board[{i}][{j - 2}] = Goal): Floor;\n')
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = Player & movement = r '
                        f'& (game_board[{i}][{j + 1}] = Box | game_board[{i}][{j + 1}] = BonGoal) & '
                        f'(game_board[{i}][{j + 2}] = Floor | game_board[{i}][{j + 2}] = Goal): Floor;\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = Player & movement = u '
                        f'& (game_board[{i - 1}][{j}] = Box | game_board[{i - 1}][{j}] = BonGoal) & '
                        f'(game_board[{i - 2}][{j}] = Floor | game_board[{i - 2}][{j}] = Goal): Floor;\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = Player & movement = d '
                        f'& (game_board[{i + 1}][{j}] = Box | game_board[{i + 1}][{j}] = BonGoal) & '
                        f'(game_board[{i + 2}][{j}] = Floor | game_board[{i + 2}][{j}] = Goal): Floor;\n\n')

                transitions += '\t\t\t-- other tiles cases\n'
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j + 2}] = Player | game_board[{i}][{j + 2}] = PonGoal) '
                        f'& movement = l & (game_board[{i}][{j + 1}] = Box | game_board[{i}][{j + 1}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Floor: Box;\n')
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j - 2}] = Player | game_board[{i}][{j - 2}] = PonGoal) '
                        f'& movement = r & (game_board[{i}][{j - 1}] = Box | game_board[{i}][{j - 1}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Floor: Box;\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\t(game_board[{i + 2}][{j}] = Player | game_board[{i + 2}][{j}] = PonGoal) '
                        f'& movement = u & (game_board[{i + 1}][{j}] = Box | game_board[{i + 1}][{j}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Floor: Box;\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i - 2}][{j}] = Player | game_board[{i - 2}][{j}] = PonGoal) '
                        f'& movement = d & (game_board[{i - 1}][{j}] = Box | game_board[{i - 1}][{j}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Floor: Box;\n\n')

                # -----------------------------------------------------------------------------------------------
                transitions += (
                    f'\t\t\t(game_board[{i}][{j + 1}] = Player | game_board[{i}][{j + 1}] = PonGoal) '
                    f'& movement = l & game_board[{i}][{j}] = Box & '
                    f'(game_board[{i}][{j - 1}] = Floor | game_board[{i}][{j - 1}] = Goal): Player;\n')
                transitions += (
                    f'\t\t\t(game_board[{i}][{j - 1}] = Player | game_board[{i}][{j - 1}] = PonGoal) '
                    f'& movement = r & game_board[{i}][{j}] = Box & '
                    f'(game_board[{i}][{j + 1}] = Floor | game_board[{i}][{j + 1}] = Goal): Player;\n')
                transitions += (
                    f'\t\t\t(game_board[{i + 1}][{j}] = Player | game_board[{i + 1}][{j}] = PonGoal) '
                    f'& movement = u & game_board[{i}][{j}] = Box & '
                    f'(game_board[{i - 1}][{j}] = Floor | game_board[{i - 1}][{j}] = Goal): Player;\n')
                transitions += (
                    f'\t\t\t(game_board[{i - 1}][{j}] = Player | game_board[{i - 1}][{j}] = PonGoal) '
                    f'& movement = d & game_board[{i}][{j}] = Box & '
                    f'(game_board[{i + 1}][{j}] = Floor | game_board[{i + 1}][{j}] = Goal): Player;\n\n')
                # -----------------------------------------------------------------------------------------------
                transitions += (
                    f'\t\t\t(game_board[{i}][{j + 1}] = Player | game_board[{i}][{j + 1}] = PonGoal) '
                    f'& movement = l & game_board[{i}][{j}] = BonGoal & '
                    f'(game_board[{i}][{j - 1}] = Floor | game_board[{i}][{j - 1}] = Goal): PonGoal;\n')
                transitions += (
                    f'\t\t\t(game_board[{i}][{j - 1}] = Player | game_board[{i}][{j - 1}] = PonGoal) '
                    f'& movement = r & game_board[{i}][{j}] = BonGoal & '
                    f'(game_board[{i}][{j + 1}] = Floor | game_board[{i}][{j + 1}] = Goal): PonGoal;\n')
                transitions += (
                    f'\t\t\t(game_board[{i + 1}][{j}] = Player | game_board[{i + 1}][{j}] = PonGoal) '
                    f'& movement = u & game_board[{i}][{j}] = BonGoal & '
                    f'(game_board[{i - 1}][{j}] = Floor | game_board[{i - 1}][{j}] = Goal): PonGoal;\n')
                transitions += (
                    f'\t\t\t(game_board[{i - 1}][{j}] = Player | game_board[{i - 1}][{j}] = PonGoal) '
                    f'& movement = d & game_board[{i}][{j}] = BonGoal & '
                    f'(game_board[{i + 1}][{j}] = Floor | game_board[{i + 1}][{j}] = Goal): PonGoal;\n\n')
                # -----------------------------------------------------------------------------------------------

                transitions += '\t\t\t-- other tiles cases\n'
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j + 2}] = Player | game_board[{i}][{j + 2}] = PonGoal) '
                        f'& movement = l & (game_board[{i}][{j + 1}] = Box | game_board[{i}][{j + 1}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Goal: BonGoal;\n')
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i}][{j - 2}] = Player | game_board[{i}][{j - 2}] = PonGoal) '
                        f'& movement = r & (game_board[{i}][{j - 1}] = Box | game_board[{i}][{j - 1}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Goal: BonGoal;\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\t(game_board[{i + 2}][{j}] = Player | game_board[{i + 2}][{j}] = PonGoal) '
                        f'& movement = u & (game_board[{i + 1}][{j}] = Box | game_board[{i + 1}][{j}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Goal: BonGoal;\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\t(game_board[{i - 2}][{j}] = Player | game_board[{i - 2}][{j}] = PonGoal) '
                        f'& movement = d & (game_board[{i - 1}][{j}] = Box | game_board[{i - 1}][{j}] = BonGoal) & '
                        f'game_board[{i}][{j}] = Goal: BonGoal;\n\n')

                transitions += '\t\t\t-- other tiles cases\n'
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j + 2}] = Player & movement = l & game_board[{i}][{j + 1}] = BonGoal & '
                        f'game_board[{i}][{j}] = Floor: PonGoal;\n')
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j - 2}] = Player & movement = r & game_board[{i}][{j - 1}] = BonGoal & '
                        f'game_board[{i}][{j}] = Floor: PonGoal;\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\tgame_board[{i + 2}][{j}] = Player & movement = u & game_board[{i + 1}][{j}] = BonGoal & '
                        f'game_board[{i}][{j}] = Floor: PonGoal;\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i - 2}][{j}] = Player & movement = d & game_board[{i - 1}][{j}] = BonGoal & '
                        f'game_board[{i}][{j}] = Floor: PonGoal;\n\n')
                # -----------------------------------------------------------------------------------------------

                # EXAMIN THE CASE OF THE MAN ON GOAL
                transitions += f'\t\t\t--Current + next cell .\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = l & game_board[{i}][{j - 1}] = Goal: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = r & game_board[{i}][{j + 1}] = Goal: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = u & game_board[{i - 1}][{j}] = Goal: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = d & game_board[{i + 1}][{j}] = Goal: Goal;\n\n'

                transitions += '\t\t\t-- other tiles cases\n'
                transitions += f'\t\t\tgame_board[{i}][{j + 1}] = PonGoal & movement = l & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j - 1}] = PonGoal & movement = r & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i + 1}][{j}] = PonGoal & movement = u & game_board[{i}][{j}] = Goal: PonGoal;\n'
                transitions += f'\t\t\tgame_board[{i - 1}][{j}] = PonGoal & movement = d & game_board[{i}][{j}] = Goal: PonGoal;\n\n'

                # -----------------------------------------------------------------------------------------------
                transitions += f'\t\t\t--Current + next cell -\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = l & game_board[{i}][{j - 1}] = Floor: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = r & game_board[{i}][{j + 1}] = Floor: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = u & game_board[{i - 1}][{j}] = Floor: Goal;\n'
                transitions += f'\t\t\tgame_board[{i}][{j}] = PonGoal & movement = d & game_board[{i + 1}][{j}] = Floor: Goal;\n\n'

                transitions += '\t\t\t-- other tiles cases\n'
                transitions += f'\t\t\tgame_board[{i}][{j + 1}] = PonGoal & movement = l & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i}][{j - 1}] = PonGoal & movement = r & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i + 1}][{j}] = PonGoal & movement = u & game_board[{i}][{j}] = Floor: Player;\n'
                transitions += f'\t\t\tgame_board[{i - 1}][{j}] = PonGoal & movement = d & game_board[{i}][{j}] = Floor: Player;\n\n'

                # -----------------------------------------------------------------------------------------------
                transitions += f'\t\t\t--Current + V next cell $ next next cell - V .\n'
                if j - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = PonGoal '
                        f'& movement = l & (game_board[{i}][{j - 1}] = Box | game_board[{i}][{j - 1}] = BonGoal) & '
                        f'(game_board[{i}][{j - 2}] = Floor | game_board[{i}][{j - 2}] = Goal): Goal;\n')
                if j + 2 < num_cols:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = PonGoal '
                        f'& movement = r & (game_board[{i}][{j + 1}] = Box | game_board[{i}][{j + 1}] = BonGoal) & '
                        f'(game_board[{i}][{j + 2}] = Floor | game_board[{i}][{j + 2}] = Goal): Goal;\n')
                if i - 2 >= 0:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = PonGoal '
                        f'& movement = u & (game_board[{i - 1}][{j}] = Box | game_board[{i - 1}][{j}] = BonGoal) & '
                        f'(game_board[{i - 2}][{j}] = Floor | game_board[{i - 2}][{j}] = Goal): Goal;\n')
                if i + 2 < num_rows:
                    transitions += (
                        f'\t\t\tgame_board[{i}][{j}] = PonGoal '
                        f'& movement = d & (game_board[{i + 1}][{j}] = Box | game_board[{i + 1}][{j}] = BonGoal) & '
                        f'(game_board[{i + 2}][{j}] = Floor | game_board[{i + 2}][{j}] = Goal): Goal;\n\n')

                # -----------------------------------------------------------------------------------------------
                # DEFAULT CASE
                transitions += f'\n\t\t\t-- Default case\n'
                transitions += f'\t\t\tTRUE: game_board[{i}][{j}];\n'
                transitions += '\t\tesac;\n\n'
                transitions += '\n\t\t'
    return transitions


def generate_win_conditions(board):
    """
    Generate the winning conditions for the Sokoban game according to the positions of the targets
    :param board: the board as a 2D list
    :return: a string containing the winning conditions
    """
    # get the locations of the targets
    targets = [(y, x) for y in range(len(board))
               for x in range(len(board[0]))
               if board[y][x] == '.' or board[y][x] == '+' or board[y][x] == '*']

    # Generate the winning conditions
    win_conditions = f'LTLSPEC !(F('
    for target in targets:
        # if we are in the last target then we don't need to add the '&' operator
        if target == targets[-1]:
            win_conditions += f'(game_board[{target[0]}][{target[1]}] = BonGoal)'
        else:
            win_conditions += f'(game_board[{target[0]}][{target[1]}] = BonGoal) & '

    win_conditions += '));'
    return win_conditions


def generate_smv_model(board, win_conditions=None):
    """"
    Generate an SMV model and winning conditions for the Sokoban game
    :param board: the board as a 2D list
    :param win_conditions: a list of winning conditions
    """
    m = len(board[0])
    n = len(board)

    # Generate the SMV model template
    smv_model = f"""
MODULE main
VAR
    -- Define the board as a 2D array
    game_board : array 0..{n-1} of array 0..{m-1} of {{Wall,Player,Box,Goal,PonGoal,BonGoal, Floor}};
    -- Define the movement options 
    movement : {{ r, l, u, d}}; 
INIT
    -- Initial state
    {create_initial_state(board, n, m)}
ASSIGN
    -- Define the transitions
    {define_transitions(board)}
        
-- Define the winning conditions
{generate_win_conditions(board)}
"""
    return smv_model


# --------------------------------MAIN FUNCTION OF THIS SCRIPT------------------------------
def gen_board(path='board1.txt'):
    """
    Generate a board from a file
    :param path: the path of the file
    :return: saves a smv model to as a NuXmv runnable file
    """
    # Read board from file
    board = read_board_from_file(path)

    # Generate SMV model and win conditions
    smv_model = generate_smv_model(board)

    # save the SMV model to a file with a meaningful name
    model_file_name = 'sokoban_model.smv'
    # save the current path
    current_path = os.getcwd()
    #### CHANGE THE PATH TO THE PATH OF YOUR nuXmv BIN FOLDER ####
    model_file_path = r'C:\Users\avidan\Desktop\לימודים\סימסטר ז\אימות פורמלי\new xmv\nuXmv-2.0.0-win64\bin'
    ################################################################
    os.chdir(model_file_path)

    with open(model_file_name, 'w') as file:
        file.write(smv_model)

    # go back to the original path
    os.chdir(current_path)

    return model_file_name
# ---------------------------------------------------------------------------------------------
