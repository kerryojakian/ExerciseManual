'''
Makes a problems set like an existing one but with similar exercises.
Does this via a series of API calls to OpenAI
'''

import GlobalUtilitiesAndValues as gv
from ArgReplace import updateArg 


from openai import OpenAI
from openai import AuthenticationError


def createModifiedSolutionPrompt(exOrig, solOrig, exNew):
    PROMPT = gv.MODSOLUTION_PROMPT_PREFIX
    PROMPT += r"\n\nExample Exercise: " + exOrig
    PROMPT += r"\n\nExample Solition: " + solOrig
    PROMPT += r"\n\nHere is the Exercise that you are making a solution for:\n" + exNew
    
    return PROMPT


def makeNewExercise(exercise, solution, newCode, client, modelToUse):
    r'''
    Input:  A single \ex as a string
            Boolean solution if we should include a solution  
    Return: A new \ex as a string which has a new exercise that is similar.
            If SOL is False, the solution field is blank
            If True, it will put a solution as follows:
            - if there was NO old solution, it just creates a new solution
            - if there WAS an old solution, it uses that as a model for the new solution.
    '''
    exText  = gv.extractArg(exercise, 0, 3)[0] # text of exercise question
    if solution:
        exSol = gv.extractArg(exercise, 0, 4)[0] # text of original solution

    # First get new exercise whether or not we have a current solution
    PROMPT = gv.EXERCISE_PROMPT_PREFIX + exText
    response = client.responses.create(model = modelToUse, input = PROMPT, timeout=30)
    newEx = response.output_text
    exercise = updateArg(exercise, r'\ex', 3, newEx)

    # If we are to add in solution ...
    # - if blank then add a new solution,
    # - otherwise use the old solution as a starting point to add in new solution
    if solution:
        if gv.stripAndDressString(exSol, [' ', '\n'], '') == '': # only replace empty solution
            PROMPT = gv.SOLUTION_PROMPT_PREFIX + newEx
        else:
            PROMPT = createModifiedSolutionPrompt(exText, exSol, newEx) 
            gv.MODSOLUTION_PROMPT_PREFIX + newEx

        response = client.responses.create(model=modelToUse, input = PROMPT, timeout=30)
        exercise = updateArg(exercise, r'\ex', 4, '\n\n' + response.output_text + '\n\n')

    # Update the code/ID of problem
    code = r'\code{' + newCode + '}'
    exercise = updateArg(exercise, r'\ex', 1, code)    
    
    return exercise


def makeParallelProblemFile():
    '''
    Queries user for a file.  Then creates a new file all the exercises made to
    be similar.
    '''
    numLen = 3 # length of number in code


    while True:
        try:
            filePath = input("Directory of file (hit enter for default of 'InputFilesDefault'):")
            filePath = gv.stripString(filePath, [" "]) # strip spaces from user input
            if filePath == '':
                filePath = "..\\" + gv.inputFolderName + "\\"
            fileName = input("File name:")
            file = open(filePath + fileName, 'r', encoding='utf-8')
            break
        except:
            print("No such file!\n")


    model = input("OpenAI model to use (hit enter for default `gpt-6-luna'):")
    model = gv.stripString(model, [" "]) # strip spaces from user input
    if model == '':
        model = "gpt-6-luna"

    while True:
        try:
            KEY = input("Your secret OpenAI API key:")
            client = OpenAI(api_key = KEY)
            client.models.list()
            break
        except AuthenticationError:
            print("Invalid key!\n")

    while True:
        user_response = input("Create solutions too (Y/N):")
        user_response = user_response.lower()
        if user_response[0] == 'y':
            SOLUTION = True
            break
        elif user_response[0] == 'n':
            SOLUTION = False
            break
        else:
            print("Respond by YES or NO ...")

    while True:
        print("For new codes in the problem, we need some info...")
        print("First, we need today's date.")
        year, month, day = gv.getDate()

        try:
            currentNum = input("Number for the first exercise (hit enter for 1): ")
            if currentNum == '':
                currentNum = 1
            currentNum = int(currentNum)
            if 1 <= currentNum:
                break
        except ValueError:
            print("Please enter integers.")

    
    startText = file.read()

    # So go to start of first listing, whether enumerate or itemize
    firstEnum = startText.find("\\begin{enumerate}")
    firstItem = startText.find("\\begin{itemize}")
    if firstEnum == -1:
        currentIndex = firstItem # if no enum, set to item
    elif firstItem == -1:
        currentIndex = firstEnum # if no item, set to enum
    else:                        # if both, set to min
        currentIndex = min(firstEnum, firstItem)

    # newText will be the return text
    # set its preamble to match start text
    newText = startText[0: currentIndex] 
    
    # index and endIndex are used in more local way than currentIndex, in order 
    # to step through the details of an exercise.
    cmd = r'\ex'
    while True:  # Loop through all instances of cmd string in text
        index = startText.find(cmd, currentIndex)
        if index == -1:
            if currentIndex != (len(startText) - 1): # if equal then odd case that at end
                currentIndex += 1 # So don't recopy last brace
                newText = newText + startText[currentIndex : ] # from current index to the end
            break

        # Next true in all cases, except the very start (Could error check on that!...)
        if startText[currentIndex] == '}':
            currentIndex += 1 # do not want to double copy end brace
        
        # fill in missing text up to the beginning of the new exercise
        newText = newText + startText[currentIndex : index]
        
        # set current index to the start of the exercise
        currentIndex = index
    
        # index and endIndex used to step thru the arguments in the command
        endIndex = index # initialize endIndex, as each loop will start with it set 
                         # before the next start of an open brace for next argument.

        # Loop to end of exercise
        for i in range( gv.numArgsInEx ):
            index = startText.find("{", endIndex) # get to open brace start of next argument
            endIndex = gv.findClosingMatch(startText, index)

        exerciseText = startText[currentIndex: endIndex+1]

        # Create code/ID for exercise
        code = gv.createDateCode(month, day, year, currentNum, numLen)
        
        # MAIN API Function call in here
        exerciseTextWithNewProblem = makeNewExercise(exerciseText, SOLUTION, code, client, model)

        currentNum += 1 # up it one for the next exercise
        newText = newText + exerciseTextWithNewProblem  
        
        # currentIndex set to position of last closing brace in the exercise
        currentIndex = endIndex
        #currentIndex = endIndex + 1 <--- OLD

    # Write new text
    outputFileName = "NEW_" + fileName

    while True:
        try:
            outputFilePath = input("Directory for new file (hit enter for default of 'OutputFilesDefault'):")
            outputFilePath = gv.stripString(outputFilePath, [" "]) # strip spaces from user input
            if outputFilePath == '':
                outputFilePath = "..\\" + gv.outputFolderName + "\\"
            outputFile = open(outputFilePath + outputFileName, 'w', encoding='utf-8')
            break
        except:
            print("Bad file path!\n")

    
    outputFile.write(newText)
    print("New file written to", outputFileName)

    outputFile.close()
    file.close()

    #input("Hit enter to close.")


