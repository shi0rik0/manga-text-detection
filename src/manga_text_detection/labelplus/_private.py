from ..comic_text_detector import TextDetector, detect_blocks

import torch
from dataclasses import dataclass
from typing import List
from pathlib import Path
import argparse

LP_OUTPUT_HEADER = """1,0
-
框内
框外
-
Default Comment
You can edit me


"""


@dataclass
class Translation:
    text: str
    x: int
    y: int


@dataclass
class MangaPage:
    filename: str
    width: int
    height: int
    translations: List[Translation]


def get_lp_output_per_file(page: MangaPage) -> str:
    pieces = [f">>>>>>>>[{page.filename}]<<<<<<<<\n"]
    for i, v in enumerate(page.translations):
        x = v.x / page.width
        y = v.y / page.height
        pieces.append(f"----------------[{i}]----------------[{x:.3f},{y:.3f},1]\n")
        pieces.append(f"{v.text}\n\n")
    return "".join(pieces)


def get_lp_output(pages: List[MangaPage]) -> str:
    pieces = []
    for i in pages:
        pieces.append(get_lp_output_per_file(i))
    return LP_OUTPUT_HEADER + "\n".join(pieces)


def main():
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("dir", type=str, help="Directory containing images")
    args = parser.parse_args()
    input_dir = Path(args.dir)
    images = [i for i in input_dir.iterdir() if i.suffix in [".jpg", ".png", ".jpeg"]]
    images.sort()
    model_path = "data/comictextdetector.pt"
    cuda = torch.cuda.is_available()
    device = "cuda" if cuda else "cpu"
    model = TextDetector(
        model_path=model_path, input_size=1024, device=device, act="leaky"
    )
    translations_list = []
    for image in images:
        blocks = detect_blocks(model, str(image))
        translations = []
        for block in blocks:
            x = (block.left + block.right) / 2
            y = (block.top + block.bottom) / 2
            translations.append(Translation(text="", x=x, y=y))
        translations_list.append(translations)
    lp_output = get_lp_output([i.name for i in images], translations_list)
    output_dir = input_dir / "翻译_0.txt"
    with open(output_dir, "w", encoding="utf-8") as f:
        f.write(lp_output)
    print(f"Output saved to {output_dir}")


if __name__ == "__main__":
    main()
