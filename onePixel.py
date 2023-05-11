from parameters import SolarPanel as sp
import pandas as pd
import os
import matplotlib.pyplot as plt

#Path of source folder for IxV files.
path = r'C:\Users\fisik\OneDrive\Imagens\tstixv'
path += '\\'

#Name of the file to be calculated.
name = 'out4'
file = name+'.csv'

#Call the function
meas = sp(path, file)
df = pd.DataFrame(meas.calculate_parameters())

#Check and create a new folder named Results
output_folder = os.path.join(path, 'Results')
os.makedirs(output_folder, exist_ok=True)

#get IxV pure data
I, V = meas.get_data()

#plot the graph
plt.plot(V, I, 'o')
meas.show_plot()
plt.show()

df.to_csv(path+'Results\\'+name)

print(df)

