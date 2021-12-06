import pandas as pd
import numpy as np
import matplotlib.pyplot as plt; plt.rcdefaults()

def graph(objects,performance,x_label,y_label):
    y_pos = np.arange(len(objects))
    plt.barh(y_pos, performance, align='center', alpha=0.5)
    plt.yticks(y_pos, objects)
    plt.xlabel(x_label)
    plt.title(y_label)
    plt.show()

df = pd.read_csv('USB-IDS-1-TEST.csv', usecols=[" Label"])
print(df.iloc[:,0].value_counts())
a = (df.iloc[:,0].value_counts())

key=a.keys()
values=a.values
attack=0
benign=0

for i in range(0,len(values)):
    if str(key[i])=="BENIGN":
        benign+=values[i]
    else:
        attack+=values[i]
        
key = [benign,attack]

labels=["Benign %"+str(round(benign/(benign+attack),2)*100),
        "Attack %"+str(round(attack/(benign+attack),2)*100)]
graph(labels,key,"Numbers","Attack and Benign Percentage")