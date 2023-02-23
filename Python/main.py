from tkinter import *
from tkinter.ttk import *
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import serial 
import mediapipe as mp
from hand_module import HandDetector
import tkinter.scrolledtext as st
import time


handDetector = HandDetector()
window = Tk()
window.geometry('780x600')
window.title("APP")
window['background'] = 'white'
video = cv2.VideoCapture(0)

canvas_w = video.get(cv2.CAP_PROP_FRAME_WIDTH) 
canvas_h = video.get(cv2.CAP_PROP_FRAME_HEIGHT)
canvas = Canvas(window,width=canvas_w,height=canvas_h, bg = "white")
# canvas.place(x=400,y=400)
canvas.pack()


btHandRec= 0
btUart = 0 
def runHandRecognize():
    global btHandRec
    btHandRec = 1 - btHandRec #đảo lại biến bw
def runUART():
    global btUart 
    btUart = 1 - btUart
   
#BUTTON
buttonUart = Button(window,text = "Run UART",command=runUART)
buttonUart.pack()
buttonUart.place(x=20,y=500)
buttonHandRec= Button(window,text = "Run Hand Recognize",command=runHandRecognize)
buttonHandRec.pack()
buttonHandRec.place(x= 20,y=540)


#Label
lbHandRec = Label(window, text = "status")
lbHandRec.pack()
lbHandRec.place(x=150,y = 540)

lbUart = Label(window,text = "status")
lbUart.pack()
lbUart.place(x=150,y = 500)

# lbScrolledText = Label(window,text= "SEND DATA")
# lbScrolledText.pack()
# lbScrolledText.place(x=450,y=500)

# def scrolledText(text):
# text_area = st.ScrolledText(window,
#                             width = 10, 
#                             height = 5, 
#                             font = ("Times New Roman",
#                                     10))

# # text_area.grid(column = 0, pady = 10, padx = 10)
# text_area.pack(pady = 10, padx = 10)
# # text_area.insert(tkinter.INSERT, "Helloasdadasdaszxcxzcxzcasdaszxcxadasdasdasdasdasdzczxczczxcasdasd")
# text_area.place(x=550,y=500)
# text_area.configure(state ='disabled')


def HandRecViewRun():
    lbHandRec.config(text="RUNING")
    bar = Progressbar(window,length=200)
    bar['value']= 100
    bar.pack(pady=10)
    bar.place(x=220, y = 540)
def HandRecViewStop():
    lbHandRec.config(text="STOP")
    bar = Progressbar(window,length=200)
    bar['value']= 0
    bar.pack(pady=10)
    bar.place(x=220, y = 540)
    
def lbUARTViewRun():
    lbUart.config(text="RUNING")
    bar = Progressbar(window,length=200)
    bar['value']= 100
    bar.pack(pady=10)
    bar.place(x=220, y = 500)
def lbUARTViewStop():
    lbUart.config(text="STOP")
    bar = Progressbar(window,length=200)
    bar['value']= 0
    bar.pack(pady=10)
    bar.place(x=220, y = 500)
#Hiển thị Camera và xử lý ảnh
def main_exe():
    global canvas,photo 
    ret, img = video.read()
    img = cv2.resize(img,(640,480))
    print(btUart)
    if btUart == 1:
        #COM = "COM5" 
        COM = "COM11" 
        #COM = "COM9"
        #COM = "COM2"
        baudRate = 9600
        ser = serial.Serial(COM,baudRate, timeout = 1) 
        lbUARTViewRun()
    else:
        lbUARTViewStop()
    print(btHandRec)
    if btHandRec == 1:   
        img = handDetector.find_hands(img)
        HandRecViewRun()
        # processBarRunHandReg()
        land_mark_list = handDetector.find_position(img,draw=False)
        # print(land_mark_list)
        fingers_up = handDetector.fingers_up()
        # print(fingers_up)
        
        # a = ser.readline()
        # string_n = a.decode()
        #     #string_data = string_n.rstrip()
        # data_rec = string_n
        # print("--------------------------------")
        # print(data_rec)

        # print(data_rec)
        if fingers_up is not None:
            max_fingers_up_count = fingers_up.count(1)
            cv2.putText(img,f'Fingers up: {str(max_fingers_up_count)}',(100,100),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),2)
            #FOR SEND DATA
            if max_fingers_up_count == 1:
                ser.write(b'1 \r\n')
            elif max_fingers_up_count == 2:
                ser.write(b'2 \r\n')
            elif max_fingers_up_count == 3:
                ser.write(b'3 \r\n')   
            else: ser.write(b'0 \r\n')  
    else: 
        HandRecViewStop()
        # processBarRunHandReg()
    # img = cv2.resize(img, dsize=None,fx=0.5,fy=0.5)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(img))
    canvas.create_image(0,0, image = photo,anchor = tkinter.NW) 
    canvas.place(x=0,y=0)
    window.after(20,main_exe)
    

if __name__ == '__main__':    
    main_exe()
    window.mainloop()
        
