import cv2
import imutils
import time
import argparse
from datetime import datetime

# Parse command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("--camera", type=str, default="webcam",
                help="Select 'webcam', 'picamera', or provide a path to a saved video.")
args = vars(ap.parse_args())

# Set camera resolution and frame rate
if args["camera"] == "webcam":
    camera_resolution = (320, 240)
    frame_rate = 16
elif args["camera"] == "picamera":
    camera_resolution = (640, 480)
    frame_rate = 16
else:
    # Check if provided path is valid
    try:
        video_path = args["camera"]
        cap = cv2.VideoCapture(video_path)
    except:
        print("Invalid video file path.")
        exit()
    # Get video properties and set resolution and frame rate
    frame_rate = int(cap.get(cv2.CAP_PROP_FPS))
    camera_resolution = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

# Initialize motion detection
avg_frame = None
motion_area_min = 500
frame_count = 0

# Main loop to capture and process frames
while True:
    # Capture frame from camera or video
    if args["camera"] == "webcam" or args["camera"] == "picamera":
        cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to the selected resolution
    frame = imutils.resize(frame, width=camera_resolution[0])

    # Convert frame to grayscale and blur it
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # If the average frame is None, initialize it
    if avg_frame is None:
        avg_frame = gray_frame.copy().astype("float")
        continue

    # Accumulate the weighted average between the current frame and previous frames
    cv2.accumulateWeighted(gray_frame, avg_frame, 0.5)

    # Compute the absolute difference between the current frame and running average frame
    frame_delta = cv2.absdiff(gray_frame, cv2.convertScaleAbs(avg_frame))

    # Threshold the delta image to detect motion
    _, thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)

    # Find contours of the motion regions
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)

    # Iterate through contours to check for motion
    for contour in contours:
        if cv2.contourArea(contour) < motion_area_min:
            continue

        # Save the first frame with motion to disk
        if frame_count == 0:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f"jc_{timestamp}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Saved {filename} with motion detected.")
            frame_count += 1
            break

    # Show the frame with motion contours for debugging (optional)
    # cv
cap.stop() if args.get("video", None) is None else cap.release()
cv2.destroyAllWindows()
