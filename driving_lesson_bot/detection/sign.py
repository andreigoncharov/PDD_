import cv2 as cv
import os
from itertools import groupby

cur_directory = os.getcwd()

path = os.path.join(cur_directory, 'signs', 'Blue')
images = os.listdir(path)
print(len(images))
print(images)
print(images)

t_path = os.path.join(cur_directory, 't_signs')
t_images = os.listdir(t_path)
#t_images.pop(0)
test_img = cv.imread(t_path + '/' + t_images[0])
print(t_path + '/' + t_images[0])
try:
    hsv = cv.cvtColor(test_img, cv.COLOR_BGR2HSV)
    hsv = cv.blur(hsv, (5, 5))
    mask = cv.inRange(hsv, (89, 124, 73), (255, 255, 255))
    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=4)
except:
    pass

count = 0
count_list = []
errors_list = []
roImg = None
for img in images:
    try:
            image = cv.imread(path + '/' + img)
            #print(path + '/' + img)
            image = cv.resize(image, (64, 64))
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

                count = 0

                for i in range(64):
                    for j in range(64):
                        if roImg[i][j] == image[i][j]:
                            count += 1
                count_list.append(count)
    except:
        pass


print(count_list)
print(max(count_list))
index = count_list.index(max(count_list))
print("max_count_list :: ", index)
print("count_list_max :: ", count_list[index])
print("img_name :: ", images[index])

cv.destroyAllWindows()

'''
k = {'noDrive': noDrive_v,
     'pedesrians': pedestrians_v,
     'raf': raf_v}
maximum = max(k.keys(), key=lambda m: k[m])
print(k)
print(maximum)

for img in images:
        image = cv.imread(path + '/' + img)
        image = cv.resize(image, (30, 30))
        image = cv.inRange(image, (89, 91, 149), (255, 255, 255))
        cv.imshow(f"{img}", image)'''

'''
for img in images:
    try:
        image = Image.open(path + '/' + img)
        #image = image.resize((30, 30))
        #image = cv.inRange(image, (89, 91, 149), (255, 255, 255))
        #cv.imshow(f"{img}", image)
    except:
        print("Error loading image")

noDrive = cv.inRange(noDrive, (89, 91, 149), (255, 255, 255))
pedestrians = cv.inRange(pedestrians, (89, 91, 149), (255, 255, 255))

cv.imshow("noDrive", noDrive)
cv.imshow("pedestrians", pedestrians)'''

'''
while(True):

    ret, frame = cap.read()
    #cv.imshow("Frame", frame)
    frameCopy = frame.copy()

    hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    hsv = cv.blur(hsv, (5, 5))
    mask = cv.inRange(hsv, (89, 124, 73), (255, 255, 255))
    cv.imshow("Mask2", mask)

    mask = cv.erode(mask, None, iterations=2)
    mask = cv.dilate(mask, None, iterations=4)
    cv.imshow("Mask2", mask)

    contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    contours = contours
    if contours:
        contours = sorted(contours, key= cv.contourArea, reverse=True)
        cv.drawContours(frame, contours, 0, (255, 0, 255), 3)

        (x, y, w, h) = cv.boundingRect(contours[0])
        cv.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 3)
        cv.imshow("Rect", frame)

        roImg = frameCopy[y:y+h, x:x+w]
        cv.imshow("Detect", roImg)
        roImg = cv.resize(roImg, (64, 64))
        roImg = cv.inRange(roImg ,  (89, 124, 73), (255, 255, 255))
        cv.imshow("Resized", roImg)

        noDrive_v = 0
        pedestrians_v = 0

        for i in range(64):
            for j in range(64):
                if roImg[i][j] == noDrive[i][j]:
                    noDrive_v += 1
                if roImg[i][j] == pedestrians[i][j]:
                    pedestrians_v += 1

        print(noDrive_v, "   ^   ", pedestrians_v)

        if pedestrians_v > 3000:
            print("pedestrian")
        elif noDrive_v > 3000:
            print("noDrive")
        else:
            print("nothing")

    if cv.waitKey(1) == ord("q"):
        break

cap.release()
cv.destroyAllWindows()'''
