import cv2
import numpy as np
from PIL import ImageGrab,Image
import pyautogui
from pynput import keyboard

def capture_and_find():
    # Capture screenshot

    screen = np.array(ImageGrab.grab())


    # Get cursor position
    # try:
    #     while True:
    x, y = pyautogui.position()
    print(x,y)
    # except Exception as e:
    #     logging.error(traceback.format_exc())

    # Define area around cursor
    width, height = 10, 10  # Adjust size as needed
    top_left_x, top_left_y = x - width // 2, y - height // 2
    bottom_right_x, bottom_right_y = x + width // 2, y + height // 2

    # Extract image from screenshot
    image = screen[top_left_y:bottom_right_y, top_left_x:bottom_right_x]



    # Convert to grayscale for template matching
    test = Image.fromarray(image)

    # Template matching
    result = cv2.matchTemplate(screen, image, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9  # Adjust threshold as needed
    loc = np.where(result >= threshold)

    # Highlight matches
    for pt in zip(*loc[::-1]):
        bottom_right = (pt[0] + 25, pt[1] + 25)
        cv2.rectangle(screen, pt, bottom_right, (0, 0, 255), 2)

    # Display result
    screenS = screen[50:595,0:769]
    cv2.imshow('Result', screenS)
    cv2.moveWindow("Result", -1024, 768)
    cv2.waitKey(1)

def main():
    def on_press(key):
        if key == keyboard.Key.space:
            capture_and_find()
    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\nProgram interrupted by user.")
    """
    while True:
        capture_and_find()
        if cv2.waitKey(1) & 0xFF == ord(' '):
            cv2.destroyAllWindows()
            break
    """


if __name__ == "__main__":
    main()
