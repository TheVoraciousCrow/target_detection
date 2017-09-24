import numpy as np
import cv2
import argparse
import imutils
#parses the arguements provided in command line
#ap = argparse.ArgumentParser(description= "this is where the image/videa source is")
#ap.add_argument('-i', "--image", help = "path to the video feed")
#args = vars(ap.parse_args())
#sourceImage= cv2.imread(args["image"])

sourceImage = cv2.imread("RBY_Targets.jpg")
#convert pixel ratio to resize image
ratio = sourceImage.shape[0] / 300.0
orig = sourceImage.copy()
sourceImage = imutils.resize(sourceImage, height = 300)
edgesOnlyImage = cv2.Canny(sourceImage, 150,250)

#show image with edges only to test if it is working
cv2.imshow("edgish", edgesOnlyImage)
cv2.waitKey(0)

#create an array containing the three desired GBR color ranges: blue,yellow, red
colorBoundaries =[
                ([45, 0, 0], [145, 95, 55]),
                ([25, 160, 180], [95, 230, 255]),
                ([50, 50, 175], [125, 115, 250]),
                ]
#loop through the ranges
for (lowerBound, upperBound) in colorBoundaries:
    #openCV needs numpy arrays, cannot omit this
    lower = np.array(lowerBound, dtype = "uint8")
    upper = np.array(upperBound, dtype = "uint8")
    #turns pixels in range white, else black
    colorMask = cv2.inRange(sourceImage, lower, upper)

    #finds union of image and mask
    maskedSourceImage = cv2.bitwise_and(sourceImage, sourceImage, mask = colorMask)
    #blurs photo slightly to reduce false positives
    blurredMaskImage = cv2.bilateralFilter(maskedSourceImage, 11, 17, 17)
    edgyPhoto = cv2.Canny(blurredMaskImage, 100, 200)

    #now we will find the actual edges in the photo by looking for contours
    (_, contours, _) = cv2.findContours(edgyPhoto.copy(), cv2.RETR_TREE,
                        cv2.CHAIN_APPROX_SIMPLE)
    #contours = sorted(contours, key = cv2.contourArea, reverse = True)
    screenContour = None #initialize variable

    for cntr in contours:
        #creates an approximation of the contours
        peri = cv2.arcLength(cntr, True)
        approx = cv2.approxPolyDP(cntr, 0.01 * peri, True)
        #checks how many points in each contour, four points => rectangle
        if len(approx) >= 4 and len(approx) <= 6:
            (x, y, w, h) = cv2.boundingRect(approx)
            aspectRatio = w / float(h)

            #compute the solidity of the original contours
            area = cv2.contourArea(cntr)
            hullArea = cv2.contourArea(cv2.convexHull(cntr))
            solidity = area / float(hullArea)

            #check to see if the width, height, and solidity and aspect ratio
            #fall within the appropriate bounds
            keepDims = w > 25 and h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2

            #check to see if all the tests were passed
            if keepDims and keepSolidity and keepAspectRatio:
                #draw an outline around the target and update the status
                cv2.drawContours(blurredMaskImage, [approx], -1, (255, 255, 0), 4)
                status = "Target aquired"
                print(status)
            else:
                print("Not Aquired", keepDims, keepSolidity, keepAspectRatio)

    #show the filtered images
    cv2.imshow("images", np.hstack([sourceImage, blurredMaskImage]))
    #cv2.imshow("Aquired Target", maskedSourceImage)
    cv2.waitKey(0)
