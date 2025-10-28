import paho.mqtt.client as mqtt
import time
import threading
from PyQt5.QtCore import QObject, pyqtSignal

class MQTTClient(QObject):
    """MQTT client that runs in a separate thread"""
    message_received = pyqtSignal(str)
    
    def __init__(self, broker="broker.hivemq.com", port=1883, topic="test/topic1"):
        super().__init__()
        self.broker = broker
        self.port = port
        self.topic = topic
        self.client = None
        self.running = False
        self.thread = None

    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")
        client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        try:
            message = msg.payload.decode()
            print(f"Received: {msg.topic} → {message}")
            # Emit the signal with the message
            self.message_received.emit(f"[{msg.topic}] {message}")
        except Exception as e:
            print(f"Error processing message: {e}")

    def start(self):
        """Start the MQTT client in a separate thread"""
        self.running = True
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()
        print("MQTT client thread started")

    def _run(self):
        """Main loop for the MQTT client thread"""
        try:
            self.client = mqtt.Client()
            self.client.on_connect = self.on_connect
            self.client.on_message = self.on_message
            
            print(f"Connecting to MQTT broker {self.broker}:{self.port}...")
            self.client.connect(self.broker, self.port, 60)
            self.client.loop_start()
            print("MQTT client connected and loop started")
            
            # Keep the thread alive
            while self.running:
                time.sleep(1)
                
        except Exception as e:
            print(f"Error in MQTT client: {e}")
        finally:
            if self.client:
                self.client.loop_stop()
                self.client.disconnect()

    def stop(self):
        """Stop the MQTT client"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
        print("MQTT client stopped")

    def publish(self, topic, message):
        """Publish a message to MQTT"""
        if self.client:
            try:
                self.client.publish(topic, message)
                print(f"Published to {topic}: {message}")
            except Exception as e:
                print(f"Error publishing message: {e}")

# Global MQTT client instance
mqtt_client = MQTTClient()

def get_mqtt_client():
    return mqtt_client