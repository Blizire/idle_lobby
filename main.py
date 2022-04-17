import win32gui
import win32ui
import win32con

from PIL import Image

# credit for this function:
# https://stackoverflow.com/questions/1080719/screenshot-an-application-regardless-of-whats-in-front-of-it
def background_screenshot(hwnd, resolution, filename="screenshot.bmp"):
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
    dataBitMap.SaveBitmapFile(cDC, filename)
    # memory cleanup
    dcObj.DeleteDC()
    cDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, wDC)
    win32gui.DeleteObject(dataBitMap.GetHandle())

# returns a mapping of all pixels
def get_pixel_map(filename):
    with Image.open(filename) as im:
        return im.getdata()

# gets the difference between two images and returns it as a percentage
def get_image_difference(pixel_array_one, pixel_array_two, max_pixel_count):
    diff_score = 1
    # iterates through both arrays and compares if the pixels are different
    for (idle_pixel, active_pixel) in zip(pixel_array_one, pixel_array_two):
        if idle_pixel == active_pixel:
            pass
        else:
            diff_score += 1
    # converts final total difference of pixels to a percentage
    diff_score_percentage = (diff_score / max_pixel_count) * 100
    return round(diff_score_percentage, 2)
    

def scanner(hwnd, resolution):
    # resolution should be the games resolution size
    width, height = resolution
    max_pixel_count = width * height

    # this will capture the initial screen that should be of the idle lobby
    background_screenshot(hwnd, resolution, filename="screenshot.bmp")
    idle_pixel_map = get_pixel_map("screenshot.bmp")
    
    # todo: write loop that scans background window continously

    # recapturing to see screen difference from here on out
    background_screenshot(hwnd, resolution, filename="active.bmp")
    active_pixel_map = get_pixel_map("active.bmp")

    # compares the the screen compared to the idle lobby capture
    # for different games the difference will have a negligible
    # difference because of animated backgrounds.
    diff_percentage = get_image_difference(idle_pixel_map, active_pixel_map, max_pixel_count)

    print(f"screen difference : {diff_percentage}%")

    return



hwnd = win32gui.FindWindow(None, "debug")
resolution = (3840, 2160)
scanner(hwnd, resolution)
print("finished.")



