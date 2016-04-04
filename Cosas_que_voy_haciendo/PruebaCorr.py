from PIL import Image, ImageDraw
import numpy as np
import cv2
import math
import json

#Imagen a comparar (L)
im = Image.open("C:/Users/malarcon/Desktop/Alcatel/Fondo2.jpg")
im = im.convert('L')
g_i = np.array(im)

#Imagen donde compararla (R)
im2 = Image.open("C:/Users/malarcon/Desktop/Alcatel/Fondo2_invert.jpg")
im2 = im2.convert('L')
g_h = np.array(im2)

media_i = g_i.sum()/((g_i.shape[0])*(g_i.shape[1]))
media_h = g_h.sum()/((g_h.shape[0])*(g_h.shape[1]))

sigma_i = math.sqrt((pow((g_i-media_i),2).sum())/((g_i.shape[0])*(g_i.shape[1])))
sigma_h = math.sqrt((pow((g_h-media_h),2).sum())/((g_h.shape[0])*(g_h.shape[1])))

sigma_ih = ((g_i-media_i)*(g_h-media_h)).sum()/((g_h.shape[0])*(g_h.shape[1]))

if sigma_ih == 0:
	corr = 1
else:
	corr = sigma_ih/(sigma_i*sigma_h)



datosJSON = np.zeros((4,2,2), 'float')
ldatosJSON = datosJSON.tolist()
vectores=open('vectores.txt','w')
json.dump(ldatosJSON, vectores)
vectores.close()
print (corr)