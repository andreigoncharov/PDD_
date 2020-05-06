import cv2 as cv
import os
import operator

cur_directory = os.getcwd()

path = os.path.join(cur_directory, 'signs', 'Blue')
images = os.listdir(path)
images.pop(0)

t_path = os.path.join(cur_directory, 't_signs')
t_images = os.listdir(t_path)
t_images.pop(0)
test_img = cv.imread(t_path + '/' + t_images[0])

hsv = cv.cvtColor(test_img, cv.COLOR_BGR2HSV)
hsv = cv.blur(hsv, (5, 5))
mask = cv.inRange(hsv, (89, 124, 73), (255, 255, 255))
mask = cv.erode(mask, None, iterations=2)
mask = cv.dilate(mask, None, iterations=4)

pedestrians = cv.imread("pedestrians.png")


pedestrians = cv.resize(pedestrians, (64, 64))


pedestrians = cv.inRange(pedestrians, (89, 91, 149), (255, 255, 255))


cv.imshow("pedestrians", pedestrians)

noDrive_v = 0
pedestrians_v = 0
raf_v = 0

for img in images:
            image = cv.imread(path + '/' + img)
            image = cv.resize(image, (30, 30))
            image = cv.inRange(image, (89, 91, 149), (255, 255, 255))
            #cv.imshow(f"{img}", image)

            contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
            contours = contours
            if contours:
                contours = sorted(contours, key=cv.contourArea, reverse=True)
                cv.drawContours(test_img, contours, 0, (255, 0, 255), 3)

                (x, y, w, h) = cv.boundingRect(contours[0])
                cv.rectangle(test_img, (x, y), (x + w, y + h), (0, 255, 0), 3)
                cv.imshow("Rect", test_img)

                roImg = test_img[y:y + h, x:x + w]
                cv.imshow("Detect", roImg)
                roImg = cv.resize(roImg, (64, 64))
                roImg = cv.inRange(roImg, (89, 124, 73), (255, 255, 255))
                cv.imshow("Resized", roImg)

                noDrive_v = 0
                pedestrians_v = 0
                raf_v = 0

                for i in range(64):
                    for j in range(64):
                        if roImg[i][j] == pedestrians[i][j]:
                            pedestrians_v += 1


                print(noDrive_v, "   ^   ", pedestrians_v, "   ^   ", raf_v)

k = {'noDrive': noDrive_v,
     'pedesrians': pedestrians_v,
     'raf': raf_v}
maximum = max(k.keys(), key=lambda m: k[m])
print(k)
print(maximum)

cv.destroyAllWindows()