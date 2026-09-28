from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo
import os


REFERENCE = Path("/Users/linxiao/.codex/skills/artifact-template-linxiao-wu-cv/assets/reference.docx")
EDITABLE = {"word/document.xml", "docProps/core.xml", "docProps/app.xml"}


def clone_info(info: ZipInfo) -> ZipInfo:
    out = ZipInfo(info.filename, info.date_time)
    out.comment = info.comment
    out.extra = info.extra
    out.internal_attr = info.internal_attr
    out.external_attr = info.external_attr
    out.create_system = info.create_system
    out.compress_type = info.compress_type
    return out


def preserve(path: Path) -> None:
    tmp = path.with_suffix(".preserved.docx")
    with ZipFile(REFERENCE) as ref, ZipFile(path) as current, ZipFile(tmp, "w", ZIP_DEFLATED) as out:
        for info in ref.infolist():
            source = current if info.filename in EDITABLE else ref
            out.writestr(clone_info(info), source.read(info.filename))
    os.replace(tmp, path)


for target in [Path("deliverables/Linxiao_Wu_CV.docx"), Path("deliverables/吴林晓_简历.docx")]:
    preserve(target)
    print(target)
