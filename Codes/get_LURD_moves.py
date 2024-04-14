import os

def extract_LURD_moves(filename):
    """
    Extract the LURD moves from the output file of the nuXmv model
    :param filename: The output file of the nuXmv model
    :return: A list of the LURD moves
    """
    # get current directory
    cwd = os.getcwd()

    #### CHANGE HERE TO THE LOCATION OF YOUR nuXmv BIN FOLDER ####
    os.chdir(r'C:\Users\avidan\Desktop\לימודים\סימסטר ז\אימות פורמלי\new xmv\nuXmv-2.0.0-win64\bin')
    ###############################################################

    # a list to store the movements
    movements = []
    # a variable to store the last movement in case it doesn't change between State
    last_movement = None

    # Open the file and iterate over the lines
    with open(filename, 'r') as file:
        for line in file:
            # If we find a line with 'State' we add the last movement to the list
            if 'State' in line:
                if last_movement is not None:
                    movements.append(last_movement)
            # If we find a line with 'movement =' we extract the movement
            elif 'movement =' in line:
                last_movement = line.split('=')[-1].strip()
            elif 'Loop starts here' in line:
                break

    #change directory back to the original directory
    os.chdir(cwd)

    # Add the last movement if there is one
    if last_movement is not None:
        movements.append(last_movement)

    return movements[:-1]


# # Example usage:
# filename = '/Users/ccg/Documents/BIU/Year 4/אימות פורמלי/83691_FP/83691-final-project/Part3/sokoban_model_board4_SAT.out'
# movements = extract_LURD_moves(filename)
# print(movements)
