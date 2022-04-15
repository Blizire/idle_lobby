import win32gui
import win32ui
import win32con

# credit for this function:
# https://stackoverflow.com/questions/1080719/screenshot-an-application-regardless-of-whats-in-front-of-it
def background_screenshot(hwnd, resolution):
    # unpack given resolution
    # todo: make routine function thatl take "int x int" format and unpack
    width, height = resolution
    # get window handle device context reference
    wDC = win32gui.GetWindowDC(hwnd)
    # create device context object from a dc handle
    dcObj=win32ui.CreateDCFromHandle(wDC)
    # creates compatible device context ( not sure exactly what this means )
    cDC=dcObj.CreateCompatibleDC()
    # create empty bitmap object
    dataBitMap = win32ui.CreateBitmap()
    # edit the bitmap object to be built against our dimensions and window
    dataBitMap.CreateCompatibleBitmap(dcObj, width, height)
    # the device context we've made targeting the bitmap object
    cDC.SelectObject(dataBitMap)
    # load screen shot data into empty bitmap
    cDC.BitBlt((0,0),(width, height) , dcObj, (0,0), win32con.SRCCOPY)
    # save to disk
    dataBitMap.SaveBitmapFile(cDC, 'screenshot.bmp')
    # memory cleanup
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

hwnd = win32gui.FindWindow(None, "Overwatch")
resolution = (3840, 2160)
background_screenshot(hwnd, resolution)