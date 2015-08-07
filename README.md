# ggrade
Tools to grade the output of a Google Forms that was used for a quiz.

This was a summer project at [Siena College](http://www.siena.edu) to bring flexible grading options to Google Forms. The primary authors are Matt Bellis and Sara Mahar. 

Check out the SAMPLES.md file if you want to see a sample.

Google Forms, primarily used for polls and surveys, is also used by a number of instructors to assign quizzes and homeworks to students. We wanted to create a command-line tool for ``easy" and flexible grading. There are plugins available for Google Forms that can do this as well, like [Flubaroo](http://www.flubaroo.com/), but we wanted something that worked with Python and text files. 

ggrade works well with some questions styles and not well with others. 

Successes!
* Multiple choice questions are trivial!
* Multiple choice with multiple possible answers are trivial!
* Numerical answers are trivial!

Partial successes
* Ranked questions can be done, but only with binary comparisons (is A bigger/smaller than B?, for example). 
* Essay questions cannot be automatically graded, but we are planning on adding a feature to dump the answers to a text/PDF file for later printing and grading by the instructor. 
** We have explored the idea of searching in short answer or essay questions for words or phrases, and computationally, we've been able to make this work. However, the challenge still remains for the instructor to search for the full range of possible correct responses.

Limitations
* There is no way to have students sketch a figure or label a figure using Google Forms. Though the instructor could have an image where different sections are labeled with A,B,C, etc., and the student must then identify those sections.

In this repository, we provide the ggrade library which handles grading and emailing the students (using your own GMail account) and a basic script to actually do the grading. All code is open source and available for editing by you!

See the [Issues](https://github.com/mattbellis/ggrade/issues) page to see outstanding bugs and upcoming enhancements. 

Feel free to contact us with comments and suggestions!



# Installation instructions.
If you're familiar with git/Github and Python packages, you can clone/fork this repository and then from the ggrade directory type

    sudo python setup.py install

More detailed instructions can be found at
[How to install the ggrade package](https://docs.google.com/presentation/d/1HF6IzTF4_QTbtqSXEil2KNgKmdbUUwM-5pxwu9fuX5I/edit?usp=sharing)

# How to use ggrade

* [How to create a quiz with Google Forms](https://docs.google.com/presentation/d/1y54EqQW6B33ZHKnn8fERqpVAjA4WE-moT8rkddE6GX8/edit?usp=sharing)
* [Assigning the quiz and creating the solutions key](https://docs.google.com/presentation/d/1B8XK8vX93PIWcP7S3MGeHZfwQtK9TXiPiSh50PnTJv8/edit?usp=sharing)
* [Downloading the student responses and adding additional feedback](https://docs.google.com/presentation/d/1nMqCg26xaxgn4N8zpg9_srxVyxpNBavNxOMx3XSW2A4/edit?usp=sharing)
* [Grading the quizzes, emailing the students, and creating summary plots](https://docs.google.com/presentation/d/1qM8dA9d7x3Mj6mlpatx0wOBEHIqm48siSz1qJqS70AQ/edit?usp=sharing)


