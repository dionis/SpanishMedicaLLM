import os
import re

from pathlib import Path
from zipfile import ZipFile 
from urllib import request

import xml.etree.ElementTree as ET


SCIELOoaiURL = "https://scielo.isciii.es/oai/scielo-oai.php";

SCIELOsetsFile = "scielo-sets.xml"

PREFIX_OAI20 = '{http://www.openarchives.org/OAI/2.0/}'

CORPUS_NAME = "down_dataset"

licences = {}

def getLicenses(corpusDirectory):
   licensesFull = {}
   licensesDirs = []
   path = Path(__file__).parent.absolute()
   iFile =  str(path) + os.sep + corpusDirectory + os.sep + "CC-licenses.txt"
   
   with open( iFile,encoding='utf8') as file:
      linesInFile = file.readlines()

      for iLine in linesInFile:
         licenseInfo = iLine.split("\t")
         licensesFull[licenseInfo[0]] = licenseInfo[1] + "\t" + licenseInfo[2]
         licensesDirs.append(licenseInfo[0])

   return (licensesDirs, licensesFull)

def getURL(): 

    print("Getting Scielo journals.")
    listSetUrl = SCIELOoaiURL + "?verb=ListSets"
    path = Path(__file__).parent.absolute()

    if os.path.exists(str(path) + os.sep + SCIELOsetsFile):
       os.remove(str(path) + os.sep + SCIELOsetsFile)

    response = request.urlretrieve(listSetUrl,  str(path) + os.sep + SCIELOsetsFile)


def getSets(licenses):
    print("Parsing Scielo journals XML.")
    path = Path(__file__).parent.absolute()
    tree = ET.parse(str(path) + os.sep + SCIELOsetsFile)
    root = tree.getroot()
    sets = []
    for group in root.findall(PREFIX_OAI20 + "ListSets"):
      for igroup in group.findall(PREFIX_OAI20 +"set"):
        for doc in igroup.findall(PREFIX_OAI20 +"setSpec"):
            setID = doc.text

            if setID in licenses:
                sets.append(setID)   

    print(sets)   
    return (sets)                


def printSets(sets):
    print("Saving Scielo journals info.")
    path = Path(__file__).parent.absolute()
    iFile =  str(path)  + os.sep + "scielo-sets.txt"

    if os.path.exists(iFile):
       os.remove(iFile)
  
    with open( iFile, encoding='utf8', mode='w+') as file:
        for iSets in sets:
           file.write(str(iSets) + '\n')

def initialiceProcess():
   licensesDirs, licensesFull = getLicenses(corpusDirectory = CORPUS_NAME)
   getURL()
   sets = getSets(licensesDirs)
   printSets(sets)

initialiceProcess()