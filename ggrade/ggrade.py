# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText
import sys
import csv
import numpy as np

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



################################################################################
def email_grade_summaries(email_address,msg_from,msg_subject,msg_body,password="xxx",isHTML=False):

    ################################################################################
    # Use my GMail account
    ################################################################################
    smtpserver = 'smtp.gmail.com'
    #smtpuser = 'matthew.bellis@gmail.com'  # for SMTP AUTH, set SMTP username here
    smtpuser = msg_from  # for SMTP AUTH, set SMTP username here
    smtppasswd = password  # for SMTP AUTH, set SMTP password here
    #me = 'matthew.bellis@gmail.com'
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
        print "Successfully sent email"
        session.quit()
    except smtplib.SMTPException:
        print "Error: unable to send email"


################################################################################
# Grade an individual problem.
################################################################################
def grade_problem(question,answer,solution,points_per_question):

    sub_points = 0
    correct = -1
    points_per_question=points_per_question
    output = ""
    points_received = 0
    extra_partial_answer=""
    missing_partial_answer=""
    
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
                    if msol==mans:
                        sub_points += points_per_answer
                    
            # Check to see if someone entered something wrong
            for mans in multiple_answers:
                found_a_match = False
                for msol in multiple_solutions:
                    if msol==mans:
                        found_a_match = True
                if found_a_match is False:
                    sub_points -= points_per_answer
                    partial_answer = mans
            if int(sub_points)==points_per_question:
                correct = 1 # Got them all!
            elif int(sub_points)<=0:
                correct = -1 # Got none or less than none! Yikes!
            else:
                correct = 0 # Got some.

        elif solution.isdigit() or is_float(solution): #check to see if the answer is a number and if it is in the range
            fraction_difference = (float(answer) - float(solution))/(float(solution)+.00000000001)
            within_tolerance = np.abs(fraction_difference)<0.05
            if within_tolerance:
                correct=1
            else:
                correct=-1
         
        # This is not a list but it is also not multiple possible answers. 
        elif answer==solution or solution==None or solution =='' or solution.lower() in answer.lower() or solution=='essay': 
            correct=1
        
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
        points_received = points_per_question #get all points
    elif correct==-1: #no points received
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

    output += "<center> <font color = \"%s\" > <h1> %s </h1> </font> %s<br> <br>  You answered:   &emsp;  %s <br>  %s" % (color,iscorrect,question,answer,extra_text)

    return output,points_received,points_per_question


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
          student = ['Name','Timestamp',[]]
	  
          if linecount==0:
              questions=phrase[2:]
          elif linecount==1:
              solutions=phrase[2:]
          else:
              student[0] = phrase[1] # Name
              student[1] = phrase[0] # Time stamp
              student[2] = phrase[2:] # Their answers
              student_answers.append(student)
          linecount+=1   
    #print student

     
    return questions,solutions,student_answers


