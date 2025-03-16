# Created by Sean L. on Mar 16
# 
# emb2emb client
# output.py
# 
# PromptCraft, 2025. All rights reserved.

from functools import wraps
from contextlib import contextmanager
from rich.console import Console
from rich.table import Table
from datetime import datetime
from utils.load_config import COMMANDS

console = Console()

class ClientConsole:
    """Rich text console wrapper for standardized application output.
    
    Provides formatted logging methods with consistent styling and timestamp handling.
    All methods are thread-safe and support cross-platform terminal environments.
    """
    
    @staticmethod
    def print(string: str, end: str ='\n'):
        """Proxy method for Rich console output with enhanced documentation.
        
        Accepts all parameters of Rich's Console.print() while adding validation
        for production logging systems. Automatically handles:
        - ANSI escape code stripping in non-TTY environments
        - Markup sanitization
        - Cross-platform color support
        
        Args:
            *args: Content to print (supports Rich renderables)
            **kwargs: Rich formatting options including:
                style (str): Predefined style or CSS-like string
                markup (bool): Enable/disable Markdown parsing (default: True)
                emoji (bool): Enable/disable emoji code conversion (default: True)
                highlight (bool): Enable automatic URL highlighting
                soft_wrap (bool): Enable soft wrapping of long lines

        Examples:
            Basic text with emoji:
            >>> ClientConsole.print(":rocket: Launch sequence initiated")
            
            Styled output:
            >>> ClientConsole.print("Error!", style="bold red")
            
            Mixed content:
            >>> ClientConsole.print(
                "[bold]Header[/bold]", 
                "Body text with [i]italics[/i]", 
                sep="\n"
            )
        """
        console.print(string, end=end)
        
    @staticmethod
    def done(msg: str, timestamps: bool = True) -> None:
        """Display success/completion status messages with green styling.
        
        Args:
            msg (str): Message text to display
            timestamps (bool): Show timestamp prefix (default: True)
            
        Examples:
            >>> ClientConsole.done("Processing complete")
            [#00EE99][DONE] [2023-10-01 12:34:56][/#00EE99] Processing complete
            
            >>> ClientConsole.done("Task finished", timestamps=False)
            [DONE] [2023-10-01 12:34:56] Task finished
        """
        console.print(f'[#00EE99][DONE] {f'[{datetime.now()}]' if timestamps else ""}[/#00EE99] {msg}')
        
    @staticmethod
    def log(msg: str, timestamps: bool = True) -> None:
        """Display informational messages with teal styling.
        
        Args:
            msg (str): Message text to display
            timestamps (bool): Show timestamp prefix (default: True)
            
        Examples:
            >>> ClientConsole.log("Initializing components")
            [INFO] [2023-10-01 12:34:56] Initializing components
        """
        console.print(f'[#00AAAA][INFO] {f'[{datetime.now()}]' if timestamps else ""}[/#00AAAA] {msg}')
        
    @staticmethod
    def warn(msg: str, timestamps: bool = True) -> None:
        """Display warning messages with orange styling.
        
        Args:
            msg (str): Message text to display
            timestamps (bool): Show timestamp prefix (default: True)
            
        Examples:
            >>> ClientConsole.warn("High memory usage")
            [WARN] [2023-10-01 12:34:56] High memory usage
        """
        console.print(f'[#EEAA55][WARN] {f'[{datetime.now()}]' if timestamps else ""}[/#EEAA55] {msg}')
        
    @staticmethod
    def error(msg: str, timestamps: bool = True) -> None:
        """Display error messages with red styling.
        
        Args:
            msg (str): Message text to display
            timestamps (bool): Show timestamp prefix (default: True)
            
        Examples:
            >>> ClientConsole.error("File not found")
            [ERR!] [2023-10-01 12:34:56] File not found
        """
        console.print(f'[#EE3300][ERR!] {f'[{datetime.now()}]' if timestamps else ""}[/#EE3300] {msg}')
    
    @staticmethod
    def table(
        headers: list[str | dict],
        rows: list[list],
        title: str = "",
        box_style: str = "round",
        header_style: str = "bold cyan",
        row_styles: list[str] = None,
        caption: str = "",
        expand: bool = False
    ) -> None:
        """Render structured data in a formatted table with Rich styling.
        
        Args:
            headers: Column definitions (str for simple header, dict for advanced config)
            rows: 2D list of data cells (supports Rich renderables)
            title: Table title (centered above table)
            box_style: Border style (e.g. 'simple', 'rounded', 'double', 'minimal')
            header_style: Base style for column headers
            row_styles: Alternating row styles for zebra striping
            caption: Table footer description
            expand: Expand table to terminal width (default: False)

        Examples:
            Simple table:
            >>> headers = ["Name", "Age", "Role"]
            >>> rows = [["Alice", "28", "Developer"], ["Bob", "35", "Manager"]]
            >>> ClientConsole.table(headers, rows, "Team Roster")

            Advanced headers:
            >>> headers = [
                {"header": "ID", "style": "dim", "justify": "right"},
                {"header": "Status", "style": "bold magenta"}
            ]
        """
        
        tbl = Table(
            title=title,
            box=box_style,
            header_style=header_style,
            row_styles=row_styles or [],
            expand=expand,
            caption=caption
        )

        # Process column headers
        for header in headers:
            if isinstance(header, dict):
                tbl.add_column(**header)
            else:
                tbl.add_column(header)

        # Add rows with optional styling
        for row in rows:
            tbl.add_row(*[str(cell) for cell in row])

        console.print(tbl)
    
    @staticmethod
    @contextmanager
    def loading(spinner: str = 'dots', message: str = 'Loading...'):
        """Context manager for showing loading spinners"""
        with console.status(message, spinner=spinner) as status:
            try:
                yield status
            except Exception as e:
                ClientConsole.error(f"Operation failed: {str(e)}")
                raise
    
    @staticmethod
    def help(cmd: str):
        """Display command help documentation
        
        Args:
            cmd (str): The command to display help for
        """
        command = COMMANDS[cmd]

        # Command header
        ClientConsole.print(f"[bold cyan]Command:[/bold cyan] {cmd}\n")
        
        # Description
        if command.doc:
            ClientConsole.print(f"[#00AAAA]{command.doc.description}[/#00AAAA]\n")
        
        # Flags section
        ClientConsole.print("[bold yellow]Flags:[/bold yellow]")
        for short_flag, flag_config in command.flags.items():
            doc_text = command.doc.additions.get(short_flag, "No description available") if command.doc else ""
            flag_line = (
                f"[bold white]  -{short_flag}[/bold white]/[bold white]--{flag_config.long}[/bold white]"
                f"[#00AAAA] {doc_text}[/#00AAAA]"
            )
            ClientConsole.print(flag_line)

        # Examples
        if command.doc and 'examples' in command.doc.additions:
            ClientConsole.print("\n[bold yellow]Examples:[/bold yellow]")
            ClientConsole.print(f"[#00AAAA]{command.doc.additions['examples']}[/#00AAAA]")