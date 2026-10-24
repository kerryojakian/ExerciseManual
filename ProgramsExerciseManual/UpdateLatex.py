'''
This updates an exercise file with the latest text of the exercise
from the main file, using the code name.
'''

import GlobalUtilitiesAndValues as gv

def UpdateLatex(startText, exerciseText):
    r'''
    Input: A string that is meant to have been read from a TEX file
    Return: String updated \ex exercises
    '''
    
    # Get to start of the problems and make endtext have matching preamble
    index = startText.find("\\begin{enumerate}")
    index = startText.find("}", index) + 1
    endText = startText[0:index] + "\n"

    while True:
        codeIndex = startText.find("\\code", index)
        if codeIndex == -1:
            break

            
        code, index = gv.extractCode(startText, codeIndex) # just end of code
        
        problemText = gv.getProblemText(code, exerciseText)
        endText = endText + problemText + "\n\n"

        
    endText = endText + "\n \\end{enumerate} \n\\end{document}"
    return(endText)


def UpdateLatex_WithFiles():

    # Get the name of the latex file and open it.

    while True:
        try:
            texFilePath = input("Path to file, excluding file name (hit enter for 'InputFilesDefault'):")
            texFilePath = gv.stripString(texFilePath, [" "]) # strip spaces from user input
            if texFilePath == '':
                texFilePath = "..\\" + gv.inputFolderName + "\\"
            fileName = input("File name:")
            texFile = open(texFilePath + fileName, 'r', encoding='utf-8')
            break
        except:
            print("No such file!\n")


    # Get the name of the exercise bank and open it (defaults to manual).
    exerciseBankName = input("Name of EXERCISE file (hit enter for default manual):")
    if exerciseBankName == "":
        exerciseBankName = "..\\" + gv.exerciseFolderName + "\\" + gv.latexManual
    exerciseBankFile = open(exerciseBankName, 'r', encoding='utf-8')

    # Key call to function which creates new output
    outText = UpdateLatex( texFile.read(), exerciseBankFile.read() )

    exerciseBankFile.close()
    texFile.close()
    
    # Write the output to the file
    while True:
        try:
            outputFilePath = input("Output file path, excluding file (hit enter for 'OutputFilesDefault'):")
            outputFilePath = gv.stripString(outputFilePath, [" "]) # strip spaces from user input
            if outputFilePath == '':
                outputFilePath = "..\\" + gv.outputFolderName + "\\"
            outputFile = open(outputFilePath + fileName, 'w', encoding='utf-8')
            break
        except:
            print("Bad file path!\n")
    
    outputFile.write(outText)
    print("Update Latex in:", outputFilePath)
    
    outputFile.close()

    
