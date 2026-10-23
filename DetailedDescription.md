# Detailed Description

Here I go beyond the ReadMe file to describe the details on how to use this package.

To use it, download all the files, keeping the existing file structure and names.
In order to use it, some functionality assumes the OpenAI package is installed for API calls to it (install it or comment out those imports).
Then run the program *MAIN.py* which is the top level program calling the other programs.  To understand what is going on, some terminology is in order.

First, each exercise in a Latex file is expressed as follows:
> \ex{\code{#1}}{#2}{#3}{#4}{#5}{#6}, where
- #1 is a unique ID for the problem (it can be anything, but I often include the date of creation to avoid reuse)
- #2 is a number indicated how much space is needed for a student solution to the problem
- #3 is the actual Latex code of the exercise
- #4 is the solution for the problem if it exists
- #5 is a rubric for grading the problem (to date, this is almost universally blank ...)
- #6 is the sequence of tags describing the problem type and categories (can be left blank)

The giant data base of problems (in the file ExerciseData/ExerciseManual.tex) is just a listing of "\ex" specs, along with some section information for a table of contents.  A problem set, or test, is then just some subset of these problems.  The problem sets can be specified by one of two file types:
- As a text file: Basically, a listing of the exercise IDs, along with surrounding Latex
- As a Latex file: Basically, a series of \ex specs, along with surrounding Latex

A (slightly awkward) aspect this package is that for the creation of files, one typically copies the initial file to the folder InputFilesDefault, then after running the appropriate protocol, the result will be in the folder OutputFilesDefault. Thus for carrying out an operation, you need to move it to InputFilesDefault first (perhaps 
from OutputFilesDefault).  This can all be avoided, as you are allowed to override where the programs read from and where they write to.

When MAIN.py is executed it offers a menu of options, and continues to execute until you opt to quit.  The options are as follows:

> A. Integrity Check: Checks the exercise manual (or another file if desired) to see that it has no repeated IDs and also gives a count on the number of exercises.  In the future, I would envision doing more - checking that the entire file is structured properly.
>
> B. Convert text  ---> LaTex: Converts a text file with just exercise ideas to a LaTex file with the exercises filled in by reading the exercises from the exercise manual (or another file if desired).
>
> C. Convert Latex ---> text: Converts a LaTex file to a text file, so that the resulting text file is basically just a listing of the exercise IDs.
>
> D. Update latex: Updates the specified LaTex file with the current exercises from the exercise manual.  Thus, the intention is that exercises are always updated in the exercise manual, so it represents the most current version - some out of date exercise set is updated with this operation.
>
> E. Select exercises from exercise bank: By choosing a series of tags, you can choose a subset of the problems from the exercise manual.  This is useful, since the exercise manual is large, and growing.
>
> F. Create solution file: Creates a solution file ...
> 
> G. Create new problem set with same kinds of problems: Creates a doppelganger problem set ...


