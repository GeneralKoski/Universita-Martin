import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from canny import canny


def sigma_comparison(path, sigmas=(0.8, 1.4, 2.5), out="sigma_comparison.png"):
    img = np.array(Image.open(path))
    fig, axes = plt.subplots(1, len(sigmas), figsize=(4 * len(sigmas), 4))
    for ax, s in zip(axes, sigmas):
        out_dict = canny(img, sigma=s, kernel_size=5)
        ax.imshow(out_dict["edges"], cmap="gray")
        ax.set_title(f"sigma = {s}")
        ax.axis("off")
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")


def threshold_comparison(path, configs=((0.05, 0.10), (0.05, 0.15), (0.10, 0.25)),
                          out="threshold_comparison.png"):
    img = np.array(Image.open(path))
    fig, axes = plt.subplots(1, len(configs), figsize=(4 * len(configs), 4))
    for ax, (lo, hi) in zip(axes, configs):
        out_dict = canny(img, sigma=1.4, low_ratio=lo, high_ratio=hi)
        ax.imshow(out_dict["edges"], cmap="gray")
        ax.set_title(f"low={lo}, high={hi}")
        ax.axis("off")
    plt.tight_layout()
    plt.savefig(out, dpi=150, bbox_inches="tight")
    print(f"Saved: {out}")


if __name__ == "__main__":
    import sys
    path = sys.argv[1] if len(sys.argv) > 1 else "test.jpg"
    sigma_comparison(path)
    threshold_comparison(path)
