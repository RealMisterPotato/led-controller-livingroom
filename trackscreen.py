from main import get_bulb
import mss
from PIL import Image
from time import sleep

IMG_SRC = "/tmp/screenshot_bulb.png"

def snap_screen():
    with mss.MSS() as sct:
        sct.shot(output=IMG_SRC)

def avarage_pixel_value_rgb(image_src:str):
    img = Image.open(image_src)
    avgpixel = (0, 0, 0)
    flattened = img.get_flattened_data()
    for pixelval in flattened:
        #print(f"(R: {pixelval[0]}, G: {pixelval[1]}, B: {pixelval[2]})")
        avgpixel = tuple(x+y for x, y in zip(avgpixel, pixelval))
    avgpixel = tuple(int(x/len(flattened)) for x in avgpixel)
    avgpixel = tuple((x if x > 0 else 1) for x in avgpixel)
    #print(avgpixel)
    return avgpixel



if __name__ == "__main__":
    bulb = get_bulb()
    bulb.ensure_on()
    try:
        for i in range(100):
            snap_screen()
            avg = avarage_pixel_value_rgb(IMG_SRC)
            bulb.set_rgb(avg[0], avg[1], avg[2])
            print(avg)
            sleep(2)
    except KeyboardInterrupt:
        bulb.set_rgb(50, 50, 50)