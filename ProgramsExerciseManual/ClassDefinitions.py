'''
- Two Data Base Classes:
1) DataBaseSpec for storing the structure of the database, and
2) DataBaseValue for storing one entry in such a database

- Classes for SQL commands:
InsertCmd, TableCmd, SelectCmd (derived classes of an abstract class)

- Class UserInterface:
For dealing with user queries - interactive and from files.
For creating a database from a specification in a latex file, and
for querying for exercises meeting certain constraints.

'''

import GlobalUtilitiesAndValues as gv


class MenuQuery:
    '''
    An object for giving the user a menu of options,
    and obtaining the user response.
    It controls all the user interface, then passes on the option
    to some underlying control.
    '''
    def __init__(self):
        self.Q = {}     # An ordered dict of options with string and description pairs
        self.exit = ''  # The exit option (should be one of the keys)
    
    def loadQueries(self, D, exit):
        if exit not in D:
            raise Exception("Exit option", exit, "must be among options!")
            
        self.Q = D
        self.exit = exit

        
    def display(self):
        for option in self.Q:
            print(str(option) + ': ' + self.Q[option])
    
    
    def query(self):
        '''
        Queries user till they give one of the valid options.
        Returns a length 2 list, where
        - First entry is True if the user did not select the Exit option,
          and False if they did select that one.
        - Second entry is the key they chose
        '''
        print()
        print()
        self.display()
        while True:
            userInput = gv.stripString( input("Option: "), [' '] )
            userInput = userInput.upper()
            if userInput in self.Q:
                break
                
        if userInput == self.exit:
            return (False, userInput)
        else:
            return (True, userInput)


##################################################
############ DATA BASE CLASSES ###################
##################################################

class DataBaseSpec:
    '''
    Keeps track of the database specification.
    '''
    def __init__(self):
        
        # Dictionary to store database spec for category fields
        # Each key is a string name of a category database field.
        # Each value is a list of allowed values.
        self.catFields = {}
        
        # Dictionary to store database spec for binary fields
        # Each key is a string name of a binary database field.
        # Each value is a binary option in this field
        self.biFields  = {}        
        
        
    def get(self, fieldType):
        '''
        Input:  The string 'CAT' (for category type) or 'BI' (for binary type)
        Output: The corresponding dictionary
        '''
        if fieldType == 'CAT':
            return self.catFields
        elif fieldType == 'BI':
            return self.biFields
        else:
            raise Exception("Column type must be: CAT or BI")
    
        
    def add(self, fieldType, fieldName, fieldValues):
        '''
        Input: fieldType is either 'CAT' or 'BI'.
               fieldName is string name. 
               fieldValues is list of string values
        Result: loads this in.
        '''
        # Could add more error checking: fieldName is string, fieldValues is appropriate list
        if fieldType == 'CAT':
            self.catFields[fieldName] = fieldValues
        elif fieldType == 'BI':
            self.biFields[fieldName] = fieldValues
        else:
            raise Exception("Column type must be: CAT or BI")
            
            
def TEST_DataBaseSpec():
    DB = DataBaseSpec()
    DB.add('CAT', 'type', ['HW', 'TEST'])
    DB.add('BI', 'topic', ['AA', 'BB', 'CCC'])
    
    print(DB.get('CAT'))
    print(DB.get('BI'))
    
    #For testing exception handling (commented out)
    #DB.get('NeitherCatNorBi')
    #print("Program Continued? ...")



class DataBaseValue:
    '''
    For one entry in a database    
    '''
    def __init__(self, DB, ID = None):
        '''
        Input:  The DataBaseSpec that it will built on, and an optional string ID
        '''
        self.DB = DB
        self.ID = ID
    
        # For storing one value in the database.
        self.catVals = {}
        self.biVals  = {}

        # Initializes the above two dictionaries, and
        # sets Boolean self.empty to True, to indicate both dictionaries currently
        # have no values set 
        self.clear()
        

    def clear(self):
        'Initialize all the categories with empty values'
        for cat in self.DB.get('CAT'):
            self.catVals[cat] = 'NULL'
            
        for bi in self.DB.get('BI'):
            self.biVals[bi] = []

        self.empty = True
            
            
    def isEmpty(self):
        'Returns True exactly when no values are set'
        return self.empty
            
            
    def setID(self, ID):
        'Input: A string.  Sets ID to given string'
        self.ID = ID

        
    def add(self, fieldName, value):
        '''
        Can store one database value. Add/modify category value
        '''
        if fieldName in self.catVals:
            self.catVals[fieldName] = value
        elif fieldName in self.biVals:
            self.biVals[fieldName].append(value)
        else:
            raise Exception("Column TypeDoes NOT Exist! - ", fieldName)
            
        self.empty = False
        

    def getID(self):
        'Returns ID'
        return self.ID
    
    
    def get(self, fieldType):
        if fieldType == 'CAT':
            return self.catVals
        elif fieldType == 'BI':
            return self.biVals
        else:
            raise Exception("Column type must be: CAT or BI")
            
            
