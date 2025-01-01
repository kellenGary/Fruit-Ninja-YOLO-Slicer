import os
from mss import mss
from PIL import Image


interval = 0.1
output_dir = os.path.abspath("./Data")
os.makedirs(output_dir, exist_ok=True)


def take_screenshot(count, output_dir):
    """
    Takes a screenshot of the top left of screen.
    this is optimized for my personal monitor so adjust this for your device.
    """
    monitor = {"top": 60, "left": 0, "width": 1280, "height": 720}
    laptop = {"top": 100, "left": 100, "width": 1528, "height": 917}

    with mss() as sct:
        screenshot = sct.grab(laptop)
        img = Image.frombytes(
            "RGB",
            (screenshot.width, screenshot.height),
            screenshot.rgb
        )

        # Uncomment these two lines to save images to Data folder
        path = os.path.join(output_dir, f"image_{count}.jpg")
        img.save(path, format="JPEG")

        # Resize the image (reduce it to 1/5th of its original size)
        new_size = (int(img.width), int(img.height))
        img = img.resize(new_size)
    return img


def clear_dir(directory):
    """Clears directory if we are saving the images."""
    if not os.path.exists(directory):
        os.makedirs(directory)
    else:
        files = os.listdir(directory)
        for f in files:
            file_path = os.path.join(directory, f)
            if os.path.isfile(file_path):
                os.remove(file_path)

