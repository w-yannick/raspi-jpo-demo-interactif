from PIL import Image
import numpy as np
import PySimpleGUI as sg; font_size=6; USING_QT=False
import cv2


# The magic bits that make the ASCII stuff work shamelessly taken from https://gist.github.com/cdiener/10491632
chars = np.asarray(list(' .,:;irsXA253hMHGS#9B&@'))
SC, GCF, WCF = .1, 1, 7/4

sg.ChangeLookAndFeel('Black')   # make it look cool

# define the window layout
NUM_LINES = 48  # number of lines of text elements. Depends on cameras image size and the variable SC (scaller)
layout =  [[sg.T(i,size=(120,1), font=('Courier', font_size), pad=(0,0), key='_OUT_'+str(i))] for i in range(NUM_LINES)]

layout += [[ sg.Button('Exit', size=(5,1))]]

window = sg.Window('OpenCV Integration', layout, location=(600,200), font='Any 18')

cap = cv2.VideoCapture(0)       
while True:
    event, values = window.Read(timeout=0)
    if event in ('Exit', None):
        break
    ret, frame = cap.read()                         

    img = Image.fromarray(frame) 
    # More magic that coverts the image to ascii
    S = (round(img.size[0] * SC * WCF), round(img.size[1] * SC))
    img = np.sum(np.asarray(img.resize(S)), axis=2)
    img -= img.min()
    img = (1.0 - img / img.max()) ** GCF * (chars.size - 1)

    # "Draw" the image in the window, one line of text at a time
    for i, r in enumerate(chars[img.astype(int)]):
        window.Element('_OUT_'+str(i)).Update("".join(r))
window.Close()
