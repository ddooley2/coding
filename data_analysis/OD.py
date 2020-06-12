import pandas as pd
import easygui as eg
import datetime as dt
import time

file_path = eg.fileopenbox(msg="Please select an Excel file with raw kinetic OD data")
df = pd.read_excel(file_path,header=26) #Save Excel data in dataframe
cut_row = df.index.get_loc(df.index[df['Unnamed: 0'] == "Results"][0]) - 2 #Trim Results from dataframe
df = df.iloc[:cut_row,1:] #Cut dataframe to region of data
df = df.dropna(how='all',axis='columns') #Remove columns with no date

#Convert time to decimal format (hrs)
for i,time in enumerate(df['Time']):
    df['Time'].iloc[i] = float(time.hour + (time.minute/60))

#Enter blank columns
b = input("\nEnter any blank columns in a comma-separated list: ")
blanks = []
for ind in b.split(","):
    blanks.append(ind.strip())

#Remove blank columns
for col in blanks:
    df = df.drop([col], axis='columns')

#Enter control columns
c = input("\nEnter any control columns in a comma-separated list: ")
controls = []
for ind in c.split(","):
    controls.append(ind.strip())

#Enter data columns 
#d = input("\nEnter any blank columns in a comma-separated list: ")
#data = []
#for ind in d.split(","):
#    data.append(ind.strip())





print(df)
#print(mat['Unnamed: 0']=="Results"))

#print(mat)
#print(mat.head(10))
#mat = mat[27,:]