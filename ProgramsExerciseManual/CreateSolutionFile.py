'''
Does an API call to OpenAI in order to add solutions to an existing
exercise file.  If a solution is already there, it does not change it.
If the solution field is blank (just spaces or empty) for a solution,
the API call gets a solution and fills it in
'''

import GlobalUtilitiesAndValues as gv
from ArgReplace import updateArg 

from openai import OpenAI
from openai import AuthenticationError



def dummyAddSolution(exercise):
    '''
    Input:  A single ex as a string
    Return: The same ex with a DUMMY solution filled in if the Solution was blank.
            If there is already a solution, then it returns unchanged exercise
    Note:   This is for testing dynamics without OpenAI calls.
    '''
    exText  = gv.extractArg(exercise, 0, 3)[0] # text of exercise question
    solText = gv.extractArg(exercise, 0, 4)[0] # text of exercise solution
    if gv.stripAndDressString(solText, [' ', '\n'], '') == '': # only replace empty solution
        PROMPT = gv.SOLUTION_PROMPT_PREFIX + exText
        output_text = "\n\nDUMMY SOLUTION!\n"
        exercise = updateArg(exercise, r'\ex', 4, '\n\n' + output_text + '\n\n')
        change = True
    else:
        change = False
        
        
    return (change, exercise)



def addSolution(exercise, client, modelToUse):
    '''
    Input:  A single ex as a string
    Return: The same ex with a solution filled in if the Solution was blank.
            If there is already a solution, then it returns unchanged exercise
    '''
    
    exText  = gv.extractArg(exercise, 0, 3)[0] # text of exercise question
    solText = gv.extractArg(exercise, 0, 4)[0] # text of exercise solution
    if gv.stripAndDressString(solText, [' ', '\n'], '') == '': # only replace empty solution
        PROMPT = gv.SOLUTION_PROMPT_PREFIX + exText
        response = client.responses.create(model = modelToUse, input = PROMPT)
        solutionText = '\n\n' + response.output_text + '\n'
        exercise = updateArg(exercise, r'\ex', 4, solutionText)
        change = True
    else:
        change = False
        
        
    return (change, exercise)


def addSolutionsToFile():
    '''
    Queries user for a file.  Then creates a new file with all missing 
    solutions filled in.
    '''    

    fileUpdateFreq = 50 # how often the file is updated
    numExProcessed = 0  # keeps track of number of exercises processed mod fileUpdateFred
    numBatches     = 0  # number of size fileUpdateFreq batches processed
    
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
    
    
            
    #pathName, fileName = gv.getPathAndFile(filePath) <--- old now?
    startText = file.read()

    # setup output file
    outputFileName = "SOLUTIONS_" + fileName

    while True:
        try:
            outputFilePath = input("Directory where you want output file (hit enter for default of 'OutputFilesDefault'):")
            outputFilePath = gv.stripString(outputFilePath, [" "]) # strip spaces from user input
            if outputFilePath == '':
                outputFilePath = "..\\" + gv.outputFolderName + "\\"
            outputFile = open(outputFilePath + outputFileName, 'w', encoding='utf-8')
            break
        except:
            print("Bad file path!\n")

    # So go to start of first listing, whether enumerate or itemize
    firstEnum = startText.find("\\begin{enumerate}")
    firstItem = startText.find("\\begin{itemize}")
    if firstEnum == -1:
        currentIndex = firstItem # if no enum, set to item
    elif firstItem == -1:
        currentIndex = firstEnum # if no item, set to enum
    else:                        # if both, set to min
        currentIndex = min(firstEnum, firstItem)

    # For large files, output in batches; this index is used
    batchIndex = 0

    # newText will be the return text
    # set its preamble to match start text
    newText = startText[0: currentIndex] 
    
    # index and endIndex are used in more local way than currentIndex, in order 
    # to step through the details of an exercise.
    cmd = r'\ex'
    while True:  # Loop through all instances of cmd string in text
        index = startText.find(cmd, currentIndex)
        if index == -1:
            newText = newText + startText[currentIndex : ] # from current index to the end
            break

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

        # Key point: Call open AI for solution!
        (change, exerciseTextWithSolution) = addSolution(exerciseText, client, model)      
        #(change, exerciseTextWithSolution) = dummyAddSolution(exerciseText) #<-- Uncomment test without openAI
        if change:
            numExProcessed += 1
        
        newText = newText + exerciseTextWithSolution  
        
        # currentIndex set to one position past the last closing brace in the exercise
        currentIndex = endIndex + 1

        # maybe write partial output
        if numExProcessed == fileUpdateFreq:
            #outputFile.seek(0)
            #outputFile.truncate()
            #outputFile.write(newText)
            #outputFile.flush()
            outputFile.write(newText[batchIndex: ]) #appends from batchIndex to end
            num = (numBatches + 1) * fileUpdateFreq
            print("Partial solutions written to", outputFileName + ".", num, "exercises so far!")
            numExProcessed = 0
            numBatches += 1
            batchIndex = len(newText) # set to index right after last of newText


    outputFile.write(newText[batchIndex: ])
    print("Complete solutions written to", outputFileName)
    print("In folder: ", outputFilePath)

    outputFile.close()
    file.close()
