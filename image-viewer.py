#!/usr/bin/env python
import time
import sys
import json
import time
import urllib.parse
import urllib.request
from PIL import Image, ImageFont, ImageDraw
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

img = Image.new("RGB", (64, 32), color=(0, 0, 0))
font = ImageFont.load("Silkscreen-8.pil")
draw = ImageDraw.Draw(img)
draw.text((3, 1), "Departures", font=font, fill="orange")

parameters = {
    "key": "blank",
    "stop_id": "PAR:2",
    "pt": "30",
    "count": "4"
}

options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.brightness = 55
options.chain_length = 1
options.pwm_lsb_nanoseconds = 270
options.hardware_mapping = "regular"

matrix = RGBMatrix(options=options)


def getcolor(h):
    if h == "000000":
        return "lightgray"
    else:
        return "rgb(" + str(tuple(int(h[m:m + 2], 16) for m in (0, 2, 4))).strip("()") + ")"


def xpos(x):
    if x > 9:
        return 50
    else:
        return 55


while True:
    try:
        url = "https://developer.cumtd.com/api/v2.2/json/" + "GetDeparturesByStop?" + urllib.parse.urlencode(parameters)

        response = urllib.request.urlopen(url)
        str_response = response.read().decode("utf-8")
        dictionary = json.loads(str_response)

        print(dictionary)
        length = (len(dictionary["departures"]))
        print("Buses as of " + dictionary["time"] + ":")
        if length == 0:
            print("No departures scheduled for this time.")
            draw.rectangle((0, 10, 64, 32), fill=(0, 0, 0))
            draw.text((3, 10), "Nothing", font=font, fill="white")
            draw.text((3, 19), "Scheduled.", font=font, fill="white")
            matrix.SetImage(img.convert("RGB"))
            img2 = img.copy()

        else:
            draw.rectangle((0, 10, 64, 32), fill=(0, 0, 0))
            for i in range(length):
                print(
                    dictionary["departures"][i]["headsign"] + "\t\t\t\t\t" + str(
                        dictionary["departures"][i]["expected_mins"]) + " minutes")
            print("----------------------------------------------------------")

            if length == 1:
                rng = 1
            else:
                rng = 2

            for j in range(rng):
                mins = dictionary["departures"][j]["expected_mins"]
                headsign = dictionary["departures"][j]["route"]["route_short_name"] + " " + \
                           dictionary["departures"][j]["route"]["route_long_name"].replace("Saturday", "").replace(
                               "Evening", "").replace("Weekend", "").replace("Sunday", "")
                draw.text((3, (10 + (j * 9))), headsign, font=font,
                          fill=getcolor(dictionary["departures"][j]["route"]["route_color"]))
                draw.text((xpos(mins), (10 + (j * 9))), str(mins), font=font,
                          fill="orange")
                img2 = img.copy()

            draw.rectangle((0, 10, 64, 32), fill=(0, 0, 0))
            for k in range(2, length):
                mins = dictionary["departures"][k]["expected_mins"]
                headsign = dictionary["departures"][k]["route"]["route_short_name"] + " " + \
                           dictionary["departures"][k]["route"]["route_long_name"].replace("Saturday", "").replace(
                               "Evening", "").replace("Weekend", "").replace("Sunday", "")
                draw.text((3, (10 + ((k - 2) * 9))), headsign, font=font,
                          fill=getcolor(dictionary["departures"][k]["route"]["route_color"]))
                draw.text((xpos(mins), (10 + ((k - 2) * 9))), str(mins), font=font,
                          fill="orange")

        for l in range(6):
            matrix.SetImage(img2.convert("RGB"))
            time.sleep(5)
            if length >= 3:
                matrix.SetImage(img.convert("RGB"))
                l += 1
                time.sleep(5)
            l += 1
    except KeyboardInterrupt:
        print("Ended by user.")
        break

    except urllib.error.URLError:
        print("Connection Error. Trying again in 30 seconds.")
        draw.rectangle((0, 10, 64, 32), fill=(0, 0, 0))
        draw.text((3, 10), "Connection", font=font, fill="white")
        draw.text((3, 19), "Error! X_X", font=font, fill="white")
        matrix.SetImage(img.convert("RGB"))
        time.sleep(30)
        continue

