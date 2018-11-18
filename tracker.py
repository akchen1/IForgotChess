import cv2
import sys

FRAME_NAME = 'tracker'
WIDTH = 1920
HEIGHT = 1080


def tracker_factory(tracker_name):
    if tracker_name == 'KCF':
        tracker = cv2.TrackerKCF_create()
    elif tracker_name == 'MIL':
        tracker = cv2.TrackerMIL_create()
    elif tracker_name == 'BOOSTING':
        tracker = cv2.TrackerBoosting_create()
    else:
        raise RuntimeError(
            'tracker type {} not supported'.format(tracker_name))

    return tracker


# def retrieve_frame(cap, width, height):
#     ret, frame = cap.read()
#     if not ret:
#         return None

#     resized_img = cv2.resize(frame, (width, height))
#     return resized_img


if len(sys.argv) != 3:
    print('tracker.py <tracker name> <video path>')
    exit(1)

tracker_name = sys.argv[1].upper()
video_path = 'helicopter1.MOV'

# create tracker
mytracker = tracker_factory(tracker_name)


# create video stream
cap = cv2.VideoCapture(video_path)


if not cap.isOpened():
    print('Cannot open stream {}'.format(video_path))
    exit(1)

ret, frame = cap.read()
if not ret:
    print('cannot read video file')
    exit(1)

bbox = cv2.selectROI(frame, False)

# initialize my tracker
mytracker.init(frame, bbox)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # calculate the fps
    timer = cv2.getTickCount()

    tracker_status, bbox = mytracker.update(frame)

    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)

    if tracker_status:
        p1 = (int(bbox[0]), int(bbox[1]))
        p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
        cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
    else:
        cv2.putText(frame, "Tracking failure detected", (100, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)

    cv2.putText(frame, tracker_name + " Tracker", (100, 20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

    # display the image
    cv2.imshow(FRAME_NAME, frame)

    if (cv2.waitKey(1) & 0xFF) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()