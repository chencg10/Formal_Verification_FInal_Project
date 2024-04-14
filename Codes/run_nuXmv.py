import subprocess
import os


def run_nuxmv(model_filename, engine=None, k=None):
    # get current directory
    cwd = os.getcwd()

    #### CHANGE HERE TO THE LOCATION OF YOUR nuXmv BIN FOLDER ####
    os.chdir(r'C:\Users\avidan\Desktop\לימודים\סימסטר ז\אימות פורמלי\new xmv\nuXmv-2.0.0-win64\bin')
    ###############################################################

    if engine == "SAT":
        # Run the command
        args = [".\\nuXmv.exe", "-int", model_filename]
        nuxmv_process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        # next command to run
        nuxmv_process.stdin.write("go_bmc\n")
        nuxmv_process.stdin.write(f"check_ltlspec_bmc -k {k}\n")
        # enter ctrl+c to exit
        nuxmv_process.stdin.write("quit\n")

    elif engine == "BDD":
        args = [".\\nuXmv.exe", "-int", model_filename]
        nuxmv_process = subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE, universal_newlines=True)
        # next command to run
        nuxmv_process.stdin.write("go\n")
        nuxmv_process.stdin.write(f"check_ltlspec\n")
        # enter ctrl+c to exit
        nuxmv_process.stdin.write("quit\n")

    else:
        # Run the command
        nuxmv_process = subprocess.Popen([".\\nuXmv.exe", model_filename], stdin=subprocess.PIPE,
                                         stdout=subprocess.PIPE, universal_newlines=True)

    # create output file name
    output_filename = model_filename.split(".")[0] + ".out"

    stdout, _ = nuxmv_process.communicate()

    # Save output to file
    with open(output_filename, "w") as f:
        f.write(stdout)
    print(f"Output saved to {output_filename}")

    # Change directory back to the original directory
    os.chdir(cwd)

    return output_filename
