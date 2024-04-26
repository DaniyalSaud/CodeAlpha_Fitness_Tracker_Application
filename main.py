from GUI import *
from PyQt5.QtWidgets import QApplication
import sys
import pandas as pd
import os


journal_data = {'Day': '', 'Height':'', 'Weight': '', "BMI":''}
today_data = {'Day': 'N/A', 'Height':'N/A', 'Weight': 'N/A', "BMI":'N/A'} 

if __name__ == '__main__':        
    app = QApplication(sys.argv)
    
    window = MainWindow(today_data, journal_data)
    window.show()
    app.exec_()