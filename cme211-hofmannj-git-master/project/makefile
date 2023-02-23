CXX := g++
CXXFLAGS := -std=c++11 -O3 -Wall -Wextra -Wconversion -Wpedantic

TARGET := main
OBJS := main.o CGSolver.o COO2CSR.o heat.o matvecops.o sparse.o

main: main.cpp CGSolver.cpp CGSolver.hpp COO2CSR.cpp COO2CSR.hpp heat.cpp heat.hpp matvecops.cpp matvecops.hpp sparse.cpp sparse.hpp
	$(CXX) $(CXXFLAGS) -o main main.cpp CGSolver.cpp COO2CSR.cpp heat.cpp matvecops.cpp sparse.cpp

.PHONY: clean
clean:
	$(RM) $(OBJS) $(TARGET)
