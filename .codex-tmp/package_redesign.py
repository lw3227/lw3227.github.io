from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED
import shutil, hashlib, re
from urllib.parse import unquote, urlparse

root = Path.cwd()
assets = [Path('Linxiao Wu.pdf'), Path('吴林晓.pdf'), *sorted(Path('project').glob('*.pdf'))]
digest = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before = {str(p): digest(p) for p in assets}
assert before['project/cnn-accelerator-datasheet.pdf'] == '807166507de4b996b1f222ead826079c795eaa8d1e0309ddf817abccee82e979'
for folder in ['cos-upload', 'upload-package', 'deliverables/linxiaowu-site-cos-2026-09-27']:
    dest = Path(folder)
    for asset in assets:
        target = dest/(asset.name if folder == 'upload-package' else asset)
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.exists() or digest(target) != before[str(asset)]:
            shutil.copy2(asset, target)
    for href in re.findall(r'href="([^"]+)"', (dest/'index.html').read_text()):
        if not href.startswith('#') and not urlparse(href).scheme:
            assert (dest/unquote(href)).is_file(), (folder, href)
for name in ['cos-upload.zip', 'deliverables/linxiaowu-site-cos-2026-09-27.zip']:
    with ZipFile(name, 'w', ZIP_DEFLATED) as z:
        for p in [Path('index.html'), *assets]:
            z.write(p, str(p))
    with ZipFile(name) as z:
        assert z.testzip() is None
        assert z.read('index.html') == Path('index.html').read_bytes()
        for asset in assets:
            assert hashlib.sha256(z.read(str(asset))).hexdigest() == before[str(asset)]
    print(name, Path(name).stat().st_size, 'bytes; HTML and all PDF hashes verified')
assert all(digest(Path(p)) == value for p,value in before.items())
print('All upload links resolve; original CV and project PDFs unchanged.')
