import oscP5.*;
import netP5.*;
import spout.*;

OscP5 oscP5;
Spout spout;

int pointX = -1;
int pointY = -1;
int spotlightSize = 80;
boolean drawing = false;

ItemToTrack[] vecItensToTrack = new ItemToTrack[3];
int[] spotlightRadiusSize = new int[3];

void setup() {
  size(640, 480, P3D);
  
  oscP5 = new OscP5(this, 8000);
  spout = new Spout(this);
  
  spout.setSenderName("Spout Processing Sender");
  
  spotlightRadiusSize[0] = spotlightSize;
  spotlightRadiusSize[1] = spotlightSize;
  spotlightRadiusSize[2] = spotlightSize;
  
  // prerender spotlights
  for(int index = 0; index < vecItensToTrack.length; index++){
    vecItensToTrack[index] = new ItemToTrack();
    vecItensToTrack[index].spotlightRadius = spotlightRadiusSize[index];
    vecItensToTrack[index].size = new PVector(vecItensToTrack[index].spotlightRadius*3, vecItensToTrack[index].spotlightRadius*3);
    vecItensToTrack[index].spotlight = createGraphics(int(vecItensToTrack[index].size.x), int(vecItensToTrack[index].size.y));
    vecItensToTrack[index].spotlight.beginDraw();
    vecItensToTrack[index].spotlight.background(0, 0); 
    drawSpotlight(vecItensToTrack[index].spotlight, vecItensToTrack[index].spotlightRadius * 3/2, vecItensToTrack[index].spotlightRadius * 3/2, vecItensToTrack[index].spotlightRadius);
    vecItensToTrack[index].spotlight.endDraw();
  
    // Apply blur to the offscreen graphics
    vecItensToTrack[index].spotlight.filter(BLUR, 15); 
  } 
}

void draw() {
  background(0); 

  for(int index = 0; index < vecItensToTrack.length; index ++){
    if(vecItensToTrack[index].isDrawing){
      image(
        vecItensToTrack[index].spotlight, 
        vecItensToTrack[index].point.x - (vecItensToTrack[index].curSize * vecItensToTrack[index].spotlightRadius * 3/2), 
        vecItensToTrack[index].point.y - (vecItensToTrack[index].curSize * vecItensToTrack[index].spotlightRadius * 3/2), 
        vecItensToTrack[index].curSize * vecItensToTrack[index].size.x,
        vecItensToTrack[index].curSize * vecItensToTrack[index].size.y
      );
    }
  }
  
  noStroke();
  fill(0, 0, 0, (vecItensToTrack[0].brightness * 255));
  rect(0, 0, width, height);
     
  spout.sendTexture();
}

void drawSpotlight(PGraphics pg, float x, float y, float radius) {
  int centerColor = color(255, 255, 220); 
  int edgeColor = color(255, 255, 220, 0); 

  for (float r = radius; r > 0; r--) {
    float inter = map(r, 0, radius, 1, 0);
    int c = lerpColor(edgeColor, centerColor, inter);
    pg.noStroke();
    pg.fill(c);
    pg.ellipse(x, y, r * 2, r * 2);
  }
}

// This function is called whenever an OSC message is received
void oscEvent(OscMessage msg) {
  println("Received OSC message with address pattern: " + msg.addrPattern());

  // RIGHT HAND
  if (msg.checkAddrPattern("/rh/pointX")) {
    if (msg.checkTypetag("i")) {  
      int receivedMessage = msg.get(0).intValue();
      vecItensToTrack[0].point.x = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/rh/pointY")) {
    if (msg.checkTypetag("i")) {  
      int receivedMessage = msg.get(0).intValue();
      vecItensToTrack[0].point.y = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/rh/brightness")) {
    if (msg.checkTypetag("f")) {  
      float receivedMessage = msg.get(0).floatValue();
      vecItensToTrack[0].brightness = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/rh/size")) {
    if (msg.checkTypetag("f")) {  
      float receivedMessage = msg.get(0).floatValue();
      vecItensToTrack[0].curSize = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/rh/isDrawing")) {
    if (msg.checkTypetag("i")) { 
      int receivedMessage = msg.get(0).intValue();
      vecItensToTrack[0].isDrawing = boolean(receivedMessage);
    }
  }
  
  // lEFT HAND
  else if (msg.checkAddrPattern("/lh/pointX")) {
    if (msg.checkTypetag("i")) {  
      int receivedMessage = msg.get(0).intValue();
      vecItensToTrack[1].point.x = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/lh/pointY")) {
    if (msg.checkTypetag("i")) {  
      int receivedMessage = msg.get(0).intValue();
      vecItensToTrack[1].point.y = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/lh/brightness")) {
    if (msg.checkTypetag("f")) {  
      float receivedMessage = msg.get(0).floatValue();
      vecItensToTrack[1].brightness = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/lh/size")) {
    if (msg.checkTypetag("f")) {  
      float receivedMessage = msg.get(0).floatValue();
      vecItensToTrack[1].curSize = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/lh/isDrawing")) {
    if (msg.checkTypetag("i")) { 
      int receivedMessage = msg.get(0).intValue();
      vecItensToTrack[1].isDrawing = boolean(receivedMessage);
    }
  }
  
  // Voluta
  else if (msg.checkAddrPattern("/vl/pointX")) {
    if (msg.checkTypetag("i")) {  
      int receivedMessage = msg.get(0).intValue();
      vecItensToTrack[2].point.x = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/vl/pointY")) {
    if (msg.checkTypetag("i")) {  
      int receivedMessage = msg.get(0).intValue();
      vecItensToTrack[2].point.y = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/vl/brightness")) {
    if (msg.checkTypetag("f")) {  
      float receivedMessage = msg.get(0).floatValue();
      vecItensToTrack[2].brightness = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/vl/size")) {
    if (msg.checkTypetag("f")) {  
      float receivedMessage = msg.get(0).floatValue();
      vecItensToTrack[2].curSize = receivedMessage;
    }
  }
  else if (msg.checkAddrPattern("/vl/isDrawing")) {
    if (msg.checkTypetag("i")) { 
      int receivedMessage = msg.get(0).intValue();
      vecItensToTrack[2].isDrawing = boolean(receivedMessage);
    }
  }
}
