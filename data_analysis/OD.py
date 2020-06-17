import pandas as pd
import easygui as eg
import datetime as dt
import time
import matplotlib.pyplot as plt


###Import data and perform initial trims (must be .xlsx file)
file_path = eg.fileopenbox(msg="Please select an Excel file with raw kinetic OD data")
df = pd.read_excel(file_path,header=26) #Save Excel data in dataframe
cut_row = df.index.get_loc(df.index[df['Unnamed: 0'] == "Results"][0]) - 2 #Trim Results from dataframe
df = df.iloc[:cut_row,1:] #Cut dataframe to region of data
df = df.dropna(how='all',axis='columns') #Remove columns with no date


###Convert time to decimal hours format
for i,time in enumerate(df['Time']):
    df['Time'].iloc[i] = float(time.hour + (time.minute/60))


###Enter blank columns
b = input("\nEnter any blank columns in a comma-separated list: ")
blanks = []
for ind in b.split(","):
    blanks.append(ind.strip())

###Remove blank columns
for col in blanks:
    df = df.drop([col], axis='columns')


###Enter control columns
c = input("\nEnter any control columns in a comma-separated list: ")
controls = []
for ind in c.split(","):
    controls.append(ind.strip())


###Enter data series
series_bool = True
names=[]
while series_bool:
    ans = str(input("\nWould you like to add a data series? "))
    if (ans == "yes" or ans == "y" or ans == "Y" or ans == "Yes" or ans == "YES"):
        data = []
        name = input("\nEnter the name for this data series: ")
        d = input("\nEnter the column(s) containing OD data for this series (separated by commas if in replicates): ")
        for ind in d.split(","):
            data.append(ind.strip())
        if len(d) > 1:
            df[name+'_avg']=df.loc[:,data].mean(axis=1) #Average duplicates, triplicates, etc.
            names.append(name+'_avg') #Save name of series to list
        else:
            df[name+'_avg']=df[data]
    else:
        series_bool = False

ax = plt.gca()

df.plot(x='Time', y=names, cmap = 'tab20', ax=ax)
df.plot(x='Time',y=controls, cmap = 'tab20b', ax=ax)
plt.show()

