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

#This snippet of code is taken from Bart Massey's reading in a wav file and is found on is found on https://github.com/BartMassey/pdx-cs-sound/blob/master/findpeak.py
#want to build samples to implement enhancing of the LSB based on the first two MSB
store_samples = []
# Iterate over frames.
for f in range(0, len(wave_bytes), frame_width):
    frame = wave_bytes[f : f + frame_width]
    # Iterate over channels.
    for c in range(0, len(frame), width):
        # Build a sample.
        sample_bytes = frame[c : c + width]
        #  Eight-bit samples are unsigned
        sample = int.from_bytes(sample_bytes,
                                byteorder='little',
                                signed=(width>1))

        store_samples.append(sample)
        #print(bin(sample))
#print(store_samples)

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
    #add if statements here to check each frame 
    if(frame_bytes[i] & 1 << 8 == 0 and frame_bytes[i] & 1 << 7 == 0):
      frame_bytes[i] = (frame_bytes[i] & 1 << 3) | bit

    elif(frame_bytes[i] & 1 << 8 == 0 and frame_bytes[i] & 1 << 7 == 1):
      frame_bytes[i] = (frame_bytes[i] & 1 << 2) | bit

    elif(frame_bytes[i] & 1 << 8 == 1 and frame_bytes[i] & 1 << 7 == 0):
      frame_bytes[i] = (frame_bytes[i] & 1 << 1) | bit

    elif(frame_bytes[i] & 1 << 8 == 1 and frame_bytes[i] & 1 << 7 == 1):
      frame_bytes[i] = (frame_bytes[i] & 1 << 1) | bit

#Get the modified bytes
modified_bytes = bytes(frame_bytes)

#Step 8 Write bytes to the audio wave file
with wav.open('modified_song.wav', 'wb') as wf:
    wf.setparams(wavfile.getparams())
    wf.writeframes(modified_bytes)

#Step 9- Close file
wavfile.close()
