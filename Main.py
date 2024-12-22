from pynput import keyboard
import time
import os
import image_capture
import slicer
from ultralytics import YOLO


model = YOLO('fruit-ninja-model.pt')


def on_press(key):
    """Monitors keyboard input to check for a q to quit"""
    try:
        if key.char == 'q':
            return False
    except AttributeError:
        pass


def read_image(img):
    """Use model to find fruits in the current frame"""
    results = model.predict(source=img, conf=0.85)
    if results:
        fruits = slicer.find_fruit(results)
        if fruits:
            slicer.sort_slice(fruits)


def execute_program(output_dir, interval):
    """Main thread to execute program"""
    image_capture.clear_dir(output_dir)
    with keyboard.Listener(on_press=on_press) as listener:
        count = 1
        while listener.running:
            img = image_capture.take_screenshot(count, output_dir)
            read_image(img)
            time.sleep(interval)
            count += 1


if __name__ == "__main__":
    output_directory = os.path.abspath("./../Data")
    execute_program(output_directory, interval=0.0001)
