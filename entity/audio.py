import json
import numpy
import sounddevice

from entity.user import User

class Audio:
  def __init__(self, filedict: dict) -> None:
    self.owner : User = filedict["owner"]
    self.rate = filedict["rate"]
    self.data : numpy.ndarray = filedict["data"]

  def play(self):
    sounddevice.play(self.data, self.rate)
    sounddevice.wait()