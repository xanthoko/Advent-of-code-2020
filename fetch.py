import sys
from utils import get_input_text_from_url

if len(sys.argv) < 2:
    print('Specify a day')
    exit()
day = sys.argv[1]
input_text = get_input_text_from_url(day)
with open(f'inputs/day{day}.txt', 'w') as f:
    f.write(input_text)
