# guitarProjection - Toca
Alternative to guitarHands for Toca, a piece for guitar, hands and projection.

Its purpose is to create a simple performance interface where 2d paths can be drawn, through which projected spotlights positions can be controled. In that way, a single knob of a controler can be mapped to two dimensions of movement, making the lights performance of the piece easier.

![spotlightsExample](examples/example1.gif)

## Contents
This performance interface for now consists in two codes: the main python code and a p4 code for the spotlights projection. This was made to facilitate a future merge between guitarProjection and guitarHands, where the tracking of the hands will be a part of the piece while still allowing other types of light expressive articulations.

## Structure
The code was structured in the following way (maybe not yet the most effective one):
* **_0_main**: main code loop, with initialisations and drawings of general information + keyboard pressing handlers
* **_1_funcs**: utils functions, as for the cooldown thread, midi interface mapings, ...
* **_2_classes**: two classes were used.
  * [**Pathway**](https://github.com/cacaiocamp/guitarProjection/blob/master/_2_classes.py#L6): class that represent each path drawn. Calculates all the inforation needed for the path + its utils, like [_Pathway.movePathwayToCurSpotlightPos_](https://github.com/cacaiocamp/guitarProjection/blob/master/_2_classes.py#L85), a method with self explaining name that allows a more flexible performance.
  * [**SpotlightPoint**](https://github.com/cacaiocamp/guitarProjection/blob/master/_2_classes.py#L102): class that represents the spotlights to be projected, storing and calculating positions of the lights in the related pathways. [_SpolightPoint.curPos_](https://github.com/cacaiocamp/guitarProjection/blob/master/_2_classes.py#L106) tuple represents the relative position inside the pathway (1 being the beginning and 127 the end) + a vertical shift value (to allow flexibility in performances), with [_SpotlightPoint.getAbsolutePoint_](https://github.com/cacaiocamp/guitarProjection/blob/master/_2_classes.py#L158) method returning the actual pixel position of curPos.
* **_3_gvars**: global variables
* **_4_pedals**: wrapper functions for each pedal pressing.

## Some explanations
### Video Mapping
The images generated by the p4 code are passed through a video mapping software to match the pixel positionings with the actual performance space. In the future, I plan to code a simple video mapping tool to remove this software dependency.


### Cooldown
The only maybe confusing functionality added is the [_cooldown_](https://github.com/cacaiocamp/guitarProjection/blob/master/_1_funcs.py#L8). 

I wanted to use the same knob to control each light for the pieces whole duration. Than, as each hand passes through many pathways, the cooldown purpose is to allow the reset of the knob positioning while not changing the current light position when changes or movements of the spotlight's curPathway happen. This gives the performer sometime to move the knob, allowing to restart the light movement at the beggining or end of the pathways, for example. 

This is represented with a white square around the spotlight circle.
![cooldownExample](examples/example2.gif)
