# ExerciseManual
This is a basic software package for creating and managing homework sets and tests (intended for math and computer science).  The philosophy of this project is summarized in the following points:
- Meant to facilitate the creation of Latex documents which contain exercises, but allow the creator to build any Latex freely around that.
- It is centered around a single Latex document which serves as the data base of exercises.
- The problems in the data base of problems are meant to be a large collection of curated exercises (i.e. yes AI can create gobs of exercises, but are the exact type of problems you want, and have they been checked ...)

*Disclaimer: I began small, and this thing grew! It is surely buggy in places, it is definitely clunky, and the code has taken a messy turn.  Though this package is already involved (by my standards!), I consider this the current development to be something like a messy logical core of what could some day be a much improved package.*

To use it, download all the files, keeping the existing file structure and names.
In order to use it some functionality assumes the OpenAI package is installed (install it or comment out those imports).
Then run the program MAIN.py which is the top level program calling the other programs.  To understand what is going on, some terminology is in order.

First, each exercise in a Latex file is expressed as follows:
> \ex{\code{#1}}{#2}{#3}{#4}{#5}{#6}, where
- #1 is a unique ID for the problem (it can be anything, but I often include the date of creation to avoid reuse)
- #2 is a number indicated how much space is needed for a student solution to the problem
- #3 is the actual Latex code of the exercise
- #4 is the solution for the problem if it exists
- #5 is a rubric for grading the problem (to date, this is almost universally blank ...)
- #6 is the sequence of tags describing the problem type and categories

The giant data base of problems is just a listing of "\ex" specs.  A problem set, or test, is then just some subset of these problems.  The problem sets can be specified by one of two file types:
- As a text file: Basically, a listing of the exercise IDs, along with surrounding Latex
- As a Latex file: Basically, a series of \ex specs, along with surrounding Latex

A (slightly awkward) aspect this package is that for the creation of files, one typically copies the initial file to the folder InputFilesDefault, then after running the appropriate protocal, the result will be in the folder OutputFilesDefault.   

When MAIN.py is executed it offers a menu of options, and continues to execute until you opt to quit.  The options are as follows:

A. Integrity check

B. File conversion 

