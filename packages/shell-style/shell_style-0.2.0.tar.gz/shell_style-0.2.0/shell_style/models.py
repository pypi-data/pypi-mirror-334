"""
Classes for Shell-Style package.
This module defines _BaseObject, Theme, Console, ProgressBar and Table.
"""

from time import sleep as _sleep
from os import get_terminal_size as _get_terminal_size
from abc import ABC as _ABC
from typing import Any as _Any
from .ssml import interpret as _interpret
from .enums import (Styles as _Styles, BackgroundColors as _BackgroundColors, ForegroundColors as _ForegroundColors,  Other as _Other)

__all__ = ["Theme", "Console", "Table", "ProgressBar", "DEFAULT_THEME"]

class _BaseObject(_ABC):
    """
    Abstract Base Class for all other classes defined here.
    Defines the help method.
    
    Args: None
    """
    
    @classmethod
    def help(cls) -> str:
        return _interpret(f"<@heading>{cls.__name__}<@stop>\n{cls.__doc__}")

class Theme(_BaseObject):
    """
    Class for themes. 
    
    Args:
        **styles
    """
    
    def __init__(self, **styles) -> None:
        self.__styles = styles
        
    @property
    def styles(self) -> dict[str, str]:
        return self.__styles
    
    @styles.setter
    def styles(self, styles: dict[str, str]) -> None:
        self.__styles.update(styles)
        
    def get_style(self, target: str) -> str:
        return str(self.__styles.get(target))
    
    def __getitem__(self, target: str) -> _Any:
        return self.__styles.get(target)
    
    def __setitem__(self, style: str, value: str) -> None:
        self.__styles[style] = value

DEFAULT_THEME = Theme(
    info=_ForegroundColors.CYAN.value, 
    warning=_ForegroundColors.YELLOW.value, 
    error=_ForegroundColors.RED.value, 
    success=_ForegroundColors.GREEN.value, 
    bold=_Styles.BOLD.value, 
    dim=_Styles.DIM.value, 
    italic=_Styles.ITALIC.value, 
    underline=_Styles.UNDERLINE.value, 
    blink=_Styles.BLINK.value, 
    inverse=_Styles.INVERSE.value, 
    hidden=_Styles.HIDDEN.value, 
    strikethrough=_Styles.STRIKETHROUGH.value, 
    fg_black=_ForegroundColors.BLACK.value, 
    fg_white=_ForegroundColors.WHITE.value, 
    fg_green=_ForegroundColors.GREEN.value, 
    fg_yellow=_ForegroundColors.YELLOW.value, 
    fg_blue=_ForegroundColors.BLUE.value, 
    fg_magenta=_ForegroundColors.MAGENTA.value, 
    fg_cyan=_ForegroundColors.CYAN.value, 
    bg_black=_BackgroundColors.BLACK.value,
    bg_red=_BackgroundColors.RED.value, 
    bg_blue=_BackgroundColors.BLUE.value, 
    stop=_Other.STOP.value,
    bg_green=_BackgroundColors.GREEN.value, 
    bg_magenta=_BackgroundColors.MAGENTA.value, 
    bg_cyan=_BackgroundColors.CYAN.value,
    bg_white=_BackgroundColors.WHITE.value, 
    default=_Styles.DEFAULT.value, 
    heading=_Styles.BOLD.value + _Styles.UNDERLINE.value
)

