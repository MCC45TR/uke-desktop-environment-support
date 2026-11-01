#!/usr/bin/env python3
"""Validate unsigned SRPM payload bytes without extracting/running source."""
from pathlib import Path
import struct,gzip,lzma,bz2
base=Path(__file__).resolve().parent
for folder,name in [(base,'nextkde'),(base/'quickshell','quickshell')]:
 rpm=next((folder/'SRPMS').glob('*.src.rpm')); raw=rpm.read_bytes()
 def end_header(off):
  assert raw[off:off+3]==b'\x8e\xad\xe8'
  count,size=struct.unpack('>II',raw[off+8:off+16]); return off+16+16*count+size
 off=(end_header(96)+7)//8*8
 payload=raw[end_header(off):]
 if payload[:2]==b'\x1f\x8b': payload=gzip.decompress(payload)
 elif payload[:6]==b'\xfd7zXZ\x00': payload=lzma.decompress(payload)
 elif payload[:3]==b'BZh': payload=bz2.decompress(payload)
 else: raise ValueError(payload[:12])
 pos=0; seen=[]
 while True:
  assert payload[pos:pos+6] in [b'070701',b'070702']
  vals=[int(payload[pos+6+i*8:pos+14+i*8],16) for i in range(13)]
  size,namesize=vals[6],vals[11]; pos+=110
  entry=payload[pos:pos+namesize-1].decode(); pos=(pos+namesize+3)//4*4
  if entry=='TRAILER!!!':break
  entry=entry.removeprefix('./'); assert '/' not in entry
  local=folder/('SPECS' if entry.endswith('.spec') else 'SOURCES')/entry
  assert payload[pos:pos+size]==local.read_bytes(),entry
  pos=(pos+size+3)//4*4; seen.append(entry)
 print(rpm.name,': all',len(seen),'payload files match source/spec bytes')
