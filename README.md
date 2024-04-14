# Formal_Verification_FInal_Project
This is a github repository of our Formal Verifiction course. the folder includes all of the codes we wrote


Codes of part 2:
    names:
          1. createBoard.py
          2. get_LURD_moves.py
          3. run_nuXmv.py
          4. main.py

For this part to run appropriately, there are several changes that need to be made.
1. in "createBoard.py" in the function "gen_board()" in line no. 419:
    Please change the path saved in the variable "model_file_path" to your nuXmv bin repo path, the smv model wont be saved in a runnable path otherwise (use an r string).
        
2. The same goes in "get_LURD_moves.py", in line no. 13, in the  os.chdir() command, please change the path to your nuXmv bin repo path so that the code will be able to read the .out file to
    extract the LRUD moves (use an r string).
    
3. The same change need to be made in "run_nuXmv.py", in line 10 pleas put in the os.chdir() command your bin repo path (use an r string).
    
4. In the main.py code, in order to use the code in part 2 mode, you need to do the following changes:
   line 10 - change the path varibale to the FULL XSB BOARD PATH.
            The board should be save in XSB format and as a .txt file in order for the code to work.
   line 18 - Should remain with the value **"SAT"** if a bmc type run is requested (a value for k will be requested if you choose to run with "SAT" engine).
             If a run without a bounded number of steps is requested then change the value to **None**.
   line 61 - the input to the main() function should be **False**


Codes of part 3:
        names: 
          1. createBoard.py
          2. get_LURD_moves.py
          3. run_nuXmv.py
          4. main.py

For this part to run appropriately, there are several changes that need to be made.
1. in "createBoard.py" in the function "gen_board()" in line no. 419:
   Please change the path saved in the variable "model_file_path" to your nuXmv bin repo path, the smv model wont be saved in a runnable path otherwise (use an r string).
                
2. The same goes in "get_LURD_moves.py", in line no. 13, in the  os.chdir() command, please change the path to your nuXmv bin repo path so that the code will be able to
   read the .out file to extract the LRUD moves (use an r string).
                
3. The same change need to be made in "run_nuXmv.py", in line 10 pleas put in the os.chdir() command your bin repo path (use an r string).
            
4. In the main.py code, in order to use the code in part 3 mode, you need to do the following changes:
   line 10 - change the path varibale to the FULL XSB BOARD PATH.
            The board should be save in XSB format and as a .txt file in order for the code to work.
   line 18 - Should be changed to **BDD** if running with BDD engine is requested or **SAT** if running with SAT engine is requested (a value for k will be requested if you choose to run with "SAT" engine).
             Using the value **None** in this line would result in running the model in the SAT engine without a bounded number of steps (k will equal None as well)
   line 61 - the input to the main() function should be **False**


Codes of part 4:
        names: 
          1. createBoard.py
          2. get_LURD_moves.py
          3. run_nuXmv.py
          4. main.py
          5. iterative_solving.py

For this part to run appropriately, there are several changes that need to be made.
1. in "createBoard.py" in the function "gen_board()" in line no. 419:
   Please change the path saved in the variable "model_file_path" to your nuXmv bin repo path, the smv model wont be saved in a runnable path otherwise (use an r string).
                
2. The same goes in "get_LURD_moves.py", in line no. 13, in the  os.chdir() command, please change the path to your nuXmv bin repo path so that the code will be able to
   read the .out file to extract the LRUD moves (use an r string).
                
3. The same change need to be made in "run_nuXmv.py", in line 10 pleas put in the os.chdir() command your bin repo path (use an r string).
            
4. In the main.py code, in order to use the code in part 4 mode (iterative mode), you need to do the following changes:
   line 10 - change the path varibale to the FULL XSB BOARD PATH.
            The board should be save in XSB format and as a .txt file in order for the code to work.
   line 18 - Should remain with the value **"SAT"** if a bmc type run is requested (a value for k will be requested if you choose to run with "SAT" engine).
             If a run without a bounded number of steps is requested then change the value to **None**.
   line 61 - the input to the main() function should be **True**
                
   5. In "iterative_solving.py" in lines 180 and 236, Please change the os.chdir() command input to your nuXmv bin repo path (use an r string).


Note - for all parts, all of the places that need to be changed are also marked in the code with comment blocks of the form:
####### some note #######
line needed to be changed
#########################



**ALL CODES SHOULD BE RUNED ONLY FROM THE main.py FILE (IN ALL PARTS)**



    
