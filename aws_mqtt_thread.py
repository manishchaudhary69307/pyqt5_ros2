import threading
import time
import sys
import os
import json
from PyQt5.QtCore import QObject, pyqtSignal

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class AWSMQTTThread(QObject):
    """AWS/MQTT client that runs in a separate thread"""
    message_received = pyqtSignal(str)
    connection_established = pyqtSignal(object)  # New signal to pass the connected client

    
    def __init__(self, use_aws=False):
        super().__init__()
        self.running = False
        self.thread = None
        self.connected = False
        self.use_aws = use_aws
        self.aws_client = None
        self.mqtt_client = None
  
      

    def start(self):
        """Start the AWS/MQTT client in a separate thread"""
        if self.running:
            print("AWS/MQTT client is already running")
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        print("AWS/MQTT client thread started")

    def _run(self):
        """Main loop for the AWS/MQTT client thread"""
        try:
            if self.use_aws:
                self._run_aws()
            else:
                self._run_mqtt()
                
        except Exception as e:
            print(f"Error in AWS/MQTT client: {e}")
        finally:
            print("AWS/MQTT client thread stopped")

    def _run_aws(self):
        """Run AWS IoT client using the correct SDK API"""
        try:
            # Import AWS client only when needed
            from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
            
            # Create MQTT client
            self.aws_client = AWSIoTMQTTClient("aws_mqtt_test")
            
            # Configure endpoint and credentials
            self.aws_client.configureEndpoint(
                "d03688871t8b22k0412fg-ats.iot.ap-northeast-2.amazonaws.com", 
                8883
            )
            self.aws_client.configureCredentials(
                "aws_certificates/AmazonRootCA1.pem",
                "aws_certificates/private.pem.key",
                "aws_certificates/device_certificate.pem.crt"
            )
            
            # Configure connection settings
            self.aws_client.configureOfflinePublishQueueing(-1)
            self.aws_client.configureDrainingFrequency(2)
            self.aws_client.configureConnectDisconnectTimeout(10)
            self.aws_client.configureMQTTOperationTimeout(5)
            
            print("🚀 Connecting AWS IoT...")
            self.aws_client.connect()
            self.connected = True
            print("AWS IoT connected successfully")

              # Emit signal with the connected client instance
            self.connection_established.emit(self.aws_client)
            
            # Subscribe to topic
            self.aws_client.subscribe("test/topic1", 1, self._on_aws_message)
            print("Subscribed to test/topic1")

            # create a timer to publish messages every 5 seconds if connected
            while not self.connected:
                time.sleep(0.1)
            self.aws_client.publish("test/topic1", json.dumps({"message": "hello from aws_mqtt_thread.py"}), 1)


            


            
            print("Published to test/topic2")
            
            # Keep the thread alive
            while self.running:
                time.sleep(0.1)
                
        except ImportError:
            print("AWS IoT library not available, falling back to MQTT")
            self._run_mqtt()
        except Exception as e:
            print(f"Failed to create/connect AWS client: {e}")
            print("Falling back to MQTT")
            self._run_mqtt()

    def _on_aws_message(self, client, userdata, message):
        """Handle messages from AWS IoT"""
        try:
            msg = message.payload.decode()
            topic = message.topic
            print(f"AWS Received: {topic} → {msg}")
            # Emit the signal to update UI
            self.message_received.emit(f"[AWS] {topic}: {msg}")
        except Exception as e:
            print(f"Error processing AWS message: {e}")

    def _run_mqtt(self):
        """Fallback to standard MQTT"""
        try:
            import paho.mqtt.client as mqtt
            
            self.mqtt_client = mqtt.Client()
            self.mqtt_client.on_connect = self._on_mqtt_connect
            self.mqtt_client.on_message = self._on_mqtt_message
            
            print("Connecting to MQTT broker broker.hivemq.com:1883...")
            self.mqtt_client.connect("broker.hivemq.com", 1883, 60)
            self.mqtt_client.loop_start()
            self.connected = True
            print("MQTT client connected successfully")
            
            # Keep the thread alive
            while self.running:
                time.sleep(0.1)
                
        except Exception as e:
            print(f"Failed to create/connect MQTT client: {e}")

    def _on_mqtt_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT broker")
            self.connected = True
            client.subscribe("test/topic1")
        else:
            print(f"Failed to connect to MQTT broker, return code {rc}")

    def _on_mqtt_message(self, client, userdata, msg):
        try:
            message = msg.payload.decode()
            print(f"MQTT Received: {msg.topic} → {message}")
            # Emit the signal to update UI
            self.message_received.emit(f"[MQTT] {msg.topic}: {message}")
        except Exception as e:
            print(f"Error processing MQTT message: {e}")

    def stop(self):
        """Stop the AWS/MQTT client"""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=2.0)
        print("AWS/MQTT client stopped")

    def publish(self, topic, message):
        print("inside publishing aws functionn----------------------------------------------------------------")

        """Publish a message"""
        if self.use_aws and self.connected and self.aws_client:
            try:
                self.aws_client.publish(topic, json.dumps(message), 1)
                print(f"Published to AWS {topic}: {message}")
            except Exception as e:
                print(f"Error publishing to AWS: {e}")
        elif self.connected and self.mqtt_client:
            try:
                self.mqtt_client.publish(topic, json.dumps(message), qos=1)
                print(f"Published to MQTT {topic}: {message}")
            except Exception as e:
                print(f"Error publishing to MQTT: {e}")
        else:
            print("Client not connected, cannot publish")