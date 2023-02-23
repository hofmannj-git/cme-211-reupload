The Stock class has private variables 'dr', 'price_vec', and 'tckr' (for the daily return, price
vector, and ticker name, respectively) and private method dailyReturn, since all of these
attributes are only utilized internally to the class and don't need to be accessed directly by
"main.cpp". The public attributes include the constructor 'Stock' and the methods
'meanReturn' and 'varReturn' which are called from "main.cpp" and therefore must be
public.

'dailyReturn' and 'meanReturn' both take in an int for the number of values they need to
loop over (so it only needs to be calculated once).

To minimize repetitive calls, I have 'varReturn' take in as an input the double output of 
'meanReturn' so it doesn't need to call it again at the local scope.

The keyword 'new' does not appear in my  program, since all of the arrays that I used are 
of the <vector> type, whose library does all of the allocating for me. This is a good way to
avoid the possibility of memory leaks, for example if I used 'new' and then forgot to 'delete'
it after use.

I could improve the program by making the output of 'dailyReturn' a class attribute instead 
of calling it each in 'varReturn' and 'numReturn' (possibly initializing it in the constructor). I 
tried to do this, but was getting some segmentation faults and didn't have time to debug 
properly, so went with the "wetter" version.

The command I used to compile my program (after debugging) was:
g++ -std=c++11 -O3 -Wall -Wextra -Wconversion -Wpedantic -o main main.cpp Stock.cpp Stock.hpp
