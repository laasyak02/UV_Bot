#!/usr/bin/env python

import rospy
from apriltag_ros.msg import AprilTagDetectionArray
from cartographer_ros_msgs.msg import LandmarkList, LandmarkEntry
def callback(apriltag_msg):
	try:
		landmark_msg = LandmarkList()
		landmark_msg.header = apriltag_msg.header
		for i in range(len(apriltag_msg.detections)):
			landmark_entry_msg = LandmarkEntry()
			landmark_entry_msg.id = str(apriltag_msg.detections[i].id[0])
			landmark_entry_msg.tracking_from_landmark_transform = apriltag_msg.detections[i].pose.pose.pose
			landmark_entry_msg.translation_weight = 1.0
			landmark_entry_msg.rotation_weight = 1.0
			landmark_msg.landmarks.append(landmark_entry_msg)
		pub.publish(landmark_msg)
		#print(landmark_msg)
		#print("*"*80)
	except Exception as e:
		print(e)

if __name__ == '__main__':
	rospy.init_node('custom_landmark_publish_node', anonymous=False)
	namespace = rospy.get_param('~namespace','')
	pub = rospy.Publisher('{}/landmark'.format(namespace), LandmarkList, queue_size=1)
	rospy.Subscriber("{}/tag_detections".format(namespace), AprilTagDetectionArray, callback, queue_size=1)
	rospy.spin()
