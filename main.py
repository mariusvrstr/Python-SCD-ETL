import os
import pandas as pd


directory = os.getcwd()

file_path = f'{directory}/etl/sample_files/ExampleFile.xlsx'

data = pd.read_excel (file_path) 
df = pd.DataFrame(data, columns= ['External Reference'])
print (df)