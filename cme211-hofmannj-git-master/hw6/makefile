CXX := g++
CXXFLAGS := -std=c++11 -O0 -g -Wall -Wextra -Wconversion -Wpedantic

TARGET := main
OBJS := main.o image.o hw6.o

main: main.cpp image.cpp image.hpp hw6.cpp hw6.hpp
	$(CXX) $(CXXFLAGS) -o main main.cpp image.cpp hw6.cpp -ljpeg

.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)
