import tkinter as tk
from tkinter import filedialog
from tkinter import *
from PIL import ImageTk, Image
import numpy
#load the trained model to classify sign
from keras.models import load_model
import os

model = load_model('traffic_recognition.h5')
#dictionary to label all traffic signs class
classes = { 1:'Ограничение максимальной скорости',
    2:'Ограничение максимальной скорости',
    3:'Ограничение максимальной скорости',
    4:'Ограничение максимальной скорости',
    5:'Ограничение максимальной скорости',
    6:'Ограничение максимальной скорости',
    7:'Конец ограничения максимальной скорости',
    8:'Ограничение максимальной скорости',
    9:'Ограничение максимальной скорости',
    10:'Обгон запрещено',
    11:'Обгон грузовым машинам запрещено',
    12:'Перекресток с второстепенной дорогой',
    13:'Главная дорога',
    14:'Уступить дорогу',
    15:'Стоп',
    16:'Движение запрещено',
    17:'Движение грузовых машин запрещено',
    18:'Въезд запрещено',
    19:'Иная опасность (аварийно опасный  участок дороги)',
    20:'Опасный поворот налево',
    21:'Опасный поворот направо',
    22:'Несколько поворотов',
    23:'Выбоина',
    24:'Скользкая дорога',
    25:'Сужение дороги справа',
    26:'Дорожные работы',
    27:'Светофорное регулирование',
    28:'Пешеходный переход',
    29:'Дети',
    30:'Выезд велосипедистов',
    31:'Остерегайтесь льда / снега',
    32:'Дикие звери',
    33:'Конец всех ограничений и запретов',
    34:'Движение направо',
    35:'Движение налево',
    36:'Движение прямо',
    37:'Движение прямо и направо',
    38:'Движение прямо и  налево',
    39:'Объезд преграды справа',
    40:'Объезд преграды слева',
    41:'Круговое движение',
    42: 'Конец запрета обгона',
    43: 'Конец запрета обгона грузовым машинам'}
cur_directory = os.getcwd()
def classify(file):
  image = Image.open(file)
  image = image.resize((30, 30))
  image = numpy.expand_dims(image, axis=0)
  pred = model.predict_classes([image])[0]
  sign = classes[pred+1]
  print(sign)
  return sign



'''if __name__=="__main__":
  #initialise GUI
  top=tk.Tk()
  top.geometry('800x600')
  top.title('Traffic sign recognition')
  top.configure(bg='#f9f6f7')
  heading = Label(top, text="Traffic sign recognition",pady=20, font=('arial',20,'bold'))
  heading.configure(background='#f9f6f7',fg='#364156')
  heading.pack()
  result=Label(top, font=('arial',15,'bold'))
  result.configure(fg='#011638',bg='#f9f6f7')
  sign_image = Label(top)
  upload=Button(top,text="Upload an image",command=upload_image,padx=10,pady=5)
  upload.configure(background='#364156', fg='black',font=('arial',10,'bold'))
  upload.pack(side=BOTTOM,pady=50)
  sign_image.pack(side=BOTTOM,expand=True)
  result.pack(side=BOTTOM,expand=True)
  top.mainloop()'''
