# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os


################################################################################
# Test to see if a string actually represents a floating point number.
################################################################################
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

################################################################################
# Test to see if a string contains a number
################################################################################
def is_number_in_string(value):

    newstring = ""
    for letter in value:
        if letter.isdigit() or letter=='.':
            newstring += letter

    return newstring

################################################################################
def email_grade_summaries(email_address,msg_from,msg_subject,msg_body,password="xxx",isHTML=False):

    ################################################################################
    # Use my GMail account
    ################################################################################
    smtpserver = 'smtp.gmail.com'
    smtpuser = msg_from  # for SMTP AUTH, set SMTP username here
    smtppasswd = password  # for SMTP AUTH, set SMTP password here
    me = msg_from

    # Create a text/plain message
    msg = MIMEText(msg_body)
    if isHTML:
        msg = MIMEText(msg_body,'html')

    msg['Subject'] = '%s' % (msg_subject)
    msg['From'] = me
    msg['To'] = email_address

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    try:
        session = smtplib.SMTP('smtp.gmail.com',587)
        session.starttls()
        session.login(smtpuser,smtppasswd)
        session.sendmail(me, email_address, msg.as_string())
        print "Successfully sent email for %s" % (email_address)
        session.quit()
    except smtplib.SMTPException:
        print "Error: unable to send email for %s" % (email_address)

################################################################################
def email_grade_summaries_plots(email_address,msg_from,msg_subject,msg_body,image_file_name,password="xxx",isHTML=False):

    ################################################################################
    # Use my GMail account - the image file is not lined up correctly. The plot is 
    # sorted by the score of the student while the email address is sorted by the 
    # time each student took the test. This needs to be fixed before emailing plots.
    ################################################################################
    smtpserver = 'smtp.gmail.com'
    smtpuser = msg_from  # for SMTP AUTH, set SMTP username here
    smtppasswd = password  # for SMTP AUTH, set SMTP password here
    me = msg_from
    
    # Create a text/plain message
    msg = MIMEMultipart()
    msgAlternative = MIMEMultipart('alternative')
    msg.attach(msgAlternative)
    if isHTML:
        msgtext = MIMEText(msg_body,'html')
        msgAlternative.attach(msgtext)

    img_data = open(image_file_name,'rb')
    image = MIMEImage(img_data.read())
    image.add_header('Content-ID','<image1>')
    msg.attach(image)
    img_data.close()

    msg['Subject'] = '%s' % (msg_subject)
    msg['From'] = me
    msg['To'] = email_address

    # Send the message via our own SMTP server, but don't include the
    # envelope header.
    try:
        session = smtplib.SMTP('smtp.gmail.com',587)
        session.starttls()
        session.login(smtpuser,smtppasswd)
        session.sendmail(me, email_address, msg.as_string())
        print "Successfully sent email"
        session.quit()
    except smtplib.SMTPException:
        print "Error: unable to send email"


