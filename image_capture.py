import os
from mss import mss
from PIL import Image


def take_screenshot(count, output_dir):
    """
    Takes a screenshot of the top left of screen.
    this is optimized for my personal monitor so adjust this for your device.
    """
    phone = {"top": 60, "left": 0, "width": 1280, "height": 720}

    with mss() as sct:
        screenshot = sct.grab(phone)
        img = Image.frombytes(
            "RGB",
            (screenshot.width, screenshot.height),
            screenshot.rgb
        )

        # Uncomment these two lines to save images to Data folder
        # path = os.path.join(output_dir, f"image_{count}.jpg")
        # img.save(path, format="JPEG")

        # Resize the image (reduce it to 1/5th of its original size)
        new_size = (int(img.width / 5), int(img.height / 5))
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

