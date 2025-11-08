import cv2
import mido
import time
import numpy as np
import _3_gvars as gvars
import _4_pedals as pedals

def listCameras(max_tested=3):
    availableCameras = []
    for i in range(max_tested):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            availableCameras.append(i)
            cap.release()
    return availableCameras

def searchCameras():
    cameras = listCameras()
    if cameras:
        print("Available cameras:")
        for cam in cameras:
            print(f"  - Camera index {cam}")


def findPorts(controlName):
    inputs = mido.get_input_names()
    outputs = mido.get_output_names()
    in_port = next((n for n in inputs if controlName in n.upper()), None)
    out_port = next((n for n in outputs if controlName in n.upper()), None)
    return in_port, out_port

def searchPorts():
    print('MIDI inputs:')
    for n in mido.get_input_names():
        print('  ', n)
    print('MIDI outputs:')
    for n in mido.get_output_names():
        print('  ', n)

def timingThread():
    while True:
        for spotlight in gvars.l_spotlightPoints:
            if spotlight.cooldownCounter > -1:
                spotlight.cooldownCounter = spotlight.cooldownCounter + 1

                if spotlight.cooldownCounter == gvars.cooldownTime:
                    spotlight.cooldownCounter = -1

        time.sleep(0.01)

def lerpPosChangeThread():
    while True:
        for spotlight in gvars.l_spotlightPoints:
            if spotlight.lerpPosCounter > 0:
                spotlight.curPos = (spotlight.curPos[0] + spotlight.difToTargetX, spotlight.curPos[1] + spotlight.difToTargetY)
                spotlight.lerpPosCounter = spotlight.lerpPosCounter + 1

                #print("rh:", spotlight.curPos[0], " || lh:", spotlight.curPos[1], " || counter: ", spotlight.lerpPosCounter)

                if spotlight.lerpPosCounter > gvars.lerpPosFrames:
                    spotlight.lerpPosCounter = 0

        if gvars.changingBrightness:
            if gvars.brightnessCounter == 0:
                gvars.brightnessStep = float(gvars.targetBrightness - gvars.curBrightness) / gvars.brightnessStepsTotal
                gvars.brightnessCounter = 1
            elif gvars.brightnessCounter == gvars.brightnessStepsTotal:
                gvars.changingBrightness = False
                gvars.brightnessCounter = 0
            
            gvars.curBrightness = gvars.curBrightness + gvars.brightnessStep
            gvars.client.send_message("/rh/brightness", gvars.curBrightness)
            gvars.client.send_message("/lh/brightness", gvars.curBrightness)
            gvars.brightnessCounter = gvars.brightnessCounter + 1
        
        if gvars.changingSize:
            if gvars.sizeCounter == 0:
                gvars.sizeStep = float(gvars.targetSize - gvars.curSize) / gvars.sizeStepsTotal
                gvars.sizeCounter = 1
            elif gvars.sizeCounter == gvars.sizeStepsTotal:
                gvars.changingSize = False
                gvars.sizeCounter = 0
            
            gvars.curSize = gvars.curSize + gvars.sizeStep
            gvars.client.send_message("/rh/size", gvars.curSize)
            gvars.client.send_message("/lh/size", gvars.curSize)
            gvars.sizeCounter = gvars.sizeCounter + 1

        time.sleep(0.01666)  # approx 60 fps, following projection code fps

def midiOutput(controlCh, val):
    with mido.open_output(gvars.outportMidi) as outport:
        msg = mido.Message('control_change', channel=0, control=controlCh, value=val)
        #print('Sending:', msg)
        outport.send(msg)   

