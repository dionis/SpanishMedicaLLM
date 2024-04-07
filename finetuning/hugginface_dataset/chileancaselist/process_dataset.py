from datasets import load_dataset
import os
import re

from pathlib import Path
from zipfile import ZipFile 

FILE_PATH = "ChilieanCaseList.zip"

path = Path(__file__).parent.absolute()

from urllib import request
URL = 'https://zenodo.org/records/7555181/files/cwlc.zip?download=1'

FILE_ZIP =  str(path) + os.sep + "ChilieanCaseList.zip"
FILE_ZIP_EXTRAC =  str(path) + os.sep + "ChilieanCaseList"

if not os.path.exists( FILE_ZIP ):
   response = request.urlretrieve(URL,  str(path) + os.sep + "ChilieanCaseList.zip")

   # loading the temp.zip and creating a zip object 
   if os.path.exists( FILE_ZIP_EXTRAC ):
        os.remove(FILE_ZIP_EXTRAC)
        os.makedirs(FILE_ZIP_EXTRAC)
        
   with ZipFile(FILE_ZIP, 'r') as zObject: 
    
        # Extracting specific file in the zip 
        # into a specific location. 
         zObject.extractall( FILE_ZIP_EXTRAC) 
         zObject.close() 

   #Open Zip

# with open( str(path) + os.sep + 'example.txt', encoding='utf8') as file:
#   """
#      # Build a dictionary with ICD-O-3 associated with 
#      # healtcare problems
#   """
#   linesInFile = file.readlines()
 
#   for index, iLine in enumerate(linesInFile): 
#     print([linesInFile[index]]) if len(linesInFile[index]) > 1 else  print('**************') if linesInFile[index] == '\n' else print ('******* ERROR ********')
 

    # if re.match('^Las dilataciones bronquiales',iLine):
    #   break
   

    # code = listOfData[0]
    # description = reduce(lambda a, b: a + " "+ b, listOfData[1:2], "")
    # royalListOfCode[code.strip()] = description.strip()