## To publish message from the terminal into broker.hivemq.com
mosquitto_pub -h broker.hivemq.com -t "agv/control" -m "Hello from terminal!"

## To subsribe message from the terminal into broker.hivemq.com

mosquitto_sub -h broker.hivemq.com -t "test/topic1" 
