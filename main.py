import math
import threading
import keyboard
import numpy as np
import torch
import pyautogui
from ultralytics import YOLO
from mss import mss
from PIL import Image

model = YOLO('fruit-ninja-modelv5s.pt')
device = 'cuda' if torch.cuda.is_available() else 'cpu'

sct = mss()


# List of class names
classes_names = ['fruit', 'ignore']


def get_mid_point(box):
    """Get the current midpoint of the given fruit"""
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    return cx, cy


def find_fruits(results):
    fruits = []
    for result in results:
        for box in result.boxes:
            if classes_names[int(box.cls)] == 'fruit' and box.conf > 0.8:
                cx, cy = get_mid_point(box)
                if cy < 850:
                    fruits.append((cx, cy))
    return fruits


def get_distance(cursor, fruit):
    """Calculates the distance that a fruit is from the cursor location"""
    return math.sqrt((fruit[0] - cursor[0])**2 + (fruit[1] - cursor[1])**2)


def slice_fruits(fruits):
    print(fruits)
    while fruits:
        fruits = sorted(fruits, key=lambda fruit: get_distance(pyautogui.position(), fruit))
        fruit = fruits[0]
        del fruits[0]

        x, y = fruit
        pyautogui.mouseDown(_pause=False)
        pyautogui.moveTo(x, y, duration=0.0, _pause=False)
        pyautogui.mouseUp(_pause=False)


def read_image(stop_event, fruits_seen):
    """Use model to find fruits in the current frame"""
    while not stop_event.is_set():
        laptop = {"top": 100, "left": 100, "width": 1528, "height": 917}
        monitor = {"top": 60, "left": 0, "width": 1280, "height": 720}
        screenshot = sct.grab(monitor)
        img = np.array(Image.frombytes("RGB", (screenshot.width, screenshot.height), screenshot.rgb))

        results = model(source=img, device=device, verbose=False, iou=0.25, conf=0.85, int8=True)
        fruits = find_fruits(results)
        fruits_seen[0] += len(fruits)
        slice_fruits(fruits)
    return fruits_seen


def print_accuracy(misses, fruits_seen):
    hits = fruits_seen - misses
    accuracy = hits / fruits_seen[0] * 100
    print(f"Accuracy: {accuracy}")


def main():
    misses = 0
    fruits_seen = [0]
    stop_event = threading.Event()
    program_thread = threading.Thread(target=read_image, args=(stop_event, fruits_seen))
    program_thread.start()
    if keyboard.is_pressed('m'):
        misses += 1
    keyboard.wait("q")
    stop_event.set()
    program_thread.join()
    sct.close()
    print_accuracy(misses, fruits_seen)


if __name__ == "__main__":
    main()

