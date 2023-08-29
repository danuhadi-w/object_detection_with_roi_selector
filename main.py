from time import sleep
import time
from capture import Capture
import keyboard
from pynput.mouse import Button, Controller as MouseController
from multiprocessing import Process

sleep(2)

is_stopped = False
click_delay_s = 0.1
start_time = time.time()
last_click = time.time()
mouse = MouseController()
p1 = None


def break_loop():
    global is_stopped
    is_stopped = True
    p1.kill()


def start_loop(cap, action, t_name):
    global last_click
    while not is_stopped:
        click_pos = cap.detect()

        if click_pos is not None:
            if action == "click":
                if (time.time() - last_click) > click_delay_s:
                    mouse.position = click_pos
                    mouse.click(Button.left, 1)
                    last_click = (time.time())

    cap.on_break_loop()


if __name__ == '__main__':
    keyboard.add_hotkey("ctrl+alt+d", break_loop)

    capture1 = Capture("cap1")
    capture1.select_roi()
    sleep(3)
    capture1.select_target_img()

    frame_count = 0

    #
    p1 = Process(target=start_loop, args=(capture1, "click", "t1"))
    #
    p1.start()
    #
    p1.join()
