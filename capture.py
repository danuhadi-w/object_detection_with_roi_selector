import cv2
import dxcam


# from PIL import Image


class Capture:
    img = None
    img_prev = None
    img_to_find = None
    x, y, w, h = None, None, None, None
    x_crop, y_crop, w_crop, h_crop = None, None, None, None

    cam = dxcam.create(output_color="BGR")

    def __init__(self, winname):
        self.winname = winname

    def select_roi(self):
        winname = "Select Area"
        first_capture = self.cam.grab()
        print(first_capture.shape)
        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(winname, 1280, 720)

        self.x, self.y, self.w, self.h = cv2.selectROI(winname, img=first_capture)

        if self.w == 0:
            exit()

        cv2.destroyWindow(winname)

    def select_target_img(self):
        winname = "Select Target"
        first_capture = self.cam.grab()

        cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(winname, 1280, 720)

        self.x_crop, self.y_crop, self.w_crop, self.h_crop = cv2.selectROI(winname, img=first_capture)

        if self.w_crop == 0:
            exit()

        cv2.destroyWindow(winname)
        self.img_to_find = first_capture[self.y_crop:self.y_crop + self.h_crop, self.x_crop:self.x_crop + self.w_crop]
        self.img_to_find = cv2.cvtColor(self.img_to_find, cv2.COLOR_BGR2GRAY)
        # Image.fromarray(self.img_to_find).show()

    def on_break_loop(self):
        self.cam.stop()
        cv2.destroyAllWindows()

    def detect(self):

        self.img = self.cam.grab(region=(self.x, self.y, self.x + self.w, self.y + self.h))
        if self.img is not None:
            self.img_prev = self.img.copy()
        elif self.img is None:
            self.img = self.img_prev

        img_grey = cv2.cvtColor(self.img.copy(), cv2.COLOR_BGR2GRAY)

        matching_result = cv2.matchTemplate(img_grey, self.img_to_find, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matching_result)

        if max_val < 0.8 * 1:
            # detection_result = self.img
            return None
        else:
            # detection_result = cv2.rectangle(self.img, max_loc, (max_loc[0] + self.w_crop, max_loc[1] + self.h_crop),
            #                                  (0, 255, 0), 3)
            detected_pos = (self.x + max_loc[0] + self.w_crop // 2, self.y + max_loc[1] + self.h_crop // 2)

            return detected_pos

        # cv2.namedWindow(self.winname)
        # cv2.moveWindow(self.winname, 0, 0)
        # cv2.resizeWindow(self.winname, 320, 320)
        # cv2.imshow(self.winname, detection_result)
