import glob
import cv2
import time
from emailing import  send_email
import os
from threading import Thread

video=cv2.VideoCapture(0) #first camera for the video capturing.
#check,frame=video.read()  # check is true if camera is accesable., frame is the frame of the picture
#print(check)
#print(frame)
time.sleep(1)

first_frame = None

status_list=[]

count=1

def clean_folder():
    images=glob.glob("images/*.png")
    for image in images:
        os.remove(image)

while True:
    status=0
    check, frame = video.read()
    gray_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (11,11) ,0) #bak incele.

    if first_frame is None:
        first_frame=gray_frame_gau

    delta_frame = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame=cv2.threshold(delta_frame,60,255,cv2.THRESH_BINARY)[1]
    dil_frame=cv2.dilate(thresh_frame,None,iterations=2) # inceleyelim
    cv2.imshow("My video", thresh_frame)

    contours,check=cv2.findContours(dil_frame,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour)<5000:
            continue
        x , y , w , h=cv2.boundingRect(contour)
        rectangle=cv2.rectangle(frame , (x,y) , (x+w , y+h) , (0 , 255 ,0) ,3)
        if rectangle.any():
            status=1
    status_list.append(status) #if'in disarisinda, for'un icerisinde eklememiz gerekir.
    #contour oldugunda direk olarak for dongusunun icerisine giriyor.
    #status 1 oluyor.
    #contour olmadiginda for'dan cikiyor.
    #status 0 oluyor.
    #status'un 0'dan 1'e gectigi zaman, kadrajda hareket oldugunu bize gosterir.
    if len(status_list) >=2:
        status_list=status_list[-2:]

    #    if status_list[0] == 0 and status_list[1] == 1: #son 2 elemani
            #Obje kadraja girdiğinde bir obje var mesajı yolluyoruz.
            #send_email()
            #email_thread = Thread(target=send_email())
            #email_thread.daemon = True
            #clean_thread = Thread(target=clean_folder())
            #clean_thread.daemon = True

        if status_list[0] == 1 and status_list[1] == 0:
            #Objec kadrajdan ciktiginda objenin resmini mail olarak yolluyoruzç
            cv2.imwrite(f"images/{count}.png",frame)
            count += 1
            all_images=glob.glob("images/*.png")
            index=int(len(all_images)/2)
            images_to_send_path=all_images[index]
            #send_email(images_to_send_path) #Objenin image'i.
            email_thread=Thread(target=send_email,args=(images_to_send_path,))
            email_thread.daemon=True
            clean_thread = Thread(target=clean_folder)
            clean_thread.daemon = True
            email_thread.start()



    cv2.imshow("Video",frame)
    key = cv2.waitKey(1)  ## delay atiyor ve key bekletiyor.
    if key==ord("q"):
        break

clean_thread.start()
video.release()
