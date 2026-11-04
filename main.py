import yeelight
import yeelight.flows
from time import sleep

def get_bulb() -> yeelight.Bulb:
    result = yeelight.discover_bulbs()
    global bulb_ip
    try:
        bulb_ip = result[0]['ip']
    except:
        bulb_ip = "192.168.1.153"
    bulb = yeelight.Bulb(bulb_ip)
    return bulb

def bulb_on():
    bulb = get_bulb()
    bulb.turn_on()

def bulb_off():
    bulb = get_bulb()
    bulb.turn_off()


def set_default_light(bulb:yeelight.Bulb):
    bulb.set_rgb(50, 50, 50)
    bulb.set_brightness(70)


if __name__ == "__main__":
    bulb = get_bulb()
    bulb.turn_on()

    #bulb.start_flow(yeelight.flows.police(70))
    #sleep(2.5)

    tr1 = [ yeelight.RGBTransition(255, 255, 255, duration=50, brightness=100)]
    flow1 = yeelight.Flow(count=0, action=yeelight.flow.Action.stay, transitions=tr1)
    tr2 = [ yeelight.RGBTransition(1, 1, 1, duration=50, brightness=2) ]
    flow2 = yeelight.Flow(count=0, action=yeelight.flow.Action.stay, transitions=tr2)

    def flick():
        dur = 0.1

        bulb.start_flow(flow1)
        sleep(dur)
        bulb.start_flow(flow2)

    def yeah():
        dur = 0.22

        flick()
        sleep(dur)

        flick()
        sleep(dur/2)
        flick()
        sleep(dur)

        flick()
        sleep(dur)
        flick()
        sleep(dur/2)
        flick()
        sleep(dur/2)
        flick()
        sleep(dur*3)




    bulb.set_rgb(255, 0, 0)
    sleep(1)
    yeah()
    yeah()

    bulb.set_rgb(50, 50, 50)