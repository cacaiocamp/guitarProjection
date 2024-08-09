import cv2
import numpy as np
import math
import _3_gvars as gvars

class Pathway:
    def __init__(self, id, type, sv = 63, isAnchorPathway = False):
        self.type = type # 0 horizontal, 1 vertical
        self.id = id
        self.l_points = []
        self.deviation = sv
        self.isAnchorPathway = isAnchorPathway

        self.hDistance = None
        self.vDistance = None
        self.hipotenusa = None

        self.l_pointsNoChange = []
    
    def calculatePathwaySize(self):
        if len(self.l_points) == 2:
            p1x, p1y = self.l_points[0]
            p2x, p2y = self.l_points[1]

            hDistance = abs(p1x - p2x)
            vDistance = abs(p1y - p2y)
            pathwaySize = math.sqrt(math.pow(hDistance, 2) + math.pow(vDistance, 2))

            self.hDistance = hDistance
            self.vDistance = vDistance
            self.hipotenusa = pathwaySize

            if (p2x < p1x) & (p2y < p1y):
                self.type = 0
            elif (p2x > p1x) & (p2y < p1y):
                self.type = 1
            elif (p2x > p1x) & (p2y > p1y):
                self.type = 2
            elif (p2x < p1x) & (p2y > p1y):
                self.type = 3

            self.l_pointsNoChange = self.l_points


    def drawPointsAndPath(self, frameD, isCurPathway = False, isSelected = False):
        thickness = 2
        color = (60, 60, 60)
        
        if isSelected:
            thickness = 5
            color = (160, 160, 160)
        elif isCurPathway:
            thickness = 3
            color = (230, 230, 230)

        for point in self.l_points:
            cv2.circle(frameD, point, 1, color, thickness)

        if len(self.l_points) > 1:
            cv2.polylines(frameD, [np.array(self.l_points)], False, color, thickness)

            x, y = self.l_points[0]
            cv2.putText(frameD, str(self.id), (x + 5, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (250, 250, 250), 1, cv2.LINE_AA)
    
    def rotatePoint(self, pointIndex, degrees, anchorPoint):
        px, py = self.l_points[pointIndex]
        ax, ay = anchorPoint

        radians = np.radians(degrees)
        cos_theta = np.cos(radians)
        sin_theta = np.sin(radians)

        # Translate point to anchor
        tx, ty = px - ax, py - ay
        
        # Rotate point
        new_x = tx * cos_theta - ty * sin_theta
        new_y = tx * sin_theta + ty * cos_theta
        
        # Translate point back
        self.l_points[pointIndex] = (int(new_x + ax), int(new_y + ay))

        return self.l_points[pointIndex]
    
    def movePathwayToCurSpotlightPos(self, curSpoitlightPoint, pathwayAnchorPoint = None):
        curSpotlightX, curSpotlightY =  curSpoitlightPoint
        
        if pathwayAnchorPoint == None: # point0 is the anchor for movement
            p0X, p0Y = self.l_pointsNoChange[0]
            p1X, p1Y = self.l_pointsNoChange[1]
            anchorPointDifferenceX = p0X - curSpotlightX
            anchorPointDifferenceY = p0Y - curSpotlightY

            self.l_points[0] = (p0X - anchorPointDifferenceX, p0Y - anchorPointDifferenceY)
            self.l_points[1] = (p1X - anchorPointDifferenceX, p1Y - anchorPointDifferenceY)

        self.calculatePathwaySize()




class SpotlightPoint:
    def __init__(self, type):
        self.type = type # 0 MD, 1 ME, 2 V
        self.curPathway = None
        self.curPos = (1, 64) # 1 - 127, inside PathwayBoundaries
        self.curBrightness = 0
        self.curSize = 0

        self.isProjecting = True

        self.pathwayXBorders = (0, 0)
        self.pathwayYBorders = (0, 0)

        self.cooldownCounter = -1 # se maior que -1, thread conta ate gvars.cooldownTimer pra liberar interface

    def setCurPathway(self, pathwayId):
        if pathwayId != None:
            self.curPathway = gvars.l_pathways[pathwayId]
        else:
            self.curPathway = None

        self.setBorderValues()

    def setBorderValues(self):
        if self.curPathway != None:
            x0, y0 = self.curPathway.l_points[0]
            x1, y1 = self.curPathway.l_points[1]

            if self.curPathway.type == 0:
                xBegin = x1
                xEnd = x0
                yBegin = y1
                yEnd = y0
            elif self.curPathway.type == 1:
                xBegin = x0
                xEnd = x1
                yBegin = y0
                yEnd = y1
            elif self.curPathway.type == 2:
                xBegin = x0
                xEnd = x1
                yBegin = y0
                yEnd = y1
            elif self.curPathway.type == 3:
                xBegin = x1
                xEnd = x0
                yBegin = y1
                yEnd = y0

            self.pathwayXBorders = (xBegin, xEnd)
            self.pathwayYBorders = (yBegin, yEnd)
    
        else:
            self.pathwayXBorders = (-100, -100)
            self.pathwayYBorders = (-100, -100)

    def getAbsolutePoint(self):
        curX, curY = self.curPos
        xMin, xMax = self.pathwayXBorders
        yMin, yMax = self.pathwayYBorders

        absX = (float(curX/127) * (xMax - xMin)) + xMin
        absY = (float(curX/127) * (yMax - yMin)) + yMin

        vDeviation = 0

        if self.curPathway != None:
            vDeviation = -1 * (float((curY - 64)/64) * (self.curPathway.deviation))

        return int(absX), int(absY + vDeviation) 

    def draw(self, frameD):
        pX, pY = self.getAbsolutePoint()

        color = (255, 255, 255)
        size = 0.5
        radius = 5
        if self.isProjecting is not True:
            color = (140, 140, 140)
            size = 0.4
            radius = 4

        cv2.circle(frameD, (pX, pY), radius, color, 4)
        cv2.putText(frameD, str(gvars.d_spotlightTypeName[self.type]), (pX - 10, pY - 10), cv2.FONT_HERSHEY_SIMPLEX, size, color, 1, cv2.LINE_AA)

        if self.cooldownCounter != -1:
            cv2.rectangle(frameD, (pX - 20, pY - 30), (pX + 20, pY + 20), color, 2)

        return pX, pY
    
    
    def spotlightSwitch(self, onoff):
        self.isProjecting = onoff

        if self.type == 0:
            gvars.client.send_message("/rh/isDrawing", int(self.isProjecting))
        elif self.type == 1:
            gvars.client.send_message("/lh/isDrawing", int(self.isProjecting))
        elif self.type == 2:
            gvars.client.send_message("/vl/isDrawing", int(self.isProjecting))

class MidiValuesStruct:
    def __init__(self):
        self.c7 = 0 # brightness maos
        self.c18 = 0 # tamanho manhos
        # MD
        self.c3 = 0 # mov no pathway
        self.c14 = 0 # cima-baixo
        # ME
        self.c4 = 0 # mov no pathway
        self.c15 = 0 # cima-baixo
        # V
        self.c5 = 0 # mov no pathway
        self.c16 = 0 # cima-baixo
        self.c8 = 0 # brightness
        self.c19 = 0 # tamanho

        # ----- mov geral
        self.c12 = 0 # rotaciona
        self.c13 = 0 # direita-esquerda
        self.c22 = 0 # cima-baixo