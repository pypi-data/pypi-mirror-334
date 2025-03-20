# Cricket
This is a package which can be used for assessing videos of bowling and batting

## How To Use
### Batting
#### Specific Shot
```python
from cricket.batting import straight_drive
decision = straight_drive.classify_entire_video("video_path")
```
There are various shots like 
- Cover drive
- Pull shot
- Sweep
- Reverse sweep
- Hook shot
- Defense

This is the implementation of straight drive.
It will also return if it was a:
- Good shot
- Bad shot

#### Overall
```python
from cricket.batting import overall_shot_detection
classifier = overall_shot_detection.CricketShotClassifier()
classifier.classify_entire_video("video_path")
```
This classifier class is compatible with the following shots:
- Straight Drive
- Cover Drive
- Sweep
- Defence
- Reverse Sweep
- Pull Shot
- Hook Shot

This will also return if it was a:
- Good Shot
- Bad Shot

### Balling
#### Specific Type

```python
from cricket.balling import fast
import cricket.utils as utils

ball_colour_range = utils.color_ranges["white"]
decision = fast.classify_entire_video("video_path", ball_colour_range)
```
This method is compatible with:
- Fast ball
- Slow ball
- Yorker
- Spin

This was an implementation of a fast ball. It will also tell if it was a:
- Good Delivery
- Bad Delivery

#### Overall
```python
from cricket.balling.overall_bowl_detection import CricketBallAnalyzer
import cricket.utils as utils

ball_colour_range = utils.color_ranges["white"]
analyser = CricketBallAnalyzer("video_path", ball_colour_range[0], ball_colour_range[1], 22)
decision = analyser.analyze_video()
```
This classifier class is compatible with:
- Fast Ball
- Slow ball
- Yorker
- Spin

### Combined
```python
from cricket.combined import classify_overall
import cricket.utils as utils

ball_colour = utils.color_ranges["white"]
decision = classify_overall("video_path", ball_colour, 22)
```
This will run both the classes given above and will return a dictionary. First key will be of bowling and second key will be of batting

**Note:** For ease of use you can import like this and it would import all things for implementation from both the subpackages
```python
from cricket import *
```