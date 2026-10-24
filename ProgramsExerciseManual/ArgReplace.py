import GlobalUtilitiesAndValues as gv

# Function to add/modify an argument in a latex command environment.
def updateArg(text, cmd, argNum, argText):
    '''
    Input:
        - text: a string (containing all text)
        - cmd: a string (intended to be latex command)
        - argNum: a positive integer (intended to be argument to modify)
                  If the number of arguments for the command is n, this is 
                  espected to be between 1 and n+1, where 1 to n, indicate
                  to change an existing argument, while n+1 means to add
                  it as a new argument.
        - argText: a string (what put in argument place)
    Output:
        A string which is the same as text, but the commands have all been updated
    Example: Calling updateArg('blah \ex{A}{B}{C} \dumb{} \ex{}{}{T}', '\ex', 2, 'NEW')
             returns 'blah \ex{A}{NEW}{C} \dumb{} \ex{}{NEW}{T}'
    '''
    
    if not( 1 <= argNum <= gv.numArgsInEx + 1 ):
        raise Exception("ARGUMENT NUMBER OUT OF RANGE")
    
    newText = ''       # Return text to construct and return
    currentIndex = 0   # Keep track of currentIndex before stepping thru arguments
                       #  in the command
    while True:  # Loop through all instances of cmd string in text
        index = text.find(cmd, currentIndex)
        if index == -1:
            newText = newText + text[currentIndex : ]
            return newText
    
        # index and endIndex used to step thru the arguments in the command
        endIndex = index # initialize endIndex, as each loop will start with it set 
                         # before the next start of an open brace for next argument.

        # Loop till at desired argument
        # In case argNum is greater than args, then just go to its end
        numArgsToLoopThru = min(argNum, gv.numArgsInEx) 
        for i in range(numArgsToLoopThru):
            index = text.find("{", endIndex) # get to open brace start of next argument
            endIndex = gv.findClosingMatch(text, index)

        # Modify desired text inbetween the 2 indices:
        
        # Consider cases on whether adding a new argument or not
        # In both cases: Should be the same from the currentIndex before the command 
        #                up to the opening brace or the closing brace 
        if argNum == gv.numArgsInEx + 1:  # This case: Adding new argument (go to closing brace)
            newText = newText + text[currentIndex: endIndex+1] + "{"   
        else: # This case: Modifying middle argument(go to opening brace)   
            newText = newText + text[currentIndex: index+1]
        
        # Finish: Put in new text for this argument
        newText = newText + argText + "}"
        
        
        # currentIndex set to the text right after the closing brace for the replaced arg
        # NOTE: It is possible that currentIndex gets set to the index one past the string
        #       which is ok, as the slicing will then give till the end of the string
        currentIndex = endIndex + 1
        
        # Continue looping till at the end of the command
        for i in range(gv.numArgsInEx - argNum):
            index = text.find("{", endIndex) # get to open brace start of next argument
            endIndex = gv.findClosingMatch(text, index)

        # Set nexText to continue to the end of the command text
        newText = newText + text[currentIndex: endIndex + 1]
        
        # Set currentIndex to right after the ending brace of the command.
        currentIndex = endIndex + 1

# Testing updateArg
# print( updateArg(r'blah \ex{A}{B}{C}{}{} \dumb{} \ex{ }{}{T}{}{}', r'\ex', 2, 'NEW') )
# print( updateArg(r'blah \ex{A}{B}{C}{}{} \dumb{} \ex{ }{}{T}{}{}', r'\ex', 6, 'NEW') )
# print( updateArg(r'blah \ex{A}{B}{C}{}{} \dumb{} \ex{ }{}{T}{}{}', r'\ex', 5, 'NEW') )
# updateArg(r'blah \ex{A}{B}{C}{}{} \dumb{} \ex{ }{}{T}{}{}', r'\ex', 8, 'NEW') # <--Error


def updateArgInFile():
    '''
    Interacts with the user.
    Ask for: file name
    Result: changes the file by changing all the arguments of that number
            by replacing with the given string
    '''
    while True:
        try:
            filePath = input("Path to file:")
            file = open(filePath, 'r', encoding='utf-8')
            break
        except:
            print("No such file!\n")
    
    while True:
        try:
            argNum  = int(input("Argument number in \\ex to modify: "))
            argText = input("Argument text to put: ")
            newText = updateArg(file.read(), '\\ex', argNum, argText)
            break
        except:
            print("Give valid inputs!\n")
    
    file.close()
    
    outputFile = open(filePath, 'w')
    outputFile.write(newText)

    outputFile.close()

    print("File has been updated.")
    input("Hit Enter End")

#updateArgInFile()

def TEST_simple():
    '''
    Just read and write ...
    '''
    name = 'testForArgReplace.tex'
    #file = open(name, 'r', encoding='utf-8')
    file = open(name, 'r')    
    newText = newText = file.read()
    file.close()
    
    outputFile = open(name, 'w')
    outputFile.write(newText)

    outputFile.close()

    print("File has been updated.")
    input("Hit Enter End")
    

def TEST_updateArg():
    argNum = 6
    argText = "BLAH"
    cmd = '\\ex'
    text = "\subsection{Log and Exponentials \topic{LE} } \ex {\code{GROUPxxxFxLEx25x04x02x001}}{0}{{\large SIMULATION:  SPREAD OF RUMOR OR DISEASE}On each round, walk around the room till the instructor says “Stop”.  At thatpoint, get into pairs and look at just eachother's paper. e is NO’s}{} {}"

    print("TEST without file")
    newText = updateArg(text, cmd, argNum, argText)
    print(newText)
    print()
    
    print("TEST WITH file: BEFORE")
    file = open('testForArgReplace.tex', 'r', encoding='utf-8')
    text = file.read()
    print(text)
    print()
    
    print("TEST WITH file: AFTER")
    newText = updateArg(text, '\\ex', argNum, argText)
    print(newText)

    outputFile = open('testForArgReplace.tex', 'w')
    outputFile.write(newText)

    
    
