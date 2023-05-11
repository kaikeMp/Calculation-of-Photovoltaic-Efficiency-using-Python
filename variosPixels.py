from parameters import SolarPanel as sp
from os import path as folder
from os import listdir, makedirs
from natsort import natsorted
import pandas as pd
import matplotlib.pyplot as plt

path = r'C:\Users\fisik\OneDrive\Imagens\tstixv'
path += '\\'

#Check and create a new folder named Results
output_folder = folder.join(path, 'Results')
makedirs(output_folder, exist_ok=True)

files = []

for file in natsorted(listdir(path)):
    if '.csv' in file:
        files.append(file)

#Declare the parameters that will receive dataframe Datas
concat = pd.DataFrame()

for file in files:
    #Call the function
    meas = sp(path, file)
    df = pd.DataFrame(meas.calculate_parameters())
    df.insert(0, 'Device', file)

        #get IxV pure data
    I, V = meas.get_data()

    #plot the graph
    plt.plot(V, I, 'o')
    meas.show_plot()
    plt.title(file.split('.')[0])
    plt.show()

    concat = pd.concat([df, concat], ignore_index=True)

concat.to_csv(path+'Results\\Results.csv')
print(concat)