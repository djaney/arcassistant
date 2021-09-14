import sys
import pathlib
import json


def get_settings_dir(name) -> pathlib.Path:
    """
    Returns a parent directory path
    where persistent application data can be stored.

    # linux: ~/.local/share
    # macOS: ~/Library/Application Support
    # windows: C:/Users/<USER>/AppData/Roaming
    """

    home = pathlib.Path.home()

    if sys.platform == "win32":
        config_path = home / "AppData/Roaming"
    elif sys.platform == "linux":
        config_path = home / ".local/share"
    elif sys.platform == "darwin":
        config_path = home / "Library/Application Support"
    else:
        raise OSError("OS not supported")

    config_path = config_path / name / "config.json"
    return config_path


def create_dir(settings_file):
    try:
        settings_file.parent.mkdir(parents=True)
    except FileExistsError:
        pass


class Settings(object):
    def __init__(self, name):
        self._settings = {
            "jira_domain": "arcanys.atlassian.net",
            "jira_username": None,
            "jira_token": None,
            "tempo_token": None,
        }
        self._file = get_settings_dir(name)

    def load(self):
        create_dir(self._file)
        if pathlib.Path.is_file(self._file):
            with open(self._file, "r") as fp:
                data = json.load(fp)
            for k, v in data.items():
                if k in self._settings:
                    self._settings[k] = v

    def save(self):
        create_dir(self._file)
        with open(self._file, "w") as fp:
            json.dump(self._settings, fp)

    def get(self, key):
        return self._settings.get(key)

    def set(self, key, value):
        self._settings[key] = value
