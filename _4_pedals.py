import pickle
import _3_gvars as gvars
import _1_funcs as funcs

def pedalNull():
    print("Pedal-Null")
    gvars.l_spotlightPoints[0].spotlightSwitch(False)
    gvars.l_spotlightPoints[1].spotlightSwitch(False)
    gvars.l_spotlightPoints[2].spotlightSwitch(False)

def pedalTest():
    print("Pedal-Test - load pathways")
    
    if gvars.pickleLoaded == False:
        with open('savedPathways.pkl', 'rb') as file:
            gvars.l_pathways = pickle.load(file)
            print("loaded pathways file--------------------")

            if len(gvars.l_pathways) > 0:
                gvars.selectedPathwayId = 0
        
        gvars.anchorPoint = gvars.l_pathways[0].l_points[0]
        gvars.pickleLoaded = True
    else:
        with open('savedPathways_reloadNoOverwrite.pkl', 'wb') as file:
                pickle.dump(gvars.l_pathways, file)
                print(gvars.l_pathways)
                print("saved pathways file--------------------")

    gvars.l_spotlightPoints[0].spotlightSwitch(True)
    gvars.l_spotlightPoints[1].spotlightSwitch(True)
    gvars.l_spotlightPoints[2].spotlightSwitch(True)

    gvars.l_spotlightPoints[0].setCurPathway(0)
    gvars.l_spotlightPoints[1].setCurPathway(0)
    gvars.l_spotlightPoints[2].setCurPathway(0)

def pedal0():
    print("Pedal 0")
    gvars.l_spotlightPoints[0].spotlightSwitch(False)
    gvars.l_spotlightPoints[1].spotlightSwitch(False)
    gvars.l_spotlightPoints[2].spotlightSwitch(False)

    gvars.l_spotlightPoints[0].setCurPathway(1)
    gvars.l_spotlightPoints[1].setCurPathway(None)
    gvars.l_spotlightPoints[2].setCurPathway(None)

def pedal1():
    print("Pedal 1")
    gvars.l_spotlightPoints[0].spotlightSwitch(True)
    gvars.l_spotlightPoints[1].spotlightSwitch(False)
    gvars.l_spotlightPoints[2].spotlightSwitch(False)
    
    gvars.l_spotlightPoints[0].setCurPathway(1)
    gvars.l_spotlightPoints[1].setCurPathway(0)
    gvars.l_spotlightPoints[2].setCurPathway(None)

def pedal2():
    print("Pedal 2")
    gvars.l_spotlightPoints[0].spotlightSwitch(True)
    gvars.l_spotlightPoints[1].spotlightSwitch(True)
    gvars.l_spotlightPoints[2].spotlightSwitch(False)
    
    gvars.l_spotlightPoints[0].setCurPathway(1)
    gvars.l_spotlightPoints[1].setCurPathway(0)
    gvars.l_spotlightPoints[2].setCurPathway(None)

def pedal3():
    print("Pedal 3")
    gvars.l_spotlightPoints[0].spotlightSwitch(True)
    gvars.l_spotlightPoints[1].spotlightSwitch(True)
    gvars.l_spotlightPoints[2].spotlightSwitch(False)

    gvars.l_pathways[2].movePathwayToCurSpotlightPos(gvars.l_spotlightPoints[0].getAbsolutePoint())
    gvars.l_spotlightPoints[0].setCurPathway(2)
    gvars.l_spotlightPoints[0].cooldownCounter = 0
    gvars.l_spotlightPoints[0].curPos = (1, 64)
    # x, y = gvars.l_spotlightPoints[0].curPos
    # gvars.l_spotlightPoints[0].curPos = (1, y)
    gvars.l_spotlightPoints[1].setCurPathway(0)
    gvars.l_spotlightPoints[2].setCurPathway(None)

