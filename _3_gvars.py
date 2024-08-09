from pythonosc import udp_client

curPedal = -2
pedalToJump = -2

scorePath = r'C:\\Users\\gudig\\OneDrive\\Documentos\\python\\guitarProjection\\toca_secao1.pdf'
scoreWindowWidth = 0
scoreWindowHeight = 0
scoreDoc = None
scoreNumPages = 0
scoreCurPage = 0

midiValues = None

l_pathways = []
selectedPathwayId = None
curSelectedPathwaysIds = []
resetingVerticaly = False

anchorPoint = None

projectingPoints = False

l_spotlightPoints = []

d_spotlightTypeName = ["MD", "ME", "V"]

ip = "127.0.0.1"
port = 8000  
client = udp_client.SimpleUDPClient(ip, port)

cooldownTime = 100

pickleLoaded = False

last0x = 0
last0y = 0

last1x = 0
last1y = 0