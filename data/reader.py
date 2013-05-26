from bson import InvalidBSON, BSON
from bson.binary import Binary

import sys
import struct

class BSONInput(object):
    """Custom file class for decoding streaming BSON,
based upon the Dumbo & "typedbytes" modules at
https://github.com/klbostee/dumbo &
https://github.com/klbostee/typedbytes
"""

    def __init__(self, fh=sys.stdin, unicode_errors='strict'):
        self.fh = fh
        self.unicode_errors = unicode_errors
        self.eof = False

    def _read(self):
        try:
            size_bits = self.fh.read(4)
            size = struct.unpack("<i", size_bits)[0] - 4 # BSON size byte includes itself
            data = size_bits + self.fh.read(size)
            if len(data) != size + 4:
                raise struct.error("Unable to cleanly read expected BSON Chunk; EOF, underful buffer or invalid object size.")
            if data[size + 4 - 1] != "\x00":
                raise InvalidBSON("Bad EOO in BSON Data")
            doc = BSON(data).decode(tz_aware=True)
            return doc
        except struct.error, e:
            #print >> sys.stderr, "Parsing Length record failed: %s" % e
            self.eof = True
            raise StopIteration(e)

    def read(self):
        try:
            return self._read()
        except StopIteration, e:
            print >> sys.stderr, "Iteration Failure: %s" % e
            return None

    def _reads(self):
        r = self._read
        while 1:
            yield r()

    def close(self):
        self.fh.close()

    __iter__ = reads = _reads
