# import modules
from PyQt5.QtWidgets import QApplication, QWidget, QLabel,QLineEdit, QPushButton, QDateEdit, QComboBox, QTableWidget, QVBoxLayout, QHBoxLayout
#App class
class ExpenseTrackerApp(QWidget):
    # main app objects and App settings
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Expense Tracker App')
        self.resize(550, 500)
        self.date_box=QDateEdit()
        self.dropdown=QComboBox()
        self.amount=QLineEdit()
        self.description=QLineEdit()


    #create objects or widgets
    #design layouts



# Run the app

