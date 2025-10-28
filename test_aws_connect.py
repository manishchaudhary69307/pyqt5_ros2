
import json
import logging
import time
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

logging.basicConfig(filename='pythonIotDeviceRegister.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger('pythonIotDevice')
logger.info("pythonIotDevice")

# Connection to the AWS IoT Core with Root CA certificate and provisioning claim credentials (private key and certificates)
def helloworldCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")
    logger.info(f"Received a new message: {message.payload} from topic: {message.topic}")
# For certificate based connection
myMQTTClient = AWSIoTMQTTClient("aws_mqtt_test")
# For TLS mutual authentication
myMQTTClient.configureEndpoint("d03688871t8b22k0412fg-ats.iot.ap-northeast-2.amazonaws.com",
                               8883)  # Provide your AWS IoT Core endpoint (Example: "abcdef12345-ats.iot.us-east-1.amazonaws.com")
myMQTTClient.configureCredentials("aws_certificates/AmazonRootCA1.pem", "aws_certificates/private.pem.key",
                                  "aws_certificates/device_certificate.pem.crt")  # Set path for Root CA and unique device credentials (use the private key and certificate retrieved from the logs in Step 1)
myMQTTClient.configureOfflinePublishQueueing(-1)
myMQTTClient.configureDrainingFrequency(2)
myMQTTClient.configureConnectDisconnectTimeout(10)
myMQTTClient.configureMQTTOperationTimeout(5)
print("initialize myMQTTClient")
logger.info("Connecting...")
myMQTTClient.connect()
myMQTTClient.subscribe("test/topic1", 1, helloworldCallback)

# while True:
#     print("Publishing a message to topic: test/topic1")
#     myMQTTClient.publish("test/topic1", json.dumps({"message": "Hello World"}), 1)
#     time.sleep(5)  # Sleep for 5 seconds before publishing the next message