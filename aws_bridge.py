import sys
import os
import time
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from test_aws_connect import AWSIoTMQTTClient
    HAS_AWS = True
except ImportError:
    print("AWS IoT library not available")
    HAS_AWS = False

class AWSBridge(QObject):
    """Bridge between AWS IoT and the UI application"""
    message_received = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.aws_client = None
        self.setup_aws()

    def setup_aws(self):
        if HAS_AWS:
            try:
                self.aws_client = AWSIoTMQTTClient(
                    endpoint="d03688871t8b22k0412fg-ats.iot.ap-northeast-2.amazonaws.com",
                    client_id="aws_mqtt_test",
                    ca_filepath="aws_certificates/AmazonRootCA1.pem",
                    cert_filepath="aws_certificates/device_certificate1.pem.crt",
                    key_filepath="aws_certificates/private.pem.key",
                    topic="test/topic"
                )
                print("AWS IoT client created successfully")
                
                # Configure message callback
                if hasattr(self.aws_client, 'configure_on_message'):
                    self.aws_client.configure_on_message(self.on_aws_message)
                elif hasattr(self.aws_client, 'on_message'):
                    self.aws_client.on_message = self.on_aws_message
                
                print("🚀 Connecting AWS IoT...")
                self.aws_client.connect()
                print("AWS IoT connected successfully")
                
            except Exception as e:
                print(f"Failed to create/connect AWS client: {e}")
                self.aws_client = None
        else:
            print("AWS IoT not available")

    def on_aws_message(self, client, userdata, message):
        """Handle messages from AWS IoT"""
        try:
            msg = message.payload.decode()
            topic = message.topic
            print(f"AWS Received: {topic} → {msg}")
            # Emit the signal to update UI
            self.message_received.emit(f"[AWS] {topic}: {msg}")
        except Exception as e:
            print(f"Error processing AWS message: {e}")

    def send_message(self, topic, message):
        """Send a message via AWS IoT"""
        if self.aws_client and hasattr(self.aws_client, 'publish'):
            try:
                self.aws_client.publish(topic, message)
                print(f"Message sent to {topic}: {message}")
            except Exception as e:
                print(f"Failed to send message: {e}")

def start_aws_bridge():
    """Start the AWS bridge"""
    bridge = AWSBridge()
    return bridge

if __name__ == "__main__":
    # Test the AWS bridge
    bridge = start_aws_bridge()
    print("AWS Bridge started. Press Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting...")