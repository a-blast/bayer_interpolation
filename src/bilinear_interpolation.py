from operator import mod
from functools import partial
import numpy as np
from functional import seq


# Add a second channel with associated RGB letter codes


## convolve the interpolation filter

def bilinearInterpolation(imageMatrix):
    height = len(imageMatrix)
    width = len(imageMatrix)
    numPixels = height * width


    # ID the color channel the pixel represents
    colorChanel = {
        (1,1) : "B",
        (1,0) : "G",
        (0,1) : "G",
        (0,0) : "R"
    }

    level = {
        "R" : 2,
        "G" : 1,
        "G1": 1,
        "G2": 1,
        "B" : 0
    }

    mod2CordsSum = lambda cords : sum(map(lambda x: mod(x,2), cords))
    interpolationFunct = (lambda cords, expectedSum: mod2CordsSum(cords) == expectedSum)

    # The sum of the %2 of the co-ordinates follow a specific pattern.
    interpolation = {
        "R" : {
            "G" : partial(interpolationFunct, expectedSum = 1),
            "B" : partial(interpolationFunct, expectedSum = 2)
        },
        "B" : {
            "G" : partial(interpolationFunct, expectedSum = 1),
            "R" : partial(interpolationFunct, expectedSum = 0)
        },
        "G": {
            "R" : partial(interpolationFunct, expectedSum = 0),
            "B" : partial(interpolationFunct, expectedSum = 2)
        }
    }


    colorImageMatrix = np.zeros((width,height,3),dtype="uint8")
    print(np.shape(colorImageMatrix))

    def setColorImg(cords, color, value):
        colorImageMatrix[cords[0],cords[1],level[color]] = value

    # Trim the last edge of pixels
    for x in range(1,width-1):
        for y in range(1,height-1):

            # get the letter code of color corresponding to the position
            channelLetter = colorChanel[(x%2,y%2)]

            # set the pixel intensity in the respective output pixel
            setColorImg((x,y),channelLetter,imageMatrix[(x,y)])

            # get surrounding local zone
            zone = {(x1,y1) for x1 in range(x-1,x+2) for y1 in range(y-1,y+2)} - {(x,y)}

            # Get the other colors in the neighborhood of the channelLetter pixel
            for color in interpolation[channelLetter]:
                # filter the surrounding zone for the correct color codes
                values = seq(zone)\
                    .filter(interpolation[channelLetter][color])\
                    .map(lambda cord : imageMatrix[cord[0],cord[1]])\
                    .to_list()

                # print("TEST")
                # # Take the mean of the filtered colors & set their value in their
                # # respective channel
                # print(x,y)
                # print(zone)
                # print(color)
                # print(channelLetter)
                meanValue = sum(values)//len(values)
                #print(meanValue,";",x,",",y,"::",color)
                setColorImg((x,y), color, meanValue)
            #print(imageMatrix[0:3,0:3])
            #print(colorImageMatrix)
            #exit()
    return colorImageMatrix







