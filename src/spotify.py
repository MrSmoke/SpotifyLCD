import urequests as requests
from models import CurrentTrack, ApiError
import ubinascii

SPOTIFY_API = "https://api.spotify.com/v1/"
OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"


def _make_authorization_headers(client_id: str, client_secret: str):
    auth_header = ubinascii.b2a_base64(
        (client_id + ":" + client_secret).encode("ascii"))
    return {'Authorization': 'Basic %s' % auth_header.decode('ascii').replace('\n', ''),
            'Content-Type': 'application/x-www-form-urlencoded'}


class Spotify:
    def __init__(self, client_id: str, client_secret: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret

    def get_currently_playing(self) -> CurrentTrack | ApiError | None:

        # Get the access token
        access_token = self._get_access_token()

        if access_token is None:
            return ApiError(0, "Access token error")

        json_data = None
        response = None
        try:

            headers = {
                'Authorization': 'Bearer {token}'.format(token=access_token)
            }

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

    def _get_access_token(self) -> str | None:
        data = "grant_type=client_credentials"
        headers = _make_authorization_headers(
            self.client_id, self.client_secret)

        response = None

        try:
            response = requests.post(OAUTH_TOKEN_URL,
                                     headers=headers,
                                     data=data,
                                     stream=True)

            if response.status_code is not 200:
                print(f"Failed to get spotify access token. {response.text}")
                return None

            token_json = response.json()

            return token_json['access_token']
        except Exception as ex:
            print(f"Failed to get Spotify access token: {ex=}, {type(ex)=}")
            return None
        finally:
            if response:
                response.close()
