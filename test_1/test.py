import json
import math

import dronekit

waypoints = {
  "coordinates":
  [
    [41.27626635781504, 1.9884008816712835],
    [41.276289876449994, 1.9885336442339285],
    [41.27631339507647, 1.9886645101885363],
    [41.27636969720847, 1.9886426991961017],
    [41.27634546591712, 1.9885089883294373],
    [41.27631980924586, 1.988385708806981]
  ]
}

picturepoints = {
  "coordinates":
  [
    [41.27626635781504, 1.9884008816712835],
    [41.27627704810471, 1.988474849384757],
    [41.276289876449994, 1.9885336442339285],
    [41.27630270479276, 1.9885952839951566],
    [41.27631339507647, 1.9886645101885363],
    [41.27636969720847, 1.9886426991961017],
    [41.27635758156391, 1.9885725246987032],
    [41.27634546591712, 1.9885089883294373],
    [41.276334062953346, 1.988448296872228],
    [41.27631980924586, 1.988385708806981]
  ]
}

waypoints_json = json.dumps(waypoints)
picturepoints_json = json.dumps(picturepoints)

pp = json.loads(picturepoints_json)
print(len(pp['coordinates']))