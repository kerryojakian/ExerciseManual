'''
Does an integrity check of some latex file of exercises.
For now it is simple; just looking for duplicate codes names of
exercises, and reports that all is fine (no duplicates) or
gives the duplicated codes
'''

import GlobalUtilitiesAndValues as gv


def integrityCheck():
    fileName = input("File to check (hit Enter to default to exercise manual):")
    if fileName == '':
        fileName = "..\\" + gv.exerciseFolderName + "\\" + gv.latexManual

    file = open(fileName, 'r', encoding='utf-8')
    text = file.read()

    codes = gv.makeCodeList(text)
    dups  = gv.findDuplicates(codes)

    # Count number of exercises
    print("Number of exercises:", len( gv.makeCodeList(text) ) )

    if dups == []:
        print("Good - No duplicate exercises!")
    else:
        print("The following codes are duplicated:")
        for c in dups:
            print(c)
              
    
