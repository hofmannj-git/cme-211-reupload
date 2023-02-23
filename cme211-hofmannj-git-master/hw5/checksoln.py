import numpy as np
import sys

def loaddata(mazefile, solnfile):
    """ This function takes in the inputs 'mazefile' and 'solnfile' and reads \
        & loads the data from those files."""
    maze = np.loadtxt(mazefile, dtype=np.int)
    soln = np.loadtxt(solnfile, dtype=np.int)
    return maze, soln


# BODY OF CODE

if __name__ == "__main__":
    
    # Determine if appropriate command line arguments were provided and if
    # not provide a usage message and exit.
    if len(sys.argv) < 3:
        print("Usage:")
        print("  $ python3 checksoln.py <maze_file> <soln_file>")
        sys.exit(0)
    
    # declares variables from inputs
    maze_file = sys.argv[1]
    soln_file = sys.argv[2]

    # Store the maze and the solution in appropriate NumPy arrays
    maze, soln = loaddata(maze_file, soln_file)
    num_rows = maze[0][0]
    num_cols = maze[0][1]
    trigger = 0 # initializing trigger

    # checking if initial position in solution is the entrance or a wall
    if any((maze[1:]==soln[0]).all(1)):
        trigger = 1
    for i in range(1,soln.shape[0]): # looping over all solution steps
        # check that you only move one position change at a time
        diff = soln[i] - soln[i-1]
        if not any((np.absolute(diff) <= 1)):
            trigger = 1
        # check that position is not a wall
        if any((maze[1:]==soln[0]).all(1)):
            trigger = 1
        # check that solution remains in bounds of the maze
        if not any(soln[i] < np.array([num_rows, num_cols])):
            trigger = 1
    # check that the final solution point is on the last line, and not a wall
    if any((maze[1:]==soln[-1]).all(1)) or (not soln[-1][0]+1 == num_rows):
        trigger = 1

    # print if valid or not
    if trigger == 0:
        print("Solution is valid!")
    else:
        print("Solution is not valid.")
