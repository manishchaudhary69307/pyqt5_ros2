from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import sys
from PyQt5.uic import loadUiType
import mysql.connector as con
import os

# Get the absolute path to the UI file
current_dir = os.path.dirname(os.path.abspath(__file__))
ui_file = os.path.join(current_dir, 'school_controls.ui')

ui, _ = loadUiType(ui_file)

class MainApp(QMainWindow, ui):
    # Define a signal to receive messages from MQTT thread
    mqtt_message_received = pyqtSignal(str)
    
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget.tabBar().setVisible(False)
        self.menubar.setVisible(False)
        # self.btn_login.clicked.connect(self.login)
        # self.menu11.triggered.connect(self.show_add_new_student_tab)
        # self.btn_save_std_details.clicked.connect(self.save_student_details)
        
        # Connect the signal to update UI
        self.mqtt_message_received.connect(self.update_ui_with_message)

          # Initialize button states dictionary
        self.aws_mqtt_thread = None

        self.button_states = {
            "forward": 0,
            "backward": 0,
            "left": 0,
            "right": 0,
            "stop": 0
        }
        
        # ... rest of your initialization
        self.setup_buttons()

        
        print("UI initialized")

    def setup_buttons(self):
        """Setup button connections"""
        # Assuming you have buttons named: btn_forward, btn_backward, etc.
        self.btn_forward.clicked.connect(lambda: self.on_direction_button_clicked("forward"))
        self.btn_backward.clicked.connect(lambda: self.on_direction_button_clicked("backward"))
        self.btn_left.clicked.connect(lambda: self.on_direction_button_clicked("left"))
        self.btn_right.clicked.connect(lambda: self.on_direction_button_clicked("right"))
        self.btn_stop.clicked.connect(lambda: self.on_direction_button_clicked("stop"))


    def on_direction_button_clicked(self, button_name):
        """
        Handle direction button clicks
        
        Args:
            button_name: Name of the button clicked ("forward", "backward", "left", "right", "stop")
        """
        # Reset all buttons to 0
        for key in self.button_states:
            self.button_states[key] = 0
        
        # Set the clicked button to 1
        self.button_states[button_name] = 1
        
        # Create message dictionary
        message = {
            "forward": self.button_states["forward"],
            "backward": self.button_states["backward"],
            "left": self.button_states["left"],
            "right": self.button_states["right"],
            "stop": self.button_states["stop"]
        }
        
        print(f"Button clicked: {button_name}")
        print(f"Publishing message: {message}")
        
        # Publish to MQTT
        topic = "agv/control"  # Change this to your actual topic
        self.publish_message(topic, message)

    def publish_message(self, topic, message):
        """Publish a message using the AWS MQTT thread"""
        if self.aws_mqtt_thread:
            self.aws_mqtt_thread.publish(topic, message)
        else:
            print("AWS MQTT thread not available")

    @pyqtSlot(str)
    def update_ui_with_message(self, message):
        """Update the UI with the received message (thread-safe)------------------------------------------------------------------------------------"""
        try:
            # self.led_full_name.setText(message)
            print(f"UI updated with: {message}")
        except Exception as e:
            print(f"Error updating UI: {e}")


    def set_aws_mqtt_thread(self, mqtt_thread):
        """Store reference to AWS MQTT thread"""
        self.aws_mqtt_thread = mqtt_thread
        print("AWS MQTT thread reference set in UI")

    # Login Form Authentication
    def login(self):
        un = self.led_username.text()
        pw = self.led_password.text()
        if un == "admin" and pw == "admin":
            self.menubar.setVisible(True)
            self.tabWidget.setCurrentIndex(1)
            self.tabWidget.tabBar().setVisible(True)
        else:
            QMessageBox.information(self, "ROS2 Project")

    # Add New Student
    def show_add_new_student_tab(self):
        self.tabWidget.setCurrentIndex(2)
        self.fill_next_registration_number()

    def fill_next_registration_number(self):
        try:
            rn = 0
            mydb = con.connect(host="localhost", user="root", 
                              password="admin@1122", db="school")
            cursor = mydb.cursor()
            cursor.execute("SELECT MAX(registration_number) FROM student")
            result = cursor.fetchone()
            if result and result[0] is not None:
                rn = result[0]
            self.led_registration_number.setText(str(rn + 1))
        except con.Error as e:
            print("Error has occurred: " + str(e))
            self.led_registration_number.setText("1001")

    def save_student_details(self):
        try:
            mydb = con.connect(host="localhost", user="root", 
                              password="admin@1122", db="school")
            cursor = mydb.cursor()
            registration_number = self.led_registration_number.text()
            # full_name = self.led_full_name.text()
            gender = self.cb_gender.currentText()
            email = self.led_email.text()
            phone = self.led_phone.text()
            address = self.tb_address.toPlainText()
            standard = self.cb_standard.currentText()
            date_of_birth = "14 april"
            age = 12
            
            qry = """INSERT INTO student(registration_number, full_name, gender, 
                     date_of_birth, age, address, phone, email, standard) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            # value = (registration_number, full_name, gender, date_of_birth, 
            #         age, address, phone, email, standard)
            value=(registration_number, full_name, "Male", "2024-11-2", 24,"kirtipr",12212222, "mahnisschaudhary@gmail.com", "hello")
            cursor.execute(qry, value)
            mydb.commit()
            QMessageBox.information(self, "Student data", 
                                   "Student data saved successfully")
            
        except con.Error as e:
            QMessageBox.critical(self, "Database Error", 
                                f"Error occurred while saving data: {str(e)}")



def start_ui():
    """Start the UI application"""
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    return app, window

if __name__ == "__main__":
    app, window = start_ui()
    sys.exit(app.exec_())