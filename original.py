#!/usr/bin/python3

import sys
import wave as wav

#The following code is based on the code written by reachsumit on github. The URL for the page is https://gist.github.com/reachsumit/5376441d341bb5c8b361a2f3e0798993. The modification to the code attempts produced an enhanced version of audio steganography with the least significant bit technique by using randomness produced by selecting a different bit in every sample to hide the secret message.

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
frame_bytes = bytearray(wave_bytes)

#Step 4: Message
message = 'This is a message' 

#Step 5: Fill out the rest of the bytes of the message to match the length of of the bytes of the audio file
mess_len = len(message) * 64
message = message + int((len(frame_bytes) - mess_len)/8) * '#'

#Step 6: Convert the message to bit array 
bits = []
bits = map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8,'0') for i in message]))

#Step 7: Replace LSB of each byte of the audio by one bit from the message bit array
for i, bit in enumerate(bits):
    frame_bytes[i] = (frame_bytes[i] & 2) | bit

#Get the modified bytes
modified_bytes = bytes(frame_bytes)

#Step 8 Write bytes to the audio wave file
with wav.open('modified_song.wav', 'wb') as wf:
    wf.setparams(wavfile.getparams())
    wf.writeframes(modified_bytes)

#Step 9- Close file
wavfile.close()
