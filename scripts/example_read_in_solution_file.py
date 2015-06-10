import sys

solutions_filename = sys.argv[1].strip('.py')

solutions_file = __import__(solutions_filename)

solutions = getattr(solutions_file,'solutions')
feedback_for_everyone = getattr(solutions_file,'feedback_for_everyone')
feedback_for_wrong_answers = getattr(solutions_file,'feedback_for_wrong_answers')

print solutions
print feedback_for_everyone
print feedback_for_wrong_answers
