import numpy as np
from numpy.lib.stride_tricks import sliding_window_view


def to_grayscale(img):
    if img.ndim == 3:
        return 0.299 * img[:, :, 0] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 2]
    return img.astype(float)


def gaussian_kernel(size, sigma):
    ax = np.arange(-(size // 2), size // 2 + 1)
    xx, yy = np.meshgrid(ax, ax)
    k = np.exp(-(xx ** 2 + yy ** 2) / (2 * sigma ** 2))
    return k / k.sum()


def convolve2d(img, kernel):
    kh, kw = kernel.shape
    ph, pw = kh // 2, kw // 2
    padded = np.pad(img, ((ph, ph), (pw, pw)), mode="edge")
    windows = sliding_window_view(padded, (kh, kw))
    flipped = kernel[::-1, ::-1]
    return np.einsum("ijkl,kl->ij", windows, flipped)


SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
SOBEL_Y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)


def sobel_gradients(img):
    gx = convolve2d(img, SOBEL_X)
    gy = convolve2d(img, SOBEL_Y)
    magnitude = np.hypot(gx, gy)
    direction = np.arctan2(gy, gx)
    return magnitude, direction


def non_max_suppression(magnitude, direction):
    M, N = magnitude.shape
    out = np.zeros_like(magnitude)
    angle = (np.rad2deg(direction) % 180)

    for i in range(1, M - 1):
        for j in range(1, N - 1):
            a = angle[i, j]
            if a < 22.5 or a >= 157.5:
                q, r = magnitude[i, j + 1], magnitude[i, j - 1]
            elif a < 67.5:
                q, r = magnitude[i + 1, j - 1], magnitude[i - 1, j + 1]
            elif a < 112.5:
                q, r = magnitude[i + 1, j], magnitude[i - 1, j]
            else:
                q, r = magnitude[i - 1, j - 1], magnitude[i + 1, j + 1]
            if magnitude[i, j] >= q and magnitude[i, j] >= r:
                out[i, j] = magnitude[i, j]
    return out


def double_threshold(img, low_ratio=0.05, high_ratio=0.15):
    high = img.max() * high_ratio
    low = high * low_ratio
    weak, strong = 75.0, 255.0
    out = np.zeros_like(img)
    out[img >= high] = strong
    out[(img >= low) & (img < high)] = weak
    return out, weak, strong


def hysteresis(img, weak=75.0, strong=255.0):
    M, N = img.shape
    out = img.copy()
    changed = True
    while changed:
        changed = False
        for i in range(1, M - 1):
            for j in range(1, N - 1):
                if out[i, j] == weak:
                    if (out[i - 1:i + 2, j - 1:j + 2] == strong).any():
                        out[i, j] = strong
                        changed = True
    out[out != strong] = 0
    return out


def canny(img, sigma=1.4, kernel_size=5, low_ratio=0.05, high_ratio=0.15):
    gray = to_grayscale(img)
    smoothed = convolve2d(gray, gaussian_kernel(kernel_size, sigma))
    magnitude, direction = sobel_gradients(smoothed)
    suppressed = non_max_suppression(magnitude, direction)
    thresholded, weak, strong = double_threshold(suppressed, low_ratio, high_ratio)
    edges = hysteresis(thresholded, weak, strong)
    return {
        "gray": gray,
        "smoothed": smoothed,
        "magnitude": magnitude,
        "direction": direction,
        "suppressed": suppressed,
        "thresholded": thresholded,
        "edges": edges,
    }
