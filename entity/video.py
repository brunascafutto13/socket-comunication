import json
import numpy
from entity.user import User

class Video:
  def __init__(self, videoDict: dict) -> None:
    self.owner : User = videoDict["owner"]
    self.frame : numpy.ndarray  = videoDict["frame"]