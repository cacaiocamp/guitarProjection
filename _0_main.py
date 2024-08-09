import cv2
import pickle
import fitz
import threading
import pyautogui
import _1_funcs as funcs
import _2_classes as classes
import _3_gvars as gvars

midi_name = 'WORLDE easy control 0'
gvars.midiValues = classes.MidiValuesStruct()

mdToProject = classes.SpotlightPoint(0)
meToProject = classes.SpotlightPoint(1)
vlToProject = classes.SpotlightPoint(2)
gvars.l_spotlightPoints.append(mdToProject)
gvars.l_spotlightPoints.append(meToProject)
gvars.l_spotlightPoints.append(vlToProject)

try:
    midi_thread = threading.Thread(target=funcs.midi_input_thread, args=(midi_name,))
    midi_thread.start()

    timingThread = threading.Thread(target=funcs.timingThread)
    timingThread.start()

    cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        raise Exception("Error: Camera not accessible.")
    
    cv2.namedWindow('clahe')
    cv2.setMouseCallback('clahe', funcs.addPathwayPoint)
    cv2.createTrackbar('curPedal', 'clahe', 0, 20, funcs.updatePedalToJump)

    screenWidth, screenHeight = pyautogui.size()
    gvars.scoreWindowWidth = int(screenWidth / 2.25)
    gvars.scoreWindowHeight = int(screenHeight - (screenHeight/20))
    gvars.scoreDoc = fitz.open(gvars.scorePath)
    gvars.scoreNumPages = gvars.scoreDoc.page_count

    cv2.namedWindow('score_view', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('score_view', gvars.scoreWindowWidth, gvars.scoreWindowHeight)

    while True:
        success, virginFrame = cap.read()
        flipped_frame = cv2.flip(virginFrame, 1)

        if not success:
            raise Exception("Error: Failed to read frame from camera.")
        
        frame = flipped_frame.copy()
        height, width = frame.shape[:2]
        
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        clahe_frame = clahe.apply(frame_gray)

        funcs.generateAndDrawSpotlightPoints(clahe_frame)

        cv2.putText(clahe_frame, str(gvars.selectedPathwayId), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 250, 250), 2, cv2.LINE_AA)
        cv2.putText(clahe_frame, "p: " + str(gvars.curPedal), (width - 110, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (250, 250, 250), 2, cv2.LINE_AA)
        cv2.putText(clahe_frame, "jump to: " + str(gvars.pedalToJump), (width - 110, height - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 250, 250), 1, cv2.LINE_AA)
        cv2.putText(clahe_frame, "curPathways: " + str(' '.join(map(str, gvars.curSelectedPathwaysIds))), (20, height - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (250, 250, 250), 1, cv2.LINE_AA)
        funcs.drawPathways(clahe_frame)
        cv2.imshow('clahe', clahe_frame)

        img = funcs.displayPage(gvars.scoreCurPage)
        cv2.imshow('score_view', img)

        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'): 
            break
        if key == ord('*'): 
            gvars.curPedal = gvars.curPedal + 1
            funcs.switchCasePedal(gvars.curPedal)
        if key == ord(' '):
            funcs.jumpToPedal(gvars.pedalToJump)
        if key == ord('w'): 
            gvars.l_spotlightPoints[0].spotlightSwitch(False)
            gvars.l_spotlightPoints[1].spotlightSwitch(False)
            gvars.l_spotlightPoints[2].spotlightSwitch(False)
        if key == ord('1'): 
            gvars.l_spotlightPoints[0].spotlightSwitch(not gvars.l_spotlightPoints[0].isProjecting)
        if key == ord('2'): 
            gvars.l_spotlightPoints[1].spotlightSwitch(not gvars.l_spotlightPoints[1].isProjecting)
        if key == ord('3'): 
            gvars.l_spotlightPoints[2].spotlightSwitch(not gvars.l_spotlightPoints[2].isProjecting)
        if key == ord('4'): 
            gvars.l_spotlightPoints[0].curPathway = gvars.l_pathways[gvars.selectedPathwayId]
            gvars.l_spotlightPoints[0].setBorderValues()
        if key == ord('5'): 
            gvars.l_spotlightPoints[1].curPathway = gvars.l_pathways[gvars.selectedPathwayId]
            gvars.l_spotlightPoints[1].setBorderValues()
        if key == ord('6'): 
            gvars.l_spotlightPoints[2].curPathway = gvars.l_pathways[gvars.selectedPathwayId]
            gvars.l_spotlightPoints[2].setBorderValues()
        elif key == ord('h'): 
            newPathway = None
            if len(gvars.l_pathways) == 0:
                newPathway = classes.Pathway(len(gvars.l_pathways), 0, 63, True)
            else:
                newPathway = classes.Pathway(len(gvars.l_pathways), 0, 63)
            gvars.l_pathways.append(newPathway)
            gvars.selectedPathwayId = len(gvars.l_pathways) - 1
        elif (key == ord('s')) | (key == ord('+')): # change selected Pathway +
            nextRoi = gvars.selectedPathwayId + 1
            if(nextRoi == len(gvars.l_pathways)):
                nextRoi = 0
            gvars.selectedPathwayId = nextRoi
        elif key == ord('-'): # change selected Roi -
            nextRoi = gvars.selectedPathwayId - 1
            if(nextRoi == -1):
                nextRoi = len(gvars.l_pathways) - 1
            gvars.selectedPathwayId = nextRoi
        elif key == ord('p'): # save pathways in pickle
            with open('savedPathways.pkl', 'wb') as file:
                pickle.dump(gvars.l_pathways, file)
                print(gvars.l_pathways)
                print("saved pathways file--------------------")
        elif key == ord('ç'): # load pathways from pickle
            with open('savedPathways.pkl', 'rb') as file:
                gvars.l_pathways = pickle.load(file)
                print("loaded pathways file--------------------")

                if len(gvars.l_pathways) > 0:
                    gvars.selectedPathwayId = 0
            
            gvars.anchorPoint = gvars.l_pathways[0].l_points[0]
            gvars.pickleLoaded = True
    
except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Release the video capture object
    if 'cap' in locals() and cap.isOpened():
        cap.release()
    
    # Close all OpenCV windows
    cv2.destroyAllWindows()
    midi_thread.join()
    timingThread.join()