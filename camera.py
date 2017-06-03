import cv2
import cv



class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(-1)
        self.video.set(cv.CV_CAP_PROP_FRAME_WIDTH, 600)
        self.video.set(cv.CV_CAP_PROP_FRAME_HEIGHT, 360)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        #cv2.imwrite("sv.jpg", image)
        image = cv2.flip(image, 1)
        
        ret, jpeg = cv2.imencode('.jpg', image)
        #return jpeg.tobytes()
        return jpeg.tostring()