class Console(_BaseObject):
    """
    Console object on which text can be printed and input can be taken.

    Args:
        title: str, 
        theme: Theme = DEFAULT_THEME
    """
    
    def __init__(self, title: str, theme: Theme = DEFAULT_THEME, print_title: bool = True) -> None:
        self.__title = title
        self.__theme = theme
        
        if print_title:
            self.print_title()
        
    def print_title(self) -> None:
        self.write(f"<@heading>{self.__title}<@stop>", alignment=_Other.CENTER.value)
        
    @property
    def theme(self) -> Theme:
        return self.__theme
    
    @theme.setter
    def theme(self, new: Theme) -> None:
        self.__theme = new
        
    @property
    def title(self) -> str:
        return self.__title
    
    @title.setter
    def title(self, new: str) -> None:
        self.__title = new
    
    def clear(self, print_title: bool = True) -> None:
        """
        Clear the terminal.
        
        Args:
            print_title: bool = True
            
        Returns: None
        """
        
        print(_Other.CLEAR.value, end="")
        if print_title:
            self.print_title()
        
    def log(self, *objects, end: str = f"{_Other.STOP.value}\n", sep: str = " ", 
            style: str = "default", alignment: str = _Other.LEFT.value) -> None:
        """
        Customized log method.
        
        Args: 
            *objects: _Any, 
            end: str = f"{_Other.STOP.value}\\n",
            alignment: str = _Other.LEFT.value,
            sep: str = " ", 
            style: str = "default"
            
        Returns: None
        """
        
        print(
        _interpret(self.__align_text(self.__theme.get_style(style) + "".join(map(str, objects)), alignment)),
        end=end, sep=sep)
            
    def write(self, *objects: _Any, alignment: str = _Other.LEFT.value, end: str = f"{_Other.STOP.value}\n", 
              sep: str = " ", style: str = "default") -> None:
        """
        Customized print method.
        
        Args:
            *objects: _Any,
            alignment: str, 
            end: str = _Other.STOP.value, 
            sep: str = "", 
            style: str
        
        Returns: None
        """
        
        print(
        _interpret(self.__align_text(self.__theme.get_style(style) + "".join(map(str, objects)), alignment)),
        end=end, sep=sep
            )
        
    def prompt(self, *objects, end: str = _Other.STOP.value, style: str = "default") -> str:
        """
        Customized input method.
        
        Args:
            *objects: _Any,
            end: str = _Other.STOP.value, 
            style: str
        
        Returns: str
        """
        
        try:
            text = input(_interpret(self.__theme.get_style(style) + "".join(obj for obj in objects) + end))
        
        except Exception as error:
            return repr(error)
        
        else:
            return text
    
    @staticmethod
    def __align_text(text: _Any, alignment: str) -> str:
        """
        Private static method for text alignment.
        
        Args:
            text: _Any, 
            alignment: str
        
        Returns: str 
        
        Raises: ValueError (if alignment is not valid)
        """
        
        width = _get_terminal_size().columns
        
        if alignment == _Other.CENTER.value:
            padding = (width - len(text)) // 2
            return " " * padding + text + " " * (width - len(text) - padding)
        
        elif alignment == _Other.RIGHT.value:
            return (" " * (width - len(text)) + text).rstrip(" ")
        
        elif alignment == _Other.LEFT.value:
            return (text + " " * (width - len(text))).lstrip(" ")
        
        else:
            raise ValueError(f"Invalid argument for function 'Console.__align_text': {alignment}")
    
class ProgressBar(_BaseObject):
    """
    Class for representing basic progress bars.
    
    Args:
        values: int,
        theme: Theme = DEFAULT_THEME
        symbol: str = "-",
        delay: float = 1
    """
    
    def __init__(self, values: int, *, theme: Theme = DEFAULT_THEME, 
                 symbol: str = "-", delay: float = 1) -> None:
        self.__values = values
        self.__theme = theme
        self.__symbol = _interpret(symbol)
        self.__delay = delay
        
    @property
    def values(self) -> int:
        return self.__values
    
    @values.setter
    def values(self, new: int) -> None:
        self.__values = new
        
    @property
    def theme(self) -> Theme:
        return self.__theme
    
    @theme.setter
    def theme(self, new: Theme) -> None:
        self.__theme = new
        
    @property
    def symbol(self) -> str:
        return self.__symbol
    
    @symbol.setter
    def symbol(self, new: str) -> None:
        self.__symbol = _interpret(new)
        
    @property
    def delay(self) -> float:
        return self.__delay
    
    @delay.setter
    def delay(self, new: float) -> None:
        self.__delay = new
        
    def run(self, style: str = "default") -> None:
        """
        Run the progress bar.
        
        Args:
            style: str = "default",
            
        Returns: None
        """
        
        for _ in range(self.__values):
            print(self.__theme.get_style(style) + self.__symbol, end=_Other.STOP.value, flush=True)
            _sleep(self.__delay)
            
