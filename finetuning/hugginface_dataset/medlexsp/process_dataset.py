from datasets import load_dataset
import os
import re

from pathlib import Path
from zipfile import ZipFile 
import tarfile

import xml.etree.ElementTree as ET

FILE_PATH = "MedLexSp_v2" + os.sep + "MedLexSp_v2" + os.sep  + "MedLexSp_v2.xml"

path = Path(__file__).parent.absolute()
tree = ET.parse(str(path) + os.sep + FILE_PATH)
root = tree.getroot()
sets = []
counterSeveralType = 0
counterDocument = 0
for group in root.findall("{http://www.lexicalmarkupframework.org/}Lexicon"):
    for igroup in group.findall("{http://www.lexicalmarkupframework.org/}LexicalEntry"):
        for item in igroup.findall("{http://www.lexicalmarkupframework.org/}Lemma"):
            print (str(item.attrib['writtenForm']).capitalize())
        counterDocument += 1 
        for doc in igroup.findall("{http://www.lexicalmarkupframework.org/}SemanticType"):
            setID = doc.attrib['val']
            print ("\t Type ==> " + str(setID).capitalize())
            sets.append(setID)  
            counterSeveralType += 1

print (f"Size of Document is {counterDocument}")        
print (f"Size of Types on Document is {counterSeveralType}")     
#print(sets)   
