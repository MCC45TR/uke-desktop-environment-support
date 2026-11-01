#!/usr/bin/env python3
"""Retrieve pinned source bytes only; never execute upstream build/install code."""
from pathlib import Path
import hashlib
import subprocess
import tempfile
import urllib.request

ROOT = Path(__file__).resolve().parent
COMMIT = '2ca59a1fbe7cd8c4b9c0b9fd960edca6788425c5'
DOWNLOADS = {
 'SOURCES/fsnotify-v1.10.1.zip': 'https://proxy.golang.org/github.com/fsnotify/fsnotify/@v/v1.10.1.zip',
 'SOURCES/x-sys-v0.13.0.zip': 'https://proxy.golang.org/golang.org/x/sys/@v/v0.13.0.zip',
 'quickshell/SOURCES/quickshell-4f508be500dea6e5732cc3d50382a0048b17e7b1.tar.gz': 'https://github.com/quickshell-mirror/quickshell/archive/4f508be500dea6e5732cc3d50382a0048b17e7b1/quickshell-4f508be500dea6e5732cc3d50382a0048b17e7b1.tar.gz',
}

def hashes():
    return {name: digest for digest, name in
            (line.split(maxsplit=1) for line in (ROOT/'SOURCE-SHA256SUMS').read_text().splitlines())}

def save_checked(name, data):
    expected = hashes()[name]
    actual = hashlib.sha256(data).hexdigest()
    if actual != expected:
        raise ValueError(f'{name}: SHA256 mismatch: {actual}; expected {expected}')
    dest = ROOT/name
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(data)
    print(f'verified {name}')

def main():
    # git fetch/archive reads source data. No checkout, submodules, or hooks.
    with tempfile.TemporaryDirectory(prefix='nextkde-source-') as work:
        subprocess.run(['git', 'init', '--bare', work], check=True)
        subprocess.run(['git', '-C', work, '-c', 'core.hooksPath=/dev/null',
                        'fetch', '--depth=1', 'https://github.com/NextKde/NextKde.git', COMMIT], check=True)
        tar = subprocess.check_output(['git', '-C', work, 'archive', '--format=tar',
                                       f'--prefix=NextKde-{COMMIT}/', COMMIT])
        data = subprocess.check_output(['gzip', '-n'], input=tar)
        save_checked(f'SOURCES/NextKde-{COMMIT}.tar.gz', data)
    for name, url in DOWNLOADS.items():
        with urllib.request.urlopen(url, timeout=120) as response:
            save_checked(name, response.read())
    # This is our reviewed archive-only helper, not upstream code.
    subprocess.run(['python3', str(ROOT/'prepare-vendor.py')], check=True)
    for name, expected in hashes().items():
        actual = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f'{name}: SHA256 mismatch')
    print('All source checksums verified; no upstream code executed.')

if __name__ == '__main__':
    main()
