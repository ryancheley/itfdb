from sense_hat import SenseHat
from datetime import datetime
import pytz
import os
import csv
from dateutil.relativedelta import relativedelta
from data_types import Schedule


def main():
    filename = get_data_file()
    data = load_file(filename)
    sense = SenseHat()
    local_tz = pytz.timezone('America/Los_Angeles')
    utc_now = pytz.utc.localize(datetime.utcnow())
    now = utc_now.astimezone(local_tz)
    for game in data:
        game_date_time = datetime.strptime(game.game_date_time, '%Y-%m-%d %I:%M %p')
        game_date_time = local_tz.localize(game_date_time)
        minute_diff = relativedelta(now, game_date_time).minutes
        hour_diff = relativedelta(now, game_date_time).hours
        day_diff = relativedelta(now, game_date_time).days
        if day_diff == 0 and hour_diff == 0 and 0 >= minute_diff >= -10:
            message = '#ITFDB!!! The Dodgers will be playing {} at {}'.format(game.game_opponent, game.game_time)
            sense.show_message(message, scroll_speed=0.05)


def get_data_file():
    base_folder = os.path.dirname(__file__)
    return os.path.join(base_folder,
                        'schedule.csv')


def load_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as fin:

        reader = csv.DictReader(fin)
        schedule = []
        for row in reader:
            p = Schedule.create_from_dict(row)
            schedule.append(p)

        return schedule


if __name__ == '__main__':
    main()
