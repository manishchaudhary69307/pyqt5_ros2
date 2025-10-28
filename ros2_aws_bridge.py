import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import json
import time

class ROSAWSBridge(Node):
    """
    Bridge between ROS 2 and AWS IoT
    - Subscribes to ROS topics and forwards to AWS IoT
    - Receives from AWS IoT and publishes to ROS topics
    """
    
    def __init__(self, aws_client=None):
        super().__init__('ros_aws_bridge')
        self.aws_client = aws_client
        self.mqtt_connected = aws_client is not None
        
        # Subscribe to ROS topics to forward to AWS
        self.ros_subscriber = self.create_subscription(
            String,
            'test_topic',  # Subscribe to the topic published by test_publisher
            self.ros_to_aws_callback,
            10
        )
        
        # Create ROS publisher for AWS → ROS messages
        self.aws_to_ros_publisher = self.create_publisher(
            String,
            'aws_messages',  # New topic for AWS messages
            10
        )
        
        self.get_logger().info('ROS-AWS Bridge Started')

    def set_aws_client(self, aws_client):
        """Set the AWS IoT client instance"""
        self.aws_client = aws_client
        self.mqtt_connected = True
        self.get_logger().info('AWS IoT client connected to bridge')

    def ros_to_aws_callback(self, msg):
        """When ROS message received, forward to AWS IoT"""
        self.get_logger().info(f'Received from ROS: "{msg.data}"')
        
        if self.aws_client and self.mqtt_connected:
            try:
                aws_msg = {
                    "source": "ros_bridge",
                    "ros_message": msg.data,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                self.aws_client.publish("ros/bridge/topic", json.dumps(aws_msg), 1)
                self.get_logger().info(f'Forwarded to AWS IoT: {json.dumps(aws_msg)}')
            except Exception as e:
                self.get_logger().error(f'Failed to forward to AWS: {str(e)}')

    def aws_to_ros_callback(self, client, userdata, message):
        """When AWS message received, forward to ROS"""
        try:
            msg_text = message.payload.decode()
            topic = message.topic
            self.get_logger().info(f'Received from AWS: "{msg_text}" on topic: {topic}')
            
            # Forward to ROS topic
            ros_msg = String()
            ros_msg.data = f"[AWS] {topic}: {msg_text}"
            self.aws_to_ros_publisher.publish(ros_msg)
            self.get_logger().info(f'Forwarded to ROS: "{ros_msg.data}"')
            
        except Exception as e:
            self.get_logger().error(f'Error processing AWS message: {str(e)}')

    def publish_to_ros(self, message):
        """Helper method to publish any message to ROS"""
        ros_msg = String()
        ros_msg.data = message
        self.aws_to_ros_publisher.publish(ros_msg)
        self.get_logger().info(f'Published to ROS: "{message}"')

def start_bridge(aws_client=None):
    """Start the ROS-AWS bridge"""
    rclpy.init()
    bridge = ROSAWSBridge(aws_client)
    return bridge