################################################################################
# Grade an individual problem.
################################################################################
def grade_problem(question,answer,solution,points_per_question,student_name,feedback_for_everyone=None,feedback_for_wrong_answers=None):
    sub_points = 0
    correct = -1
    points_per_question=points_per_question
    output = ""
    points_received = 0
    extra_partial_answer=""
    missing_partial_answer=""
    essay_output = ""
    
    
    if type(solution) is not list: #check for solution to not be a list 

        # If it is a multiple choice answer and there can be multiple solutions.
        if ',' in solution:
            multiple_solutions = solution.split(',')
            multiple_answers = answer.split(',')
            nsolutions = float(len(multiple_solutions))
            points_per_answer = points_per_question/nsolutions
            sub_points = 0


            # Check to see if they got all the answers.
            for msol in multiple_solutions:
                for mans in multiple_answers:
                    if msol.strip()==mans.strip():
                        sub_points += points_per_answer

	    # Takes points off if student checked a wrong answer - uncomment to utilize this.                    
            '''# Check to see if someone entered something wrong 
            for mans in multiple_answers:
                found_a_match = False
                for msol in multiple_solutions:
                    if msol.strip()==mans.strip():
                        found_a_match = True
                if found_a_match is False:
                    sub_points -= points_per_answer
                    partial_answer = mans
            '''

            if int(sub_points)==points_per_question:
                correct = 1 # Got them all!
            elif int(sub_points)<=0:
                correct = -1 # Got none or less than none! Yikes!
            else:
                correct = 0 # Got some.

        elif solution.isdigit() or is_float(solution): # Check to see if the answer is a number and if it is in the range.
            if answer.isdigit() or is_float(answer):
                fraction_difference = (float(answer) - float(solution))/(float(solution)+.00000000001)
                within_tolerance = np.abs(fraction_difference)<0.01
                #within_tolerance = np.abs(fraction_difference)<0.05
                #within_tolerance = np.abs(fraction_difference)<0.10
                if within_tolerance:
                    correct=1
                else:
                    correct=-1
            elif is_number_in_string(answer).isdigit() or is_float(is_number_in_string(answer)):
                temp_answer = float(is_number_in_string(answer))
                fraction_difference = (float(temp_answer) - float(solution))/(float(solution)+.00000000001)
                within_tolerance = np.abs(fraction_difference)<0.05
                if within_tolerance:
                    correct=1
                else:
                    correct=-1
            else:
                correct = -1
        # This is not a list but it is also not multiple possible answers. 
        elif answer.strip()==solution.strip() or solution==None or solution =='' or solution.lower() in answer.lower(): 
            correct=1
        elif solution.lower()=='essay':
		correct =1
		
                essay_output += "\n\\newpage \n{\large \\bf %s}\\\ \n" % (student_name)
                essay_output += "\\\ Question: %s \n \\\ " % (question) 
    		essay_output += "\\\ Answer: %s\n" % (answer)
                
		
        
    # If it is a list, then we will explicitly loop over the options.
    else:
        for s in solution:
            if answer==s:
                correct=1

    output += """<p style= \"text-align:center \"  >*************************************************************************************************** </p>"""
    
    color = 'blue'
    iscorrect = 'CORRECT!'
    extra_text = ""

    if correct==1:
        points_received = points_per_question # Get all points.
    elif correct==-1: # No points received.
        color = 'red'
        iscorrect = 'Incorrect.'
        extra_text = "  <b>The correct answer is:  &emsp;%s </center> </b>" % (solution)
    elif correct==0:
        color = 'green'
        iscorrect = 'Partially correct.'  
        if extra_partial_answer is not "":
             extra_text = "This is not a solution: &emsp;%s <br>" % (extra_partial_answer)
        if missing_partial_answer is not "":
             extra_text += "Answers that are missing: &emsp;%s <br>" % (missing_partial_answer)
        extra_text += "  <b>The correct answer is:  &emsp;%s <br> </b> </center>" % (solution)
        
        # This is for partial credit on multiple answers.
        points_received = sub_points

    if feedback_for_everyone is not None:
        extra_text += "<center>  <i>&emsp;%s <br> </i> </center>" % (feedback_for_everyone)

    if correct!=1 and feedback_for_wrong_answers is not None:
        extra_text += "<center>  <font color = \"%s\" > <i>&emsp;%s <br> </i> </font> </center>" % (color,feedback_for_wrong_answers)

    output += "<center> <font color = \"%s\" > <h1> %s </h1> </font> %s<br> <br>  You answered:   &emsp;  %s <br>  %s" % (color,iscorrect,question,answer,extra_text)

    return output,points_received,points_per_question,essay_output


################################################################################
# Read in a tab-separated file.
################################################################################
def read_tab_file(file_name): #reading a tab file once downloaded from Google Forms
    infile = csv.reader(open(file_name, 'rb'),delimiter = '\t')
    linecount=0
    questions=[]
    student_answers=[]
    solutions = []
    
    for phrase in infile:
          students=[]
          student = ['Email','Timestamp','Name',[]]
	  
          if linecount==0:
              questions=phrase[3:]
          elif linecount==1:
              solutions=phrase[3:]
          else:
              student[0] = phrase[1] # Email
              student[1] = phrase[0] # Time stamp
              student[2] = phrase[2] # Student's name
              student[3] = phrase[3:] # The student's answers
              student_answers.append(student)
          linecount+=1   

    return questions,solutions,student_answers

def make_plots(student_scores,nstudents,student_info,assignment_summary,questions):

###############################################################################
# Plots each student's score on one figure. It then loops through each students
# scores and plots the current student's score. So the number of figures equals 
# the number of students. Each student has a different graph depending on what 
# their score is. Also, sorts the scores.
###############################################################################

    student_scores=sorted(student_scores)

    average=sum(student_scores)/float(len(student_scores))
    student_info= sorted(student_info.items(),key=lambda x:x[1])
    num_of_students = np.arange(0,nstudents,1)

    for i,student in enumerate(student_info):
        fig=plt.figure()
        student_plot=plt.scatter(num_of_students,student_scores,color='b',marker='^',s=300,label='Individual student scores')
        average_plot=plt.plot([0,nstudents],[average,average],'r--',label='Average score')
        current_score = plt.scatter(i+1,student[1],color='g',marker='o',s=600,label='Your score')
        plt.yticks(np.arange(0,100,5))
        plt.xticks(np.arange(1,nstudents+1,1))
        plt.xlim(-1,nstudents+1)
        plt.legend(loc='lower left')
        plt.title('Summary of Class Scores')
        plt.xlabel('Student')
        plt.ylabel('Score')
        fig.savefig('student'+ str(i+1) + '.png')

###############################################################################
# Summarize the student responses and how the class performed on each
# question and plot the summary of each student.
###############################################################################

    colors=['lightskyblue','lightcoral']
    labels=[r'Right',r'Wrong']
    question_label=[]
    plt.figure()
    num_of_students=0
    for q,question in zip(assignment_summary.transpose(),questions):
        ntot = len(q)
        ncorrect = q.sum()
        print "Out of %d people %d got this question right---- %4.2f%%" % (ntot,ncorrect,100*ncorrect/ntot)
        question_num = 'Question #' + str(num_of_students+1)
        question_label.append(question_num)
        the_grid=GridSpec(len(questions),1)
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


