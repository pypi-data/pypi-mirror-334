import os
import json
import shutil


def get_user_config_dir():
    """Return the user configuration directory for anki_packager."""
    if os.name == "nt":  # Windows
        config_dir = os.path.join(
            os.environ.get("APPDATA", ""), "anki_packager"
        )
    else:  # macOS/Linux
        config_dir = os.path.join(
            os.path.expanduser("~"), ".config", "anki_packager"
        )

    os.makedirs(config_dir, exist_ok=True)
    return config_dir


def get_config_path():
    config_dir = get_user_config_dir()
    return os.path.join(config_dir, "config.json")


def get_dictionary_dir():
    config_dir = get_user_config_dir()
    dict_dir = os.path.join(config_dir, "dicts")
    os.makedirs(dict_dir, exist_ok=True)
    return dict_dir


def load_config():
    config_path = get_config_path()

    if not os.path.exists(config_path):
        initialize_config()

    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def initialize_config():
    config_dir = get_user_config_dir()

    package_dir = os.path.dirname(os.path.abspath(__file__))
    pkg_config_dir = os.path.join(os.path.dirname(package_dir), "config")

    if not os.path.exists(pkg_config_dir):
        pkg_config_dir = os.path.join(package_dir, "config")

    default_config = {
        "API_KEY": "",
        "API_BASE": "",
        "MODEL": "",
        "PROXY": "127.0.0.1:7890",
        "EUDIC_TOKEN": "",
        "EUDIC_ID": "0",
        "DECK_NAME": "anki-packager",
    }

    # Create config file
    config_path = os.path.join(config_dir, "config.json")
    template_path = os.path.join(pkg_config_dir, "config.json")

    if os.path.exists(template_path):
        shutil.copy2(template_path, config_path)
    else:
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)

    # Create vocabulary.txt if needed
    vocab_path = os.path.join(config_dir, "vocabulary.txt")
    if not os.path.exists(vocab_path):
        with open(vocab_path, "w", encoding="utf-8") as f:
            f.write("# Add your vocabulary words here, one per line\n")

    print(f"Configuration initialized at {config_dir}")
    print(
        f"Please edit {config_path} to configure your API keys and preferences"
    )
