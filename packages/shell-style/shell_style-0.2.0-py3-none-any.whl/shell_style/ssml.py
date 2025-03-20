"""
Contains SSML (Shell-Style Markup Language) functionality for the Shell-Style package.
Defines strip_ansi, interpret, ssml_to_ansi, ansi_to_ssml, html_to_ssml and ssml_to_html
"""

from .enums import (Styles as _Styles, ForegroundColors as _ForegroundColors, BackgroundColors as _BackgroundColors, Other as _Other)

__all__ = ["interpret", "ssml_to_ansi", "ansi_to_ssml", "html_to_ssml", "ssml_to_html"]

def interpret(text: str, mode: int = 0) -> str:
    """
    Interpret SSML to ANSI, ANSI to SSML, HTML to SSML or SSML to HTML dependng on the mode
    
    Args:
        text: str,
        mode: int = 0 (must be between 0 and 3)
        
    Returns: str 
    """
    
    match mode:
        case 0:
            return ssml_to_ansi(text)
        
        case 1:
            return ansi_to_ssml(text)
        
        case 2:
            return ssml_to_html(text)
        
        case 3:
            return html_to_ssml(text)

        case _:
            raise ValueError(f"Invalid \"mode\" argument: {mode}. Must be between 0 and 3")

def ssml_to_ansi(text: str) -> str:
    """
    Interprets SSML (Shell-Style Markup Language) text into ANSI escape sequences
    
    Args:
        text: str 
        
    Returns: str 
    """
    
    ssml_to_ansi_map = {
        "<@bold>": _Styles.BOLD.value,
        "<@dim>": _Styles.DIM.value,
        "<@italic>": _Styles.ITALIC.value,
        "<@underline>": _Styles.UNDERLINE.value,
        "<@blink>": _Styles.BLINK.value,
        "<@inverse>": _Styles.INVERSE.value,
        "<@hidden>": _Styles.HIDDEN.value,
        "<@strikethrough>": _Styles.STRIKETHROUGH.value,
        "<@fg_black>": _ForegroundColors.BLACK.value,
        "<@fg_red>": _ForegroundColors.RED.value,
        "<@fg_green>": _ForegroundColors.GREEN.value,
        "<@fg_yellow>": _ForegroundColors.YELLOW.value,
        "<@fg_blue>": _ForegroundColors.BLUE.value,
        "<@fg_magenta>": _ForegroundColors.MAGENTA.value,
        "<@fg_cyan>": _ForegroundColors.CYAN.value,
        "<@fg_white>": _ForegroundColors.WHITE.value,
        "<@bg_black>": _BackgroundColors.BLACK.value,
        "<@bg_red>": _BackgroundColors.RED.value,
        "<@bg_green>": _BackgroundColors.GREEN.value,
        "<@bg_blue>": _BackgroundColors.BLUE.value,
        "<@bg_magenta>": _BackgroundColors.MAGENTA.value,
        "<@bg_cyan>": _BackgroundColors.CYAN.value,
        "<@bg_white>": _BackgroundColors.WHITE.value,
        "<@stop>": _Other.STOP.value,
        "<@info>": _ForegroundColors.CYAN.value,
        "<@success>": _ForegroundColors.GREEN.value,
        "<@warning>": _ForegroundColors.YELLOW.value,
        "<@error>": _ForegroundColors.RED.value,
        "<@heading>": (_Styles.BOLD.value + _Styles.UNDERLINE.value)
    }

    for ssml, ansi in ssml_to_ansi_map.items():
        text = text.replace(ssml, ansi)

    return text

def ansi_to_ssml(text: str) -> str:
    """
    Interprets ANSI escape sequences into SSML (Shell-Style Markup Language) text
    
    Args:
        text: str 
        
    Returns: str 
    """
    
    ansi_to_ssml_map = {
        _Styles.BOLD.value: "<@bold>",
        _Styles.DIM.value: "<@dim>",
        _Styles.ITALIC.value: "<@italic>",
        _Styles.UNDERLINE.value: "<@underline>",
        _Styles.BLINK.value: "<@blink>",
        _Styles.INVERSE.value: "<@inverse>",
        _Styles.HIDDEN.value: "<@hidden>",
        _Styles.STRIKETHROUGH.value: "<@strikethrough>",
        _ForegroundColors.BLACK.value: "<@fg_black>",
        _ForegroundColors.RED.value: "<@fg_red>",
        _ForegroundColors.GREEN.value: "<@fg_green>",
        _ForegroundColors.YELLOW.value: "<@fg_yellow>",
        _ForegroundColors.BLUE.value: "<@fg_blue>",
        _ForegroundColors.MAGENTA.value: "<@fg_magenta>",
        _ForegroundColors.CYAN.value: "<@fg_cyan>",
        _ForegroundColors.WHITE.value: "<@fg_white>",
        _BackgroundColors.BLACK.value: "<@bg_black>",
        _BackgroundColors.RED.value: "<@bg_red>",
        _BackgroundColors.GREEN.value: "<@bg_green>",
        _BackgroundColors.BLUE.value: "<@bg_blue>",
        _BackgroundColors.MAGENTA.value: "<@bg_magenta>",
        _BackgroundColors.CYAN.value: "<@bg_cyan>",
        _BackgroundColors.WHITE.value: "<@bg_white>",
        _Other.STOP.value: "<@stop>",
        _ForegroundColors.CYAN.value: "<@info>",
        _ForegroundColors.GREEN.value: "<@success>",
        _ForegroundColors.YELLOW.value: "<@warning>",
        _ForegroundColors.RED.value: "<@error>",
        (_Styles.BOLD.value + _Styles.UNDERLINE.value): "<@heading>",               
    }

    for ansi, ssml in ansi_to_ssml_map.items():
        text = text.replace(ansi, ssml)

    return text

