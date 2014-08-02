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

def read_format_chunk(song, fp):
  song.song_positions = fp.read(1)
  song.restart_position = fp.read(1)
  song.pattern_data = fp.read(128)
  song.format = fp.read(4)

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
  s = Song()

  s.name = fp.read(20)
  print 'name:', s.name

  # repeat for each sample...
  s.samples = []
  for i in range(0, 31): # we'll trim later if we were wrong
    s.samples.append(read_sample(fp))

  read_format_chunk(s, fp)
  if s.format != 'M.K.':
    # shit we need to rewind by 134 bytes + 16 samples
    # then try again
    s.samples = s.samples[:15]
    seek_distance = 134 + (16 * 30)
    fp.seek(-seek_distance, 1)
    read_format_chunk(s, fp)

  print '# of samples:', len(s.samples)
  for sample in s.samples:
    print 'sample name:', sample.name
  print 'Format:', s.format

  # read pattern data
  # read sample data

finally:
  fp.close()

# play back
