import requests


def get_input_text_from_url(day):
    """
    Returns:
        string: The text of the response (puzzle input)
    Raises:
        ValueError: Session cookie is invalid
    """
    # NOTE: the cookie might need to be refreshed
    session_cookie = '53616c7465645f5f6104714e96b2eff50399bd7e83c39c81a77c07927958a02bd0ae33e547765235a01e7d3fed18d1ec'
    cookies = {'session': session_cookie}

    try:
        resp = requests.get(f'https://adventofcode.com/2020/day/{day}/input',
                            cookies=cookies)
    except requests.exceptions.ConnectionError:
        print('[ERROR] Could not connect to url')
        raise ConnectionError

    if resp.status_code == 400:
        print(f'[ERROR] {resp.text}')
        raise ValueError('Invalid session cookie')

    return resp.text[:-1]  # remove the last \n


def get_example_input():
    with open('temp.txt', 'r') as f:
        return f.read()