def pedal4():
    print("Pedal 4")
    gvars.l_spotlightPoints[0].spotlightSwitch(True)
    gvars.l_spotlightPoints[1].spotlightSwitch(True)
    gvars.l_spotlightPoints[2].spotlightSwitch(False)
    
    gvars.l_spotlightPoints[0].setCurPathway(0)
    gvars.l_spotlightPoints[0].cooldownCounter = 0
    gvars.l_spotlightPoints[0].curPos = (10, 64)
    gvars.l_spotlightPoints[1].setCurPathway(0)
    gvars.l_spotlightPoints[2].setCurPathway(None)

# def pedal5():
#     print("Pedal 5")
#     gvars.l_spotlightPoints[0].spotlightSwitch(True)
#     gvars.l_spotlightPoints[1].spotlightSwitch(True)
#     gvars.l_spotlightPoints[2].spotlightSwitch(False)
    
#     gvars.l_spotlightPoints[0].setCurPathway(0)
#     gvars.l_spotlightPoints[1].setCurPathway(0)
#     gvars.l_spotlightPoints[2].setCurPathway(None)

# def pedal6():
#     print("Pedal 6")
#     gvars.l_spotlightPoints[0].spotlightSwitch(True)
#     gvars.l_spotlightPoints[1].spotlightSwitch(True)
#     gvars.l_spotlightPoints[2].spotlightSwitch(False)
    
#     gvars.l_spotlightPoints[0].setCurPathway(0)
#     gvars.l_spotlightPoints[1].setCurPathway(0)
#     gvars.l_spotlightPoints[2].setCurPathway(None)
    

# def pedal7():
#     print("Pedal 7")

#     gvars.l_spotlightPoints[0].spotlightSwitch(True)
#     gvars.l_spotlightPoints[1].spotlightSwitch(True)
#     gvars.l_spotlightPoints[2].spotlightSwitch(False)
    
#     gvars.l_spotlightPoints[0].setCurPathway(0)
#     gvars.l_spotlightPoints[1].setCurPathway(0)
#     gvars.l_spotlightPoints[2].setCurPathway(None)

# def pedal8():
#     print("Pedal 8")
#     gvars.l_spotlightPoints[0].spotlightSwitch(True)
#     gvars.l_spotlightPoints[1].spotlightSwitch(True)
#     gvars.l_spotlightPoints[2].spotlightSwitch(False)
    
#     gvars.l_spotlightPoints[0].setCurPathway(0)
#     gvars.l_spotlightPoints[1].setCurPathway(0)
#     gvars.l_spotlightPoints[2].setCurPathway(None)

def pedal9():
    print("Pedal 9")
    gvars.l_spotlightPoints[0].spotlightSwitch(True)
    gvars.l_spotlightPoints[1].spotlightSwitch(False)
    gvars.l_spotlightPoints[2].spotlightSwitch(False)

    gvars.l_spotlightPoints[0].setCurPathway(3)
    gvars.l_spotlightPoints[0].cooldownCounter = 0
    x, y = gvars.l_spotlightPoints[0].curPos
    gvars.l_spotlightPoints[0].curPos = (64, y)
    gvars.l_spotlightPoints[1].setCurPathway(None)
    gvars.l_spotlightPoints[2].setCurPathway(None)

def pedal10():
    print("Pedal 10")
    gvars.l_spotlightPoints[0].spotlightSwitch(True)
    gvars.l_spotlightPoints[1].spotlightSwitch(False)
    gvars.l_spotlightPoints[2].spotlightSwitch(False)

    gvars.l_pathways[4].movePathwayToCurSpotlightPos(gvars.l_spotlightPoints[0].getAbsolutePoint())
    gvars.l_spotlightPoints[0].setCurPathway(4)
    gvars.l_spotlightPoints[0].cooldownCounter = 0
    gvars.l_spotlightPoints[0].curPos = (127, 64)
    # x, y = gvars.l_spotlightPoints[0].curPos
    # gvars.l_spotlightPoints[0].curPos = (127, y)
    gvars.l_spotlightPoints[1].setCurPathway(None)
    gvars.l_spotlightPoints[2].setCurPathway(None)

