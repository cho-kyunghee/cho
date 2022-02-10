import os

os.system(f'arecord -D plughw:1,0 -c 2 -r 16000 -f S32_LE -d 10 -t wav -q -vv –V stereo stream.raw;sox stream.raw -c 1 -b 16 stream.wav')