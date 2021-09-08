# -*- coding: utf-8 -*-
"""titanic_data_cleaning.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OtcncWQW-RFcwNzRH4i4-As6Oj-JU71p
"""
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import precision_recall_fscore_support

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

this_directory = os.path.dirname(os.path.realpath(__file__))


"""# Extract, transform, and load
Extract, transform, and load (ETL) is an approach used to retrieve data from different sources, transform them according to certain requirements and then load the transformed data into a desired source. This notebook contains a short walkthrough of an ETL approach, with an additional focus on inspecting, contemplating and transforming the raw data.

Our raw Titanic dataset is here loaded into a panda in python, from a CSV file. Below that, we will import a dataset with abbreviations for relevant ports.
"""

#titanic_dataset = pd.read_csv(this_directory+"\\titanic.csv")
titanic_dataset = pd.read_csv(os.path.join(this_directory, "titanic.csv"))

#print(titanic_dataset.head())



"""Koden under printer de fem første radene i datasettet. Har du noen tanker om datasettet fra det du ser? Forklaring på noen av kolonnenavnene:

Pclass - Passenger class (fare class)

Sibsp - Amount of siblings and potential partner onboard	

Parch -  Amount of parents or children onboard	

Ticket - ticket number	

Fare - ticket price	

Cabin - cabin number	

Embarked - port of embarkment  
"""


"""### How to interpret this dataset?
What is your first thoughts about this dataset? Composition of different data types, possible analytical utilizations, lack of information for your possible utilization, quality etc.?

In addition, we have a dataset containing the full port name and the linked abbreviation for each port. Run the code in order to load and print the dataset. 

The columns are:

Abbrevation - abbreviation linked to 'Embarked' in titanic.csv (foreign key)

Port_name - full port name
"""



def plot_distributions():
    fig, axes = plt.subplots(nrows=4, ncols=2, sharex=False,  sharey=False)

    fig.set_size_inches([8.3, 11.7])  # A4

    #------------------------------------------------------------------------------------------
    # Age distribution:
    #------------------------------------------------------------------------------------------
    ages = titanic_dataset["Age"]
    ax = axes[0,0]
    ax.hist(ages, bins=np.arange(ages.max()), label="Ages")
    ax.set_xlabel("age (year)")
    ax.set_ylabel("N individuals")
    ax.legend()


    #------------------------------------------------------------------------------------------
    # Ticket price distribution:
    #------------------------------------------------------------------------------------------
    fares = titanic_dataset["Fare"]
    ax = axes[0,1]
    fares.hist(ax=ax, label="Ticket prices", bins=np.arange(550, step=25))
    ax.set_xlabel("price (pound)")
    ax.legend()


    #------------------------------------------------------------------------------------------
    # Survivorship distribution:
    #------------------------------------------------------------------------------------------
    survivorship = titanic_dataset["Survived"]
    ax = axes[1,0]
    survivorship.hist(ax=ax, rwidth=1, bins=[0,1,2], label="Survivorship")
    ax.set_xticks([0.5, 1.49])
    ax.set_ylabel("N individuals")
    ax.legend()
    ax.set_ylabel("N individuals")
    ax.set_xticklabels(["died", "survived"])
    ax.legend()


    #------------------------------------------------------------------------------------------
    # Sex distribution:
    #------------------------------------------------------------------------------------------
    sex = titanic_dataset["Sex"]

    ax = axes[1,1]
    hist = sex.hist(ax=ax, rwidth=1, bins=[0,1,2], label="Sex")
    ax.set_xticks([0.5, 1.49])
    ax.legend()


    #------------------------------------------------------------------------------------------
    # Parch distribution:
    #------------------------------------------------------------------------------------------
    parch = titanic_dataset["Parch"]

    ax = axes[2,0]
    hist = parch.hist(ax=ax, bins=np.arange(parch.max()+2)-0.5, label="Parch (children)")
    ax.set_xticks([0,1,2,3,4,5,6])
    ax.set_ylabel("N individuals")
    ax.set_xlabel("N children")
    ax.legend()


    #------------------------------------------------------------------------------------------
    # Passenger class distribution:
    #------------------------------------------------------------------------------------------
    passenger_class = titanic_dataset["Pclass"]

    ax = axes[2,1]
    hist = passenger_class.hist(ax=ax, 
                      bins=np.arange(0,4)+0.5, 
                      label="Passenger classes")

    ax.set_xticks([1,2,3])
    ax.set_xlabel("class")
    ax.legend()


    #------------------------------------------------------------------------------------------
    # Sibling/spouse distribution:
    #------------------------------------------------------------------------------------------
    sibspouse = titanic_dataset["SibSp"]

    ax = axes[3,0]
    sibspouse.hist(ax=ax, 
                   bins=np.arange(sibspouse.max()+2)-0.5, 
                   label="Siblings/spouses")

    ax.set_ylabel("N individuals")
    ax.set_xlabel("N siblings/spouses")
    ax.legend()


    #------------------------------------------------------------------------------------------
    # Embarked distribution:
    #------------------------------------------------------------------------------------------
    data = titanic_dataset["Embarked"]

    ax = axes[3,1]
    data.hist(ax=ax, 
               bins=[0,1,2,3],
               label="Embarked")

    ax.set_xticks(np.array(ax.get_xticks())+0.49)
    ax.set_xlabel("port")
    ax.legend()

    # save figure:
    fig.suptitle("Parameter distributions", )
    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    fig.savefig("figs/distributions.pdf")



