import requests


def get_input_text(day):
    with open(f'inputs/day{day}.txt', 'r') as f:
        return f.read()


def get_example_input_text():
    with open('inputs/example.txt', 'r') as f:
        return f.read()


def get_input_text_from_url(day):
    """
    Returns:
        string: The text of the response (puzzle input)
    Raises:
        ValueError: Session cookie is invalid
    """
    # NOTE: the cookie might need to be refreshed
    session_cookie = '53616c7465645f5f1a10e5e3e3d5b62fde22c33527146dda7a6d25fd1625fd3e3edb12d1facb663c0eb269932ec5b039'
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
