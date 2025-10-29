import os
from datetime import datetime as dt

class LogColors:
    """ANSI color codes for terminal output"""
    RESET = '\033[0m'
    BLUE = '\033[94m'
    GRAY = '\033[90m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'

def smart_log(*args, **kwargs) -> None:
    """
    Custom logging function with multiple options for formatting and output.
    
    Args:
        *args: Message components to log (will be converted to strings)
        **kwargs: Logging options:
            - level: 'info', 'debug', 'warning', 'error' (default: 'info')
            - timestamp: True/False (default: False)
            - date: True/False (default: False)
            - save_to: file path to append messages (without colors)
            - colored: True/False (default: True)
    """
    # default options
    level = kwargs.get('level', 'info').lower()
    show_timestamp = kwargs.get('timestamp', False)
    show_date = kwargs.get('date', False)
    save_to = kwargs.get('save_to', None)
    colored_output = kwargs.get('colored', True)
    
    # convert all message components to strings and join
    message = ' '.join(str(arg) for arg in args)
    
    # build prefix with timestamp and date if requested
    prefix_parts = []
    
    if show_date or show_timestamp:
        now = dt.now()
        if show_date and show_timestamp:
            prefix_parts.append(now.strftime("%Y-%m-%d %H:%M:%S"))
        elif show_date:
            prefix_parts.append(now.strftime("%Y-%m-%d"))
        elif show_timestamp:
            prefix_parts.append(now.strftime("%H:%M:%S"))
    
    # add level prefix
    level_prefix = f"[{level.upper()}]"
    prefix_parts.append(level_prefix)
    
    # create full prefix
    prefix = " ".join(prefix_parts)
    if prefix:
        full_message = f"{prefix} {message}"
    else:
        full_message = message
    
    # color mapping
    color_map = {
        'info': LogColors.BLUE,
        'debug': LogColors.GRAY,
        'warning': LogColors.YELLOW,
        'error': LogColors.RED + LogColors.BOLD
    }
    
    # print with colors if enabled
    if colored_output and level in color_map:
        print(f"{color_map[level]}{full_message}{LogColors.RESET}")
    else:
        print(full_message)
    
    # save to file if requested (without colors)
    if save_to:
        try:
            # only create directories if the path contains subdirectories
            directory = os.path.dirname(save_to)
            if directory and not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            with open(save_to, 'a', encoding='utf-8') as f:
                # save without any color codes
                file_message = full_message
                f.write(file_message + '\n')
        except Exception as e:
            error_msg = f"[ERROR] Failed to write to log file {save_to}: {e}"
            if colored_output:
                print(f"{LogColors.RED}{error_msg}{LogColors.RESET}")
            else:
                print(error_msg)


if __name__ == "__main__":
    print("=== Testing Smart Log Function ===\n")
    
    print("1. Basic level tests:")
    smart_log("This is an info message", level="info")
    smart_log("This is a debug message", level="debug")
    smart_log("This is a warning message", level="warning")
    smart_log("This is an error message", level="error")
    
    print("\n2. With timestamp and date:")
    smart_log("Message with timestamp", timestamp=True)
    smart_log("Message with date", date=True)
    smart_log("Message with both", timestamp=True, date=True)
    
    print("\n3. Multiple arguments:")
    smart_log("User", "John", "logged in from", "192.168.1.1", level="info")
    smart_log("Calculation result:", 42, 3.14, [1, 2, 3], level="debug")
    
    print("\n4. Without colors:")
    smart_log("This message has no colors", colored=False)
    smart_log("Error without colors", level="error", colored=False)
    
    print("\n5. File logging test:")
    log_file = "test_log.txt"
    smart_log("This should be saved to file", level="info", save_to=log_file, timestamp=True)
    smart_log("Another file entry", level="warning", save_to=log_file, date=True)
    
    print(f"\nCheck the file '{log_file}' to see the saved logs (without colors)")
    
    # show file contents
    try:
        if os.path.exists(log_file):
            print(f"\nContents of {log_file}:")
            with open(log_file, 'r') as f:
                print(f.read())
    except Exception as e:
        print(f"Could not read log file: {e}")