def survival_rates():

    survivorship = titanic_dataset["Survived"]
    sex = titanic_dataset["Sex"]

    
    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=False,  sharey=False)


    N_total_survived = np.sum(survivorship==1)

    N_male_survivors = np.sum((survivorship==1)*(sex=="male"))
    N_female_survivors = np.sum((survivorship==1)*(sex=="female"))

    N_total_men = np.sum(sex=="male")
    N_total_women = np.sum(sex=="female")
    
    print("Male survival rate: ", N_male_survivors/N_total_men)
    print("Female survival rate: ", N_female_survivors/N_total_women)
    print("Percentage of survivors that are male: ", N_male_survivors/N_total_survived)



def scatter2d(classA, classB):


    # this will be color encoded
    survivorship = titanic_dataset["Survived"]

    setA = titanic_dataset[classA]
    setB = titanic_dataset[classB]

    fig, ax = plt.subplots(nrows=1, ncols=1, sharex=False,  sharey=False)

    s=12 # size of dots

    # plot dead:
    ix = np.where(survivorship==0)[0]
    ax.scatter(setA[ix],
               setB[ix],
               label="dead", 
               s=s)

    
    # plot survived:
    ix = np.where(survivorship==1)[0]
    ax.scatter(setA[ix],
               setB[ix],
               label="survived",
               s=s)

    # ax.scatter(setA, 
    #            setB, 
    #            color=np.array(["C0", "C1"])[survivorship],
    #            s=8)
    
    ax.legend()
    ax.set_xlabel(classA)
    ax.set_ylabel(classB)

    fig.savefig(f"figs/scatter2d_{classA}_{classB}")
    


#pd.set_option('max_columns', 12)


#------------------------------------------------------------------------------------------------
# Plots                                                                                         :
#------------------------------------------------------------------------------------------------
survival_rates()
plot_distributions()
scatter2d("Age", "Fare")


"""
Tanker om datasettet:
    * Plottet fordelingene

    * Tanker:
        - Overlevelse og kjønn har ganske like histogrammer 
            + Trenger ikke bety stort, men var verdt å undersøke
            + Undersøkte nedi her

        - Prior: 
            + Passenger class, ticker price, age, sex vil ha mye å si for overlevelse
            + Men: passenger class og ticket price representerer ca. det samme

        - Rasterplot:
            + Overraskende uniformt fordelt over alder og billettpris
            + Men ser ut som tettheten i overlevelse øker relativt til druknede med økende billettpris

        - Må konvertere strings til tall for AI

    * Spm: Teller vi barn dobbelt hvis begge foreldrene er på?
        - Hva med søsken?


    * Se på sannsynlighet for overlevelse som funksjon av billettpris
    * Se på sannsynlighet for overlevelse som funksjon av alder
    * Se på sannsynlighet for overlevelse som funksjon av kjønn
"""


#ports_dataset = pd.read_csv(this_directory+"\\port_abbrevations.csv")
ports_dataset = pd.read_csv(os.path.join(this_directory, "port_abbrevations.csv"))
ports_dataset.head()



