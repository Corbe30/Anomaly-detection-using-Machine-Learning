from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
 
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
 
 
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import csv
import time
import warnings
warnings.filterwarnings("ignore")
 
#this function creates a folder named "feaure_graph" in the program directory.
def folder(f_name):
    try:
        if not os.path.exists(f_name):
            os.makedirs(f_name)
    except OSError:
        print ("The folder could not be created!")
        
# CSV file is named in which the results are saved.
result="./results/results_Final.csv"
# CSV files names: #The names of the dataset files (csv_files). 
csv_files=["USB-IDS-1-TRAINING.csv"]
path=""
repetition=1
 
#this function creates a folder named "results" and "result_graph_1" in the program directory.
def folder(f_name): 
    try:
        if not os.path.exists(f_name):
            os.makedirs(f_name)
    except OSError:
        print ("The folder could not be created!")
 
folder_name="./results/"
folder(folder_name)
folder_name="./results/result_graph_Final/"
folder(folder_name)

# the 20 features selected by the file "04_2_feature_selection_for_attack_files.py" are used here. (+ Label Feature)
usecols=["Bwd Packet Length Std","Flow Bytes/s","Total Length of Fwd Packets","Fwd Packet Length Std","Flow IAT Std",
"Flow IAT Min","Fwd IAT Total","Flow Duration","Bwd Packet Length Max","Flow IAT Max","Flow IAT Mean","Total Length of Bwd Packets",
"Fwd Packet Length Min","Bwd Packet Length Mean","Flow Packets/s","Fwd Packet Length Mean","Total Backward Packets","Total Fwd Packets",
"Fwd Packet Length Max","Bwd Packet Length Min",'Label']
 
#The machine learning algorithms to be used are defined in a dictionary (ml_list).
ml_list={
"Nearest Neighbors":KNeighborsClassifier(3)
}
others=[" Bwd Packet Length Std", "Flow Bytes/s", "Total Length of Fwd Packets", " Fwd Packet Length Std",
     " Flow IAT Std", " Flow IAT Min", "Fwd IAT Total", " Label"]
 
#In this part different sets of properties for machine learning methods are defined as follows:
algorithms_features={
"Nearest Neighbors":others
}
seconds=time.time()#time stamp for all processing time

#A CSV file is created to save the results obtained.
with open(result, "w", newline="",encoding="utf-8") as f:
    wrt = csv.writer(f)
    wrt.writerow(["File","ML algorithm","accuracy","Precision", "Recall" , "F1-score","Time"])

#this loop runs on the list containing the filenames.Operations are repeated for all attack files
for j in csv_files:
    # print output header
    print ('%-17s %-17s  %-15s %-15s %-15s %-15s %-15s' % ("File","ML algorithm","accuracy","Precision", "Recall" , "F1-score","Time"))
    feature_list=others
    #read an attack file.
    df=pd.read_csv(path+j, usecols=others) 
    df=df.fillna(0)
    attack_or_not=[]

    #it changes the normal label to "1" and the attack tag to "0" for use in the machine learning algorithm
    for i in df[" Label"]: 
        if i =="BENIGN":
            attack_or_not.append(1)
        else:
            attack_or_not.append(0)
    df[" Label"]=attack_or_not
 
    #this section separates the label and the data into two separate pieces, as Label=y Data=X 
    y = df[" Label"] 
    del df[" Label"]
    feature_list.remove(' Label')

    #this loop runs on the list containing the machine learning algorithm.
    for ii in ml_list:
        X = df[algorithms_features[ii]]
        precision=[]
        recall=[]
        f1=[]
        accuracy=[]
        t_time=[]

        # This loop allows cross-validation and machine learning algorithm to be repeated 1 time
        for i in range(repetition): 
            #time stamp for processing time
            second=time.time()
            # cross-validation
            #  data (X) and labels (y) are divided into 2 parts to be sent to the machine learning algorithm. 
            #  So, in total there are 4 tracks: training data(X_train), training tag (y_train), test data(X_test) and test tag(y_test).
            X_train, X_test, y_train, y_test = train_test_split(X, y,test_size = 0.20, random_state = repetition)
 
            #machine learning algorithm is applied in this section
            #choose algorithm from ml_list dictionary                                                                          
            clf = ml_list[ii]
            clf.fit(X_train, y_train)
            predict =clf.predict(X_test)
        
            #makes "classification report" and assigns the precision, f-measure, and recall values.s.    
            f_1=f1_score(y_test, predict, average='macro')
            pr=precision_score(y_test, predict, average='macro')
            rc=recall_score(y_test, predict, average='macro')
            precision.append(float(pr))
            recall.append(float(rc))
            f1.append(float(f_1))
            accuracy.append(clf.score(X_test, y_test))
            t_time.append(float((time.time()-second)) )
        print ('%-17s %-17s  %-15s %-15s %-15s %-15s %-15s' % (j[0:-4],ii,str(round(np.mean(accuracy),2)),str(round(np.mean(precision),2)), 
            str(round(np.mean(recall),2)),str(round(np.mean(f1),2)),str(round(np.mean(t_time),4))))#the avarage result of the ten repetitions is printed on the screen.

        # all the values found are saved in the opened file.
        with open(result, "a", newline="",encoding="utf-8") as f: 
            wrt = csv.writer(f)
            for i in range(0,len(t_time)):
                wrt.writerow([j[0:-4],ii,accuracy[i],precision[i],recall[i],f1[i],t_time[i]])#file name, algorithm name, precision, recall and f-measure are writed in CSV file

        # In this section, Box graphics are created for the results of machine learning algorithms and saved in the feaure_graph folder.
        plt.boxplot(f1)
        plt.title("All Dataset - " +str(ii))
        plt.ylabel('F-measure')
        plt.savefig(folder_name+j[0:-4]+str(ii)+".pdf",bbox_inches='tight', papertype = 'a4', orientation = 'portrait', format = 'pdf')
        plt.show()# you can remove the # sign if you want to see the graphics simultaneously

print("mission accomplished!")
print("Total operation time: = ",time.time()- seconds ,"seconds")