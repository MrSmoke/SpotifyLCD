import urequests as requests
from models import CurrentTrack, ApiError

SPOTIFY_API = "https://api.spotify.com/v1/"


headers = {
    'Authorization': 'Bearer {token}'.format(token="todo")
}


def get_currently_playing() -> CurrentTrack | ApiError | None:
    response = None
    json_data = None

    try:
        response = requests.get(url=SPOTIFY_API + "me/player/currently-playing",
                                headers=headers,
                                stream=True)

        status_code = response.status_code

        # If we have no content, then we have no track playing, so return nothing
        if status_code == 204:
            return None

        json_data = response.json()

    except Exception as ex:
        print(f"Failed to access Spotify: {ex=}, {type(ex)=}")
        return ApiError(0, "Failed to access Spotify")

    finally:
        if response:
            response.close()

    error = json_data.get("error")

    # Check if we have an error and if we do, return that
    if error is not None:
        return ApiError(status_code, error.get("message", ""))

    # Extract the track data and return a CurrentTrack object
    track = json_data["item"]
    artist_names = (artist["name"] for artist in track["artists"])

    return CurrentTrack(name=track["name"], artist=", ".join(artist_names), album="Unknown", is_playing=json_data["is_playing"])
