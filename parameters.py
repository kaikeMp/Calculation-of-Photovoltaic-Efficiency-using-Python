import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np

class SolarPanel:
    def __init__(self, path, file, amps='mA', area=0.09, pin = 1):
        self.path = path
        self.file = file
        self.amps = amps
        self.area = area
        self.pin = pin
        
        self.I, self.V = self.get_data()
        self.interpolate_df = self.interpolate()
        
    def get_data(self):
        """
        Instruction: This function must export a tuple with two pandas.core.series.Series - (I, V) both with the 
        same length of the dataframe imported 
        """
        conv = 1
        if self.amps == 'mA':
            conv = 1
        elif self.amps == 'A':
            conv = 1000
        ixv = pd.read_csv(self.path+self.file, header=None)
        V = ixv[0]
        I = ixv[1]/conv
        return (I, V)

    def interpolate(self):
        """
        Instruction: This function must export a dataframe with 3 columns and length equal to 1000 as 
        is estipulated in line intvolt
        """
        interp_func = interp1d(self.V, self.I, kind='cubic')
        intvolt = np.linspace(self.V.min(), self.V.max(), num=1000)
        intcur = interp_func(intvolt)
        interpolate = pd.DataFrame({'Voltage': intvolt, 'Current': intcur, 'Power': intvolt * intcur}, index=None)
        return interpolate

    def show_plot(self):
        """
        Instruction: This function must plot a graph
        """
        plt.plot(self.interpolate_df['Voltage'], self.interpolate_df['Current'])

    def calculate_parameters(self):
        """
        Instruction: This function must export a dictionary with the following parameters:
        'Isc (mA)', 'Voc (V)', 'Pmax (W)', 'Imp (mA)', 'Vmp (V)', 'PCE (%)', 'FF (%)', 'Jsc (mA)'
        """
        # calculate max power
        Pmax = abs(self.interpolate_df['Power'].min())

        # calculate Maximum V and I
        Vmp = abs(self.interpolate_df[self.interpolate_df['Power'] == self.interpolate_df['Power'].min()]['Voltage']).to_numpy()[0]
        Imp = abs(self.interpolate_df[self.interpolate_df['Power'] == self.interpolate_df['Power'].min()]['Current']).to_numpy()[0]

        # Calculate Isc and Voc
        Isc = (self.interpolate_df[self.interpolate_df['Voltage'].abs() == self.interpolate_df['Voltage'].abs().min()]['Current']).to_numpy()[0] * (-1)
        Voc = (self.interpolate_df[self.interpolate_df['Current'].abs() == self.interpolate_df['Current'].abs().min()]['Voltage']).to_numpy()[0]

        # Calculate FF
        FF = abs(Imp * Vmp / (Isc * Voc))

        # Calculate Jsc
        Jsc = Isc / self.area

        # Calculate PCE
        PCE = abs(Voc * Isc * FF / self.area)/self.pin

        return {'Isc (mA)': [Isc], 'Voc (V)': [Voc], 'Pmax (W)': [Pmax], 'Imp (mA)': [Imp], 'Vmp (V)': [Vmp], 'PCE (%)': [PCE], 'FF (%)': [FF * 100], 'Jsc (mA)': [Jsc]}


if '__main__' == '__name__':
    path = r'C:\Users\fisik\OneDrive\Imagens\tstixv'
    path += '\\'

    file = 'out4.csv'

    meas = SolarPanel(path, file)

    df = pd.DataFrame(meas.calculate_parameters())
    print(df)