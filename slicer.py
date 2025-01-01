import math
import pyautogui


# List of class names
classes_names = ['fruit', 'ignore']


def get_mid_point(box):
    """Get the current midpoint of the given fruit"""
    x1, y1, x2, y2 = map(int, box.xyxy[0])
    cx = (x1 + x2) // 2
    cy = (y1 + y2) // 2
    return cx, cy


def get_distance(cursor, fruit):
    """Calculates the distance that a fruit is from the cursor location"""
    return math.sqrt((fruit[0] - cursor[0])**2 + (fruit[1] - cursor[1])**2)


def one_slice(fruits):
    """"Method used to slice one fruit at a time based on distance from mouse"""
    pyautogui.mouseDown()
    i = 0
    while fruits:
        fruits = sorted(fruits, key=lambda fruit: get_distance(pyautogui.position(), fruit))
        fruit = fruits[i]
        del fruits[i]
        x2, y2 = fruit
        pyautogui.moveTo(x2 * 0.5, y2 * 0.5)
    pyautogui.mouseUp()


def find_fruit(results):
    """Function to store fruits using their bounding box location"""
    fruits = []
    for result in results:
        for box in result.boxes:
            if classes_names[int(box.cls)] == 'fruit' and box.conf > 0.8:
                cx, cy = get_mid_point(box)
                if cy < 1750:
                    fruits.append((cx, cy))
    return fruits
