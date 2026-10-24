# GLOBAL VARIABLES
'''
Has general information used by a range of the other parts of the program:
- Has globabl variables
- Has basic utility functions
- Has prompts used for API calls to OpenAI
'''

#Next rootDir should be old
#rootDir = r"C:\Users\Kerry\Dropbox\MY_STUFF\MY_MATERIALS\Programs\Python\ExerciseManual"

key = r"\putProb" 
code = r"\code"
queryLoc = r"%***PUT QUERY***"        # where query is placed in template file
exerciseLoc = r"%***PUT PROBLEMS***"  # where problems are placed in template
dataBaseName = r"ExerciseCategories.db"  # Database name
dataBaseResults = r"DataBaseResults"  # Database name
latexManual = r"ExerciseManual.tex"      # Name of exercise manual
outputFolderName = r"OutputFilesDefault" # Folder where output files put
inputFolderName = r"InputFilesDefault" # Folder where input files some from
exerciseFolderName = r"ExerciseData"       # Folder with exercise data
templateFolderName = r"Templates"       # Folder with template data
#otherDataFolderName = r"ExerciseData\OtherData" # Folder with other data besides exercise manual
noTagStr = r"notags"

# list of characters to treat as separarting whitespace
whiteSpaceChars = ['\n', ',', ';', '%']


numArgsInEx = 6 # number of arguments in \ex command
dbArg = 6 # location of database commands in \ex
binaries = ['topics'] # REMOVE?

# NEXT two NOT used??
idArg = 1 # location of ID in \ex.
newone = 1 # ??

#####################################
####### PROMPTS START HERE 
#####################################

SOLUTION_PROMPT_PREFIX = r"""
You are generating a LaTeX solution for a math exercise database.

OUTPUT RULES (must follow exactly):

1. Return ONLY LaTeX for the solution.
2. Do NOT include explanations outside the solution.
3. Do NOT use the environments:
   verbatim, lstlisting, minted, minipage.
4. If Python code is needed, use \\texttt{{...}} or plain text lines (do NOT put it in a verbatim environment).
5. Do NOT include document headers, packages, or \\begin{{document}}.
6. Do NOT wrap the output in Markdown code fences 
(do not use ``` or ```tex, do not use ```latex, do not use anything else like that). 
Return only the raw LaTeX text.
7. Do NOT write the word ``Solution'' before the solution; just give the solution.

Return the solution in the following format:

<latex solution here>


2 EXAMPLES FOLLOW. 
Example 1 Exercise: Write a while-loop that sums the numbers from 10 to 200.
A good response:

\\texttt{total = 0}

\\texttt{num = 10}

\\texttt{while num <= 200:}

\\quad \\texttt{total += num}

\\quad \\texttt{num += 1}


Example Exercise 2: Let $h(t) = -4t$. Evaluate $h(-x)$ and $h(x - 2)$.
A good response:

$h(-x) = -4(-x) = 4x$

$h(x-2) = -4(x-2) = -4x + 8$



Here is the Exercise that you are making a solution for:

"""

MODSOLUTION_PROMPT_PREFIX = r"""
You are generating a LaTeX solution for a math exercise database.

OUTPUT RULES (must follow exactly):

1. Return ONLY LaTeX for the solution.
2. Do NOT include explanations outside the solution.
3. Do NOT use the environments:
   verbatim, lstlisting, minted, minipage.
4. If Python code is needed, use \\texttt{{...}} or plain text lines (do NOT put it in a verbatim environment).
5. Do NOT include document headers, packages, or \\begin{{document}}.
6. Do NOT wrap the output in Markdown code fences 
(do not use ``` or ```tex, do not use ```latex, do not use anything else like that). 
Return only the raw LaTeX text.
7. Do NOT write the word ``Solution'' before the solution; just give the solution.


First you will receive a similar exercise and solution, as an example.
"""



