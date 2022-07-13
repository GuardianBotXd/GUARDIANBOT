from sample_config import Config


class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 10
    API_HASH = "eb06d4abfb49dc3eeb1aeb98ae0f581e"
    # the name to display in your alive message
    ALIVE_NAME = "Your value"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "Your value"
    # After cloning the repo and installing requirements do python3 telesetup.py an fill that value with this
    GUARDIAN_STRING = "Your value"
    # create a new bot in @botfather and fill the following vales with bottoken
    BOT_TOKEN = "Your value"
    # command handler
    HANDLER = "."
    # spam of assistant
    SPAM = "Your Value"
    UPSTREAM_REPO = "pro"
    # Your City's TimeZone
    TZ = "Your value"
