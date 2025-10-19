from pythonosc import udp_client

controller = ""

curPedal = -2
pedalToJump = -2

scorePath = r'C:\\Users\\gudig\\Documents\\python\\guitarProjection\\toca_secao1.pdf'
scoreWindowWidth = 0
scoreWindowHeight = 0
scoreDoc = None
scoreNumPages = 0
scoreCurPage = 0

midiValues = None
outportMidi = None

l_pathways = []
selectedPathwayId = None
curSelectedPathwaysIds = []
resetingVerticaly = False

anchorPoint = None

projectingPoints = False
usingCooldown = False

l_spotlightPoints = []

d_spotlightTypeName = ["MD", "ME", "V"]

ip = "127.0.0.1"
port = 8000  
client = udp_client.SimpleUDPClient(ip, port)

cooldownTime = 100
lerpPosFrames = 4

changingBrightness = False
curBrightness = 0
targetBrightness = 0
brightnessStep = 0
brightnessCounter = 0
brightnessStepsTotal = 4.0

changingSize = False
curSize = 0
targetSize = 0
sizeStep = 0
sizeCounter = 0
sizeStepsTotal = 4.0

pickleLoaded = False

last0x = 0
last0y = 0

last1x = 0
last1y = 0