def TEST_DataBaseValue():
    DB = DataBaseSpec()
    DB.add('CAT', 'type', ['HW', 'TEST'])
    DB.add('BI', 'topic', ['AA', 'BB', 'CCC'])
    
    DBval = DataBaseValue(DB, 'blah111')
    print(DBval.get('CAT'))
    print(DBval.get('BI'))
    
    DBval.add('type', 'TEST')
    DBval.add('topic', 'ALG')
    DBval.add('topic', 'FRAC')
    #DBval.add('notExist', 'hi') # <-- exception check
    
    print(DBval.getID())
    print(DBval.get('CAT'))
    print(DBval.get('BI'))
    #DBval.get("BadCat") # <-- exception check



##################################################
############## COMMAND CLASSES ###################
##################################################

class SQL_Command:
    '''
    Abstract class for various SQL commands, just with methods described in general.
    They must be over-ridden by derived classes
    '''
    def __init__(self):
        # The initial string for the command should be specified
        self.initialString = ''
    
    
    def makeCommandString(self):
        '''
        Input:  No input.
        Output: Based on the current internal data, produces and returns a string
                for the relevant SQL command
        '''
        raise Exception("MUST SPECIFY: makeCommandString() method")


class CreateTableCommand(SQL_Command):
    '''
    Used for creating a Create-Table command
    '''
    
    def __init__(self, DB):
        self.initialString = "CREATE TABLE exercise ( ID TEXT, "
        self.DB = DB
        
    
    def makeCommandString(self):
        DBstring = self.initialString
        
        # First do category fields
        catFields = self.DB.get('CAT')
        for cat in catFields:
            # Create string of category names for a given category
            valueString = ''
            for x in catFields[cat]:
                valueString += "\'" + x + "\'" + " ,"
            valueString = valueString[:-1] # remove last comma
            
            DBstring += gv.quoteIt(cat) + ' TEXT CHECK(' + gv.quoteIt(cat) + ' IN (' + valueString + ')), '
            
        # Second do binary fields
        biFields = self.DB.get('BI')
        for biCat in biFields: # name biCat not relevant for table creation
            for bi in biFields[biCat]:
                DBstring += gv.quoteIt(bi) + ' BOOLEAN CHECK(' + gv.quoteIt(bi) + ' IS NULL OR ' + gv.quoteIt(bi) + ' = True), '

        DBstring = DBstring[ :-2 ] # remove last space and comma
        DBstring += ' )'
        
        return DBstring
    
def TEST_CreateTableCommand():
    DB = DataBaseSpec()
    DB.add('CAT', 'type', ['HW', 'TEST'])
    DB.add('BI', 'topic', ['AA', 'BB', 'CCC'])
    T = CreateTableCommand(DB)   
    print( T.makeCommandString() )



class InsertionCommand(SQL_Command):

    def __init__(self, DBval):
        self.initialString = "INSERT INTO exercise "
        self.DBval = DBval
    
    
    def makeCommandString(self):
        '''
        Input:  No input.
        Output: Based on the current internal data, produces and returns a string
                for the relevant SQL command
                Example of kind of output:
                INSERT INTO exercise (type, ID, style, flag) VALUES (NULL, 9,'june20','u')
        '''
        
        headerList   = '(ID, ' # will be list of column headers
        valueList    = '(' + gv.quoteIt(self.DBval.getID()) + ', '  # will be list of corresponding values
        
        catFields = self.DBval.get('CAT')
        for cat in catFields:
            headerList += gv.quoteIt(cat) + ', '
            value = catFields[cat]
            if not( gv.isNull(value) ): # non Null must be quoted. Null must not. 
                value = gv.quoteIt(value)
            valueList  += value + ', '
            
        biFields = self.DBval.get('BI')
        for biCat in biFields: # binary category name not relevant for insertion
            for biVal in biFields[biCat]:
                headerList += gv.quoteIt(biVal) + ', '
                valueList  += 'True, '
            
        headerList = headerList[ :-2 ] + ' )' # remove last space+comma, add closing parenth
        valueList  = valueList[ :-2 ]  + ' )' # remove last space+comma, add closing parenth
        
        insertionCmd = self.initialString + headerList + " VALUES " + valueList
        return insertionCmd  
    
