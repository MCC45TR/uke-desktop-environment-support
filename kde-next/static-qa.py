#!/usr/bin/env python3
"""Read-only packaging contracts; --sources also checks fetched archives."""
from pathlib import Path
import argparse
import hashlib
import re
import tarfile

root = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--sources', action='store_true')
args = parser.parse_args()
for spec in [root/'SPECS/nextkde.spec', root/'quickshell/SPECS/quickshell.spec']:
    text = spec.read_text()
    assert '%(' not in text and '%{lua:' not in text, spec
    assert not re.search(r'^%(?:pre|post|preun|postun|pretrans|posttrans|trigger\w*|filetrigger\w*|transfiletrigger\w*)\b', text, re.M), spec
    assert re.search(r'^ExclusiveArch:\s+aarch64\s*$', text, re.M), spec
    assert re.search(r'^%global commit [0-9a-f]{40}$', text, re.M), spec
    print(spec.name, 'pinned, aarch64-only, no parse-time shell/Lua or activation scriptlets')
for line in (root/'PACKAGING-SHA256SUMS').read_text().splitlines():
    digest, name = line.split(maxsplit=1)
    assert hashlib.sha256((root/name).read_bytes()).hexdigest() == digest, name
print('Packaging text checksums verified')
if args.sources:
    for line in (root/'SOURCE-SHA256SUMS').read_text().splitlines():
        digest, name = line.split(maxsplit=1)
        assert hashlib.sha256((root/name).read_bytes()).hexdigest() == digest, name
    with tarfile.open(root/'SOURCES/nextkde-go-vendor.tar.gz') as tar:
        for member in tar.getmembers():
            assert member.isfile() and not member.name.startswith('/') and '..' not in Path(member.name).parts
            assert member.uid == member.gid == member.mtime == 0
    print('Pinned source hashes and safe deterministic vendor metadata verified')
print('NOT TESTED: native RPM build, upstream tests, runtime, SELinux, target hardware')
