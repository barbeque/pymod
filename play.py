import struct

def read_sample(fp):
  s = Sample()
  s.name = fp.read(22)
  s.length = struct.unpack('>H', fp.read(2))[0]
  s.finetune = fp.read(1)
  s.volume = fp.read(1)
  s.repeat_offset = struct.unpack('>H', fp.read(2))[0]
  s.repeat_length = struct.unpack('>H', fp.read(2))[0]
  return s

class Song:
  def __init__(self):
    self.name = ''
    self.samples = []
    self.song_positions = 0
    self.restart_position = 0
    self.patterns = []
    self.format = ''
    self.pattern_data = []
    self.sample_data = []

class Sample:
  def __init__(self):
    self.name = ''
    self.length = 0
    self.finetune = 0
    self.volume = 0
    self.repeat_offset = 0
    self.repeat_length = 0

fp = open('freezerend.mod', 'rb')

try:
  name = fp.read(20)
  print 'name:', name

  # repeat for each sample...
  samples = []
  for i in range(0, 31):
    samples.append(read_sample(fp))
    print 'sample name:', samples[-1].name

  # identify format
  # read pattern data
  # read sample data

finally:
  fp.close()

# play back
