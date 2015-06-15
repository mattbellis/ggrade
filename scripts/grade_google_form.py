from ggrade import read_tab_file,grade_problem,email_grade_summaries
import numpy as np
import getpass
import sys
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

################################################################################
# Read in the file with the student responses. 
# (Response Form from Google Forms)
################################################################################
infilename = sys.argv[1]

questions,solutions,student_responses=read_tab_file(infilename)


################################################################################
# Read in the solutions from a different file.
#solutions_filename = sys.argv[1].strip('.py')
solutions_filename = 'solutions'

solutions_file = __import__(solutions_filename)

solutions = getattr(solutions_file,'solutions')
feedback_for_everyone = getattr(solutions_file,'feedback_for_everyone')
feedback_for_wrong_answers = getattr(solutions_file,'feedback_for_wrong_answers')

print solutions
print feedback_for_everyone
print feedback_for_wrong_answers

################################################################################

# We will need put in the password here. 
my_email_address = None
password = None

#my_email_address = getpass.getpass("Enter address from which to send email: ")
#password = getpass.getpass()

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
    # work.
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
        # emailing the stduent.
        output += sub_output

        # Ccalculate total number of points and points possibl.e
        total += points_received 
        total_possible += points_possible 
    student_scores.append((total/float(total_possible))*100) 
    student_info[student_email]= ((total/float(total_possible))*100)

    # Now we've looped over all the problems for that student.
    # Append a string which summarizes their performance. 
    output += "<center> <br> <br> <b> Grade: %6.3f out of %d ----- %4.2f </b> </center>" % (total,total_possible,100*(total/float(total_possible)))


    ############################################################################
    # Email the student the feedback.
    ############################################################################
    if password is not None:
         email_grade_summaries(student_email,my_email_address,'Brownie and cookie physics test',output,password,isHTML=True)

student_scores=sorted(student_scores)

average=sum(student_scores)/float(len(student_scores))
student_info= sorted(student_info.items(),key=lambda x:x[1])
x = np.arange(1,nstudents+1,1)

print student_info


for i,student in enumerate(student_info):
    plt.figure()
    student_plot=plt.scatter(x,student_scores,color='b',marker='^',s=300,label='Individual student scores')
    average_plot=plt.plot([0,nstudents],[average,average],'r--',label='Average score')
    current_score = plt.scatter(i+1,student[1],color='g',marker='o',s=600,label='Your score')
    plt.yticks(np.arange(0,100,5))
    plt.xticks(np.arange(0,nstudents,1))
    plt.xlim(-1,nstudents+1)
    plt.legend(loc='lower left')
    plt.title('Summary of Class Scores')
    plt.xlabel('Student')
    plt.ylabel('Score')

################################################################################
# Summarize the student responses and how the class performed on each
# question.
################################################################################
colors=['lightskyblue','lightcoral']
labels=[r'Right',r'Wrong']
question_label=[]

x=0
for q,question in zip(assignment_summary.transpose(),questions):
    ntot = len(q)
    ncorrect = q.sum()
    print "Out of %d people %d got this question right---- %4.2f%%" % (ntot,ncorrect,100*ncorrect/ntot)
    question_num = 'Question #' + str(x+1)
    question_label.append(question_num)
    the_grid=GridSpec(7,1)
    sizes=[ncorrect,ntot-ncorrect]
    plt.subplot(the_grid[x,0],aspect=1)
    patches, texts = plt.pie(sizes,colors=colors,shadow=True)
    plt.axis('equal')
    plt.tight_layout()
    x+=1
    plt.title(question_num,fontweight='bold')
    plt.text(1.5,0.1,'%4.1f%% of students got this question right' % (100*ncorrect/ntot))

plt.legend(patches,labels,loc=('lower left'),shadow=True)
    

plt.show()







