from tempfile import TemporaryDirectory as tempdir
from zipfile import ZipFile as zip
from tarfile import open as tar
from os import chdir as cd
from os import listdir as ls
from os import rename as mv
from os import mkdir
from os import getcwd as pwd
from functools import partial
from sys import argv
from contextlib import contextmanager as _withibler
try : from pip import main as pipman
except: from pip._internal import main as pipman

class EnterDir:
	__slots__ = tuple('dir pwdv'.split())
	def __init__(self, x, y):
		self.dir, self.pwdv = x, y

def __enterdirc__(dir, pwdv):
	cd(dir)
	yield EnterDir(dir, pwdv)
	cd(pwdv)

@_withibler
def enterdir(dir):
	yield from __enterdirc__(dir, pwd())

def unzipping_core(umm, zipf):
	with entetdir(umm.dir) as man: zipf.extractall()

def unziping_part(f, fun):
	 with zip(f) as zipf:
 		with tempdir() as txzingsp:
 			with enterdir(txzingsp) as umm:
 				umm.dir = f[:-4]
 				mkdir(umm.dir)
 				unzipping_core(umm, zipf)
 				fun(umm.dir)

def untgzing_push(txzingsp, fun, tgzf):
	with enterdir(txzingsp) as dir: fun(ls(tgzf)[0])

def untgzing_part(f, fun):
	with tar(f, 'r:gz') as tgzf:
		with tempdir() as txzingsp:
			try: pass
			finally:
				try: tgzf.extractall(txzingsp)
				finally: untgzing_push(txzingsp, fun, tgzf)

def txzpkg(x):
	with tempdir() as dir:
		with tar(f'{x}.txz', 'w:xz') as txzf:
			with enterdir(dir):
				try: pipman(['download', x])
				finally:
					for _ in ((unziping_part if f[-4:] == '.whl' else untgzing_part)(f, txzf.add) for f in ls()):pass

def main():
    txzpkg(input('txzpkg-download : ')) if len(argv) == 1 else txzpkg(argv[1])

if __name__ == "__main__": main()