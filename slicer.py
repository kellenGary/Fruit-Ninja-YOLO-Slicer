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
    sorted_fruit = sorted(fruits, key=lambda fruit: get_distance(pyautogui.position(), fruit))
    for fruit in sorted_fruit:
        x2, y2 = fruit
        pyautogui.mouseDown()
        pyautogui.moveTo(x2 * 5, y2 * 5)
        pyautogui.mouseUp()


def sort_slice(fruits):
    """Method to slice all fruits sorted by their x coord"""
    sorted_fruits = sorted(fruits, key=lambda fruit: fruit[0])
    x1, y1 = sorted_fruits[0]
    pyautogui.mouseDown()
    for i in range(1, len(sorted_fruits)):
        pyautogui.moveTo(x1, y1)
        x2, y2 = sorted_fruits[i]
        pyautogui.moveTo(x2, y2)
        x1, y1 = x2, y2
    pyautogui.mouseUp()


def find_fruit(results):
    """Function to store fruits using their bounding box location"""
    fruits = []
    for result in results:
        for box in result.boxes:
            if classes_names[int(box.cls)] == 'fruit' and box.conf > 0.8:
                cx, cy = get_mid_point(box)
                fruits.append((cx, cy))
    return fruits
