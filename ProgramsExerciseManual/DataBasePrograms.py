'''
Functions for data base operations
'''

import sqlite3 as sql
import GlobalUtilitiesAndValues as gv
import ClassDefinitions as cl


def fileToSQLdatabase():
    '''
    Queries user for a file name (which is expected to be in certain format)
    Creates SQLite database file

    NOTE: For now, it is very simple, and just does this:
        - Erases current database.
        - Creates a new table from specification in latex file.
        - For each exercise, loads in an entry into the database
    '''
    while True:
        try:
            filePath = input("File with database spec (hit Enter to default to exercise manual):")
            if filePath == '':
                filePath = "..\\" + gv.exerciseFolderName + "\\" + gv.latexManual

            file = open(filePath, 'r', encoding='utf-8')
            break
        except:
            print("No such file!\n")
    
    text = file.read()
    
    #print()
    #print("*** !! PROCEEDING WILL DELETE CURRENT DATABASE !! ***")
    #input("Hit Enter To Proceed ...")
    
    dataBasePath = gv.dataBaseName
    conEC = sql.connect(dataBasePath)
    curEC = conEC.cursor()
    curEC.execute("DROP TABLE IF EXISTS exercise") # erases current database
    
    # Build new database table from text
    U = cl.UserInterface()
    DB = U.createDBfromText(text)
    cmd = cl.CreateTableCommand(DB)
    curEC.execute( cmd.makeCommandString() )

    # Add database entry for each exercise
    DBvals = U.populateDBfromText(DB, text)
    for val in DBvals:
        cmd = cl.InsertionCommand(val)
        try:
            curEC.execute( cmd.makeCommandString() )
        except:
            raise Exception("ILLEGAL INSERTION:", cmd.makeCommandString())
        
    
    conEC.commit()
    file.close()
    conEC.close()
    
    #print("New database created.")
    #input("Hit Enter To Close")



def createTxtFromIDs(startText, idList, query):
    '''
    Input:  text meant to be a template latex file.
            Two key pieces of text are looked for:
            1) %***PUT QUERY***
            2) %***PUT PROBLEMS***
            If (1) is not there, it does nothing; if so puts the query info
              that created the file.
            If (2) is not there, does nothing; if so, puts problems there.
            Expects (1) before (2).
            
    Output: text which is the same, but just includes exercises with 
            requested IDs, but as prob file.
            Can be converted to latex if desired.
    '''
    
    # Get to location right after the Query part and put in query
    index = startText.find(gv.queryLoc)
    index = index + len(gv.queryLoc)
    endText = startText[0:index] + "\n" + query +"\n"
    lastIndex = index

    # Get to location right after the Problem part and put problems
    index = startText.find(gv.exerciseLoc)
    index = index + len(gv.exerciseLoc)
    endText = endText + startText[lastIndex:index] + "\n"

    for ID in idList:
        endText = endText + "\\putProb{" + ID + "}\n\n"

    endText = endText + startText[index: ]
        
    return(endText)




def SQLdatabaseToProblemFile():
    '''
    Queries the user for which problems they care about.
    Creates appropriate TXT file.
    '''
    
    # Open standard exercise manual which has database spec
    try:
        # get full file path and name as string:
        fileString = "..\\" + gv.exerciseFolderName + "\\" + gv.latexManual
        file = open(fileString, 'r', encoding='utf-8')
    except:
        raise Exception("No such file!\n")
        
    text = file.read()
    U = cl.UserInterface()
    DB = U.createDBfromText(text)
    
    # Query user for fields wanted
    DBval = U.getUserQuery(DB)
    cmd = cl.SelectionCommand(DBval) 
    
    # Open Database for query
    dataBasePath = gv.dataBaseName
    conEC = sql.connect(dataBasePath)
    curEC = conEC.cursor()
    
    # Get all results of query
    result = curEC.execute( cmd.makeCommandString() )
    entries = result.fetchall()
    
    # Make query into list of IDs
    newEntries = []
    for e in entries:
        newEntries.append(e[0])
        
    # From ID list, and template file, create the txt fill, populate template
    while True:
        try:
            filePath = input("Path to template file (hit enter for default):")
            if filePath == '':
                filePath = '..\\' +gv.templateFolderName + '\\' + 'DatabaseResults.txt'
            print(filePath)
            templateFile = open(filePath, 'r', encoding='utf-8')
            break
        except:
            print("No such file!\n")

    templateText = templateFile.read()
    filledText = createTxtFromIDs(templateText, newEntries, cmd.makeCommandString())
    
    outputFileName = input("Output file name (hit enter for default name):")
    if outputFileName == '':
        outputFileName = gv.dataBaseResults
    outputFilePath = '..\\' + gv.outputFolderName + '\\' + outputFileName + '.txt'
    outputFile = open(outputFilePath, 'w')
    outputFile.write(filledText)
    
    print("Database results at:", gv.outputFolderName + '\\' + outputFileName + '.txt')
