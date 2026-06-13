from sense_hat import SenseHat
from datetime import datetime
import pytz
from dateutil.relativedelta import relativedelta
import statsapi

# MLB Stats API team id for the Los Angeles Dodgers.
DODGERS_TEAM_ID = 119
LOCAL_TZ = pytz.timezone("America/Los_Angeles")


def main():
    sense = SenseHat()
    now = datetime.now(pytz.utc).astimezone(LOCAL_TZ)
    for game in get_games(now):
        game_date_time = parse_game_datetime(game["game_datetime"])
        diff = relativedelta(now, game_date_time)
        if (
            diff.months == 0
            and diff.days == 0
            and diff.hours == 0
            and 0 >= diff.minutes >= -10
        ):
            opponent = get_opponent(game)
            game_time = game_date_time.strftime("%-I:%M %p")
            message = "#ITFDB!!! The Dodgers will be playing {} at {}".format(
                opponent, game_time
            )
            sense.show_message(message, scroll_speed=0.05)


def get_games(now):
    """Fetch today's Dodgers schedule from the MLB Stats API."""
    return statsapi.schedule(date=now.strftime("%Y-%m-%d"), team=DODGERS_TEAM_ID)


def parse_game_datetime(game_datetime):
    """Convert the API's UTC ISO 8601 start time to local time."""
    utc_dt = datetime.fromisoformat(game_datetime).astimezone(pytz.utc)
    return utc_dt.astimezone(LOCAL_TZ)


def get_opponent(game):
    """Return the opponent name, prefixed with 'at' for away games."""
    if game["home_id"] == DODGERS_TEAM_ID:
        return game["away_name"]
    return "at {}".format(game["home_name"])


if __name__ == "__main__":
    main()