EXERCISE_PROMPT_PREFIX = r"""
You will be given a LaTeX math exercise below (called the GIVEN exercise).
You should generate a Latex math exercise that is similar to the GIVEN exercise (called the NEW exercise).

OUTPUT RULES for the NEW exercise (must follow exactly):

1. Return ONLY LaTeX.
2. Do NOT include explanations outside the exercise.
3. Do NOT use the environments:
   verbatim, lstlisting, minted, minipage.
4. If Python code is needed, use \\texttt{{...}} or plain text lines (do NOT put it in a verbatim environment).
5. Do NOT include document headers, packages, or \\begin{{document}}.
6. Do NOT wrap the output in Markdown code fences 
(do not use ``` or ```tex, do not use ```latex, do not use anything else like that). 
Return only the raw LaTeX text.
7. The NEW exercise you generate should be of a similar difficulty:
    a. Fractions should be used in the NEW exercise if and only if they are used in the GIVEN exercise.
    b. The degree of an equation in the NEW exercise should be the same as the degree of an exercise in the GIVEN exercise.

2 EXAMPLES FOLLOW. 
Example 1 GIVEN Exercise: Write a while-loop that sums the numbers from 10 to 200.

A good response to Example 1:
Write a while-loop that sums the numbers from 40 to 500.

Example 2 GIVEN exercise: Let $h(t) = -4t$. Evaluate $h(\frac{-x}{2})$ and $h(x - 2)$.

A good response to Example 2:
Let $f(x) = -7x$. Evaluate $f(x - 3)$ and $f(\frac{-2x}{3})$.


Here is the Exercise that you are given. Generate a similar exercise:

"""


#####################################
####### PROMPTS END HERE 
#####################################


def findDuplicates(L):
    'Returns a list of items which are duplicated'
    dups = []
    for i in range(len(L)):
        for j in range(len(L)):
            if i != j:
                if (L[i] == L[j]) and (L[i] not in dups):
                    dups.append(L[i])
                    
    return dups


# Next function used in latex conversion, but not best way...
def extractCode(S, i):
    '''
    Starting at some index i in the string S, this returns:
    First the text inbetween the next "{return this}" and
    Second, the index right after the final "}"
    '''
    start = S.find('{', i) + 1
    end   = S.find('}', start)
    return S[start: end], (end + 1)


def convertFileName(name, suffix):
    '''
    Input: Two strings -
      - first is a file name which has a suffix
      - second is a new suffix
    Return: the same file name replaced by new suffix
    '''
    dotLocation = name.find('.')
    outputName  = name[0 : dotLocation]
    outputName  = outputName + '.' + suffix
    return outputName


def getPathAndFile(path):
    '''
    Input: a string which is expected to be a directory with a file at the end.
    Two Outputs: name of directory, and file name
    '''
    prevIndex = 0
    currIndex = 0
    while True:
        currIndex = path.find("\\", prevIndex+1)
        if currIndex == -1:
            break
        prevIndex = currIndex
        
    return path[0:prevIndex+1], path[prevIndex+1: ]


def findClosingMatch(S, start):
    '''
    Given input string S and index start.
    At S[start] there should be a "{".  There may be many openning '{' and closing '}'
    The return is the index the closing '}' that matches S[start]
    NOTE: CHANGED TO RETURN AT LAST }
    '''
    
    # Could check that S[start] is actually open brace; just assuming
    braceIndex = start + 1 
    openBraces = 1 
    
    while openBraces != 0:
        openBrace  = S.find('{', braceIndex)
        closeBrace = S.find('}', braceIndex)
        if -1 < openBrace < closeBrace: # watch out for none find is -1
            openBraces += 1
            braceIndex = openBrace
        else:
            openBraces -= 1
            braceIndex = closeBrace
            
        braceIndex += 1
        
    return braceIndex - 1


