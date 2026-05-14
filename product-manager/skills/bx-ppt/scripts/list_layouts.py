#!/usr/bin/env python3
"""List slide masters and layouts in a .pptx template.

Usage:
  python scripts/list_layouts.py                              # bundled template
  python scripts/list_layouts.py path/to/other-template.pptx  # any template

Reads the OOXML zip directly (no python-pptx dependency) so it works in the
same environment as the rest of the skill's scripts.
"""
import sys
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = SKILL_DIR / "template" / "Solomon Default Template.pptx"

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}


def _resolve_target(master_path: str, target: str) -> str:
    """Resolve a target relative to a master's part path into an archive path."""
    base_parts = master_path.split("/")[:-1]
    for seg in target.split("/"):
        if seg == "..":
            if base_parts:
                base_parts.pop()
        elif seg and seg != ".":
            base_parts.append(seg)
    return "/".join(base_parts)


def _layout_files_for_master(z: zipfile.ZipFile, master_path: str) -> list[str]:
    """Return slideLayout part paths in the master's sldLayoutIdLst order.

    PowerPoint and python-pptx use this order; rels alone don't guarantee it.
    """
    rels_path = master_path.replace("slideMasters/", "slideMasters/_rels/") + ".rels"
    if rels_path not in z.namelist():
        return []
    rels = ET.fromstring(z.read(rels_path))
    rid_to_target = {r.get("Id"): r.get("Target") for r in rels}

    master_root = ET.fromstring(z.read(master_path))
    id_lst = master_root.find("p:sldLayoutIdLst", NS)
    rid_attr = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"

    paths: list[str] = []
    if id_lst is not None:
        for item in id_lst:
            rid = item.get(rid_attr)
            target = rid_to_target.get(rid)
            if target:
                paths.append(_resolve_target(master_path, target))
    if not paths:  # fallback: any layout-typed rel
        for rel in rels:
            if rel.get("Type", "").endswith("/slideLayout"):
                paths.append(_resolve_target(master_path, rel.get("Target")))
    return paths


def _placeholders(csld: ET.Element) -> list[str]:
    out = []
    for sp in csld.findall(".//p:sp", NS):
        ph = sp.find(".//p:nvSpPr/p:nvPr/p:ph", NS)
        if ph is None:
            continue
        ptype = ph.get("type", "body")
        idx = ph.get("idx", "0")
        out.append(f"{ptype}@{idx}" if idx != "0" else ptype)
    return out


def main(path: Path) -> None:
    if not path.exists():
        sys.exit(f"Template not found: {path}")
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        # Slide size
        pres = ET.fromstring(z.read("ppt/presentation.xml"))
        sld_sz = pres.find("p:sldSz", NS)
        cx = int(sld_sz.get("cx"))
        cy = int(sld_sz.get("cy"))
        print(f"Template: {path.name}")
        print(f"Slide size: {cx/914400:.2f}\" x {cy/914400:.2f}\" ({cx} x {cy} EMU)")

        masters = sorted(n for n in names if n.startswith("ppt/slideMasters/slideMaster") and n.endswith(".xml"))
        for mi, mpath in enumerate(masters):
            mroot = ET.fromstring(z.read(mpath))
            mcsld = mroot.find("p:cSld", NS)
            mname = mcsld.get("name") or "<unnamed>"
            print(f"\nMaster [{mi}]: {mpath.split('/')[-1]}  cSld.name={mname!r}")

            layout_paths = _layout_files_for_master(z, mpath)
            if not layout_paths:
                layout_paths = sorted(n for n in names if n.startswith("ppt/slideLayouts/slideLayout") and n.endswith(".xml"))

            for li, lpath in enumerate(layout_paths):
                if lpath not in names:
                    continue
                lroot = ET.fromstring(z.read(lpath))
                lcsld = lroot.find("p:cSld", NS)
                lname = lcsld.get("name") if lcsld is not None else "<unknown>"
                phs = _placeholders(lcsld) if lcsld is not None else []
                print(f"  Layout [{li}]: {lpath.split('/')[-1]:<22} name={lname!r}")
                print(f"    placeholders: {phs}")


if __name__ == "__main__":
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_TEMPLATE
    main(target)
