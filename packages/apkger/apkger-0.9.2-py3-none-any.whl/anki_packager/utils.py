import os
import json
import platform
import shutil
import pkg_resources


def get_user_config_dir():
    """
    Returns the platform-specific user configuration directory.
    Windows: %APPDATA%/anki_packager
    macOS/Linux: ~/.config/anki_packager
    """
    if platform.system() == "Windows":
        return os.path.join(os.environ.get("APPDATA", ""), "anki_packager")
    else:
        return os.path.expanduser("~/.config/anki_packager")


def initialize_config():
    config_dir = get_user_config_dir()
    os.makedirs(config_dir, exist_ok=True)
    config_subdir = os.path.join(config_dir, "config")
    os.makedirs(config_subdir, exist_ok=True)
    dicts_dir = os.path.join(config_dir, "dicts")
    os.makedirs(dicts_dir, exist_ok=True)

    # Default configuration
    default_config = {
        "API_KEY": "",
        "API_BASE": "",
        "MODEL": "",
        "PROXY": "127.0.0.1:7890",
        "EUDIC_TOKEN": "",
        "EUDIC_ID": "0",
        "DECK_NAME": "anki-packager",
    }

    config_path = os.path.join(config_subdir, "config.json")
    if not os.path.exists(config_path):
        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2)

    vocab_path = os.path.join(config_subdir, "vocabulary.txt")
    if not os.path.exists(vocab_path):
        with open(vocab_path, "w", encoding="utf-8") as f:
            f.write("")

    failed_path = os.path.join(config_subdir, "failed_path.txt")
    if not os.path.exists(failed_path):
        with open(failed_path, "w", encoding="utf-8") as f:
            f.write("")

    try:
        # 使用pkg_resources获取包内资源
        dict_files = ["单词释义比例词典-带词性.mdx", "有道词语辨析.mdx"]
        for dict_file in dict_files:
            src_path = pkg_resources.resource_filename(
                "anki_packager", f"dicts/{dict_file}"
            )
            dst_path = os.path.join(dicts_dir, dict_file)
            if os.path.exists(src_path) and not os.path.exists(dst_path):
                shutil.copy2(src_path, dst_path)
    except Exception as e:
        print(f"Warning: Could not copy dictionary files: {e}")

    print(f"\033[1;31m配置文件位于: {config_path}:请修改进行配置 \033[0m")
