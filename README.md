# Formal_Verification_FInal_Project
This is a github repository of our Formal Verifiction course. the folder includes all of the codes we wrote


Codes of part 1:
    names: 
          a. createBoard.py
          b. get_LURD_moves.py
          c. run_nuXmv.py
          d. main.py

    For this part to run appropriately, there are several changes that need to be made.
    1. in "createBoard.py" in the function "gen_board()" in line no. 419:
        Please change the path saved in the variable "model_file_path" to your nuXmv bin repo path, the smv model wont be saved in a runnable path otherwise (use an r string).
    2. The same goes in "get_LURD_moves.py", in line no. 13, in the  os.chdir() command, please change the path to your nuXmv bin repo path so that the code will be able to read the .out file to           extract the LRUD moves (use an r string).
    3. The same change need to be made in "run_nuXmv.py", in line 10 pleas put in the os.chdir() command your bin repo path (use an r string).
    4. In the main.py code, in order to use the code in part 2 mode, you need to do the following changes:
