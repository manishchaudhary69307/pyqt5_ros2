import sys
import os
from PyQt5.QtWidgets import QApplication
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import the school UI and AWS/MQTT thread
from school import start_ui
from aws_mqtt_thread import AWSMQTTThread



# def on_connection_established(aws_client):
#     """Callback when AWS connection is established"""
#     print("AWS IoT connection established, passing client to UI")
#     window.set_aws_client(aws_client)

def main():
    # Create AWS/MQTT thread instance - set use_aws=False to skip AWS
    aws_mqtt_thread = AWSMQTTThread(use_aws=False)
    
    # Start the UI application first (main thread)
    app, window = start_ui()
    
    # Connect AWS/MQTT thread to UI
    aws_mqtt_thread.message_received.connect(window.update_ui_with_message)

    # wait a moment to ensure if the connection is established
    # time.sleep(2)
    time.sleep(5)




    

    
    # Start AWS/MQTT client in a separate thread (non-blocking)
    aws_mqtt_thread.start()

    # Pass the AWS MQTT thread object to the UI window
    window.set_aws_mqtt_thread(aws_mqtt_thread)    
    print("UI and MQTT client started in separate threads")
    print("UI is running in main thread")
    print("MQTT is running in background thread")
    
    # Start the application event loop
      # Start application
    try:
        sys.exit(app.exec_())
    except KeyboardInterrupt:
        print("\nKeyboard interrupt received. Shutting down...")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
         # Close Qt application
        if app:
            print("Closing Qt application...")
            app.quit()  

if __name__ == "__main__":
    main()