def TEST_InsertionCommand():
    DB = DataBaseSpec()
    DB.add('CAT', 'type', ['HW', 'TEST'])
    DB.add('BI', 'topic', ['AA', 'BB', 'CCC'])
    
    DBval = DataBaseValue(DB)    
    DBval.add('type', 'TEST')
    DBval.add('topic', 'ALG')
    DBval.add('topic', 'FRAC')
    DBval.setID('blah123')
    
    I = InsertionCommand(DBval)
    print( I.makeCommandString() )



class SelectionCommand(SQL_Command):
    
    def __init__(self, DBval):
        self.initialString = 'SELECT ID FROM exercise WHERE '
        self.DBval = DBval
        
        
    def makeCommandString(self):
        '''
        Input:  No input.
        Output: Based on the current internal data, produces and returns a string
                for the relevant SQL command. Example output:
                " SELECT ID FROM exercise WHERE type = 'HW' and style='basic' " 
        '''   
        selectString = self.initialString
        
        catValues = self.DBval.get('CAT')
        for cat in catValues:
            val = catValues[cat]
            if not gv.isNull(val): # only non-NULL constrain search
                val = gv.quoteIt(val)
                selectString += gv.quoteIt(cat) + "= " + val + " and "
            
        biValues = self.DBval.get('BI')
        for biCat in biValues: # name of binary category not relevent here
            for bi in biValues[biCat]:
                selectString += gv.quoteIt(bi) + "= True and "
        
        if self.DBval.isEmpty(): # in the odd case that there are no qualifiers
            selectString = selectString[ :-6] # remove ending ' WHERE '
        else:
            selectString = selectString[ :-5] # remove last ' and '
            
        return selectString
    
    
def TEST_SelectionCommand():
    DB = DataBaseSpec()
    DB.add('CAT', 'type', ['HW', 'TEST'])
    DB.add('BI', 'topic', ['AA', 'BB', 'CCC'])
    
    DBval = DataBaseValue(DB)    
    #DBval.add('type', 'NULL') # or: 
    DBval.add('type', 'TEST')
    DBval.add('topic', 'ALG')
    DBval.add('topic', 'FRAC')
    
    
    S = SelectionCommand(DBval)
    print( S.makeCommandString() )



#########################################################
############## USER INTERFACE CLASSE ####################
#########################################################


