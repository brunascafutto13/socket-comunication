import sounddevice
import soundfile
import numpy as np

def main():
  pathfile = 'stereo_file.mp3'
  buffer = np.ones((100000 * 2, 1))
  soundfile.write(pathfile, buffer, 44100)

  data, fs = soundfile.read(pathfile)

  sounddevice.play(data, fs)
  

  sounddevice.wait()
   
 


main()