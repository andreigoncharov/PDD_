import cv2
import os

def nothing(x):
    pass

#cap = cv2.VideoCapture(0)

cv2.namedWindow('result2')

cur_directory = os.getcwd()
t_path = os.path.join(cur_directory, 't_signs')
t_images = os.listdir(t_path)
print(t_images)
t_images.pop(0)
test_img = cv2.imread(t_path + '/' + t_images[0])

cv2.imshow('image', test_img)

cv2.createTrackbar('minb', 'result2', 0, 255, nothing)
cv2.createTrackbar('ming', 'result2', 0, 255, nothing)
cv2.createTrackbar('minr', 'result2', 0, 255, nothing)

cv2.createTrackbar('maxb', 'result2', 0, 255, nothing)
cv2.createTrackbar('maxg', 'result2', 0, 255, nothing)
cv2.createTrackbar('maxr', 'result2', 0, 255, nothing)

while(True):

    #ret, frame = cap.read()

    minb = cv2.getTrackbarPos('minb', 'result2')
    ming = cv2.getTrackbarPos('ming', 'result2')
    minr = cv2.getTrackbarPos('minr', 'result2')

    maxb = cv2.getTrackbarPos('maxb', 'result2')
    maxg = cv2.getTrackbarPos('maxg', 'result2')
    maxr = cv2.getTrackbarPos('maxr', 'result2')

    '''print(minb)
    print(ming)
    print(minr)
    print(maxb)
    print(maxg)
    print(maxr)'''

    #mask = cv2.inRange(frame, (minb, ming, minr), (maxb, maxg, maxr))
    mask2 = cv2.inRange(test_img, (minb, ming, minr), (maxb, maxg, maxr))

    #cv2.imshow('mask', mask)
    #result = cv2.bitwise_and(frame, frame, mask=mask)
    result2 = cv2.bitwise_and(test_img, test_img, mask=mask2)
    #cv2.imshow('result', result)
    cv2.imshow('result2', result2)


    if cv2.waitKey(1) == ord("q"):
        break

#cap.release()
cv2.destroyAllWindows()