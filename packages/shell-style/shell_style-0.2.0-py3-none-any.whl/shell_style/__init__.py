"""        
Shell-Style: A Python Package for styling terminal output.
Supports ANSI escape codes, tables, progress bars, and more
"""

from sys import stdout as _stdout
from warnings import warn as _warn
from os import (getenv as _getenv, environ as _environ)
from .models import (ProgressBar as _ProgressBar, DEFAULT_THEME)
from re import compile as _compile

# Set __all__
__all__ = ["rgb_to_ansi", "hex_to_ansi", "run_progress_bar", "DEFAULT_THEME", "strip_ansi"]

# Check whether the terminal is compatible with Shell-Style    
_compatible = 0

if _stdout.isatty():
    _compatible += 1
    
term = _getenv("TERM", "")
if term and ("xterm" in term or "color" in term):
    _compatible += 1
    
if _environ.get("COLORTERM", "").lower() in ("truecolor", "24bit"):
    _compatible += 1
    
if _compatible == 1:
    _warn("Warning: This terminal may not be compatible with ShellStyle", Warning)

if _compatible == 0:
    _warn("Warning: This terminal is probably not compatible with ShellStyle", Warning)
    
def rgb_to_ansi(red: int, green: int, blue: int, mode: str = "fg") -> str:
    """
    Convert a RGB code into an ANSI escape sequence. Only works on 
    modern terminals.
    
    Args:
        red: int, 
        green: int, 
        blue: int, 
        mode: str = "fg"
    
    Returns: str
    """
    
    for value in (red, green, blue):
        if value < 0 or value > 255:
            raise ValueError("Arguments must be less than 255 and more than one")
    
    return f"\033[38;2;{red};{green};{blue}m" if mode == "fg" else f"\033[48;2;{red};{green};{blue}m"

def hex_to_ansi(code: str, mode: str = "fg") -> str:
    """
    Convert a HEX code into an ANSI escape sequence after converting
    it into a RGB code. Only works on modern terminals.
    
    Args:
        code: str, 
        mode: str = "fg"
    
    Returns: str
    """
    
    code = code.strip()
    
    if "#" in code:
        code = code.strip().replace("#", "")
    
    if len(code) > 6:
        raise ValueError("Argument code must be a valid hex code")
    
    return rgb_to_ansi(int(code[0:2], 16), int(code[2:4], 16), int(code[4:6], 16), mode)

def run_progress_bar(values: int, *, delay: float = 1, symbol: str = "-") -> None:
        """
        Run a progress bar.
        
        Args: 
            values: int,
            delay: float = 1,
            style: str = "default"
            
        Returns: NoReturn
        """
        
        progress_bar = _ProgressBar(values)
        progress_bar.run()

def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape sequences from a string.

    Args:
        text: str

    Returns: str
    """

    ansi_escape = _compile(r"\x1b\[[0-9;]*m")
    return ansi_escape.sub("", text)
        