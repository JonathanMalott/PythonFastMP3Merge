#!/usr/bin/env python
# mp3cat.py - tiny mp3 frame editor
# by Yusuke Shinyama  *public domain*
#
#  usage: $ ./mp3cat.py 'f[0:]' a.mp3 b.mp3 > c.mp3
#

import sys, re, fileinput
from struct import unpack
stderr = sys.stderr

# read MPEG frames
BITRATE1 = [0, 32, 40, 48, 56, 64, 80, 96, 112, 128, 160, 192, 224, 256, 320]
BITRATE2 = [0, 8, 16, 24, 32, 40, 48, 56, 64, 80, 96, 112, 128, 144, 160]
SAMPLERATE1 = [44100, 48000, 32000]
SAMPLERATE2 = [22050, 24000, 16000]
SAMPLERATE25 = [11025, 12000, 8000]
def read_frames(frames, fname, verbose=False):
    with open(fname, 'rb') as fp:
      while 1:
        x = fp.read(4)
        if not x:
          break
        elif x.startswith(b'TAG'):
          # TAG - ignored
          data = bytes(x[3])+fp.read(128-4)
          if verbose:
            print('TAG', repr(data), file=stderr)
        elif x.startswith(b'ID3'):
          # ID3 - ignored
          #int   byte
          version = bytes(x[3])+fp.read(1)
          flags = ord(fp.read(1))
          s = [ c & 127 for c in fp.read(4) ]
          size = (s[0]<<21) | (s[1]<<14) | (s[2]<<7) | s[3]
          data = fp.read(size)
          if verbose:
            print('ID3', repr(data), file=stderr)
        else:
          h = unpack('>L', x)[0]
          assert (h & 0xffe00000) == 0xffe00000, '!Frame Sync: %r' % x
          version = (h & 0x00180000) >> 19
          assert version != 1
          assert (h & 0x00060000) == 0x00020000, '!Layer3'
          protected = not (h & 0x00010000)
          b = (h & 0xf000) >> 12
          assert b != 0 and b != 15, '!Bitrate'
          if version == 3:                      # V1
            bitrate = BITRATE1[b]
          else:                                 # V2 or V2.5
            bitrate = BITRATE2[b]
          s = (h & 0x0c00) >> 10
          assert s != 3, '!SampleRate'
          if version == 3:                      # V1
            samplerate = SAMPLERATE1[s]
          elif version == 2:                    # V2
            samplerate = SAMPLERATE2[s]
          elif version == 0:                    # V2.5
            samplerate = SAMPLERATE25[s]
          nsamples = 1152
          if samplerate <= 24000:
            nsamples = 576
          pad = (h & 0x0200) >> 9
          channel = (h & 0xc0) >> 6
          joint = (h & 0x30) >> 4
          copyright = bool(h & 8)
          original = bool(h & 4)
          emphasis = h & 3
          if version == 3:
            framesize = 144000 * bitrate / samplerate + pad
          else:
            framesize = 72000 * bitrate / samplerate + pad
          data = bytes(x)+fp.read(int(framesize)-4)
          if verbose:
            print('Frame%d: bitrate=%dk, samplerate=%d, framesize=%d' % \
                  (len(frames), bitrate, samplerate, framesize), file=stderr)
          frames.append(data)
    return


#returns raw bytes of merged files
def mergeTwoMP3(files):
      PAT = re.compile(r'^[\[\]:0-9f+]*$')
      import sys, getopt
      verbose = False
      expr = 'f[0:]'
      allframes = []
      for fname in files:
        read_frames(allframes, fname, verbose)
      if expr:
        oo = []
        for f in eval(expr, {'f':allframes}):
            #outFile.write(f)
            oo.append(f)
        return oo




