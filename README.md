# steganography

The purpose of this project is to try to enhance LSB steganography based on the article "An Enhanced Least Significant Bit Modification Technique for Audio Steganography" by Muhammad Asad, Junaid Gilani, and Adnan Khalid. The reason why I chose to work on this specifically is because there are code out there which does LSB steganography, but there is not much information or attempts to enhanced this technique; thus I wanted to give it shot and attempt to do so.

To run the code to hide the message, the command should be something like:
python3 original.py song.wav

To run the code to get the message, the command should be something like:
python3 decode.py modified_song.wav

There are still many issues with this code. The details are within the writeup.txt.

