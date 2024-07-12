class User:
  def __init__(self, nickname: str):
    self.nickname : str = nickname
  
  def __repr__(self) -> str:
    res : dict = {
      "nickname": self.nickname
    }
    
    return f'{res}'