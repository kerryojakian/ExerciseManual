'''
Functions for converting a text file (that just has the code names
for exercises) into a complete latex exercise file.
'''

import GlobalUtilitiesAndValues as gv


def convertTextToLatex():

    while True:
        try:
            textFilePath = input("Path to file, excluding file name (hit enter for 'InputFilesDefault'):")
            textFilePath = gv.stripString(textFilePath, [" "]) # strip spaces from user input
            if textFilePath == '':
                textFilePath = "..\\" + gv.inputFolderName + "\\"
            fileName = input("File name:")
            textFile = open(textFilePath + fileName, 'r', encoding='utf-8')
            break
        except:
            print("No such file!\n")

    
    exerciseBankName = input("Name of EXERCISE file (hit enter for default manual):")
    if exerciseBankName == "":
        exerciseBankName = "..\\" + gv.exerciseFolderName + "\\" + gv.latexManual
    exerciseBankFile = open(exerciseBankName, 'r', encoding='utf-8')
    
    exerciseText = exerciseBankFile.read() 
    startText = textFile.read()
    endText = ''
    
    while True:
        index = startText.find(gv.key)
        if index == -1:
            endText = endText + startText
            break
            
        code, endIndex = gv.extractCode(startText, index)
        problemText = gv.getProblemText(code, exerciseText)
        endText = endText + startText[0:index] + problemText
        startText = startText[endIndex : ]
        
    
    outputFileName = gv.convertFileName(fileName,'tex')

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
    
    
    outputFile = open(outputFilePath + outputFileName, 'w')
    outputFile.write(endText)

    print("Output TEX file at:", outputFileName)
    print("In folder: ", outputFilePath)

    textFile.close()
    outputFile.close()


