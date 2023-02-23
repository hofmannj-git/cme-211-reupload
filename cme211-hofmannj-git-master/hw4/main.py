import sys
import truss

if len(sys.argv) < 3:
    print('Usage:')
    print('  python3 main.py [joints file] [beams file] [optional plot output '\
          'file]')
    sys.exit(0)

file_joint = sys.argv[1]
file_beams = sys.argv[2]

a = truss.Truss(file_joint, file_beams)

if len(sys.argv) > 3: # calls PlotGeometry if third input specified
    file_plot = sys.argv[3]
    a.PlotGeometry(file_plot)

print(a)