def midi_input_thread(port_name):
    with mido.open_input(port_name) as inport:
        for msg in inport:
            if msg.type == 'control_change':
                # print(f"Control change: {msg.control} with value {msg.value}")
                if gvars.controller == "WORLDE EASY CONTROL 0":
                    # MD-------------------------------------------------------------
                    if msg.control == 3:
                        gvars.midiValues.c3 = msg.value + 1
                        if len(gvars.l_spotlightPoints) != 0:
                            if (gvars.l_spotlightPoints[0].cooldownCounter == -1) | (gvars.usingCooldown == False):
                                x, y = gvars.l_spotlightPoints[0].curPos
                                x = gvars.midiValues.c3
                                gvars.l_spotlightPoints[0].curPos = (x, y)
                    elif msg.control == 14:
                        lastVal = gvars.midiValues.c14
                        gvars.midiValues.c14 = (msg.value + 1) - 63
                        if not gvars.resetingVerticaly:
                            if len(gvars.l_spotlightPoints) != 0:
                                x, y = gvars.l_spotlightPoints[0].curPos
                                verticalChange = y + ((lastVal - gvars.midiValues.c14) * - 1)
                                gvars.l_spotlightPoints[0].curPos = (x, verticalChange)
                    # ME-------------------------------------------------------------
                    elif msg.control == 4:
                        gvars.midiValues.c4 = msg.value + 1
                        if len(gvars.l_spotlightPoints) != 0:
                            if (gvars.l_spotlightPoints[1].cooldownCounter == -1) | (gvars.usingCooldown == False):
                                x, y = gvars.l_spotlightPoints[1].curPos
                                x = gvars.midiValues.c4
                                gvars.l_spotlightPoints[1].curPos = (x, y)
                    elif msg.control == 15:
                        gvars.midiValues.c15 = msg.value + 1
                        if len(gvars.l_spotlightPoints) != 0:
                            x, y = gvars.l_spotlightPoints[1].curPos
                            y = gvars.midiValues.c15
                            gvars.l_spotlightPoints[1].curPos = (x, y)
                    # # V-------------------------------------------------------------
                    elif msg.control == 5:
                        gvars.midiValues.c5 = msg.value + 1
                        if len(gvars.l_spotlightPoints) != 0:
                            if (gvars.l_spotlightPoints[2].cooldownCounter == -1) | (gvars.usingCooldown == False):
                                x, y = gvars.l_spotlightPoints[2].curPos
                                x = gvars.midiValues.c5
                                gvars.l_spotlightPoints[2].curPos = (x, y)
                    elif msg.control == 16:
                        gvars.midiValues.c16 = msg.value + 1
                        if len(gvars.l_spotlightPoints) != 0:
                            x, y = gvars.l_spotlightPoints[2].curPos
                            y = gvars.midiValues.c16
                            gvars.l_spotlightPoints[2].curPos = (x, y)
                    
                    # brightness - size - hands
                    elif msg.control == 7:
                        gvars.midiValues.c7 = msg.value
                        convertedVal = abs(float(msg.value/126) - 1)

                        gvars.client.send_message("/rh/brightness", convertedVal)
                        gvars.client.send_message("/lh/brightness", convertedVal)
                    elif msg.control == 18:
                        gvars.midiValues.c18 = msg.value
                        convertedVal = (msg.value + 1)/127

                        gvars.client.send_message("/rh/size", convertedVal)
                        gvars.client.send_message("/lh/size", convertedVal)
                    # Color
                    elif msg.control == 19:
                        if len(gvars.l_spotlightPoints) != 0:
                            convertedVal = float(msg.value/127)

                            gvars.client.send_message("/color/red", convertedVal)
                    elif msg.control == 20:
                        if len(gvars.l_spotlightPoints) != 0:
                            convertedVal = float(msg.value/127)
                            gvars.client.send_message("/color/green", convertedVal)
                    elif msg.control == 21:
                        if len(gvars.l_spotlightPoints) != 0:
                            convertedVal = float(msg.value/127)

                            gvars.client.send_message("/color/blue", convertedVal)

                    # rotate - move
                    elif msg.control == 12:
                        midVal = msg.value - 63
                        rotateAllPathways(midVal)
                        gvars.midiValues.c12 = midVal
                        updateSpotlightsBorderValues()
                    elif msg.control == 13:
                        midVal = msg.value - 63
                        moveAllPathways((midVal - gvars.midiValues.c13), 0)
                        gvars.midiValues.c13 = midVal
                        updateSpotlightsBorderValues()
                    elif msg.control == 22:
                        midVal = (msg.value - 63) * -1
                        moveAllPathways(0, (midVal - gvars.midiValues.c22))
                        gvars.midiValues.c22 = midVal
                        updateSpotlightsBorderValues()
                    # pass pages
                    elif msg.control == 35:
                        if (gvars.scoreCurPage < gvars.scoreNumPages - 1) & (msg.value == 127):
                            gvars.scoreCurPage = gvars.scoreCurPage + 1
                    elif msg.control == 34:
                        if (gvars.scoreCurPage > 0) & (msg.value == 127):
                            gvars.scoreCurPage = gvars.scoreCurPage - 1
                    elif msg.control == 33:
                        if msg.value == 127:
                            gvars.resetingVerticaly = True
                        else:
                            gvars.resetingVerticaly = False

                elif gvars.controller == "BEHRINGER XTOUCH COMPACT":
                    # MD-------------------------------------------------------------
                    if msg.control == 64:
                        gvars.midiValues.c64 = msg.value + 1
                        if len(gvars.l_spotlightPoints) != 0:
                            if (gvars.l_spotlightPoints[0].cooldownCounter == -1) | (gvars.usingCooldown == False):
                                x, y = gvars.l_spotlightPoints[0].curPos
                                x = gvars.midiValues.c64

                                gvars.l_spotlightPoints[0].calculateAndStartLerpCurPos(x, y)
                                #gvars.l_spotlightPoints[0].curPos = (x, y)
                    elif msg.control == 14:
                        lastVal = gvars.midiValues.c14
                        gvars.midiValues.c14 = (msg.value + 1) - 65
                        #gvars.midiValues.c14 = msg.value + 1
                        if not gvars.resetingVerticaly:
                            if len(gvars.l_spotlightPoints) != 0:
                                x, y = gvars.l_spotlightPoints[0].curPos
                                #y = gvars.midiValues.c14
                                verticalChange = y + ((lastVal - gvars.midiValues.c14) * - 1)
                                
                                #print(gvars.midiValues.c14, " || ", lastVal, " || ", verticalChange, " || ", y)
                                gvars.l_spotlightPoints[0].calculateAndStartLerpCurPos(x, verticalChange)
                                #gvars.l_spotlightPoints[0].curPos = (x, verticalChange)
                    # ME-------------------------------------------------------------
                    elif msg.control == 65:
                        gvars.midiValues.c65 = msg.value + 1
                        if len(gvars.l_spotlightPoints) != 0:
                            if (gvars.l_spotlightPoints[1].cooldownCounter == -1) | (gvars.usingCooldown == False):
                                x, y = gvars.l_spotlightPoints[1].curPos
                                x = gvars.midiValues.c65
                                gvars.l_spotlightPoints[1].calculateAndStartLerpCurPos(x, y)
                                #gvars.l_spotlightPoints[1].curPos = (x, y)
                    elif msg.control == 15:
                        gvars.midiValues.c15 = msg.value + 1
                        if len(gvars.l_spotlightPoints) != 0:
                            x, y = gvars.l_spotlightPoints[1].curPos
                            y = gvars.midiValues.c15
                            gvars.l_spotlightPoints[1].calculateAndStartLerpCurPos(x, y)
                            #gvars.l_spotlightPoints[1].curPos = (x, y)


                    # brightness - size - hands
                    elif msg.control == 18:
                        gvars.midiValues.c18 = msg.value
                        convertedVal = abs(float(msg.value/126) - 1)
                        #gvars.client.send_message("/rh/brightness", convertedVal)
                        #gvars.client.send_message("/lh/brightness", convertedVal)
                        gvars.targetBrightness = convertedVal
                        gvars.changingBrightness = True
                        gvars.brightnessCounter = 0
                    elif msg.control == 17:
                        gvars.midiValues.c17 = msg.value
                        convertedVal = (msg.value + 1)/127
                        #gvars.client.send_message("/rh/size", convertedVal)
                        #gvars.client.send_message("/lh/size", convertedVal)
                        gvars.targetSize = convertedVal
                        gvars.changingSize = True
                        gvars.sizeCounter = 0
                    # Color
                    elif msg.control == 81:
                        if len(gvars.l_spotlightPoints) != 0:
                            convertedVal = float(msg.value/126)
                            gvars.client.send_message("/color/red", convertedVal)
                    elif msg.control == 83:
                        if len(gvars.l_spotlightPoints) != 0:
                            convertedVal = float(msg.value/126)
                            gvars.client.send_message("/color/green", convertedVal)
                    elif msg.control == 85:
                        if len(gvars.l_spotlightPoints) != 0:
                            convertedVal = float(msg.value/126)
                            gvars.client.send_message("/color/blue", convertedVal)
                    # rotate - move
                    elif msg.control == 67:
                        midVal = msg.value - 63
                        rotateAllPathways(midVal)
                        gvars.midiValues.c67 = midVal
                        updateSpotlightsBorderValues()
                    elif msg.control == 66:
                        midVal = msg.value - 63
                        moveAllPathways((midVal - gvars.midiValues.c66), 0)
                        gvars.midiValues.c66 = midVal
                        updateSpotlightsBorderValues()
                    elif msg.control == 16:
                        midVal = (msg.value - 63) * -1
                        moveAllPathways(0, (midVal - gvars.midiValues.c16))
                        gvars.midiValues.c16 = midVal
                        updateSpotlightsBorderValues()
                    # pass pages
                    elif msg.control == 101:
                        if (gvars.scoreCurPage < gvars.scoreNumPages - 1) & (msg.value == 127):
                            gvars.scoreCurPage = gvars.scoreCurPage + 1
                    elif msg.control == 100:
                        if (gvars.scoreCurPage > 0) & (msg.value == 127):
                            gvars.scoreCurPage = gvars.scoreCurPage - 1
                    elif msg.control == 102:
                        if msg.value == 127:
                            gvars.resetingVerticaly = True
                        else:
                            gvars.resetingVerticaly = False


