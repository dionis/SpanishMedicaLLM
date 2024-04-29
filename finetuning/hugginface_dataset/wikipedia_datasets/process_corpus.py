from pathlib import Path
import os
import numpy as np

import os
import time
import math
from huggingface_hub import login
from datasets import load_dataset, concatenate_datasets
from functools import reduce
import pandas as pd

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

HF_TOKEN = ''
DATASET_TO_LOAD = 'PlanTL-GOB-ES/pharmaconer'
DATASET_TO_UPDATE = 'somosnlp/spanish_medica_llm'

CSV_FILE_NAME = "enfermedades_long.csv"

#Loggin to Huggin Face
login(token = HF_TOKEN)

dataset_CODING = load_dataset(DATASET_TO_LOAD)
dataset_CODING
royalListOfCode = {}
issues_path = 'dataset'
tokenizer = AutoTokenizer.from_pretrained("DeepESP/gpt2-spanish-medium")
DATASET_SOURCE_ID = '7'
#Read current path
path = Path(__file__).parent.absolute()

def readCsvFIle():
    """
    """
    cantemistDstDict = {
        'raw_text': '',
        'topic': '',
        'speciallity': '',
        'raw_text_type': 'question',
        'topic_type': '',
        'source': DATASET_SOURCE_ID,
        'country': '',
        'document_id': ''
    }

    totalOfTokens = 0
    corpusToLoad = []
    countCopySeveralDocument = 0
    counteOriginalDocument = 0
    idFile = 0
    path = Path(__file__).parent.absolute()
    both_diagnostic_tratamient = open_text = type_tratamient = type_diagnostic = both_diagnostic_tratamient = 0
    df = pd.read_csv(f"{str(path)+ os.sep + CSV_FILE_NAME}",encoding='utf8')
    df = df.replace({np.nan: None})
    print(df.columns)

    for i in range(len(df)):
      
      counteOriginalDocument += 1  
      newCorpusRow = cantemistDstDict.copy()
      idFile += 1
      text = df.loc[i, 'Abstract']

      newCorpusRow['speciallity'] = df.loc[i, 'Enfermedad'] if df.loc[i, 'Enfermedad'] != None else ''

      listOfTokens = tokenizer.tokenize(text)
      currentSizeOfTokens = len(listOfTokens)
      totalOfTokens += currentSizeOfTokens  
        
      newCorpusRow['raw_text'] = text
      newCorpusRow['document_id'] = str(idFile)

      if df.loc[i, 'Tratamiento'] == None and df.loc[i, 'Diagnostico'] == None:
         open_text += 1
         newCorpusRow['topic_type'] = 'open_text'
         newCorpusRow['raw_text_type'] = 'open_text'
      elif df.loc[i, 'Tratamiento'] != None and df.loc[i, 'Diagnostico'] == None:
         type_tratamient += 1
         newCorpusRow['topic_type'] = 'medical_diagnostic'         
         newCorpusRow['topic'] = df.loc[i, 'Tratamiento']
      elif  df.loc[i, 'Tratamiento'] == None and df.loc[i, 'Diagnostico'] != None:
         type_diagnostic += 1
         newCorpusRow['topic_type'] = 'medical_topic'
         newCorpusRow['topic'] = df.loc[i, 'Diagnostico']
      elif  df.loc[i, 'Tratamiento'] != None and df.loc[i, 'Diagnostico'] != None:
         both_diagnostic_tratamient += 1
         tratmentCorpusRow = newCorpusRow.copy()

         newCorpusRow['topic_type'] = 'medical_diagnostic'
         newCorpusRow['topic'] = df.loc[i, 'Diagnostico']

         tratmentCorpusRow['topic_type'] = 'medical_topic'
         tratmentCorpusRow['topic'] = df.loc[i, 'Tratamiento']
         corpusToLoad.append(tratmentCorpusRow)

      corpusToLoad.append(newCorpusRow)
      #print(df.loc[i, "Abstract"], df.loc[i, "Diagnostico"])
    print(" Size with Open Text " + str(open_text))
    print(" Size with only tratamient " + str(type_tratamient))
    print(" Size with only diagnosti " + str(type_diagnostic))
    print(" Size with both tratamient and diagnosti " + str(both_diagnostic_tratamient))
    
    dfToHub = pd.DataFrame.from_records(corpusToLoad)

    if os.path.exists(f"{str(path)}/{issues_path}/spanish_medical_llms.jsonl"):
      os.remove(f"{str(path)}/{issues_path}/spanish_medical_llms.jsonl")


    dfToHub.to_json(f"{str(path)}/{issues_path}/spanish_medical_llms.jsonl", orient="records", lines=True)
    print(
            f"Downloaded all the issues for {DATASET_TO_LOAD}! Dataset stored at {issues_path}/spanish_medical_llms.jsonl"
    )

    print(' On dataset there are as document ', counteOriginalDocument)
    print(' On dataset there are as copy document ', countCopySeveralDocument)
    print(' On dataset there are as size of Tokens ', totalOfTokens)
    file = Path(f"{str(path)}/{issues_path}/spanish_medical_llms.jsonl")  # or Path('./doc.txt')
    size = file.stat().st_size
    print ('File size on Kilobytes (kB)', size >> 10)  # 5242880 kilobytes (kB)
    print ('File size on Megabytes  (MB)', size >> 20 ) # 5120 megabytes (MB)
    print ('File size on Gigabytes (GB)', size >> 30 ) # 5 gigabytes (GB)

    ##Update local dataset with cloud dataset
    local_spanish_dataset = load_dataset("json", data_files=f"{str(path)}/{issues_path}/spanish_medical_llms.jsonl", split="train")

    print ('<== Local Dataset ==> ')
    print(local_spanish_dataset)

    try:  
        spanish_dataset = load_dataset(DATASET_TO_UPDATE, split="train")
        spanish_dataset = concatenate_datasets([spanish_dataset, local_spanish_dataset])
        print('<--- Copy files --->')
    except Exception:
        spanish_dataset = local_spanish_dataset

    spanish_dataset.push_to_hub(DATASET_TO_UPDATE)

    print(spanish_dataset)
readCsvFIle()





