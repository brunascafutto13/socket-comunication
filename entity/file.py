import sounddevice

class File:
  def __init__(self, filedict: dict) -> None:
    self.rate = filedict["rate"]
    self.data = filedict["data"]

  def play(self):
    sounddevice.play(self.data, self.rate)
    sounddevice.wait()
