from ggrade import read_tab_file
import argparse

################################################################################
################################################################################
def main():

    # Parse the input arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('infile_name', type=str, default=None, help='Input file name',nargs='?')
    parser.add_argument('--solutions-file', dest='outfile_name', type=str,\
            default='solutions.py', help='Name of output file to write the solutions to.')

    args = parser.parse_args()

    # Open the file and pull out the information.
    questions,solutions,student_answers = None,None,None
    if args.infile_name is not None:
        questions,solutions,student_answers = read_tab_file(args.infile_name)

    outfile_name = 'solutions.py'
    outfile = open(outfile_name,'w+')

    output = "solutions = [ \n"

    # For now, assume the solutions are the first one.
    for solution in solutions:
        output += "\t\"%s\"\n" % (solution)

    output += "] \n"

    print output

################################################################################
################################################################################
if __name__=="__main__":
    main()
