from main import get_bulb
import time
import random
from sys import argv
import argparse




if __name__ == "__main__":

    #args
    parser = argparse.ArgumentParser(description="Switch between random LED colors")
    parser.add_argument("-c", "--count", type=int, default=10, help="Amount of iterations")
    parser.add_argument("-d", "--delay", type=int, default=100, help="Delay in ms between each iteration")
    args = parser.parse_args()
    count = int(args.count)
    delay = float(args.delay)/1000

    bulb = get_bulb()
    for i in range(count):
        bulb.set_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        time.sleep(delay)