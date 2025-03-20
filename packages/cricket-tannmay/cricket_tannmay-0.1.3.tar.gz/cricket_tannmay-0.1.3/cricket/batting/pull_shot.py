import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose


# Function to calculate the angle between three points
def calculate_angle(a, b, c):
    a = np.array(a)  # First point
    b = np.array(b)  # Midpoint
    c = np.array(c)  # Last point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360.0 - angle

    return angle


# Function to classify frame based on pull shot logic
def classify_frame(landmarks):
    # Extracting key points: Shoulder, Elbow, Wrist for both arms
    left_shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER].y]
    left_elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_ELBOW].y]
    left_wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST].x,
                  landmarks[mp_pose.PoseLandmark.LEFT_WRIST].y]

    right_shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].x,
                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER].y]
    right_elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW].y]
    right_wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].x,
                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST].y]

    # Calculate arm angles
    left_arm_angle = calculate_angle(left_shoulder, left_elbow, left_wrist)
    right_arm_angle = calculate_angle(right_shoulder, right_elbow, right_wrist)

    # Check torso rotation using shoulder movement
    left_hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP].x, landmarks[mp_pose.PoseLandmark.LEFT_HIP].y]
    right_hip = [landmarks[mp_pose.PoseLandmark.RIGHT_HIP].x, landmarks[mp_pose.PoseLandmark.RIGHT_HIP].y]
    torso_rotation_angle = calculate_angle(left_shoulder, left_hip, right_hip)

    # Pull shot logic:
    if 80 <= left_arm_angle <= 130 or 80 <= right_arm_angle <= 130:
        if 30 <= torso_rotation_angle <= 60:
            return "Good Pull Shot"
        else:
            return "Bad Pull Shot"
    else:
        return "Not a Pull Shot"


# Analyze video to classify frames
def analyze_video(video_path):
    analysis = {}
    cap = cv2.VideoCapture(video_path)
    pose = mp_pose.Pose()
    frame_idx = 0

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)

            if results.pose_landmarks:
                shot_classification = classify_frame(results.pose_landmarks.landmark)
                analysis[frame_idx] = shot_classification

            frame_idx += 1

    finally:
        cap.release()

    return analysis


# Classify the entire video based on frame results
def classify_entire_video(video_path):
    analysis = analyze_video(video_path)

    # Count occurrences of each classification
    good_pull_count = sum(1 for v in analysis.values() if v == "Good Pull Shot")
    bad_pull_count = sum(1 for v in analysis.values() if v == "Bad Pull Shot")
    not_pull_count = sum(1 for v in analysis.values() if v == "Not a Pull Shot")

    total_frames = len(analysis)

    # Final classification logic
    if total_frames == 0:
        return "No Valid Frames Detected"

    if good_pull_count / total_frames >= 0.5:
        return "Good Pull Shot"
    elif bad_pull_count / total_frames >= 0.5:
        return "Bad Pull Shot"
    else:
        return "Not a Pull Shot"
