import win32gui, win32api, win32ui, win32con

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


def main():
    getScreenshot()

if __name__ == '__main__':
    main()
