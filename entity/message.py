class Message:
  def __init__(self, messagerDict: dict) -> None:
    self.owner = messagerDict["owner"]
    self.content = messagerDict["content"]
