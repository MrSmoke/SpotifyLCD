from config import Config
from time import sleep
import network
import machine
import uasyncio as asyncio

from spotify import Spotify
from display import Display
from models import CurrentTrack, ApiError

# 1 sec sleep at the start to make it easier to read all the console output
sleep(1)

# Load the config
config = Config('config.json')

# Create a new instance of our display before we start
display = Display(columns=int(config.get('lcd.columns')),
                  rows=int(config.get('lcd.rows')))

# Initialise spotify
spotify = Spotify(client_id=config.get('spotify.clientId'),
                  client_secret=config.get('spotify.clientSecret'))

def get_display_text(currently_playing) -> list[str]:

    if type(currently_playing) is ApiError:
        return ["API Error - " + str(currently_playing.status_code), currently_playing.message]

    if type(currently_playing) is CurrentTrack:
        return [currently_playing.name, currently_playing.artist]

    return ["", ""]


async def connect():
    # Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    count = 0

    if not wlan.active():
        print("Wlan not active")
        wlan.active(True)

    ssid = config.get('wifi.ssid')

    if not wlan.isconnected():
        print(f"Connecting to wlan...{ssid}")
        wlan.connect(config.get('wifi.ssid'), config.get('wifi.password'))

    while not wlan.isconnected():
        count += 1
        print(f'[{count}] Waiting for connection...')
        await asyncio.sleep(1)

    print(wlan.ifconfig())

# The main function
async def main():
    display.on()
    display.print_lines(["Connecting to Wifi..."])

    print("Starting...")

    # Connect to the WiFi
    try:
        await connect()
    except KeyboardInterrupt:
        print("stopped.")
        exit()

    # Turn on LED to say we are ready
    led = machine.Pin("LED", machine.Pin.OUT)
    led.on()

    display.print_lines(["Connected!"])

    # Start the main loop
    while True:
        current_track = spotify.get_currently_playing()

        if current_track is None:
            # Turn off display as there is nothing playing
            display.off()

        else:
            # Ensure the display is on
            display.on()

            text_lines = get_display_text(current_track)
            display.print_lines(text_lines)

        await asyncio.sleep(10)

try:
    asyncio.run(main())
finally:
    asyncio.new_event_loop()
