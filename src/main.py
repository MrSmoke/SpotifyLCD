from time import sleep
import spotify
from display import Display
from models import CurrentTrack, ApiError


def get_display_text(currently_playing: CurrentTrack | ApiError) -> list[str]:
    match currently_playing:
        case ApiError() as error:
            return ["API Error - " + str(error.status_code), error.message]

        case CurrentTrack():
            # print("Currently playing: \"{track.name}\" - \"{track.artist}\". Playing: {track.is_playing}".format(track=playing))
            return [currently_playing.name, currently_playing.artist]

        case _:
            return ["", ""]


# Create a new instance of our display before we start
display = Display(columns=20, rows=2)

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

    sleep(10)
