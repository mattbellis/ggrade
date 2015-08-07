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

    solutions_string = "solutions = [ \n"
    extra_feedback_string = "feedback_for_everyone = [ \n"
    incorrect_feedback_string = "feedback_for_wrong_answers = [ \n"
    points_per_question_string = "points_per_question = [ \n"

    nsolutions = len(solutions)

    # For now, assume the solutions are the first one.
    for i,solution in enumerate(solutions):
        solutions_string += "\t\"%s\"" % (solution)
        extra_feedback_string += "\tNone" 
        incorrect_feedback_string += "\tNone" 
        points_per_question_string += "10"
        if i != nsolutions-1:
            solutions_string += ", # Question %d\n" % (i+1)
            extra_feedback_string += ", # Question %d\n" % (i+1)
            incorrect_feedback_string += ", # Question %d\n" % (i+1)
            points_per_question_string += ", # Question %d\n" % (i+1)
        else:
            solutions_string += " # Question %d \n" % (i+1)
            extra_feedback_string += " # Question %d \n" % (i+1)
            incorrect_feedback_string += " # Question %d \n" % (i+1)
            points_per_question_string += " # Question %d \n" % (i+1)

    solutions_string += "] \n"
    extra_feedback_string += "] \n"
    incorrect_feedback_string += "] \n"
    points_per_question_string += "] \n"

    # Write the output to a file.
    
    outfile_name = args.outfile_name
    outfile = open(outfile_name,'w+')
    outfile.write("# -*- coding: utf-8 -*-")
    outfile.write("\n")
    outfile.write(solutions_string)
    outfile.write("\n")
    outfile.write(extra_feedback_string)
    outfile.write("\n")
    outfile.write(incorrect_feedback_string)
    outfile.write("\n")
    outfile.write(points_per_question_string)
    outfile.close()

################################################################################
################################################################################
if __name__=="__main__":
    main()