def displayPage(pageNumber):
    page = gvars.scoreDoc.load_page(pageNumber)
    pix = page.get_pixmap()
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)

    if pix.n == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR) 

    img = cv2.resize(img, (gvars.scoreWindowWidth, gvars.scoreWindowHeight))
    return img
                    
def updatePedalToJump(val):
    gvars.pedalToJump = val - 2

def addPathwayPoint(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if len(gvars.l_pathways) > 0:
            newPoint = (x, y)
            numPoints = len(gvars.l_pathways[gvars.selectedPathwayId].l_points)

            if (numPoints == 0) & (gvars.l_pathways[gvars.selectedPathwayId].isAnchorPathway):
                gvars.anchorPoint = newPoint
                gvars.l_pathways[gvars.selectedPathwayId].l_points.append(newPoint)
            else:
                if numPoints <= 1:
                    gvars.l_pathways[gvars.selectedPathwayId].l_points.append(newPoint)
                else:
                    gvars.l_pathways[gvars.selectedPathwayId].l_points[numPoints - 1] = newPoint

                gvars.l_pathways[gvars.selectedPathwayId].calculatePathwaySize()
            
            updateSpotlightsBorderValues()
    
    elif event == cv2.EVENT_RBUTTONDOWN:
        if len(gvars.l_pathways[gvars.selectedPathwayId].l_points) > 0:
            gvars.l_pathways[gvars.selectedPathwayId].l_points.pop()

def drawPathways(frameD):
    selectedPathwaysIds = []

    for spotlight in gvars.l_spotlightPoints:
        if spotlight.curPathway != None:
            selectedPathwaysIds.append(spotlight.curPathway.id)

    gvars.curSelectedPathwaysIds = selectedPathwaysIds

    for pathway in gvars.l_pathways:
        isSelected = False
        isCurPathway = False
        
        for selectedPathwayId in selectedPathwaysIds:
            if pathway.id == selectedPathwayId:
                isCurPathway = True

        if pathway.id == gvars.selectedPathwayId:
            isSelected = True

        
        pathway.drawPointsAndPath(frameD, isCurPathway, isSelected)

def mapMidiToRotation(midiVal):
    #midiValDiff = midiVal - gvars.midiValues.c12
    midiValDiff = midiVal - gvars.midiValues.c67
    degrees = midiValDiff * (90 / 126)
    return degrees

def rotateAllPathways(midiVal):
    degreesToRotate = mapMidiToRotation(midiVal)

    for indexPathway, pathway in enumerate(gvars.l_pathways):
        for indexPoint, point in enumerate(pathway.l_points):
            if (indexPathway != 0) | (indexPoint != 0):
                gvars.l_pathways[indexPathway].rotatePoint(indexPoint, degreesToRotate, gvars.anchorPoint)
    

def moveAllPathways(moveX = 0, moveY = 0):
    for indexPathway, pathway in enumerate(gvars.l_pathways):
        for indexPoint, point in enumerate(pathway.l_points):
            x, y = gvars.l_pathways[indexPathway].l_points[indexPoint]
            gvars.l_pathways[indexPathway].l_points[indexPoint] = (x + moveX, y + moveY)

def generateAndDrawSpotlightPoints(frameD):
    for spotlightPoint in gvars.l_spotlightPoints:
        if (spotlightPoint.curPathway is not None):
            if len(spotlightPoint.curPathway.l_points) > 1:
                pX, pY = spotlightPoint.draw(frameD)

                if spotlightPoint.isProjecting:
                    if spotlightPoint.type == 0:
                        gvars.client.send_message("/rh/pointX", pX)
                        gvars.client.send_message("/rh/pointY", pY)
                    if spotlightPoint.type == 1:
                        gvars.client.send_message("/lh/pointX", pX)
                        gvars.client.send_message("/lh/pointY", pY)
                    if spotlightPoint.type == 2:
                        gvars.client.send_message("/vl/pointX", pX)
                        gvars.client.send_message("/vl/pointY", pY)

def updateSpotlightsBorderValues():
    for spotlightPoint in gvars.l_spotlightPoints:
        if (spotlightPoint.curPathway is not None):
            spotlightPoint.setBorderValues()
    
def switchCasePedal(value):
    # switcher = {
    #     -2: pedals.pedalNull,
    #     -1: pedals.pedalTest,
    #     0: pedals.pedal0,
    #     1: pedals.pedal1,
    #     2: pedals.pedal2,
    #     3: pedals.pedal3,
    #     4: pedals.pedal4,
    #     5: pedals.pedal5,
    #     6: pedals.pedal6,
    #     7: pedals.pedal7,
    #     8: pedals.pedal8,
    #     9: pedals.pedal9,
    #     10: pedals.pedal10,
    #     11: pedals.pedal11,
    #     12: pedals.pedal12,
    #     13: pedals.pedal13,
    #     14: pedals.pedal14,
    #     15: pedals.pedal15,
    #     16: pedals.pedal16,
    #     17: pedals.pedal17,
    #     18: pedals.pedalNull
    # }
    switcher = {
        -2: pedals.pedalNull,
        -1: pedals.pedalTest,
        0: pedals.pedal0,
        1: pedals.pedal1,
        2: pedals.pedal2,
        3: pedals.pedal3,
        4: pedals.pedal4,
        5: pedals.pedal9,
        6: pedals.pedal10,
        7: pedals.pedal10emeio,
        8: pedals.pedal12,
        9: pedals.pedal14,
        10: pedals.pedal16,
        11: pedals.pedalNull
    }
    return switcher.get(value, pedals.default_case)()

def jumpToPedal(newPedal):    
    gvars.curPedal = newPedal
    switchCasePedal(newPedal)
