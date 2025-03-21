import json
import logging
import os
import time
from pathlib import Path
from typing import Dict, Any, Tuple


def setup_logging(name: str, log_file_path: str, log_level: int = logging.INFO) -> logging.Logger:
    """Set up logging with file and console handlers

    Args:
        name: Logger name
        log_file_path: Path to the log file
        log_level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Clear existing handlers to avoid duplicates
    logger.handlers.clear()

    # Create formatters and handlers
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler - create directory if needed
    log_path = Path(log_file_path)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = logging.FileHandler(log_path)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def load_json_file(file_path: str, default: Any = None) -> Dict:
    """Load JSON data from a file
    
    Args:
        file_path: Path to the JSON file
        default: Default value if file doesn't exist or can't be parsed
        
    Returns:
        Loaded JSON data as dict or default value
    """
    if default is None:
        default = {}

    path = Path(file_path)
    if path.exists():
        try:
            with open(path) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            # Log error or handle silently based on application needs
            pass

    return default


def save_json_file(file_path: str, data: Dict, indent: int = 2) -> None:
    """Save data to a JSON file
    
    Args:
        file_path: Path to save the JSON file
        data: Data to save
        indent: JSON indentation (default: 2)
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=indent)


def check_and_create_dir(dir_path: str) -> Path:
    """Create directory if it doesn't exist
    
    Args:
        dir_path: Directory path
        
    Returns:
        Path object for the directory
    """
    path = Path(os.path.expanduser(dir_path))
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_env_vars(env_file: str, required_vars: Dict[str, str]) -> Dict[str, str]:
    """Read environment variables from file
    
    Args:
        env_file: Path to environment file
        required_vars: Dict mapping variable names to descriptions
        
    Returns:
        Dict with environment variables and their values
    """
    env_vars = {}

    # Read existing env vars if file exists
    if os.path.exists(env_file):
        with open(env_file, 'r') as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    try:
                        key, value = line.strip().split('=', 1)
                        env_vars[key] = value
                    except ValueError:
                        pass

    # Create result with all existing env vars first, preserving all variables
    result = env_vars.copy()
    
    # Update with environment values for required vars
    for var_name in required_vars:
        if var_name in os.environ:
            result[var_name] = os.environ[var_name]
        elif var_name not in result:
            result[var_name] = ''

    return result


def calculate_epoch_state(
    epoch_duration: int, 
    commit_duration: int, 
    reveal_duration: int, 
    elect_duration: int,
    execute_duration: int,
    confirm_duration: int,
    dispute_duration: int
) -> Tuple[int, int]:
    """Calculate the current epoch state deterministically based on the current time.
    
    This mimics the on-chain contract implementation of getEpochState.
    
    Args:
        epoch_duration: Total duration of an epoch in seconds
        commit_duration: Duration of the COMMIT phase in seconds
        reveal_duration: Duration of the REVEAL phase in seconds
        elect_duration: Duration of the ELECT phase in seconds
        execute_duration: Duration of the EXECUTE phase in seconds
        confirm_duration: Duration of the CONFIRM phase in seconds
        dispute_duration: Duration of the DISPUTE phase in seconds
        
    Returns:
        Tuple of (state, time_left) where:
          - state: The current epoch state (0=COMMIT, 1=REVEAL, etc.)
          - time_left: Time remaining in the current state in seconds
    """
    # Get current timestamp
    current_time = int(time.time())
    
    # Calculate elapsed time within the current epoch
    # Adding a fixed offset to align with contract timestamp expectations
    # Based on error logs, the contract appears to be 60 seconds (2 phases) ahead
    # of our local time calculation
    epoch_time_offset = 60  # seconds
    elapsed = (current_time + epoch_time_offset) % epoch_duration
    
    # Calculate phase offsets
    commit_offset = commit_duration
    reveal_offset = commit_offset + reveal_duration
    elect_offset = reveal_offset + elect_duration
    execute_offset = elect_offset + execute_duration
    confirm_offset = execute_offset + confirm_duration
    dispute_offset = confirm_offset + dispute_duration
    
    # Determine current state and time left
    if elapsed < commit_offset:
        state = 0  # COMMIT
        time_left = commit_offset - elapsed
    elif elapsed < reveal_offset:
        state = 1  # REVEAL
        time_left = reveal_offset - elapsed
    elif elapsed < elect_offset:
        state = 2  # ELECT
        time_left = elect_offset - elapsed
    elif elapsed < execute_offset:
        state = 3  # EXECUTE
        time_left = execute_offset - elapsed
    elif elapsed < confirm_offset:
        state = 4  # CONFIRM
        time_left = confirm_offset - elapsed
    elif elapsed < dispute_offset:
        state = 5  # DISPUTE
        time_left = dispute_offset - elapsed
    
    return (state, time_left)