# NEWEVER FUNCTION BELOW WHICH WOULD SUBSUME SOME OTHER FUNCTIONS
# WHICH DO SPECIAL CASE OF THIS.
def extractArg(text, index, arg):
    '''
    Input:  Some text as a string, and an integer index into this text.
    Output: Assumes that index is at the start of \\ex, that is at the slash.
            The \\ex command has a number of arguments, enclosed in braces.
            This returns the text in the braces corresponding to arg, along 
            with the index of the end of the \\ex command: i.e. at the ending brace
            
            For example: If arg is 3, this will skip the first 2 braced arguments,
            and return the text in the third one, along with the index to the end 
            of the \\ex command.
    '''
    
    endIndex = index # initialize endIndex, as each loop will start with it set 
                     # before the next start of an open brace for next argument.
        
    # Loop till at desired argument
    for i in range(arg):
        index = text.find("{", endIndex) # get to open brace start of next argument
        endIndex = findClosingMatch(text, index)
        
    # Get desired text inbetween the 2 indices, but not including the braces
    argText = text[ index+1 : endIndex ]
    
    # Continue looping till at the end of the \\ex command
    for i in range(numArgsInEx - arg):
        index = text.find("{", endIndex) # get to open brace start of next argument
        endIndex = findClosingMatch(text, index)
            
        
    return argText, endIndex




def getProblemText(code, exText):
    '''
    From the code and the exercises return just the string of the problem with
    the given code.
    '''
    index = exText.find(code)
    start = exText.rfind(r"\ex", 0, index) # PUT "r" in front to make raw string
    braceIndex = start
    
    for i in range(numArgsInEx): # since \ex has 5 arguments CHANGE
        braceIndex = exText.find('{', braceIndex)
        braceIndex = findClosingMatch(exText, braceIndex)
        

    return exText[start : braceIndex + 1 ]


# CAN BE SUBSUMED BY ABOVE FUNCTS.
def makeCodeList(S):
    '''
    Returns a list of all codes, that is text
    appearing in a code{...} or in a putProb{...}
    '''
    L = []
    currentIndex = 0
    while True:
        nextProb = S.find(key, currentIndex)
        nextCode = S.find(code, currentIndex)
        if (nextProb == -1) and (nextCode == -1):
            break
        
        if nextProb == -1:
            currentIndex = nextCode
        elif nextCode == -1:
            currentIndex = nextProb
        else:
            currentIndex = min(nextProb, nextCode)
            
        startIndex = S.find('{', currentIndex) + 1
        endIndex   = S.find('}', startIndex)
        L.append(S[startIndex : endIndex])
        
        currentIndex = endIndex
            
    return L


def stripString(S, L):
    '''
    Input:   String S and list L of characters
    Output:  The string S with the characters in L removed.
    Example: stripString("hi you  ", [' ', 'y']) returns "hiou"
    '''
    strippedStr = ''
    # Keep string, but remove characters from L
    for x in S:
        if not( x in L ): # keep non-L character as is
            strippedStr = strippedStr + x 
        # else: do nothing, i.e. character is lost
    
    return strippedStr

def TESTstripString():
    print("Should be hiou:")
    print( stripString("hi you  ", [' ', 'y']) )
    

def stripAndDressString(S, L, ch):
    '''
    Input:   String S and list L of characters and a single character ch
    Output:  The string S with each character in L replaced by the character ch.
    Example: stripAndDressString("hi you  ", [' ', 'y'], 'X') returns "hiXXouXX"
    '''
    strippedStr = ''
    # Turn characters from L into ch
    for x in S:
        if x in L:
            strippedStr = strippedStr + ch # turn into character ch
        else:
            strippedStr = strippedStr + x  # else keep character as is
    
    return strippedStr

def TESTstripAndDressString():
    print("Should be hiXXouXX:")
    print( stripAndDressString("hi you  ", [' ', 'y'], 'X') )
    

 
