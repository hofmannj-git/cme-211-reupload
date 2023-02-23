#include <fstream>
#include <iostream>
#include <string>


// Confirm that appropriate command line arguments were provided and if not provide a usage message and exit.

//  to read the maze you should confirm there is sufficient storage space in the array, initialize all of the values in the array to a constant value, and then for each line with a row and column pair you should change the value at that location in the array to indicate the presence of a wall.

// Verify that appropriate static array storage is available for storing the maze. You can setup your static array for the largest maze file provided, but should still have your program confirm at runtime that the array is large enough. We emphasize that you should store the maze in a static array. -- Please ensure you understand what it means to declare a static array (i.e. length is known at compile time); if you read in the dimensions of the maze and then use these input values to determine how much storage to allocate in an array, you are not using static arrays!

// Find the maze entrance at the opening in the first row and store this as your first position in the solution file

// Use the right hand wall following algorithm to move through the maze without going through any walls, storing each position in the solution file. We expect that a valid path should not involve duplicated adjacent entries, i.e. if we treat each valid position in a path as a unit time-step, we shouldn’t force the user of our directions to “wait” or “remain” at a position without moving.

// Exit on the last row and store this as your last position in the solution file.
