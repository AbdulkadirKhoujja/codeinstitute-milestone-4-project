"""Render the preserved original text wireframes, without inventing historical images."""

import html
import re
from pathlib import Path

root = Path(__file__).resolve().parent.parent
source = root / "docs/design/phase-3-wireframes.md"
blocks = re.findall(r"```text\n(.*?)```", source.read_text(encoding="utf-8"), re.S)
destination = root / "docs/design/wireframes"
destination.mkdir(parents=True, exist_ok=True)
for name, block in zip(("discovery", "booking", "owner"), blocks, strict=True):
    lines = block.rstrip().splitlines()
    height = 105 + len(lines) * 26
    content = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="{height}" viewBox="0 0 1100 {height}" role="img" aria-label="Original SkillSeat {name} text planning wireframe rendered during Phase 4">',
        '<rect width="100%" height="100%" fill="#f8f7f2"/>',
        '<text x="24" y="30" font-family="sans-serif" font-size="18" fill="#183c36">Original planning: 17 October 2026 · Image rendering: Phase 4, 19 October 2026</text>',
        '<text x="24" y="57" font-family="sans-serif" font-size="14" fill="#4f625a">Faithful rendering of the preserved text artefact; no original image wireframe existed.</text>',
    ]
    for index, line in enumerate(lines):
        content.append(
            f'<text x="24" y="{94 + index * 26}" xml:space="preserve" font-family="monospace" font-size="19" fill="#183c36">{html.escape(line)}</text>'
        )
    content.append("</svg>")
    (destination / f"{name}-original-text.svg").write_text("\n".join(content), encoding="utf-8")
    print(f"Rendered {name} from unchanged original text.")
