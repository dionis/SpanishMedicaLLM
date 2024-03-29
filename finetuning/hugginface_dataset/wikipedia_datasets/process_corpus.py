import pandas as pd
from pathlib import Path
import os
CSV_FILE_NAME = "enfermedades_long.csv"

def readCsvFIle():
    """
    """
    path = Path(__file__).parent.absolute()

    df = pd.read_csv(f"{str(path)+ os.sep + CSV_FILE_NAME}",encoding='utf8')
    print(df.columns)
    for i in range(len(df)):
      print(df.loc[i, "Abstract"], df.loc[i, "Diagnostico"])

readCsvFIle()





