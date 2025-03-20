import json
from pathlib import Path


def get_config() -> dict:
    config_fp = Path('~/.config/conexao/config.json').expanduser()
    return json.loads(config_fp.read_text(encoding='utf8'))
