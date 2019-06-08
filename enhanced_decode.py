#!/usr/bin/python3

#The following code is based on the code written by reachsumit on github. The URL for the page is https://gist.github.com/reachsumit/583c76ffd740e1a952d65da3c676931f. This is the file to decode the enhanced LSB message in from enhanced.py and the modifications to the code is to decode the message based on the enhancement..

import sys
import wave as wav

#Step 1: Get signal file to write and the associated information with the file
wavfile = wav.open(sys.argv[1], 'rb')
#channels per frame
channels = wavfile.getnchannels()
#bytes per sample
width = wavfile.getsampwidth()
#sample rate
rate = wavfile.getframerate()
#number of frames
frames = wavfile.getnframes()
#length of frames
frame_width = width * channels

#Step 2: Read frames
wave_bytes = wavfile.readframes(frames)

#Step 3: Convert to byte array
frame_bytes = bytearray(list(wave_bytes))

#Step 3: Extract the LSB of each byte in the wav file to get bits of the message encoded in the wav file
#extract_LSB = [frame_bytes[i] & 1 for i in range(len(frame_bytes))]
for i in range(len(frame_bytes)):
    if(frame_bytes[i] & 1 << 8 == 0 and frame_bytes[i] & 1 << 7 == 0):
      extract_LSB = [(frame_bytes[i] & 1 << 3)]

    elif(frame_bytes[i] & 1 << 8 == 0 and frame_bytes[i] & 1 << 7 == 1):
      extract_LSB= [(frame_bytes[i] & 1 << 2)]

    elif(frame_bytes[i] & 1 << 8 == 1 and frame_bytes[i] & 1 << 7 == 0):
      extract_LSB = [(frame_bytes[i] & 1 << 1)]

    elif(frame_bytes[i] & 1 << 8 == 1 and frame_bytes[i] & 1 << 7 == 1):
      extract_LSB = [(frame_bytes[i] & 1 << 1)] 
      
#Step 4: Get the message by converting the byte array back to the string 
decode_message = ''.join(chr(int(''.join(map(str, extract_LSB[i:i+8])), 2)) for i in range(0, len(extract_LSB), 8))

#Step 5: Get rid of the filler characters 
decoded = decode_message.split('#')[0]

#Step 6: Print out the message
print("Message: ", decoded)