def getWordList(text, start, end):
    '''
    Input:  text string and integer indices
    Output: list of words in this snippet, where we take words to be any text
            separated by whitespace or comas or semi-colons.
            The latex comment symbol '%' is treated as whitespace
    '''    
    # Get requested snippet of text, turning whitespace characters into space character
    strippedStr = stripAndDressString(text[start : end], whiteSpaceChars, ' ')
    
    # Do a split on Space character.
    # But Want consecutive spaces to be viewed as one space, so need to 
    # then remove unwanted empty strings
    wordList = strippedStr.split(' ')
    while '' in wordList:
        wordList.remove('')  
    
    return wordList

def TESTgetWordList():
    text1 = "..blah6 one   two three    four    done "
    print("TEST text1:", text1)
    print( text1[6], len(text1), text1[37] )
    print( getWordList(text1, 6, 37) )
    print()
    
    text2 = "..blah6 one \n two three    four    done "
    print("TEST text2:", text2)
    print( text2[6], len(text2), text2[37] )
    print( getWordList(text2, 6, 37) )
    print()
    
    text3 = ".Xblah6\none \n two%three %%   four\n    %done "
    print("TEST text3:", text3)
    ln = len(text3)
    print( text3[1], ln, text3[ln-1] )
    print( getWordList(text3, 6, ln) )
    print()


def quoteIt(S):
    '''
    Input:   A String
    Ouput:   The same string with a left and right double quote
    Example: On input "tester" it returns ""tester""
    '''
    return '"' + S + '"'

def TEST_quoteIt():
    print(quoteIt("tester"))

def OLDquoteIt(S): # CAN DELETE ONCE SURE NOT NEED
    '''
    Input:   A String
    Ouput:   The same string with a left and right single quote
    Example: On input "tester" it returns "'tester'"
    '''
    return "'" + S + "'"




# NOTE: USE THIS? MAYBE DO IN DIFFERENT WAY?
def getCode(text, index):
    '''
    Input:  A string of text, and an integer index into it
    Output: The next ID/code string in text, starting at index 
    '''
    index = text.find(code, index) # get to '\code' string
    codeString = extractCode(text, index) # get actual id
    return codeString[0] # return just first entry, the string
    

def isNull(S):
    '''
    Input: String
    Output: Boolean True exactly when the string is 'NULL' 
    (where capitalization or not, is not relevant)
    '''
    return S.lower() == 'null'

def TEST_isNull():
    print(isNull('NuLl'))
    print(isNull('nullyy'))


def numToStr(num, numLen):
    '''
    Converts num into a number of length numLen
    - truncates left digits down as needed
    - adds zeros to left as needed
    '''
    if num < 0 or numLen < 0:
        raise Exception("Bad Negative")
    if numLen == 0:
        raise Exception("Zero Length")
    
    num = str(num)
    ln  = len(num)
    
    if ln > numLen:    # truncate extra ln-numLen left digits
        num = num[ ln-numLen : ]
    elif ln < numLen:  # add extra zeroes
        num = '0'*(numLen - ln) + num
        
    return num


def createDateCode(month, day, year, num, numLen):
    '''
    From given info creates a single string code of form:
    CxYEARxMONTHxDAYxNUM 
    where year, month and day will be made into 2 digits
          num will be made into numLen digits
    Ex: 
    '''
    codeStart = 'C'
    delim = 'x'
    month = numToStr(month, 2)
    day   = numToStr(day,   2)
    year  = numToStr(year,  2)
    code  = codeStart + delim + year + delim + month + delim + day
    code  += delim + numToStr(num, numLen)

    return code


def getDate():
    '''
    Function queries the user for the date (i.e. year, month, day as integers),
    till they give a reasonable answer
    '''

    while True:
        try:
            year = int(input("Enter year: "))
            month = int(input("Enter month: "))
            day = int(input("Enter day: "))

            correct = True

            if year < 1000 or year > 9999:
                correct = False

            if month < 1 or month > 12:
                correct = False

            if day < 1 or day > 31:
                correct = False

            if correct:
                break
            else:
                print("Invalid date. Try again.")

        except ValueError:
            print("Please enter integers.")

    return year, month, day

