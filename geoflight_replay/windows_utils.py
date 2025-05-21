import pyautogui
import pygetwindow as gw
from time import sleep
from .constants import DEFAULT_TOP_CROP_PIX

def show_available_windows():
    """
    Shows the list of available windows.
    """
    all_windows = [w.title for w in gw.getAllWindows() if w.title.strip()]
    if not all_windows:
        all_windows = ["(No windows detected)"]
    print("Available windows: ")
    print(all_windows)


def activate_and_maximize_window(window_title="Microsoft Flight Simulator", width=1024, height=1024):
    """
    Attempts to find a window with a title containing the given string and maximizes it.
    """
    try:
        winFS = gw.getWindowsWithTitle(window_title)[0]
    except IndexError:
        print(f"Could not find '{window_title}'")
        show_available_windows()
        return False

    pyautogui.press('altleft') # Workaround for allowing control and maximization of the window 
    winFS.activate()
    # sleep(1)
    # winFS.maximize()
    sleep(1)
    winFS.resizeTo(width+16,height+DEFAULT_TOP_CROP_PIX+8)

    return True