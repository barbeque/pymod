import struct

def read_sample(fp):
  s = Sample()
  s.name = fp.read(22)
  s.length = struct.unpack('>H', fp.read(2))[0]
  s.finetune = struct.unpack('B', fp.read(1))[0]
  s.volume = struct.unpack('B', fp.read(1))[0]
  s.repeat_offset = struct.unpack('>H', fp.read(2))[0]
  s.repeat_length = struct.unpack('>H', fp.read(2))[0]
  return s

def read_format_chunk(song, fp):
  song.song_positions = struct.unpack('B', fp.read(1))[0]
  song.restart_position = struct.unpack('B', fp.read(1))[0]
  for i in range(0, 128):
    song.patterns.append(struct.unpack('B', fp.read(1))[0])
  song.format = fp.read(4)

def read_pattern(fp):
  p = Pattern()

  for d in range(0, 64):
    for channel in range(0, 4):
      division = PatternDivision()
      division.sample_index = struct.unpack('B', fp.read(1))[0]
      # now load 24 bits/3 bytes and split them into 12 bits each
      b1, b2, b3 = struct.unpack('BBB', fp.read(3))

      # goes like this:
      # SSSSSSSS, PPPPPPPP, PPPPEEEE, EEEEEEEE
      left = (b1 << 4) | (b2 >> 4) # big endian!
      right = ((b2 << 8) & 0xf00) | b3 # shift left eight spots, knock off top 4

      division.sample_period = left
      division.effect = right

      p.divisions.append(division)

  return p

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

class Pattern:
  def __init__(self):
    self.divisions = [] # 64 divisions * 4 channels.

class PatternDivision:
  def __init__(self):
    self.sample_index = 0
    self.sample_period = 0
    self.effect = 0

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
    # we were wrong.
    # we need to rewind by 134 bytes + 16 samples
    # because this is not a 31-sample song
    s.samples = s.samples[:15]
    seek_distance = 134 + (16 * 30)
    fp.seek(-seek_distance, 1)
    read_format_chunk(s, fp)

  print '# of samples:', len(s.samples)
  for sample in s.samples:
    print 'sample name:', sample.name, 'length (in words):', sample.length
  print 'Format:', s.format

  # determine the count of patterns
  pattern_count = max(s.patterns) + 1 # 0-indexed.
  print 'number of patterns:', pattern_count

  # read pattern data
  for i in range(0, pattern_count):
    s.pattern_data.append(read_pattern(fp))

  # read sample data
  for sample_ref in s.samples:
    if sample_ref.length > 1: # indicating non-empty sample
      bytes = []
      for i in range(0, 2 * sample_ref.length): # length is in words, so double it for bytes
        bytes.append(struct.unpack('b', fp.read(1))[0])
      s.sample_data.append(bytes)
    else:
      s.sample_data.append([]) # don't break indices!!
      #print 'zero length sample:', sample_ref.name

finally:
  fp.close()

# play back
