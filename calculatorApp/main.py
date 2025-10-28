#import 
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton, QTextEdit, QHBoxLayout, QLineEdit
from PyQt5.QtGui import QFont

#App settings
app=QApplication([])
main_window=QWidget()
main_window.setWindowTitle("Calculator App")
main_window.resize(400, 300)


#all objects or widgets
text_box=QLineEdit()
text_box.setFont(QFont("Cosmic Sans MS", 20,))
text_box.setStyleSheet("QLineEdit {background-color: white; color: black; padding: 10px; border: 2px solid gray; border-radius: 8px;margin-bottom: 20px;}")
grid=QGridLayout()

buttons=["7", "8", "9", "/",
          "4", "5", "6", "*",
          "1", "2", "3", "-",
          "0", "C", "=", "+"]

clear=QPushButton("C")
delete=QPushButton("<")

def button_click():
    sender=app.sender()
    text=sender.text()
    if text =="=":
        symbol=text_box.text()
        try:
            result=eval(symbol)
            text_box.setText(str(result))
        except Exception as e:
            text_box.setText("Error")
    elif text=="C":
        text_box.clear()
    elif text=="<":
        current_text=text_box.text()
        text_box.setText(current_text[:-1])
    else:
        current_text=text_box.text()
        text_box.setText(current_text+text)






row=0
col=0
for text in buttons:
    btn=QPushButton(text)
    btn.setStyleSheet("QPushButton {" \
    "font:25pt Cosmic Sans MS;" \
        "background-color: #4CAF50;" \
        "padding: 10px;" \
        "border: none;" \
        "color: white;" \
        "border-radius: 5px;" \
        "}" 
    )
    btn.setFixedSize(50, 50)
    grid.addWidget(btn, row,col)
    btn.clicked.connect(button_click)
    col += 1
    if col > 3:
        col = 0
        row += 1

clear.clicked.connect(button_click)
delete.clicked.connect(button_click)

#design
master_layout=QVBoxLayout()
row=QHBoxLayout()

master_layout.addWidget(text_box)
master_layout.addLayout(grid)

row.addWidget(clear, alignment=Qt.AlignCenter)
row.addWidget(delete, alignment=Qt.AlignCenter)
master_layout.addLayout(row)


main_window.setLayout(master_layout)

#show and run the app
main_window.show()
app.exec_()

