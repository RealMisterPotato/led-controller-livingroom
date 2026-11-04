from main import get_bulb, set_default_light
from PIL import Image, ImageGrab
from time import sleep
import numpy as np
import argparse
from yeelight import Bulb, BulbException, flows

def snap_screen() -> Image:
    screenshot_image = ImageGrab.grab()
    return screenshot_image

def avarage_pixel_value_rgb(image:Image, alpha):
    img = image
    flattened = img.get_flattened_data()
    arr = np.array(flattened)

    # 1. Calculate raw vividness (standard deviation per pixel)
    vividness = np.std(arr, axis=1)

    # Normalize vividness between 0 and 1 so it plays nicely with alpha
    if np.max(vividness) > 0:
        vividness_norm = vividness / np.max(vividness)
    else:
        vividness_norm = np.zeros_like(vividness)

    # 2. Control Parameter (0.0 = completely equal weights, 1.0 = gray gets zero weight)
    # Lower this value to give gray pixels more influence!
    _alpha = alpha

    # 3. Calculate final blended weights
    weights = _alpha * vividness_norm + (1 - _alpha)

    # 4. Compute the weighted average
    weighted_rgb_avg = np.average(arr, axis=0, weights=weights)

    return weighted_rgb_avg



if __name__ == "__main__":
    # arguments
    parser = argparse.ArgumentParser("Track the screen's average pixel color and set it to the LED light in realtime.")
    parser.add_argument("-a", "--alpha", type=float, default=0.92, help="Influence of colors other than the greyscale colors")
    parser.add_argument("-d", "--delay", type=int, default=400, help="Delay in ms between each iteration")
    parser.add_argument("-t", "--threshold", type=int, default=30, help="Sum of change in rgb value to trigger a call")
    parser.add_argument("-f", "--force", action="store_true", help="Continue even if a bulb exception is raised")
    args = parser.parse_args();
    delay = args.delay/1000

    # ensure the bulb is on
    bulb:Bulb = get_bulb()
    bulb.ensure_on()
    prev_rgb_value = None
    try:
        while True:
            image = snap_screen()
            avg = avarage_pixel_value_rgb(image, args.alpha)
            avg = (int(avg[0]), int(avg[1]), int(avg[2]))
            try:
                # calculate change in rgb sum
                if prev_rgb_value != None:
                    diff = (abs(prev_rgb_value[0] - avg[0]), abs(prev_rgb_value[1] - avg[1]), abs(prev_rgb_value[2] - avg[2]))
                    sum_diff = diff[0] + diff[1] + diff[2]
                    print("Difference in RGB values:")
                    print(str(diff) + ", " + str(sum_diff) + "\n\n")

                if prev_rgb_value == None or sum_diff >= args.threshold:
                    bulb.set_rgb(avg[0], avg[1], avg[2])
                    tup_max = max(avg[0], max(avg[1], avg[2]))
                    rel = float(tup_max/255)
                    brightness = rel*100
                    bulb.set_brightness(brightness)
                    print(f"Set: RGB={avg}, Brightness={brightness}%\n\n")
                    prev_rgb_value = avg

                sleep(delay)
            except BulbException:
                print("bulbexception")
                if not args.force:
                    raise BulbException
                sleep(1)
    except KeyboardInterrupt:
        bulb.set_rgb(0, 50, 200)
        bulb.set_brightness(100)
        sleep(1)
    finally:
        set_default_light(bulb)