"""## Transform
Before the dataset should be utilized, some steps remain to be undertaken. In the upcoming steps, you will be asked to inspect, clean and enhance the quality of the dataset. Please think about other steps that should be consideren in this phase. If such exist, are they nessecary, are they neglectable etc.?

### Handle empty entries (missing values)
Run the following code to print Null values for each column. What do you see? Which actions can be taken when missing values appear in your dataset?

Answer:
    * Depends on the data, of course
    * Can remove data with missing values, as we do
    * Can intrapolate, as we do with the missing ages
        - Could do it stochastically, i.e. draw from a distribution with the mean,
          instead of setting missing values to the mean
"""


# Detecting missing values:

for col in titanic_dataset.columns:
    # dataframe.isnull() returns an array where with True for all null elements, False the others
    pct_missing = np.mean(titanic_dataset[col].isnull())
    print('{} - {}%'.format(col, round(pct_missing*100,1)))



"""
Please develop your code in the appropriate slots to perform the following transformations:
- Remove the column "Cabin".
- Replace Null values in the "Age" column with average age.
- Remove passengers with Null values in the "Embarked" column."""


# Code here to remove the "Cabin" column
titanic_dataset.drop(labels="Cabin", axis="columns", inplace=True)


# Code here to replace Null values in the "Age" column with the average age
# NB! Checked that the NaN values didn't affect the mean
ages = titanic_dataset["Age"]
mean_age = np.mean(ages)
ages.fillna(value=mean_age, inplace=True)


# Code here to remove passengers with Null values in the "Embarked" column 
# (Passengers without embarkment information)
embarked = titanic_dataset["Embarked"]
indices_with_null = np.where(embarked.isnull())[0]  # for some reason np.where returns the
                                                    # array in a tuple, so we need [0]
titanic_dataset.drop(indices_with_null, inplace=True)



"""### Handle duplicate data entries
Why is it unfavorable with duplicates in our dataset? Inspect if there
duplicates exist in the titanic.csv dataset. 

Answer:
    * Duplicates will weigh one specific datapoint multiple times
    * Risk biasing the analysis
    * But if the duplicates are actually from different people that has 
      identical values, they should be kept

"""

# Code here to inspect if duplicates exist in titanic.csv (titanic_dataset)
duplicates = np.where(titanic_dataset.duplicated())[0]
n_duplicates = len(duplicates)
print("Number of duplicates is", n_duplicates)



"""### Relevant and nessecary information distributed among different sources
A particular dataset will often lack essential informationm. Information is often distributed among a wide range of databases, applications, files etc. If relevant data is distributed between two tables, as in our case, and we need to gather the information, what could be a way forward?

Answer:
    * In general:
        - Gather them separately 
        - Store in simular format so they can be combined
        - Join them, unless there is a good reason not to
    * Our case:
        - We could just change the names in the existing Embarked class
        - Or we can add a new column
"""

"""### Join two datasets
In our case, we would like to have the full port name added to every entry (passenger) in our titantic dataset.
"""
# Code here to add port name to each entry (passenger) in the titanic_dataset
port_names = ports_dataset["Port_name"]
port_abbrevations = ports_dataset["Abbrevation"]

# Copy embarked:
embarked = titanic_dataset["Embarked"]
titanic_dataset["Full_port_name"] = embarked.copy()
titanic_dataset["Port_enum"] = embarked.copy()

# Then replace the copies with the corresponding port name:
for abr, fullname, port_enum in zip(port_abbrevations, port_names, [0,1,2]): 
    titanic_dataset["Full_port_name"].replace(to_replace=abr, value=fullname, inplace=True)
    titanic_dataset["Port_enum"].replace(to_replace=abr, value=port_enum, inplace=True)


# 0 = Cherbourg
# 1 = Queenstown
# 2 = Southampton


"""### Irrelevant columns
Picture us utilizing the dataset for passenger survival predictions. Are there columns that should be removed or that you consider fairly irrelevant for such a prediction?


Answer:
    * Ticket numbers seem irrelevant (cabin numbers are already removed)
    * Intuitively, embarked seems irrelevant
    * Number of children seems important, not sure about siblings/spouses
    * Passenger class and fare price likely encode the same information
        - Could easily check if they overlap at all
    * What about ports? 
        - Conceivable that rich and poor had separate ports
        - Doesn't seem very likely, but I don't know much about early 1900s ports

"""


# Run the following to inspect the present columns
print("Inspect columns:")
print(titanic_dataset.columns)


# Hint: Does some columns reflect the same information? If so, remove them from the dataset.
# Code here to remove columns if deemed nessecary

