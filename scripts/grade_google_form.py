from ggrade import read_tab_file,grade_problem,email_grade_summaries
import numpy as np
import getpass
import sys
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import csv

###############################################################################
# Read in the file with the student responses. 
# (Response Form from Google Forms)
###############################################################################
make_plots = False
send_emails = False

if len(sys.argv) >2:
    print "yes"
    if sys.argv[2]=="email":
         send_emails = True
    elif sys.argv[2] == "plots":
         make_plots=True
    else:
         print "Invalid entry for 4th entry"
    if len(sys.argv) > 3:
        if sys.argv[3]=="email":
            send_emails = True
        elif sys.argv[3] == "plots":
            make_plots=True
        else:
            print "Invalid entry for 5th entry"

infilename = sys.argv[1]
questions,solutions,student_responses=read_tab_file(infilename)


###############################################################################
# Read in the solutions from a different file.
# Should change solutions_filename with each quiz that has different solutions
# and feeback feedback.
###############################################################################
#solutions_filename = sys.argv[1].strip('.py')
solutions_filename = 'solutions' 

solutions_file = __import__(solutions_filename)

solutions = getattr(solutions_file,'solutions')
feedback_for_everyone = getattr(solutions_file,'feedback_for_everyone')
feedback_for_wrong_answers = getattr(solutions_file,'feedback_for_wrong_answers')

print solutions
print feedback_for_everyone
print feedback_for_wrong_answers

###############################################################################
# If "emails" and entered into the command line, it will prompt the user for 
# their Google username and password.
###############################################################################
my_email_address = None
password = None

if send_emails:
    my_email_address = getpass.getpass("Enter address from which to send email: ")
    password = getpass.getpass()

scores_file = csv.writer(open('student_scores.csv', "wb"),delimiter=',')
scores_file.writerow(['Time -------------------------Student Email------------Student Score'])

points_per_question=10

nstudents = len(student_responses)
nquestions = len(questions)
student_scores=[]
student_info={}

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
    # work- if username is automatically grabbed from Google Forms.
    student_email=student[0]
    #student_email="se30maha@siena.edu"
    time = student[1]

    print "Grading scores for %s" % (student_email)

    # Create an empty string for the email body we will send to the student.
    output = ""

    for question_number,(response,solution,question,fe,fw) in enumerate(zip(student[2],solutions,questions,feedback_for_everyone,feedback_for_wrong_answers)):
        # Grade an individual problem
        sub_output,points_received,points_possible=grade_problem(question,response,solution,points_per_question,fe,fw) 
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
    
    scores_file.writerow([time,'----------',student_email,'----------',this_student_score])

    ###########################################################################
    # Email the student the feedback.
    ###########################################################################
    if password is not None:
         email_grade_summaries(student_email,my_email_address,'Brownie and cookie physics test',output,password,isHTML=True)


###############################################################################
# Plots each student's score on one figure. It then loops through each students
# scores and plots the current student's score. So the number of figures equals 
# the number of students. Each student has a different graph depending on what 
# their score is. Also, sorts the scores.
###############################################################################

if make_plots:

    student_scores=sorted(student_scores)

    average=sum(student_scores)/float(len(student_scores))
    student_info= sorted(student_info.items(),key=lambda x:x[1])
    num_of_students = np.arange(0,nstudents,1)

    print student_info


    for i,student in enumerate(student_info):
        plt.figure()
        student_plot=plt.scatter(num_of_students,student_scores,color='b',marker='^',s=300,label='Individual student scores')
        average_plot=plt.plot([0,nstudents],[average,average],'r--',label='Average score')
        current_score = plt.scatter(i,student[1],color='g',marker='o',s=600,label='Your score')
        plt.yticks(np.arange(0,100,5))
        plt.xticks(np.arange(0,nstudents,1))
        plt.xlim(-1,nstudents+1)
        plt.legend(loc='lower left')
        plt.title('Summary of Class Scores')
        plt.xlabel('Student')
        plt.ylabel('Score')

###############################################################################
# Summarize the student responses and how the class performed on each
# question and plot the summary of each student.
###############################################################################
    colors=['lightskyblue','lightcoral']
    labels=[r'Right',r'Wrong']
    question_label=[]

    num_of_students=0
    for q,question in zip(assignment_summary.transpose(),questions):
        ntot = len(q)
        ncorrect = q.sum()
        print "Out of %d people %d got this question right---- %4.2f%%" % (ntot,ncorrect,100*ncorrect/ntot)
        question_num = 'Question #' + str(num_of_students+1)
        question_label.append(question_num)
        the_grid=GridSpec(7,1)
        sizes=[ncorrect,ntot-ncorrect]
        plt.subplot(the_grid[num_of_students,0],aspect=1)
        patches, texts = plt.pie(sizes,colors=colors,shadow=True)
        plt.axis('equal')
        plt.tight_layout()
        num_of_students+=1
        plt.title(question_num,fontweight='bold')
        plt.text(1.5,0.1,'%4.1f%% of students got this question right' % (100*ncorrect/ntot))
    plt.legend(patches,labels,loc=('lower left'),shadow=True)
    

    plt.show()







