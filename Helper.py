
import pickle
import pandas as pd

def binary_Write(df):
    df.to_pickle("myfile.bin")

def binary_Read(fileName):
    data = pd.read_pickle(fileName)
    return data


