from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION_PATTERN = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)$")


def render_version_info(version: str) -> str:
    match = VERSION_PATTERN.fullmatch(version.strip())
    if match is None:
        raise ValueError(f"Versão inválida: {version!r}")

    major, minor, patch = (int(match.group(key)) for key in ("major", "minor", "patch"))
    version_tuple = (major, minor, patch, 0)
    display_version = f"{major}.{minor}.{patch}.0"

    return f'''# UTF-8
VSVersionInfo(
  ffi=FixedFileInfo(
    filevers={version_tuple},
    prodvers={version_tuple},
    mask=0x3f,
    flags=0x0,
    OS=0x4,
    fileType=0x1,
    subtype=0x0,
    date=(0, 0)
    ),
  kids=[
    StringFileInfo(
      [
      StringTable(
        '040904B0',
        [
          StringStruct('CompanyName', 'AndreVazao'),
          StringStruct('FileDescription', 'ECU Pro Tune'),
          StringStruct('FileVersion', '{display_version}'),
          StringStruct('InternalName', 'ECUProTune'),
          StringStruct('OriginalFilename', 'ECUProTune.exe'),
          StringStruct('ProductName', 'ECU Pro Tune'),
          StringStruct('ProductVersion', '{display_version}')
        ])
      ]),
    VarFileInfo([VarStruct('Translation', [1033, 1200])])
  ]
)
'''


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate PyInstaller Windows executable version metadata."
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "build" / "windows_version_info.txt",
        help="Output path for the PyInstaller version resource file.",
    )
    args = parser.parse_args()

    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    content = render_version_info(version)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(content, encoding="utf-8")
    print(f"Windows version metadata generated: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
