from dotenv import load_dotenv
import json
import os
from pathlib import Path
from typing import Optional


def save_configs(env_path: Optional[str] = ".", log_path: Optional[str] = ".") -> None:
    env_path = Path(env_path).resolve()
    log_path = Path(log_path).resolve()

    if not env_path.exists():
        raise ValueError(f"Error: The environment path '{env_path}' does not exist.")
    if not log_path.exists():
        raise ValueError(f"Error: The log path '{log_path}' does not exist.")

    config = {"env_file_path": str(env_path), "log_file_path": str(log_path)}
    config_file = Path("config.json")

    with config_file.open("w") as f:
        json.dump(config, f, indent=4)

    print(f"Configuration saved successfully:")
    print(f"  - .env file path: {env_path}")
    print(f"  - Log file path: {log_path}")


def get_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            config_file = json.load(file)
            ENV_PATH, LOG_PATH = config_file.get(
                "env_file_path"
            ) + "/.env", config_file.get("log_file_path")
            load_dotenv(ENV_PATH)
            return (
                LOG_PATH,
                os.getenv("BASE_URL"),
                os.getenv("TOKEN_TIME"),
                os.getenv("QUEUE_BASE_URL"),
            )


def get_API_config():
    if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            config_file = json.load(file)
            ENV_PATH = config_file.get("env_file_path") + "/.env"
            load_dotenv(ENV_PATH)
            return (
                os.getenv("ZILLOW_BASE_URL"),
                os.getenv("ZILLOW_USERNAME"),
                os.getenv("ZILLOW_PASSWORD"),
                os.getenv("PROPSTREAM_BASE_URL"),
                os.getenv("PROPSTREAM_USERNAME"),
                os.getenv("PROPSTREAM_PASSWORD"),
                os.getenv("PROPSTREAM_LOGIN_URL"),
                os.getenv("TRACERS_BASE_URL"),
                os.getenv("TRACERS_USERNAME"),
                os.getenv("TRACERS_PASSWORD"),
            )

def get_telnyx_config():
     if os.path.exists("config.json"):
        with open("config.json", "r") as file:
            config_file = json.load(file)
            ENV_PATH = config_file.get("env_file_path") + "/.env"
            load_dotenv(ENV_PATH)
            return (
                os.getenv("TELNYX_BASE_URL"),
                os.getenv("TELNYX_API_KEY")
            )
