import numpy as np
import cv2
import argparse
import imutils
#parses the arguements provided in command line
#ap = argparse.ArgumentParser(description= "this is where the image/videa source is")
#ap.add_argument('-i', "--image", help = "path to the video feed")
#args = vars(ap.parse_args())

    #sourcePixel= cv2.imread(args["image"])
sourcePixel = cv2.imread("RBY_targets.jpg")
#convert pixel ratio to resize image
ratio = sourcePixel.shape[0] / 300.0
orig = sourcePixel.copy()
sourcePixel = imutils.resize(sourcePixel, height = 300)
gray = cv2.cvtColor(sourcePixel, cv2.COLOR_BGR2GRAY)
edge = cv2.Canny(sourcePixel, 100,200)

#show image with edges only to test if it is working
cv2.imshow("edgish", edge)
cv2.waitKey(0)

#create an array containing the three desired color ranges
boundaries =[
                ([17, 15, 100], [50, 56, 200]),
                ([86, 31, 4], [220, 88, 50]),
                ([25, 146, 190], [62, 174, 250]),
                ]
    #loop through the ranges
for (lower, upper) in boundaries:
        #openCV needs numpy arrays, cannot omit this
    lower = np.array(lower, dtype = "uint8")
    upper = np.array(upper, dtype = "uint8")
        #turns pixels in range white, else blaxk
    colorMask = cv2.inRange(sourcePixel, lower, upper)

        #finds union of image and mask
    outputArray = cv2.bitwise_and(sourcePixel, sourcePixel, mask = colorMask)
    blurredOutputArray = cv2.bilateralFilter(outputArray, 11, 17, 17)
    edgyPhoto = cv2.Canny(blurredOutputArray, 100, 200)

    #now we will find the actual edges in the photo
    (_, contours, _) = cv2.findContours(edgyPhoto.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse = True)
    screenContour = None #initialize variable

    for cntr in contours:
            #creates a n approximation of the contours
        peri = cv2.arcLength(cntr, True)
        approx = cv2.approxPolyDP(cntr, 0.01 * peri, True)
            #checks how many points in each contour, four points => square
        if len(approx) >= 4 and len(approx) <= 6:
            (x, y, w, h) = cv2.boundRect(approx)
            aspectRatio = w / float(h)

            #compute the solidity of the original contours
            area = cv2.contourArea(cntr)
            hullArea = cv2.contourArea(cv2.convexHull(cntr))
            solidity = area / float(hullArea)

            #check to see if the width, height, and solidity and aspect ratio
            #fall within the appropriate bounds
            keepDims = w> 225 adn h > 25
            keepSolidity = solidity > 0.9
            keepAspectRatio = aspectRatio >= 0.8 and aspectRatio <= 1.2

            #check to see if all the tests were passed
            if keepDims and keepSolidity and keepaspectRa:
                #draw an outline around the target and update the status

    cv2.drawContours(blurredOutputArray, [screenContour], -1, (255,255,255), 5)




    #draws rectangle on specified points
    cv2.rectangle(edgyPhoto, (115,120), (170, 150), (0,255,0), 5) #image,top left, top right, color(b,g,r), thickness
    cv2.putText(edgyPhoto, "Tarp #{}".format("3"), (130,130), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255,255,0), 1)
    # show the images
    #cv2.imshow("images", np.hstack([sourcePixel, blurredOutputArray]))
    cv2.imshow("edgy", edgyPhoto)
    cv2.waitKey(0)
