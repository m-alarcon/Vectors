import numpy as np
import cv2

kernel=np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]], 'uint8')
signal=np.array([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]], 'uint8')

rows=signal.shape[0]-kernel.shape[0]+1
cols=signal.shape[1]-kernel.shape[1]+1
output=np.zeros((rows,cols), 'uint8')

kernel_reversed=np.rot90(np.rot90(kernel))

for i in range(0, output.shape[0]):
   for j in range(0, output.shape[1]):
        #desplazando el kernel
        signal_patch=signal[i:i+len(kernel),j:j+len(kernel)]   
        output[i][j]=(kernel_reversed*signal_patch).sum()

print (signal_patch)
print (output)