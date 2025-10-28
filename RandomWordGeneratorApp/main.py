#import modules
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton
from random import choice

my_words = ["apple", "banana", "cherry", "date", "elderberry", "fig", "grape", "honeydew"]

#Main app objects and App settings
app=QApplication([])
main_window=QWidget()
main_window.setWindowTitle("Random Word Generator")
main_window.resize(400, 300)

#Create all app objects
title= QLabel("Random word generator")
text1= QLabel("?")
text2= QLabel("?")
text3=QLabel("?")

button1=QPushButton("click me")
button2=QPushButton("click me")
button3=QPushButton("click me")



#All design here
master_layout= QVBoxLayout()
row1= QHBoxLayout()
row2=QHBoxLayout()
row3=QHBoxLayout()

#Add widgets to rows
row1.addWidget(title, alignment=Qt.AlignCenter)
row2.addWidget(text1, alignment=Qt.AlignCenter)
row2.addWidget(text2, alignment=Qt.AlignCenter)
row2.addWidget(text3, alignment=Qt.AlignCenter)

row3.addWidget(button1)
row3.addWidget(button2)
row3.addWidget(button3)

master_layout.addLayout(row1)
master_layout.addLayout(row2)
master_layout.addLayout(row3)

main_window.setLayout(master_layout)

#functions to generate random words and connect buttons
def generate_random_word_from_list():
    return choice(my_words)


def on_button1_click():
    random_word = generate_random_word_from_list()
    text1.setText(random_word)
def on_button2_click():
    random_word = generate_random_word_from_list()
    text2.setText(random_word)
def on_button3_click():
    random_word = generate_random_word_from_list()
    text3.setText(random_word)

#events 
button1.clicked.connect(on_button1_click)
button2.clicked.connect(on_button2_click)
button3.clicked.connect(on_button3_click)


#show or run our app
main_window.show()
app.exec_()