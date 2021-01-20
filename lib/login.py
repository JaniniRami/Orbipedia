import requests
import credentials

def space_track_login():
    payload_login = {
        'identity': credentials.space_track_email,
        'password': credentials.space_track_password
        }

    with requests.Session() as session:
        login_url = "https://www.space-track.org/ajaxauth/login"

        try:
            session.get(login_url, timeout=5)
            session.post(login_url, data=payload_login)
        except (TimeoutError, ConnectionError, requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            print('[!] Connection Error')
            return 0
    return session
