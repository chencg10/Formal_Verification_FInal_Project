from createBoard import *
from run_nuXmv import *
# regular expression library
import re
import time


def get_goals_positions(board="board1.txt"):
    """
    Get all the goal's positions from the board
    :param board:  to get the goals from
    :return: the goal positions and the board
    """
    # first gen some board
    board_to_gen = board
    board = read_board_from_file(board_to_gen)
    # get the goals positions
    goals = [(y, x) for y in range(len(board))
             for x in range(len(board[0]))
             if board[y][x] == "." or board[y][x] == "+" or board[y][x] == "*"
             ]

    return goals, board


def gen_board_with_one_goal(goal_pos, board):
    """
    Generate an SMV model and winning conditions for the Sokoban game
    :param goal_pos: the position of the goal on the board.
    :param board: the board to generate the model for.
    """
    m = len(board[0])
    n = len(board)

    # Generate the SMV model template
    smv_model = f"""
    MODULE main
    VAR
        -- Define the board as a 2D array
        game_board : array 0..{n - 1} of array 0..{m - 1} of {{Wall,Player,Box,Goal,PonGoal,BonGoal, Floor}};
        -- Define the movement options 
        movement : {{ r, l, u, d}}; 
    INIT
        -- Initial state
        {create_initial_state(board, n, m)}
    ASSIGN
        -- Define the transitions
        {define_transitions(board)}

    -- Define the winning conditions
    {iterative_gen_win_conditions(goal_pos)}
    """
    return smv_model


def iterative_gen_win_conditions(goals):
    """
    Generate the winning conditions for the Sokoban game
    :param goals: the goal position on the board.
    """
    win_conditions = f'LTLSPEC !(F('
    for goal in goals:
        # if we are in the last goal, we don't need to add the '&' operator
        if goal == goals[-1]:
            win_conditions += f'(game_board[{goal[0]}][{goal[1]}] = BonGoal)'
        else:
            win_conditions += f'(game_board[{goal[0]}][{goal[1]}] = BonGoal) & '

    win_conditions += '));'
    return win_conditions


def read_output_file(file):
    """
    Read the lines from the .out file
    :param file: the file to read the final state from
    :return: all the lines in the file as a string
    """
    with open(file, "r") as f:
        final_state = f.read()

    return final_state


def extract_lines_between_states(output):
    """
    Extract the lines between the states from the output of nuXmv
    This is a generator function
    :param output: the output of nuXmv
    :return: the lines between the states
    """
    # a list to hold the lines between the states
    lines_between_states = []
    # a flag to indicate if we are between states
    start = False

    # iterate over the lines in the output
    for line in output.split('\n'):
        # if we find the 'State' line, we are between states
        if 'State' in line:
            # if we are already between states, yield the lines between the states and reset the list
            # if not, set the flag to True because we are now between states
            if not start:
                lines_between_states = []
                start = True
            else:
                yield lines_between_states
                lines_between_states = []
        # if we are not between states, continue to the next line
        # if we are between states, add the line to the list
        elif start:
            lines_between_states.append(line)

    # if we are between states at the end of the file, yield the lines between the states
    if start:
        yield lines_between_states


def update_board(board, positions_to_update):
    """
    Update the board with the new positions and translate the new values to XSB format
    :param board: the board to update
    :param positions_to_update: the positions to update
    :return: the updated board
    """
    # given the positions to update, update the board
    for pos in positions_to_update:
        y, x = int(pos[0]), int(pos[1])
        # interpret the new value to XSB format
        if pos[2] == "Wall":
            board[y][x] = "#"
        elif pos[2] == "Player":
            board[y][x] = "@"
        elif pos[2] == "Box":
            board[y][x] = "$"
        elif pos[2] == "Goal":
            board[y][x] = "."
        elif pos[2] == "PonGoal":
            board[y][x] = "+"
        elif pos[2] == "BonGoal":
            board[y][x] = "*"
        elif pos[2] == "Floor":
            board[y][x] = "-"


