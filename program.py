#from sense_hat import SenseHat
from datetime import datetime
import pytz
import os
import csv

from data_types import Schedule


def main():
    filename = get_data_file()
    data = load_file(filename)
    #sense = SenseHat()
    utc_now = pytz.utc.localize(datetime.utcnow())
    now = pst_now = utc_now.astimezone(pytz.timezone("America/Los_Angeles"))
    message = '#ITFDB!!!'
    print(now)
    print(data)


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
