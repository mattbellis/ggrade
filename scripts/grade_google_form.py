from ggrade import read_tab_file,grade_problem,email_grade_summaries
import numpy as np
import getpass
import sys

################################################################################
# Read in the file with the student responses. 
# (Response Form from Google Forms)
################################################################################
infilename = sys.argv[1]

questions,solutions,student_responses=read_tab_file(infilename)

# We will need put in the password here. 
my_email_address = None
password = None

my_email_address = getpass.getpass("Enter address from which to send email: ")
password = getpass.getpass()

points_per_question=10

nstudents = len(student_responses)
nquestions = len(questions)

print "# of students:  %d" % (nstudents)
print "# of questions: %d" % (nquestions)

# Creates a matrix of number of students and number of questions to see 
# who got questions wrong/right. We initialize it to everyone getting it
# correct.
assignment_summary = np.ones((nstudents,nquestions)) 

# Loop over each student.
for i,student in enumerate(student_responses):
    total=0 # Total points the student received.
    total_possible=0 # Total possible points achievable.

    # Grab the student email and the timestamp of when they submitted their
    # work.
    student_email=student[0]
    time = student[1]

    print "Grading scores for %s" % (student_email)

    # Create an empty string for the email body we will send to the student.
    output = ""

    for question_number,(response,solution,question) in enumerate(zip(student[2],solutions,questions)):
        # Grade an individual problem
        sub_output,points_received,points_possible=grade_problem(question,response,solution,points_per_question) 
        # Keep track of how many points the student got for each problem.
        # If the student didn't get all the possible points, change the 1 in the matrix to a 0.
        if points_possible != points_received: 
            assignment_summary[i][question_number]=0

        # Attach the feedback from that question to the total feedback we'll be 
        # emailing the stduent.
        output += sub_output

        # Ccalculate total number of points and points possibl.e
        total += points_received 
        total_possible += points_possible 

    # Now we've looped over all the problems for that student.
    # Append a string which summarizes their performance. 
    output += "<center> <br> <br> <b> Grade: %6.3f out of %d ----- %4.2f </b> </center>" % (total,total_possible,100*(total/float(total_possible)))


    ############################################################################
    # Email the student the feedback.
    ############################################################################
    if password is not None:
         email_grade_summaries(student_email,my_email_address,'Samples test grade',output,password,isHTML=True)



################################################################################
# Summarize the student responses and how the class performed on each
# question.
################################################################################
for q in assignment_summary.transpose():
    ntot = len(q)
    ncorrect = q.sum()
    print "Out of %d people %d got this question right---- %4.2f%%" % (ntot,ncorrect,100*ncorrect/ntot) #prints how many people got each question right







