#!/usr/bin/env python3
"""Pure archive processing; verifies Go dirhash against pinned upstream go.sum.
No upstream source or setup scripts are executed. Paths are relative to this script.
"""
import base64, hashlib, io, pathlib, tarfile, zipfile, gzip
root = pathlib.Path(__file__).resolve().parent
modules = [
 ('github.com/fsnotify/fsnotify','v1.10.1','fsnotify-v1.10.1.zip','h1:b0/UzAf9yR5rhf3RPm9gf3ehBPpf0oZKIjtpKrx59Ho='),
 ('golang.org/x/sys','v0.13.0','x-sys-v0.13.0.zip','h1:Af8nKPmuFypiUBjVoU9V20FiaFXOcuZI21p0ycVYYGE='),
]
files={}
for mod,version,name,expected in modules:
    with zipfile.ZipFile(root/'SOURCES'/name) as z:
        names=sorted(n for n in z.namelist() if not n.endswith('/'))
        lines=''.join(hashlib.sha256(z.read(n)).hexdigest()+'  '+n+'\n' for n in names)
        got='h1:'+base64.b64encode(hashlib.sha256(lines.encode()).digest()).decode()
        assert got==expected,(mod,got,expected)
        print(mod,version,'Go h1 verified',got)
        prefix=mod+'@'+version+'/'
        for n in names:
            assert n.startswith(prefix)
            relative=n[len(prefix):]
            assert '..' not in pathlib.PurePosixPath(relative).parts
            files['vendor/'+mod+'/'+relative]=z.read(n)
        print(z.read(prefix+'go.mod').decode())
files['vendor/modules.txt']=b'''# github.com/fsnotify/fsnotify v1.10.1
## explicit; go 1.23
github.com/fsnotify/fsnotify
# golang.org/x/sys v0.13.0
## explicit; go 1.17
golang.org/x/sys/unix
golang.org/x/sys/windows
'''
with open(root/'SOURCES'/'nextkde-go-vendor.tar.gz','wb') as out:
    with gzip.GzipFile(filename='',mode='wb',fileobj=out,mtime=0) as gz:
        with tarfile.open(fileobj=gz,mode='w|') as tar:
            for name,data in sorted(files.items()):
                entry=tarfile.TarInfo(name); entry.size=len(data); entry.mode=0o644; entry.mtime=0
                tar.addfile(entry,io.BytesIO(data))
