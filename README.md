# ggrade
Tools to grade the output of a Google Forms that was used for a quiz.

This was a summer project at [Siena College](http://www.siena.edu) to bring flexible grading options to Google Forms. The primary authors are Matt Bellis and Sara Mahar. 

Google Forms, primarily used for polls and surveys, is also used by a number of instructors to assign quizzes and homeworks to students. We wanted to create a command-line tool for ``easy" and flexible grading. There are plugins available for Google Forms that can do this as well, like [Flubaroo](http://www.flubaroo.com/), but we wanted something that worked with Python and text files. 

ggrade works well with some questions styles and not well with others. 

Successes!
* Multiple choice questions are trivial!
* Multiple choice with multiple possible answers are trivial!
* Numerical answers are trivial!

Partial successes
* Ranked questions can be done, but only with binary comparisons (is A bigger/smaller than B?, for example). 
* Essay questions cannot be automatically graded, but we are planning on adding a feature to dump the answers to a text/PDF file for later printing and grading by the instructor. 

Limitations
* There is no way to have students sketch a figure or label a figure using Google Forms. Though the instructor could have an image where different sections are labeled with A,B,C, etc., and the student must then identify those sections.

In this repository, we provide the ggrade library which handles grading and emailing the students (using your own GMail account) and a basic script to actually do the grading. All code is open source and available for editing by you!

See the [Issues](https://github.com/mattbellis/ggrade/issues) page to see outstanding bugs and upcoming enhancements. 

Feel free to contact us with comments and suggestions!



# Installation instructions.
[How to install the ggrade package](https://docs.google.com/presentation/d/1HF6IzTF4_QTbtqSXEil2KNgKmdbUUwM-5pxwu9fuX5I/edit?usp=sharing)

# How to use ggrade

* How to create a quiz with Google Forms
* Assigning the quiz and creating the solutions key
* Downloading the student responses and adding additional feedback
* Grading the quizzes, emailing the students, and creating summary plots


