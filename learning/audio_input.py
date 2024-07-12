#!/usr/bin/env python3
"""An example for using a stream in an asyncio coroutine.

This example shows how to create a stream in a coroutine and how to wait for
the completion of the stream.

You need Python 3.7 or newer to run this.

"""
import asyncio
import sys

import numpy as np
import sounddevice as sd
import soundfile

async def record_buffer(buffer, **kwargs):
    loop = asyncio.get_event_loop()
    event = asyncio.Event()
    idx = 0

    def callback(indata, frame_count, time_info, status):
        nonlocal idx
        if status:
            print(status)
        remainder = len(buffer) - idx
        if remainder == 0:
            loop.call_soon_threadsafe(event.set)
            raise sd.CallbackStop
        indata = indata[:remainder]
        buffer[idx:idx + len(indata)] = indata
        idx += len(indata)

    stream = sd.InputStream(callback=callback, dtype=buffer.dtype,
                            channels=buffer.shape[1], **kwargs)
    with stream:
        await event.wait()


async def play_buffer(buffer, **kwargs):
    loop = asyncio.get_event_loop()
    event = asyncio.Event()
    idx = 0

    def callback(outdata, frame_count, time_info, status):
        nonlocal idx
        if status:
            print(status)
        remainder = len(buffer) - idx
        if remainder == 0:
            loop.call_soon_threadsafe(event.set)
            raise sd.CallbackStop
        valid_frames = frame_count if remainder >= frame_count else remainder
        outdata[:valid_frames] = buffer[idx:idx + valid_frames]
        outdata[valid_frames:] = 0
        idx += valid_frames

    stream = sd.OutputStream(callback=callback, dtype=buffer.dtype,
                             channels=buffer.shape[1], **kwargs)
    with stream:
        await event.wait()


async def main(channels=1, dtype='float32', **kwargs):
  opt = 1
  while opt != 0:
    print('Digite uma das opções abaixo')
    print('0 ------ Para sair do programa')
    print('1 ------ Gravar um áudio')

    opt = int(input())

    match opt:
        case 1:
          print('Digite o nome do arquivo')
          filename = str(input())
          seconds = int(input('Quantos segundos você deseja gravar: '))
          frames = seconds * 50000
          print()
          buffer = np.empty((frames, channels), dtype=dtype)
          print('Gravando ...')
          await record_buffer(buffer, **kwargs)
          print('O áudio gravado foi ...')
          await play_buffer(buffer, **kwargs)

          print(buffer)
          
          soundfile.write(rf'../public/{filename}.mp3', buffer, 44100)
          print('done')
          print()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit('\nInterrupted by user')