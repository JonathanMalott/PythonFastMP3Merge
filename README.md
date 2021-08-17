# Python Fast MP3 Merge
A python script for quickly merging two MP3 files into one without any external libraries or the need to re-encode.

# The Issue
Using a python library like PyDub is great, but for some applications that require fast speeds it is not ideal. The issue is that Pydub will decode an MP3 file into a lossless byte-array (which can take several seconds for a large MP3) and then re-encode it when saving it back to an MP3 format (which again can take 15 or 20 seconds depending on the size).

This library can do the same tasks pyDub can do in less than a second or so. 

# Usage
```
mergeTwoMP3(['13.mp3','15.mp3'])
```
