This package is modified from [dmMaze/comic-text-detector](https://github.com/dmMaze/comic-text-detector).

## Example

```python
from comic_text_detector import TextDetector, detect_blocks
import torch

model_path = "data/comictextdetector.pt"
image_path = "data/input.jpg"
device = "cuda" if torch.cuda.is_available() else "cpu"
model = TextDetector(
    model_path=model_path, input_size=1024, device=device, act="leaky"
)
blocks = detect_blocks(model, image_path)
for block in blocks:
    print(block.left, block.top, block.right, block.bottom)
```
