#include <fstream>
#include <iostream>
#include <string>

// adapted some lines from the following for indexing:
// https://www.geeksforgeeks.org/find-index-first-1-sorted-array-0s-1s/
int openingindex(int maze[201][201]){
    for (int i = 0; i < 201; i++) {
        if (maze[0][i] == 0) {
            return i;
        }
    }
    return -1;
}

int calc_num_rows(std::string mazefile){
    std::ifstream f;
    f.open(mazefile);
    int n = 0;
    if (f.is_open()) {
        int row, col;
        while (f >> row >> col){
            if (n == 0){
                return row;
                f.close();
                break;
            }
        }
    }
    return -1;
}

int main(int argc , char * argv []){
    
    // Confirm that appropriate command line arguments were provided and if not provide a usage message and exit.
    if (argc < 3) {
        std::cout << "Usage: \n ./mazesolver <maze file> <solution file>" \
        << std::endl ;
        return 0;
    }
    std::string mazefile = argv[1];
    std::string solnfile = argv[2];
    
    // initializing and confirming allocatable maze dataset, loading wall data
    int maze[201][201];
    int nrows = sizeof(maze) / sizeof(maze[0]);
    int ncols = sizeof(maze[0]) / sizeof(maze[0][0]);
    int n = 0;
    std::ifstream f;
    f.open(mazefile);
    if (f.is_open()) {
        int row, col;
        while (f >> row >> col){
            if (n == 0){
                if (row <= nrows and col <= ncols) {
                    // initializing the maze array to all zeros
                    for (int i = 0; i < 201; i++) {
                        for (int j = 0; j < 201; j++) {
                            maze[i][j] = 0;
                            }
                    }
                }
                else{   // confirming sufficient storage space in array
                    std::cout << "Not enough storage available" << std::endl;
                    return 0;
                }
            }
            // changing the values in the array to signify a wall
            else {
                maze[row][col] = 1;
            }
            n++; // add to counter
        }
    }
    f.close();
    
    // implementing right hand wall following algorithm
    int index_start = openingindex(maze);
    int current_row = 0; // initializing current position
    int current_col = index_start;
    int num_rows = calc_num_rows(mazefile);
    enum direction{
        left,
        right,
        up,
        down
    };
    std::ofstream g;
    g.open(solnfile);
    direction d = down;
    // looping until you are in the final row
    while (current_row < (num_rows - 1)){
        // calling function to write to file
        g << current_row << " " << current_col << std::endl;

        // testing if current & left/right directions are free
        int free_yn = 1;
        int free_right = 1;
        int free_left = 1;
        switch(d){
            case left:
                free_yn = maze[current_row][current_col-1];
                free_right = maze[current_row-1][current_col];
                free_left = maze[current_row+1][current_col]; break;
            case right:
                free_yn = maze[current_row][current_col+1];
                free_right = maze[current_row+1][current_col];
                free_left = maze[current_row-1][current_col]; break;
            case down:
                free_yn = maze[current_row+1][current_col];
                free_right = maze[current_row][current_col-1];
                free_left = maze[current_row][current_col+1]; break;
            case up:
                free_yn = maze[current_row-1][current_col];
                free_right = maze[current_row][current_col+1];
                free_left = maze[current_row][current_col-1]; break;
        }
        // if possible turn right (relative to current direction)
        if (free_right == 0){
            switch(d){
                case left:
                    d = up; break;
                case right:
                    d = down; break;
                case down:
                    d = left; break;
                case up:
                    d = right; break;
            }
        }
        // then, if possible go straight
        else if (free_yn == 0){
        }
        // then, if possible go left (relative to current direction)
        else if (free_left == 0){
            switch(d){
                case left:
                    d = down; break;
                case right:
                    d = up; break;
                case down:
                    d = right; break;
                case up:
                    d = left; break;
            }
        }
        // then, if at dead end, turn around
        else{
            switch(d){
                case left:
                    d = right; break;
                case right:
                    d = left; break;
                case down:
                    d = up; break;
                case up:
                    d = down; break;
            }
        }
        // update location to go in the final direction
        switch(d){
            case left:
                current_col--; break;
            case right:
                current_col++; break;
            case down:
                current_row++; break;
            case up:
                current_row--; break;
        }
    }
    // printing the final row location
    g << current_row << " " << current_col << std::endl;
    return 0;
}
