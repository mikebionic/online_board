import cv2
import rect
import numpy as np

class Scanner(object):
    # http://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
    def four_point_transform(self, image, rect):
    	# obtain a consistent order of the points and unpack them
        # individually
        (tl, tr, br, bl) = rect
    
        # compute the width of the new image, which will be the
        # maximum distance between bottom-right and bottom-left
        # x-coordiates or the top-right and top-left x-coordinates
        widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
        widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))
    
        # compute the height of the new image, which will be the
        # maximum distance between the top-right and bottom-right
        # y-coordinates or the top-left and bottom-left y-coordinates
        heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
        heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))
    
        # now that we have the dimensions of the new image, construct
        # the set of destination points to obtain a "birds eye view",
        # (i.e. top-down view) of the image, again specifying points
        # in the top-left, top-right, bottom-right, and bottom-left
        # order
        dst = np.array([
            [0, 0],
            [maxWidth - 1, 0],
            [maxWidth - 1, maxHeight - 1],
            [0, maxHeight - 1]], dtype = "float32")
    
        # compute the perspective transform matrix and then apply it
        M = cv2.getPerspectiveTransform(rect, dst)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
        # return the warped image
        return warped

    # https://github.com/vipul-sharma20/document-scanner
    def detect_edge(self, image, enabled_transform = False):
        dst = None
        orig = image.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 0, 20)
        _, contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

        contours = sorted(contours, key=cv2.contourArea, reverse=True)

        for cnt in contours:
            epsilon = 0.051 * cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, epsilon, True)

            if len(approx) == 4:
                target = approx
                cv2.drawContours(image, [target], -1, (0, 255, 0), 2)

                if enabled_transform:
                    approx = rect.rectify(target)
                    # pts2 = np.float32([[0,0],[800,0],[800,800],[0,800]])
                    # M = cv2.getPerspectiveTransform(approx,pts2)
                    # dst = cv2.warpPerspective(orig,M,(800,800))
                    dst = self.four_point_transform(orig, approx)
                break

        return image, dst