titanic_dataset.drop(labels="Pclass", axis="columns", inplace=True)
titanic_dataset.drop(labels="Ticket", axis="columns", inplace=True)
titanic_dataset.drop(labels="PassengerId", axis="columns", inplace=True)
titanic_dataset.drop(labels="Name", axis="columns", inplace=True)
titanic_dataset.drop(labels="Embarked", axis="columns", inplace=True)


print("Final result:")
print(titanic_dataset.columns)


"""## Save
We need to save our new enhanced dataset.
"""



# Code here to save titanic_dataset as a new CSV
titanic_dataset.to_csv("cleaned_dataset.csv")
print("Saved.")


"""### Additional questions
Have you made up your mind regarding other transformations, inspections or measures that should be taken to increase the quality and consistency of the titanic dataset?

"""


# Convert strings to numbers for the sex and Full_port_name classes:

# Then replace the copies with the corresponding port name:
for gender, val in zip(["male", "female"], [0,1]): 
    titanic_dataset["Sex"].replace(to_replace=gender, value=val, inplace=True)




# Write some thoughts around the bonus question here:
"""
Answer:

    * Remove "Survived"-column --> this will be the labels

    * Zero-mean and normalize the data is usually nice
    * Could downsample the age data into fewer groups
        - Same with ticket price
"""



"""# Simple Survival Modelling

Create a model that predicts if a given passenger survives, based on columns you deem relevant. You can choose an approach or a technique yourself. The accuracy and applicability is not too important, but we would like you to make some considerations around the approach (is it actually suitable, what is the advantages or disadvantages etc.)
"""
print("  ") 
print("Normalizing:")

# Zero-meaning and normalizing:
# convert to tensors:

titanic_dataset2 = titanic_dataset.copy()
titanic_dataset2.drop(labels="Full_port_name", axis="columns", inplace=True)
titanic_dataset2.drop(labels="Survived", axis="columns", inplace=True)

age_mean = np.mean(titanic_dataset2["Age"])
age_std = np.std(titanic_dataset2["Age"])
titanic_dataset2["Age"] = (titanic_dataset2["Age"]-age_mean)/age_std


classes_for_normalizing = ["Age", "Fare"]
for c in classes_for_normalizing: 
    mean = np.mean(titanic_dataset2[c])
    std = np.std(titanic_dataset2[c])
    titanic_dataset2[c] = (titanic_dataset2[c]-mean)/std



titanic_tensor = tf.convert_to_tensor(titanic_dataset2)
titanic_labels = tf.convert_to_tensor(titanic_dataset["Survived"].copy())

input_size = titanic_tensor.shape[1]
output_size = 2
hidden_layers = [32, 32]

inputs = keras.Input(shape=(input_size, ), 
                     name="input_layer")

# Forward pass:
x = inputs
# for i in range(len(hidden_layers)):
#     x = layers.Dense(units=hidden_layers[i], activation="relu")(x)  

# Output:
outputs = layers.Dense(units=output_size, activation="softmax")(x)


#x = layers.Conv2D(filters=32, kernel_size=(3, 3), activation="relu")(inputs)

#Wx = layers.Flatten()(x)
#x = layers.Dropout(0.5)(x)
# x = layers.Dense(units=128, activation='relu')(x)
# x = layers.BatchNormalization()(x)

#outputs = layers.Dense(units=n_classes, activation='softmax')(x)

model = keras.Model(inputs=inputs, outputs=outputs, name="titanic_model") 
model.summary()


##-----------------------------------------------------------------------------
## Training                                                                   : 
##-----------------------------------------------------------------------------
#loss = keras.losses.CategoricalCrossentropy(from_logits=False)
loss = keras.losses.BinaryCrossentropy(from_logits=False)

model.compile(
    loss=loss,
    optimizer=keras.optimizers.Adam(),
    metrics=["accuracy"],
)
print(titanic_tensor.shape)
print(titanic_labels.shape)

history = model.fit(titanic_tensor, 
                    titanic_labels, 
                    batch_size=1,
                    epochs=10,
                    validation_split=0.2)





# Implement a modell predicting 'Survived' here. 
# Tip: It may be that the data set needs some further transformation. 
# Tips: Remember that you can easily import a library or method of your choice.

"""To obtain an impression of your model's performance, we would like to have a quick look at the precision and recall. Please obtain the precision and recall for your survival prediciton model, and comment on the findings. 

"""

# Obtain the recall and precision here.




def main():
    #plot_distributions()
    return 0

if __name__=="__main__":
    main()
