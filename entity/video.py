class Video:
  def __init__(self, videoDict: dict) -> None:
    self.owner = videoDict["owner"]
    self.frame = videoDict["frame"]