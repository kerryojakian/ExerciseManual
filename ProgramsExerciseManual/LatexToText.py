'''
Functions for converting a latex exercise file to a simple
text exercise file which just lists the codes of the exercises.
'''

import GlobalUtilitiesAndValues as gv

def LatexToText(text):
    '''
    Input: A string that is meant to have been read from a TEX file
    Return: String with ex just converted to \\putProb with code
    '''
    startText = text
    
    # Get to start of the problems and make endtext have matching preamble
    index = startText.find("\\begin{enumerate}")
    endText = startText[0:index] + "\\begin{enumerate}\n\n" # deal with \b - backspace char
    index = startText.find("}") + 1
    
    while True:
        index = startText.find("\\code", index)
        if index == -1:
            break
            
        code, endIndex = gv.extractCode(startText, index) # just end of code
        endText = endText + "\\putProb{" + code + "}\n\n" 
        index = endIndex
        
    endText = endText + "\\end{enumerate} \n\\end{document}"
    return(endText)


def LatexToText_WithFiles():

    while True:
        try:
            filePath = input("Path to file, excluding file name (hit enter for 'InputFilesDefault'):")
            filePath = gv.stripString(filePath, [" "]) # strip spaces from user input
            if filePath == '':
                filePath = "..\\" + gv.inputFolderName + "\\"
            fileName = input("File name:")
            texFile = open(filePath + fileName, 'r', encoding='utf-8')
            break
        except:
            print("No such file!\n")

    
    outText = LatexToText( texFile.read() )
    outputFileName = gv.convertFileName(fileName, "txt")

    while True:
        try:
            outputFilePath = input("Output file path, excluding file (hit enter for 'OutputFilesDefault'):")
            outputFilePath = gv.stripString(outputFilePath, [" "]) # strip spaces from user input
            if outputFilePath == '':
                outputFilePath = "..\\" + gv.outputFolderName + "\\"
            outputFile = open(outputFilePath + outputFileName, 'w', encoding='utf-8')
            break
        except:
            print("Bad file path!\n")

    outputFile.write(outText)

    print("Output TEXT file at:", outputFileName)
    print("In folder: ", outputFilePath)

    texFile.close()
    outputFile.close()


    

