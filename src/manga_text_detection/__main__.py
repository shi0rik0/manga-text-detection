from .comic_text_detector import TextDetector, detect_blocks
from .labelplus import get_lp_output, Translation, MangaPage

import win32com.client
import torch
import cv2
import numpy as np
from typing import Optional, List
from pathlib import Path

MODEL_PATH = "data/comictextdetector.pt"


def imread(imgpath, read_type=cv2.IMREAD_COLOR):
    """Use this instead of cv2.imread() to read image with non-ASCII characters in path."""
    return cv2.imdecode(np.fromfile(imgpath, dtype=np.uint8), read_type)


def select_folder() -> Optional[str]:
    shell = win32com.client.Dispatch("Shell.Application")
    folder = shell.BrowseForFolder(0, "选择一个文件夹", 0)

    if folder:
        folder_path = folder.Items().Item().Path
        return folder_path
    else:
        return None


def main_wrapper(func):
    """Decorator to handle exceptions and print error messages."""

    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"发生错误: {e}")
        input("按 Enter 键退出...")

    return wrapper


@main_wrapper
def main():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"PyTorch 使用的设备: {device}")
    detector = TextDetector(
        model_path=MODEL_PATH, input_size=1024, device=device, act="leaky"
    )
    folder = select_folder()

    if not folder:
        print("没有选择文件夹")
        return

    print(f"选择的文件夹: {folder}")
    folder = Path(folder)

    if not folder.is_dir():
        print(f"{folder} 不是一个有效的文件夹")
        return

    blocks_list = []

    image_files = [
        i
        for i in folder.iterdir()
        if i.is_file() and i.suffix.lower() in [".jpg", ".jpeg", ".png"]
    ]
    image_files.sort(key=lambda x: x.name)

    for i, v in enumerate(image_files):
        print(f"正在处理第 {i+1}/{len(image_files)} 个图片: {v.name}")
        blocks = detect_blocks(detector, str(v))
        blocks_list.append((v, blocks))

    pages: List[MangaPage] = []

    for file, blocks in blocks_list:
        img = imread(str(file))
        height, width = img.shape[:2]
        translations = []

        for i in blocks:
            text = ""
            x = (i.left + i.right) / 2
            y = (i.top + i.bottom) / 2
            translations.append(Translation(text, x, y))

        page = MangaPage(file.name, width, height, translations)
        pages.append(page)

    lp_output = get_lp_output(pages)

    with open(folder / "翻译_0.txt", "w", encoding="utf-8") as f:
        f.write(lp_output)

    print('标注结果已保存到 "翻译_0.txt"')


if __name__ == "__main__":
    main()
