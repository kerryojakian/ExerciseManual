'''
This provides a console interface with a menu of operations that
can be done on various exercise files
'''

import collections as co
import GlobalUtilitiesAndValues as gv
import IntegrityCheckExercises as tg
import LatexToText as lt
import TextToLatex as tl
import UpdateLatex as up
import DataBasePrograms as db
import ClassDefinitions as cl
import CreateSolutionFile as cf
import CreateDoppelganger as dp



def doOperation(option):
    if option == 'A':
        tg.integrityCheck()
    elif option == 'B':
        tl.convertTextToLatex()
    elif option == 'C':
        lt.LatexToText_WithFiles()
    elif option == 'D':
        up.UpdateLatex_WithFiles()
    elif option == 'E':
        db.fileToSQLdatabase() # build updated database
        db.SQLdatabaseToProblemFile() # get user selection and make file
    elif option == 'F':
        cf.addSolutionsToFile()
    elif option == 'G':
        dp.makeParallelProblemFile()


def main():
    Q = cl.MenuQuery()
    options = co.OrderedDict([ ('A', "Integrity Check"), \
                               ('B', "Convert text  ---> LaTex"), \
                               ('C', "Convert Latex ---> text"), \
                               ('D', "Update latex"), \
                               ('E', "Select exercises from exercise bank"), \
                               ('F', "Create solution file"), \
                               ('G', "Create new problem set with same kinds of problems"), \
                               ('X', "Exit")])
    Q.loadQueries(options, 'X')
    while True:
        (exitValue, response) = Q.query()
        if exitValue == False:
            break
            
        doOperation(response)

main()




