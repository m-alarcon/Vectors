from PIL import Image, ImageDraw
import numpy as np
import cv2
import math
import json

pixeles = 0
nombre_imagen = "Cuadrado"

im = Image.open("C:/Users/malarcon/Images/"+nombre_imagen+"/frame1.bmp")
(ancho, largo) = im.size
ancho_bloq = int(ancho/32)
print (ancho_bloq)