#!/usr/bin/env python3

#Mathajas
#Showing battery state on screen of Vector Face.



import anki_vector
import sys
import time

from anki_vector.util import degrees

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    sys.exit("Cannot import from PIL. Do `pip3 install --user Pillow` to install")

def calulate_butt(_hm_butt):
    # calulate battery
    # zero = 3.5 100% = 4.3
    hm_butt = _hm_butt-3.5
    proc = (hm_butt/0.8)
    if proc>100: proc=100
    return proc

def make_batt_image(_proc_butt):
    '''Make a PIL.Image with the given text printed on it

   Args:
       text_to_draw (string): the text to draw to the image
       x (int): x pixel location
       y (int): y pixel location
       font (PIL.ImageFont): the font to use

   Returns:
       :class:(`PIL.Image.Image`): a PIL image with the text drawn on it
   '''
    dimensions = (184, 96)
    loaded = 110-(110*_proc_butt)
    if loaded<0: loaded=0
    print ("loaded: " + str(loaded))
    shape1 = [(40, 20), (154, 76)]
    shape2 = [(28, 40), (40, 56)]
    shape3 = [(42+loaded,22),(152,74)]
    # make a blank image for the text, initialized to opaque black
    batt_image_bg = Image.new('RGB', dimensions, (0, 0, 0, 255))

    # get a drawing context
    sq1 = ImageDraw.Draw(batt_image_bg)
    sq1.rectangle(shape1, fill="#9ca79b")
    sq1.rectangle(shape2, fill="#9ca79b")
    if _proc_butt > 0.5 : sq1.rectangle(shape3, fill="#004e36")
    elif _proc_butt > 0.3 : sq1.rectangle(shape3, fill="#eeb932")
    else : sq1.rectangle(shape3, fill="#7d0d2b")
    return batt_image_bg




# Set text to create image from here


def main():
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial) as robot:

        # If necessary, Move Vector's Head and Lift to make it easy to see his face
        robot.behavior.set_head_angle(degrees(40.0))
        robot.behavior.set_lift_height(0.0)
        #get battery state and add it to text;
        battery_state = robot.get_battery_state()
        if battery_state:
            hm_butt = battery_state.battery_volts
            print("hm_butt: " + str(hm_butt))
            proc_butt = calulate_butt(hm_butt)
            print(proc_butt)
        face_image = make_batt_image(proc_butt)

        # Convert the image to the format used by the Screen
        print("Display Battery on Vector's face...")
        screen_data = anki_vector.screen.convert_image_to_screen_data(
            face_image)
        robot.screen.set_screen_with_image_data(screen_data, 5.0, interrupt_running=True)
        print("Sleep 5s")
        time.sleep(5)
        print("Disconnect")

if __name__ == "__main__":
    main()