def extract_pos_to_change(lines_between_states):
    """
    Extract the positions to change from the output of nuXmv
    :param lines_between_states: the lines between the states
    :return: the positions to change
    """
    # a list to hold the positions to change
    pos_to_change = []
    # iterate over the lines between the states
    for line in lines_between_states:
        # if we find the 'game_board' line, we need to extract the positions to change
        if "game_board" in line:
            # if we find the 'Wall' line, we don't need to change anything
            if "Wall" in line:
                continue
            # if we find the 'game_board' line, we need to extract the positions to change
            else:
                # extract the positions to change and the new value after the '=' sign using regular expressions
                pos_to_change.append(re.findall(r'\[([0-9]+)\]\[([0-9]+)\] = (\w+)', line))
    # return the positions to change
    return pos_to_change


def build_new_init_state(board, output_file):
    """
    Build the new init state of the board using the output of nuXmv
    :param board: the board to update
    :param output_file: the output file of nuXmv run
    :return: the updated board
    """

    #save the current directory
    cwd = os.getcwd()
    #### CHANGE HERE TO THE LOCATION OF YOUR nuXmv BIN FOLDER ####
    os.chdir(r'C:\Users\avidan\Desktop\לימודים\סימסטר ז\אימות פורמלי\new xmv\nuXmv-2.0.0-win64\bin')
    ###############################################################

    # read the output file
    # output_file = "/Users/ccg/Documents/BIU/Year 4/אימות פורמלי/83691_FP/83691-final-project/Part3/sokoban_model_board4_SAT.out"
    output = read_output_file(output_file)

    # Change directory back to the original directory
    os.chdir(cwd)

    # remove all lines until the first 'State' line and if there is no 'State' line, end the function
    if 'State' not in output:
        return -1
    else:
        output = output[output.index('State'):]

    # extract the lines between the states
    for lines in extract_lines_between_states(output):
        # get the lines
        lines_between_states = lines
        # extract the positions to change
        pos_to_change = extract_pos_to_change(lines_between_states)
        # convert the list to a list of tuples
        pos_to_change = [pos[0] for pos in pos_to_change]
        # update the board
        update_board(board, pos_to_change)

    return board


def solve_iteratively(board_to_read):
    """
    Solve the Sokoban game iteratively,
    updating the goal after each iteration,
    and running nuXmv.
    Also, measure the time it takes to run each iteration.
    :param board_to_read: the board to solve
    :return:
    """
    # get the goals and the board from the file
    name_of_board = board_to_read.split(".")[0]
    goals, board = get_goals_positions(board_to_read)

    # a list to hold the run times and the iteration number
    run_times = []

    goals_of_iteration = []
    for gi, goal in enumerate(goals):
        # pop first goal:
        goals_of_iteration.append(goal)
        # generate the SMV model using the current goals and the current board state
        smv_model = gen_board_with_one_goal(goals_of_iteration, board)

        # get the current path
        current_path = os.getcwd()
        #### CHANGE HERE TO THE LOCATION OF YOUR nuXmv BIN FOLDER ####
        os.chdir(r'C:\Users\avidan\Desktop\לימודים\סימסטר ז\אימות פורמלי\new xmv\nuXmv-2.0.0-win64\bin')
        ###############################################################
        with open(f"{name_of_board}_{goals_of_iteration}.smv", "w") as f:
            f.write(smv_model)
        # change the path back to the original path
        os.chdir(current_path)

        # run nuXmv
        # ask for the k value
        k = int(input("Enter k value for BMC: "))
        start_time = time.time()
        output_file = run_nuxmv(f"{name_of_board}_{goals_of_iteration}.smv", engine="SAT", k=k)
        stop_time = time.time()

        # save the run time and the iteration number
        run_times.append(((stop_time - start_time), (gi + 1)))

        # build the new init state
        board = build_new_init_state(board, output_file)

        if board == -1:
            print("No solution available to this board")
            return []

    # print the total run time and the total number of iterations to solve the board:
    print(f"Total run time: {sum([t for t, _ in run_times]):.3f} seconds")
    print(f"Total number of iterations: {len(run_times)}")

    return run_times
