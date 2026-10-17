#!/usr/bin/env python3
"""校验并解包显式提供的官方 Web 发布归档；不联网下载、不覆盖已有编辑器。"""
import pathlib,json,hashlib,zipfile,sys,stat
root=pathlib.Path(__file__).resolve().parent;lock=json.loads((root/'editor.lock.json').read_text());archive=pathlib.Path(sys.argv[1]);dest=root/'dist/editor'
if hashlib.sha256(archive.read_bytes()).hexdigest()!=lock['sha256']:raise SystemExit('Archive checksum mismatch')
if dest.exists():raise SystemExit('dist/editor already exists; choose a fresh build directory')
with zipfile.ZipFile(archive) as z:
 entries=[]
 for i in z.infolist():
  parts=pathlib.PurePosixPath(i.filename).parts[1:]
  if not parts or i.is_dir():continue
  if '..' in parts or any('\\' in p for p in parts) or stat.S_ISLNK(i.external_attr>>16):raise SystemExit('Unsafe archive path')
  entries.append((i,parts))
 if sum(i.file_size for i,_ in entries)>1024**3:raise SystemExit('Archive too large')
 for i,parts in entries:
  out=dest.joinpath(*parts);out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(z.read(i))
print(dest)
