JHofmann Short Answers

1.1  

A) There are no problems with it, as i and n are of the same type.

B) The code will not compile, as the first index matrix[4] is one beyond the maximum value of the rows, since it has initialized to have four total rows (and C++ is a 0-based indexing language).

C) There are no problems with it, since dt and array are both double types.

D) The snippet performs and unsafe operations with non-deterministic behaviors, since n has already been declared as an int, the action double n=5 won't have the intended behaviors.

E) Because 2^8 is 256, the unsigned int range for 8-bit representations is 0 to 255. The  code will throw an error or print a nonsense value for p+1, since it can't actually increment 255.

F) The smaller numbers get, the more likely machine precision errors will be encountered. Multiplying small numbers will produce even smaller numbers, making precision errors likelier. When you care about the value you output, then this precision is important to be aware of. Somehow converting the probabilities to larger magnitude values where precision is less of an issue would be a good idea.

1.2

A) On the stack, memory is fixed (specified by the OS) and managed by the compiler. On the heap, memory is managed by the programmer and is arbitrary in size.

B) In line 10, triplet is initialized to return an array of pointers, not int, as declared in line 4 of make_triplet . In this case, it is returning the pointer at index [1] for both cases, which happens to be the same, rather than the desired values of 2 and 3.

C) This corrected the output because triplet is now a freshly allocated array of pointers to ints (line 4), so when called it returns the value associated with those pointers.

D) It does introduce a memory leak, since "new" was used to make memory space but it was never deleted using a "delete" expression.

E) Instead of using "new", you could use another container type like a vector, whose memory management is already taken care of as part of the library.