class UserInterface:
    'Class for user interface via text or file.  Really just a collection of functions now'

    # Used by create data base
    def _addField(self, DB, text, start, end):
        'Used to add one field of database'
        
        index = text.find("[", start)
        fieldName  = gv.stripString( text[start : index], ' ') # gets name (with spaces removed)
        nextIndex = text.find("]", index)
        colType = gv.stripString( text[index+1 : nextIndex], ' ') # get column type (spaces removed)
        index = text.find(":", nextIndex)

        # Get list of values for the given column type (separated by whitespace, colons,
        # semi-colons, or '%')    
        wordList = gv.getWordList(text, index+1, end)

        # If next true then category type so name is column name and wordlist are possible vals
        if colType == 'cat': 
            DB.add('CAT', fieldName, wordList)
            #self.catFields[name] = wordList

        # else if binary
        elif colType == 'binary': 
            DB.add('BI', fieldName, wordList)
            #self.biFields[name] = wordList
            
        else: # else not one of two allowed types
            raise Exception("UNKNOW TYPE!")
        
  
    def createDBfromText(self, text):
        '''
        Input: String text.
        Ouput: DataBaseSpec object which encodes the text.
        '''
        DB = DataBaseSpec()
        
        # Get to the start of the database
        index = text.find("DATABASE_START")

        while True:
            indexStartBrace = text.find("{", index)
            indexDBend      = text.find("DATABASE_END", index)
            if indexStartBrace == -1 or (indexDBend < indexStartBrace):
                break # then done reading entries

            index = indexStartBrace
            endIndex = text.find("}", index)
        
            self._addField(DB, text, index+1, endIndex)
            
            index = endIndex
            
        return DB
    
    
    def _addDBentry(self, DB, entrytext):
        '''
        Input:  Database object and 
                the entry text for a single item to insert into data base
        Output: Corresponding DB value object
        Remark: If a category value is missing, it is set to `NULL' 
                (since they default to NULL)
        '''
        DBval = DataBaseValue(DB)
        
        # Database commands split at colons
        cmdPieces = entrytext.split(':')

        # Get first colType
        colType = gv.stripString(cmdPieces[0], [' ', '\n', '%'])

        for i in range(1, len(cmdPieces)-1): # skip first and last
            words = gv.getWordList(cmdPieces[i], 0, len(cmdPieces[i]))
            for val in words[:-1]: # skip last word, since it is next column type
                DBval.add(colType, val)

            colType = words[-1] # last word is next colType

        # Deal with last entry, where difference is that the last words are all values
        words = gv.getWordList(cmdPieces[-1], 0, len(cmdPieces[-1]))
        for val in words: # now include all words as vals (including last word)
            DBval.add(colType, val)

        return DBval
    
        
    def populateDBfromText(self, DB, text):
        '''
        Input: BD object and String text that is meant to be from a TEX file
        Ouput: List of DB value objects extracted from text.
        '''
        DBvals = []
        
        # Get to start of the problems and make endtext have matching preamble
        # Otherwise there is a fear that \ex could refer to something else.
        index = text.find("\\begin{enumerate}")
        index = text.find("}") + 1

        while True:
            index = text.find("\\ex", index)
            if index == -1:
                break

            # Get exercise ID
            code = gv.getCode(text, index)

            # Should get commands from argument for database info
            subtext, endIndex = gv.extractArg(text, index, gv.dbArg)

            # If the tag text is empty or is "NOTAGS" (and case)
            # then do NOT add; otherwise do.
            strippedSubText = gv.stripString(subtext, [' ', '%', '\n'])
            strippedSubText = strippedSubText.lower()
            if (strippedSubText != gv.noTagStr) and (strippedSubText != ''):
                DBval = self._addDBentry(DB, subtext)
                DBval.setID(code)
                DBvals.append(DBval)

            index = endIndex
        
        return DBvals
    
    
    def getUserQuery(self, DB):
        '''
        Input:  A database specification object
        Output: A database value object that results from querying user.
        '''
        DBval = DataBaseValue(DB)
        
        # First do category field queries
        catDict = DB.get('CAT')
        for cat in catDict:
            print("For category '", cat, "' possible values:", catDict[cat])
            while True: # ask till get valid value
                val = input("Your choice (hit enter for NULL):")
                val = gv.stripString(val, [' ', ',', ';', '%'])
                if val == '' or val.lower() == 'null':
                    val = 'NULL'
                if val == 'NULL' or ( val in catDict[cat] ):
                    break # got legal value
                else:
                    print("Not Valid Value! Try again ...")
                    
            if val != 'NULL': # Not actually a problem to add NULL since that is default
                DBval.add(cat, val)
            print()
        
        # Second, do binary queries
        biDict = DB.get('BI')
        for bi in biDict:
            while True: # query till get valid input
                print("For", bi, "options:", biDict[bi])
                vals = input("Your choices space or comma separated (hit enter for none):") # should put error checking!
                valList = gv.getWordList(vals, 0, len(vals)) # consider entire string
                valSet  = set(valList)
                if valSet.issubset(set(biDict[bi])): # choices should all be valid
                    break
                else:
                    print("Invalid choice! Try again ...")

            # Add these valid binary queries
            for val in valSet:
                DBval.add(bi, val)
            print()
            
        return DBval


# Test createDBfromText from UserInterface class
def TEST_createDBfromText():
    try:
        filePath = input("Path to file:")
        file = open(filePath, 'r', encoding='utf-8')
    except:
        print("No such file!\n")
    
    text = file.read()
    U = UserInterface()
    DB = U.createDBfromText(text)
    
    print( DB.get('CAT') )
    print( DB.get('BI') )


def TEST_addDBentry():
    DB = DataBaseSpec()
    DB.add('CAT', 'type', ['HW', 'TEST'])
    DB.add('BI', 'topic', ['AA', 'BB', 'CCC'])
    
    U = UserInterface()
    entrytext = '  type: HW   topic: BB  CCC '
    DBval = U._addDBentry(DB, entrytext)
    
    print(DBval.get('CAT'))
    print(DBval.get('BI'))


def TEST_populateDBfromText():
    
    try:
        filePath = input("Path to file:")
        file = open(filePath, 'r', encoding='utf-8')
    except:
        print("No such file!\n")
    
    text = file.read()
    U = UserInterface()
    DB = U.createDBfromText(text)
    
    print("FIRST CHECK DATA BASE SPEC")
    print( DB.get('CAT') )
    print( DB.get('BI') )
    
    print()
    print("NOW CHECK DATA BASE population")
    
    L = U.populateDBfromText(DB, text)
    print("READY TO PRINT L")
    for val in L:
        print(val.get('CAT'))
        print(val.get('BI'))
        print()


def TEST_getUserQuery():
    DB = DataBaseSpec()
    DB.add('CAT', 'type', ['HW', 'TEST'])
    DB.add('BI', 'topic', ['AA', 'BB', 'CCC'])
    
    U = UserInterface()
    DBval = U.getUserQuery(DB)
    print(DBval.get('CAT'))
    print(DBval.get('BI'))
    
    

