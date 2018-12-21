#!/usr/bin/python
import socket, time import cv import cv2 import Image, StringIO
 
#capture = cv.CaptureFromCAM(0) cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_WIDTH, 320) 
#cv.SetCaptureProperty(capture, cv.CV_CAP_PROP_FRAME_HEIGHT, 240)
cap=cv2.VideoCapture(0) ret=cap.set(3,320) ret=cap.set(4,240)
 
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM) sock.bind(("0.0.0.0", 9996)) sock.listen(2)
 
dst, dst_addr = sock.accept() print "Destination Connected by", dst_addr
 
while True:
    #img = cv.QueryFrame(capture)
    ret, frame = cap.read()
    img=cv.fromarray(frame)
    pi = Image.fromstring("RGB", cv.GetSize(img), img.tostring())
    buf = StringIO.StringIO()
    pi.save(buf, format = "JPEG")
    jpeg = buf.getvalue()
    buf.close()
    transfer = jpeg.replace("\n", "\-n")
    #print len(transfer), transfer[-1]
   
    try:
        dst.sendall(transfer + "\n")
        time.sleep(0.04)
    except Exception as ex:
        dst, dst_addr = sock.accept()
        print "Destination Connected Again By", dst_addr
    except KeyboardInterrupt:
        print "Interrupted"
        break
 
 
dst.close()
sock.close()