class Table(_BaseObject):
    """
    Table class for representing data.
    
    Args: 
        columns: int = 0,
        theme: Theme = DEFAULT_THEME
    """
    
    def __init__(self, columns: int = 0, theme: Theme = DEFAULT_THEME) -> None:
        self.__columns = columns
        if columns < 0:
            self.__columns = 0
        self.__theme = theme
        self.__rows = 0
        self.__table = []
        
    def add_row(self, *objects: _Any, style: str = "default") -> None:
        """
        Add a row to self.__table.
        
        Args:
            *objects: _Any
            
        Returns: None
        """
        
        interpreted_objects = []
        
        for obj in objects:
            interpreted_objects.append(_interpret(self.__theme.get_style(style) + str(obj) + _Other.STOP.value))
            
        while len(interpreted_objects) < self.__columns:
            interpreted_objects.append(None)
            
        while len(interpreted_objects) > self.__columns:
            interpreted_objects.pop()
            
        self.__table.append(interpreted_objects)
        self.__rows += 1
        
    def del_row(self, index: int) -> None:
        """
        Delete a row in self.__table.
        
        Args:
            index: int
            
        Returns: None    
        """
        
        del self.__table[index]
        self.__rows -= 1
        
    def del_column(self, index: int) -> None:
        """
        Delete a column in self.__table.
        
        Args:
            index: int
            
        Returns: None
        """
        
        for row in self.__table:
            del row[index]
            
        self.__columns -= 1
        
    def add_column(self, placeholder: _Any = "", style: str = "default") -> None:
        """
        Add a column in self.__table.
        
        Args:
            placeholder: _Any = ""
            
        Returns: None
        """
        
        placeholder = _interpret(self.__theme.get_style(style) + str(placeholder) + _Other.STOP.value)
        
        for row in self.__table:
            row.append(placeholder)
        
        self.__columns += 1
            
    def get_column(self, row_index: int, column_index: int) -> _Any:
        """
        Get the information in a column in self.__table.
        
        Args:
            row_index: int,
            column_index: int
            
        Returns: _Any
        """
        
        return self.__table[row_index][column_index]
    
    def set_column(self, info: _Any, row_index: int, column_index: int, style: str = "default") -> None:
        """
        Set the information in a column in self.__table.
        
        Args:
            info: _Any,
            row_index: int,
            column_index: int
            
        Returns: None
        """
        
        self.__table[row_index][column_index] = _interpret(self.__theme.get_style(style) + str(info) + _Other.STOP.value)
        
    def get_row(self, index: int) -> list:
        """
        Returns a row in self.__table.
        
        Args:
            index: int
            
        Returns: list
        """
        
        return self.__table[index]
    
    def get_table(self) -> str:
        """
        Return a string representation of self.__table.
        
        Args: None
        
        Returns: str
        """
        
        return_str = ""
        
        for row in self.__table:
            for column in row:
                return_str += f"| {column} |"
            return_str += "\n"
            
        return return_str
    
    def display(self) -> None:
        print(self.get_table())

    def symbol_separated_values(self, symbol: str = ",") -> str:
        """
        Turn self.__table into a symbol separated format, like CSV, TSV, SSV or PSV.
        
        Args:
            symbol: str = ","
            
        Returns: str
        """
        
        text = ""
        
        for row in self.__table:
            for column in row: 
                if symbol in column:
                    text += f"\"{column}\"{symbol}"
                else:
                    text += f"{column}{symbol}"
                
            text += "\n"
            
        return text
    
    def load(self, path: str, symbol: str = ",") -> None:
        """
        Load self.__table into a file, typically a CSV, TSV, SSV or PSV.
        
        Args:
            path: str,
            symbol: str = ","
            
        Returns: None
        """
        
        with open(path, "w") as file:
            file.write(self.symbol_separated_values(symbol))
        
    @property
    def rows(self) -> int:
        return self.__rows
    
    @property
    def columns(self) -> int:
        return self.__columns
    
    @property
    def table(self) -> list[list[_Any]]:
        return self.__table
    
    @property
    def theme(self) -> Theme:
        return self.__theme
    
    @theme.setter
    def theme(self, new: Theme) -> None:
        self.__theme = new
    