from imageio import imread
import matplotlib.pyplot as plt
from PIL import Image

from bilinear_interpolation import bilinearInterpolation


img = imread("../img/onionBayer.png")
imgReg = imread("../img/onion.png")

plt.imshow(imgReg)
#plt.imshow(img[80:100,80:100])
plt.show()

out=bilinearInterpolation(img)
print(out)
out = Image.fromarray(out,'RGB')
out.show()
