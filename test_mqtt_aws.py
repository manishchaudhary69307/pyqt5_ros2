#!/usr/bin/env python3
import time
from awscrt import io, mqtt
from awsiot import mqtt_connection_builder

# 🔑 CONFIGURATION: replace with your actual file paths
ENDPOINT = "d03688871t8b22k0412fg-ats.iot.ap-northeast-2.amazonaws.com"
CLIENT_ID = "aws_mqtt_test"
TOPIC = "test/topic"

CA_FILEPATH = "aws_certificates/AmazonRootCA1.pem"
CERT_FILEPATH ="aws_certificates/device_certificate1.pem.crt"
KEY_FILEPATH = "aws_certificates/private.pem.key"

# 1️⃣ Setup event loop and bootstrap
evt_loop = io.EventLoopGroup(1)
resolver = io.DefaultHostResolver(evt_loop)
bootstrap = io.ClientBootstrap(evt_loop, resolver)

# 2️⃣ Build MQTT connection with file paths
mqtt_conn = mqtt_connection_builder.mtls_from_path(
    endpoint=ENDPOINT,
    cert_filepath=CERT_FILEPATH,
    pri_key_filepath=KEY_FILEPATH,
    ca_filepath=CA_FILEPATH,
    client_bootstrap=bootstrap,
    client_id=CLIENT_ID,
    clean_session=False,
    keep_alive_secs=30,
    port=8883,
    tcp_connect_timeout_ms=10000,
    protocol_operation_timeout_ms=10000,
    on_connection_interrupted=lambda conn, err: print("⚠️ Connection interrupted:", err),
    on_connection_resumed=lambda conn, rc: print("🔁 Connection resumed")
)

print(f"📶 Connecting to {ENDPOINT} as '{CLIENT_ID}'...")
mqtt_conn.connect().result()
print("✅ Connected!")

# Subscribe callback
def on_message(topic, payload, **kwargs):
    print(f"📥 Received on '{topic}': {payload.decode()}")

mqtt_conn.subscribe(topic=TOPIC, qos=mqtt.QoS.AT_LEAST_ONCE, callback=on_message).result()
print(f"✅ Subscribed to '{TOPIC}'")

# Publish a few messages
for i in range(5):
    msg = f"Hard-coded message {i+1}"
    print(f"📤 Publishing: {msg}")
    mqtt_conn.publish(topic=TOPIC, payload=msg, qos=mqtt.QoS.AT_LEAST_ONCE).result()
    time.sleep(1)

time.sleep(2)

# Disconnect
mqtt_conn.disconnect().result()
print("🔌 Disconnected")