def ssml_to_html(text: str) -> str:
    """
    Interprets SSML (Shell Style Markup Language) text into HTML text

    Args:
        text: str

    Returns: str
    """

    ssml_to_html_map = {
        "<@bold>": "<span style=\"font-weight:bold\">",
        "<@dim>": "<span style=\"opacity:0.6\">",
        "<@italic>": "<span style=\"font-style:italic\">",
        "<@underline>": "<span style=\"text-decoration:underline\">",
        "<@blink>": "<span style=\"animation:blink 1s step-end infinite\">",
        "<@inverse>": "<span style=\"color:white;background-color:black\">",
        "<@hidden>": "<span style=\"visibility:hidden\">",
        "<@strikethrough>": "<span style=\"text-decoration:line-through\">",
        "<@fg_black>": "<span style=\"color:black\">",
        "<@fg_red>": "<span style=\"color:red\">",
        "<@fg_green>": "<span style=\"color:green\">",
        "<@fg_yellow>": "<span style=\"color:yellow\">",
        "<@fg_blue>": "<span style=\"color:blue\">",
        "<@fg_magenta>": "<span style=\"color:magenta\">",
        "<@fg_cyan>": "<span style=\"color:cyan\">",
        "<@fg_white>": "<span style=\"color:white\">",
        "<@bg_black>": "<span style=\"background-color:black\">",
        "<@bg_red>": "<span style=\"background-color:red\">",
        "<@bg_green>": "<span style=\"background-color:green\">",
        "<@bg_blue>": "<span style=\"background-color:blue\">",
        "<@bg_magenta>": "<span style=\"background-color:magenta\">",
        "<@bg_cyan>": "<span style=\"background-color:cyan\">",
        "<@bg_white>": "<span style=\"background-color:white\">",
        "<@stop>": "</span>",
        "<@info>": "<span style=\"color:cyan\">",
        "<@success>": "<span style=\"color:green\">",
        "<@warning>": "<span style=\"color:yellow\">",
        "<@error>": "<span style=\"color:red\">",
        "<@heading>": "<span style=\"font-weight:bold;text-decoration:underline\">"
    }

    for ssml, html in ssml_to_html_map.items:
        text = text.replace(ssml, html)

    return text

def html_to_ssml(text: str) -> str:
    """
    Interprets HTML text into SSML (Shell Style Markup Language) text

    Args:
        text: str

    Returns: str
    """

    html_to_ssml_map = {
        "<span style=\"font-weight:bold\">": "<@bold>",
        "<span style=\"opacity:0.6\">": "<@dim>",
        "<span style=\"font-style:italic\">": "<@italic>",
        "<span style=\"text-decoration:underline\">": "<@underline>",
        "<span style=\"animation:blink 1s step-end infinite\">": "<@blink>",
        "<span style=\"color:white;background-color:black\">": "<@inverse>",
        "<span style=\"visibility:hidden\">": "<@hidden>",
        "<span style=\"text-decoration:line-through\">": "<@strikethrough>",
        "<span style=\"color:black\">": "<@fg_black>",
        "<span style=\"color:red\">": "<@fg_red>",
        "<span style=\"color:green\">": "<@fg_green>",
        "<span style=\"color:yellow\">": "<@fg_yellow>",
        "<span style=\"color:blue\">": "<@fg_blue>",
        "<span style=\"color:magenta\">": "<@fg_magenta>",
        "<span style=\"color:cyan\">": "<@fg_cyan>",
        "<span style=\"color:white\">": "<@fg_white>",
        "<span style=\"background-color:black\">": "<@bg_black>",
        "<span style=\"background-color:red\">": "<@bg_red>",
        "<span style=\"background-color:green\">": "<@bg_green>",
        "<span style=\"background-color:blue\">": "<@bg_blue>",
        "<span style=\"background-color:magenta\">": "<@bg_magenta>",
        "<span style=\"background-color:cyan\">": "<@bg_cyan>",
        "<span style=\"background-color:white\">": "<@bg_white>",
        "</span>": "<@stop>",
        "<span style=\"color:cyan\">": "<@info>",
        "<span style=\"color:green\">": "<@success>",
        "<span style=\"color:yellow\">": "<@warning>",
        "<span style=\"color:red\">": "<@error>",
        "<span style=\"font-weight:bold;text-decoration:underline\">": "<@heading>"
    }

    for html, ssml in html_to_ssml_map.items:
        text = text.replace(html, ssml)

    return text