def pedal10emeio():
    print("Pedal 10 e meio")
    gvars.l_spotlightPoints[0].spotlightSwitch(True)
    gvars.l_spotlightPoints[1].spotlightSwitch(False)
    gvars.l_spotlightPoints[2].spotlightSwitch(False)

    gvars.l_pathways[5].movePathwayToCurSpotlightPos(gvars.l_spotlightPoints[0].getAbsolutePoint())
    gvars.l_spotlightPoints[0].setCurPathway(5)
    gvars.l_spotlightPoints[0].cooldownCounter = 0
    gvars.l_spotlightPoints[0].curPos = (1, 64)
    # x, y = gvars.l_spotlightPoints[0].curPos
    # gvars.l_spotlightPoints[0].curPos = (1, y)
    gvars.l_spotlightPoints[1].setCurPathway(None)
    gvars.l_spotlightPoints[2].setCurPathway(None)

# def pedal11():
#     print("Pedal 11")

def pedal12():
    print("Pedal 12")
    gvars.l_spotlightPoints[0].spotlightSwitch(True)
    gvars.l_spotlightPoints[1].spotlightSwitch(False)
    gvars.l_spotlightPoints[2].spotlightSwitch(False)

    gvars.l_spotlightPoints[0].setCurPathway(6)
    x, y = gvars.l_spotlightPoints[0].curPos
    gvars.l_spotlightPoints[0].curPos = (1, y)
    gvars.l_spotlightPoints[1].setCurPathway(None)
    gvars.l_spotlightPoints[2].setCurPathway(None)

# def pedal13():
#     print("Pedal 13")
#     gvars.l_spotlightPoints[0].spotlightSwitch(True)
#     gvars.l_spotlightPoints[1].spotlightSwitch(False)
#     gvars.l_spotlightPoints[2].spotlightSwitch(False)

#     gvars.l_spotlightPoints[0].setCurPathway(6)
#     gvars.l_spotlightPoints[1].setCurPathway(None)
#     gvars.l_spotlightPoints[2].setCurPathway(None)

def pedal14():
    print("Pedal 14")
    gvars.l_spotlightPoints[0].spotlightSwitch(False)
    gvars.l_spotlightPoints[1].spotlightSwitch(False)
    gvars.l_spotlightPoints[2].spotlightSwitch(True)

    gvars.l_spotlightPoints[0].setCurPathway(None)
    gvars.l_spotlightPoints[1].setCurPathway(None)
    gvars.l_spotlightPoints[2].setCurPathway(7)

# def pedal15():
#     print("Pedal 15")
#     gvars.l_spotlightPoints[0].spotlightSwitch(False)
#     gvars.l_spotlightPoints[1].spotlightSwitch(False)
#     gvars.l_spotlightPoints[2].spotlightSwitch(True)

#     gvars.l_spotlightPoints[0].setCurPathway(None)
#     gvars.l_spotlightPoints[1].setCurPathway(None)
#     gvars.l_spotlightPoints[2].setCurPathway(7)
    
def pedal16():
    print("Pedal 16")
    gvars.l_spotlightPoints[0].spotlightSwitch(False)
    gvars.l_spotlightPoints[1].spotlightSwitch(False)
    gvars.l_spotlightPoints[2].spotlightSwitch(True)

    gvars.l_spotlightPoints[0].setCurPathway(None)
    gvars.l_spotlightPoints[1].setCurPathway(None)
    gvars.l_spotlightPoints[2].setCurPathway(8)
    
# def pedal17():
#     print("Pedal 17")
#     gvars.l_spotlightPoints[0].spotlightSwitch(False)
#     gvars.l_spotlightPoints[1].spotlightSwitch(False)
#     gvars.l_spotlightPoints[2].spotlightSwitch(True)

#     gvars.l_spotlightPoints[0].setCurPathway(None)
#     gvars.l_spotlightPoints[1].setCurPathway(None)
#     gvars.l_spotlightPoints[2].setCurPathway(8)

def default_case():
    print("pedal function doesnt exist")