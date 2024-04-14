from createBoard import *
from get_LURD_moves import *
import run_nuXmv
import time
from iterative_solving import *


def main(isIterative=False):
    ##### CHANGE HERE TO THE FULL BOARD PATH #####
    path = "board10.txt"
    ##############################################

    if not isIterative:
        # Create the board
        board_file_name = gen_board(path)

        #### CHANGE HERE TO THE ENGINE YOU WANT TO USE ####
        engine = "SAT"
        ###################################################

        # if the engine is SAT, we need to enter the k value
        if engine == "SAT":
            k = int(input("Enter k value for BMC: "))
        else:
            k = None

        # Measure the time it takes to run the model
        start_time = time.time()
        # Run nuXmv
        output_file_name = run_nuXmv.run_nuxmv(board_file_name, engine=engine, k=k)
        # Stop the timer
        stop_time = time.time()

        # Print the time it took to run the model
        #print(f"Time to run {path} on {engine} engine is: {stop_time - start_time:.3f} seconds")

        # Extract the LURD moves from the output file
        moves = extract_LURD_moves(output_file_name)
        # if there is no solution
        if len(moves) == 0 and engine == "SAT":
            print("No solution available to this board at this k value")
        elif len(moves) == 0 and engine == "BDD":
            print("No solution available to this board")
        else:
            # print the moves to win
            print("Path to win:")
            str_lurd = ""
            for move in moves:
                str_lurd += move.upper() + " "
            print(str_lurd)

    else:
        # Solve the Sokoban game iteratively
        run_times = solve_iteratively(path)
        for run_time, iteration in run_times:
            print(f"Time to run iteration {iteration} is: {run_time:.3f} seconds")


if __name__ == "__main__":
    #### CHANGE HERE TO True TO RUN THE ITERATIVE SOLVING OR False IF REGULAR SOLVING IS REQUESTED ####
    main(False)
    #####################################################################################################
