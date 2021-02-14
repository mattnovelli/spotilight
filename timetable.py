import json
import time
import urllib.parse
import urllib.request
from PIL import Image, ImageFont, ImageDraw
#from rgbmatrix import RGBMatrix, RGBMatrixOptions

img = Image.new('RGB', (64, 32), color=(0, 0, 0))
font = ImageFont.load("Silkscreen-8.pil")
draw = ImageDraw.Draw(img)
draw.text((3, 1), "Departures", font=font, fill='orange')

parameters = {
    "key": "blank",
    "stop_id": "PAR:2",
    "pt": "30",
    "count": "4"
}


def getcolor(h):
    if h == "000000":
        return "lightgray"
    else:
        return 'rgb(' + str(tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))).strip('()') + ')'


def xpos(x):
    if x > 9:
        return 50
    else:
        return 55



try:
    while True:
        url = "https://developer.cumtd.com/api/v2.2/json/" + "GetDeparturesByStop?" + urllib.parse.urlencode(parameters)

        dictionary = json.load(urllib.request.urlopen(url))

        print(dictionary)
        length = (len(dictionary["departures"]))
        if len(dictionary["departures"]) == 0:
            print("No departures scheduled for this time.")
            draw.text((3, 10), "Nothing", font=font, fill='white')
            draw.text((3, 19), "Scheduled.", font=font, fill='white')
            img.save("board1.ppm", format="ppm")
            img.save("board2.ppm", format="ppm")

        else:
            draw.rectangle((0, 10, 64, 32), fill=(0, 0, 0))
            for i in range(length):
                print(
                    dictionary["departures"][i]["headsign"] + "\t\t\t\t\t" + str(
                        dictionary["departures"][i]["expected_mins"]) + " minutes")
            for j in range(1):
                mins = dictionary["departures"][j]["expected_mins"]
                headsign = dictionary["departures"][j]["route"]["route_short_name"] + " " + \
                           dictionary["departures"][j]["route"]["route_long_name"].replace("Saturday", "").replace("Evening", "").replace("Weekend", "")
                draw.text((3, (10 + (j * 9))), headsign, font=font,
                          fill=getcolor(dictionary["departures"][j]["route"]["route_color"]))
                draw.text((xpos(mins), (10 + (j * 9))), str(mins), font=font,
                          fill="orange")

            img.save("board1.ppm", format="ppm")
            draw.rectangle((0, 10, 64, 32), fill=(0, 0, 0))
            for k in range(2, length):
                mins = dictionary["departures"][k]["expected_mins"]
                headsign = dictionary["departures"][k]["route"]["route_short_name"] + " " + \
                           dictionary["departures"][k]["route"]["route_long_name"]
                draw.text((3, (10 + ((k - 2) * 9))), headsign, font=font,
                          fill=getcolor(dictionary["departures"][k]["route"]["route_color"]))
                draw.text((xpos(mins), (10 + ((k - 2) * 9))), str(mins), font=font,
                          fill="orange")
                img.save("board2.ppm", format="ppm")
        time.sleep(30)
except KeyboardInterrupt:
    print("Ended by user.")

except urllib.error.URLError:
    print("Connection Error.")
    draw.text((3, 10), "Connection", font=font, fill='white')
    draw.text((3, 19), "Error! X_X", font=font, fill='white')
    img.save("board1.ppm", format="ppm")
    img.save("board2.ppm", format="ppm")
