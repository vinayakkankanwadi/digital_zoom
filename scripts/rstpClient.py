import cv2
import numpy as np
import os

def zoom(frame, scale):
    # get original size of image
    (oh, ow) = frame.shape[:2]
    #############################
    # scale image
    #############################
    width = int(frame.shape[1] * scale)
    height = int(frame.shape[0] * scale)
    dims = (width,height)
    #return CV.resize(frame, dims, interpolation=CV.INTER_CUBIC)
    frame = cv2.resize(frame, dims, interpolation=cv2.INTER_CUBIC)
    ##########################
    # crop to the original size of the frame
    # measure from center, so we zoom on center
    # ch = center of current height
    # coh = center of original height
    ##########################
    (h, w) = frame.shape[:2]
    ch = int(h/2)
    cw = int(w/2)
    coh = int(oh/2)
    cow = int(ow/2)
    # NOTE: its img[y: y + h, x: x + w]
    return frame[ch-coh:ch+coh, cw-cow:cw+cow]

print(os.environ.get("OPENCV_FFMPEG_CAPTURE_OPTIONS"))
os.environ["OPENCV_FFMPEG_CAPTURE_OPTIONS"] = "rtsp_transport;udp"
print("Running RSTP Client")

#vcap = cv2.VideoCapture("rtsp://192.168.1.2:5554/camera", cv2.CAP_FFMPEG)
#cap = cv2.VideoCapture("rtsp://192.168.0.220:5540/", cv2.CAP_FFMPEG)
cap = cv2.VideoCapture("rtsp://192.168.13.95:8900/live", cv2.CAP_FFMPEG)

print(cap.isOpened())

# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video file")

# Read until video is completed
while (cap.isOpened()):

    # Capture frame-by-frame
    ret, frame = cap.read()
#    print(ret)
    if ret == True:
        # Display the resulting frame
        zoomframe = zoom(frame,4)
        Hori = np.concatenate((frame, zoomframe), axis=1)
        cv2.imshow('Frame', Hori)

        # Press Q on keyboard to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release
# the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()
