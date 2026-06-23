import sys
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from canny import canny


def main(path, sigma=1.4, kernel_size=5, low_ratio=0.05, high_ratio=0.15):
    img = np.array(Image.open(path))
    out = canny(img, sigma=sigma, kernel_size=kernel_size,
                low_ratio=low_ratio, high_ratio=high_ratio)

    fig, axes = plt.subplots(2, 3, figsize=(12, 8))
    titles = ["Grayscale", "Gaussian smoothing", "Gradient magnitude",
              "Non-max suppression", "Double threshold", "Final edges"]
    keys = ["gray", "smoothed", "magnitude", "suppressed", "thresholded", "edges"]
    for ax, title, key in zip(axes.flat, titles, keys):
        ax.imshow(out[key], cmap="gray")
        ax.set_title(title)
        ax.axis("off")
    plt.tight_layout()
    plt.savefig("pipeline.png", dpi=150, bbox_inches="tight")
    Image.fromarray(out["edges"].astype(np.uint8)).save("edges.png")
    print("Saved: pipeline.png, edges.png")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <image_path> [sigma] [kernel_size] [low_ratio] [high_ratio]")
        sys.exit(1)
    args = sys.argv[1:]
    kwargs = {}
    if len(args) > 1: kwargs["sigma"] = float(args[1])
    if len(args) > 2: kwargs["kernel_size"] = int(args[2])
    if len(args) > 3: kwargs["low_ratio"] = float(args[3])
    if len(args) > 4: kwargs["high_ratio"] = float(args[4])
    main(args[0], **kwargs)
