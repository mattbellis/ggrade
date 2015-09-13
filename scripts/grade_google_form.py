from ggrade import read_tab_file,grade_problem,email_grade_summaries,make_plots,email_grade_summaries_plots
import numpy as np
import getpass
import sys
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import csv
import argparse

###############################################################################
# If you type in "--plots" or "--email" in the command line, it will set the 
# corresponding boolean true. Later, it will execute the command if true.
# Also needs the solution file to execute.
###############################################################################

parser = argparse.ArgumentParser()
parser.add_argument('infilename',type=str,default=None,help='Input file name',nargs='?')
parser.add_argument('--emails',action='store_true',dest='send_emails',default=False,help='Call --email if you want emails to be sent')
parser.add_argument('--test',action='store_true',dest='test',default=False,help='Send emails to instructor email.')
parser.add_argument('--plots',action='store_true',dest='make_plots_bool',default=False,help='Call --plots if you want plots to be made')
parser.add_argument('--emailplots',action='store_true',dest='email_and_plots',default=False,help='Call --plots if you want plots to be made')
parser.add_argument('--solutions-file',dest='solutions_filename',type=str,default='solutions.py',help='Name of the file that has the solutions/feedback')
parser.add_argument('--score_file',dest='student_score_file',type=str,default='student_scores.csv',help='Name of the file that will organize the students email and score.')
parser.add_argument('--essay_file',dest='essay_file_name',type=str,default='essay.tex',help='If there is an essay that needs to be written to a file, type the name of the file you want created for the essays/long answers to be graded by hand.')
args=parser.parse_args()

send_emails=args.send_emails
make_plots_bool=args.make_plots_bool
email_and_plots=args.email_and_plots

###############################################################################
# Read in the file with the student responses. 
# (Response Form from Google Forms)
###############################################################################
questions,solutions,student_responses=read_tab_file(args.infilename)

###############################################################################
# Read in the solutions from a different file.
# Should change solutions_filename with each quiz that has different solutions
# and feedback.
###############################################################################

solutions_filename = args.solutions_filename.strip('.py') 
solutions_file = __import__(solutions_filename)

solutions = getattr(solutions_file,'solutions')
feedback_for_everyone = getattr(solutions_file,'feedback_for_everyone')
feedback_for_wrong_answers = getattr(solutions_file,'feedback_for_wrong_answers')
points_per_question_list = getattr(solutions_file, 'points_per_question')


# Opening file for essay answers as a LaTex file.
essay_file_name = args.essay_file_name
essay_file = open(essay_file_name,"w")
essay_file.write('\documentclass[12pt]{article} \n\usepackage{amsmath} \n\\begin{document}')


###############################################################################
# If "emails" and entered into the command line, it will prompt the user for 
# their Google username and password.
###############################################################################

my_email_address = None
password = None

if send_emails or email_and_plots:
    my_email_address = getpass.getpass("Enter address from which to send email: ")
    password = getpass.getpass()
    email_subject=raw_input("What do you want your email subject line to say? ")

scores_file = csv.writer(open(args.student_score_file, "wb"),delimiter=',')
scores_file.writerow(['Date/Time','Student Email','Student Name','Student Score'])


nstudents = len(student_responses)
nquestions = len(questions)
student_scores=[]
student_info={}
print "# of students:  %d" % (nstudents)
print "# of questions: %d" % (nquestions)

###############################################################################
# Creates a matrix of number of students and number of questions to see 
# who got questions wrong/right. We initialize it to everyone getting it
# correct.
###############################################################################
assignment_summary = np.ones((nstudents,nquestions)) 
essay_string = ""

for i,student in enumerate(student_responses):
    total=0 
    total_possible=0 
    student_email=student[0]
    time = student[1]
    student_name=student[2]
    output = ""
    output += "<center> <b> This test is intended for %s </b> </center>" % (student_name)
    
    

    for question_number,(response,solution,question,fe,fw,points_per_question) in enumerate(zip(student[3],solutions,questions,feedback_for_everyone,feedback_for_wrong_answers,points_per_question_list)):
        sub_output,points_received,points_possible,essay_output=grade_problem(question,response,solution,points_per_question,student_name,fe,fw) 
        if essay_output is not "":
                essay_string +=essay_output
        if points_possible != points_received: 
            assignment_summary[i][question_number]=0
        output += sub_output
        total += points_received 
        total_possible += points_possible 
    this_student_score = round((total/float(total_possible))*100,2)
    student_scores.append(this_student_score) 
    student_info[student_email]= (this_student_score)
    output += "<center> <br> <br> <b> Grade: %6.3f out of %d ----- %4.2f </b> </center>" % (total,total_possible,100*(total/float(total_possible)))

    # Emailing the plots- not in the right order.
    if email_and_plots:
        image_path ='./student%d.png' % (i+1) 

    	if password is not None:
         	email_grade_summaries_plots(student_email,my_email_address,email_subject,output,image_path,password,isHTML=True)

if make_plots_bool:
    make_plots(student_scores,nstudents,student_info,assignment_summary,questions)
print essay_string

# Loop over each student.
for i,student in enumerate(student_responses):
    total=0 # Total points the student received.
    total_possible=0 # Total possible points achievable.

    # Grab the student email and the timestamp of when they submitted their
    # work- if username is automatically grabbed from Google Forms.
    
    student_email=student[0]
    time = student[1]
    student_name = student[2]

    # Create an empty string for the email body we will send to the student.
    output = ""
    output += "<center> <b> This test is intended for %s </b> </center>" % (student_name)

    for question_number,(response,solution,question,fe,fw,points_per_question) in enumerate(zip(student[3],solutions,questions,feedback_for_everyone,feedback_for_wrong_answers,points_per_question_list)):
        # Grade an individual problem
        sub_output,points_received,points_possible,essay_output=grade_problem(question,response,solution,points_per_question,student_name,fe,fw) 

        # Keep track of how many points the student got for each problem.
        # If the student didn't get all the possible points, change the 1 in the matrix to a 0.
        if points_possible != points_received: 
            assignment_summary[i][question_number]=0

        # Attach the feedback from that question to the total feedback we'll be 
        # emailing the student.
        output += sub_output

        # Calculate total number of points and points possible.
        total += points_received 
        total_possible += points_possible 
    this_student_score = round((total/float(total_possible))*100,2)
    student_scores.append(this_student_score) 
    student_info[student_email]= (this_student_score)

    # Now we've looped over all the problems for that student.
    # Append a string which summarizes their performance. 
    output += "<center> <br> <br> <b> Grade: %6.3f out of %d ----- %4.2f </b> </center>" % (total,total_possible,100*(total/float(total_possible)))
    
    #Writes info to the file that keeps students scores.
    scores_file.writerow([time,student_email,student_name,this_student_score])

    
        
    ###########################################################################
    # Email the student the feedback.
    ###########################################################################
    if password is not None and send_emails:
        if args.test:
            student_email = my_email_address 
        email_grade_summaries(student_email,my_email_address,email_subject,output,password,isHTML=True)


##########################################################################
# Writing out approproate information for LaTex file
##########################################################################
essay_file.write("%s \end{document}" % (essay_string))
essay_file.close()










