import cv2
 
font = cv2.FONT_ITALIC
 

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "./haarcascade_frontalface_default.xml")  # 얼굴찾기 haar 파일
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "./haarcascade_eye.xml") # 눈찾기 haar 파일
 
cam = cv2.VideoCapture(0)

 
while True:
    ret, frame = cam.read()
    if ret is False:
        break
    
    roi = frame[0:500,0:500]
    rows, cols, _ = roi.shape
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)


    faces = face_cascade.detectMultiScale(gray_roi,1.3, 5)

    for(x,y, w,h) in faces:
        roi_gray = gray_roi[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0,255,0), 2)
 
 

    #gray_roi = cv2.GaussianBlur(gray_roi, (7, 7), 0)
    _, threshold = cv2.threshold(gray_roi, 25, 255, cv2.THRESH_BINARY_INV)
    contours, hierarchy = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=lambda x: cv2.contourArea(x), reverse=True)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        cv2.drawContours(roi, [cnt], -1, (0, 0, 255), 3)
        cv2.rectangle(roi, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.line(roi, (x + int(w/2), 0), (x + int(w/2), rows), (0, 255, 0), 2)
        cv2.line(roi, (0, y + int(h/2)), (cols, y + int(h/2)), (0, 255, 0), 2)
        break

    cv2.imshow("Threshold", threshold)
    cv2.imshow("gray roi", gray_roi)
    cv2.imshow("Roi", roi)
    key = cv2.waitKey(30)
    if key == 27:
        break
cv2.destroyAllWindows()
 
