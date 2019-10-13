import os
from os import listdir
from os.path import isfile, join

newDir = 'bioPDFs/'
def main():
    
    files = [f for f in listdir(os.getcwd()) if isfile(join(os.getcwd(), f))]
    pdfFiles = [f for f in files if f.endswith('.pdf')]

    for filePath in pdfFiles:
        newPath = newDir + filePath
        os.rename(filePath,newPath)
    print('done')


main()
