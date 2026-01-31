"""Output formatting utilities for MedKit CLI modules.

This module provides unified output formatting functions for displaying
results in a consistent, readable format using the Rich library.
"""

from typing import Any, Dict, Union
from pydantic import BaseModel
from rich.console import Console
from rich.panel import Panel


def print_result(
    result: Union[BaseModel, Dict[str, Any], Any],
    verbose: bool = False,
    title: str = "Result",
    border_style: str = "cyan"
) -> None:
    """Print result in a formatted manner using rich.

    This function handles multiple result types:
    - Pydantic BaseModel instances
    - Dictionary objects
    - Plain text/other objects

    Args:
        result: The result to print (BaseModel, dict, or other)
        verbose: Enable verbose output (currently unused, for future expansion)
        title: Title for the output panel
        border_style: Border style for panels (default: "cyan")
    """
    console = Console()

    if result is None:
        console.print("[yellow]No result to display[/yellow]")
        return

    # Convert Pydantic models to dict
    if isinstance(result, BaseModel):
        result_dict = result.model_dump()
    elif isinstance(result, dict):
        result_dict = result
    else:
        # For other types, display as-is
        console.print(Panel(
            str(result),
            title=title,
            border_style=border_style,
        ))
        return

    # Display dictionary results in organized sections
    for section_name, section_value in result_dict.items():
        if section_value is not None:
            formatted_text = _format_value(section_value)

            console.print(Panel(
                formatted_text,
                title=section_name.replace('_', ' ').title(),
                border_style=border_style,
            ))


def _format_value(value: Any, indent: int = 0) -> str:
    """Format a value for display.

    Args:
        value: The value to format
        indent: Indentation level (for nested structures)

    Returns:
        Formatted string representation
    """
    indent_str = "  " * indent

    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            key_display = k.replace('_', ' ').title()
            if isinstance(v, (dict, list)):
                lines.append(f"{indent_str}[bold]{key_display}:[/bold]")
                lines.append(_format_value(v, indent + 1))
            else:
                lines.append(f"{indent_str}[bold]{key_display}:[/bold] {v}")
        return "\n".join(lines)

    elif isinstance(value, list):
        if not value:
            return f"{indent_str}[dim](empty)[/dim]"

        lines = []
        for i, item in enumerate(value, 1):
            if isinstance(item, (dict, list)):
                lines.append(f"{indent_str}[bold]{i}.[/bold]")
                lines.append(_format_value(item, indent + 1))
            else:
                lines.append(f"{indent_str}[bold]{i}.[/bold] {item}")
        return "\n".join(lines)

    else:
        return f"{indent_str}{value}"


def print_simple_result(
    result: Union[str, Dict[str, Any]],
    title: str = "Result",
    border_style: str = "cyan"
) -> None:
    """Print a simple result (string or flat dict) using rich.

    Args:
        result: String or dictionary to display
        title: Title for the output panel
        border_style: Border style for panel
    """
    console = Console()

    if result is None:
        console.print("[yellow]No result to display[/yellow]")
        return

    if isinstance(result, dict):
        formatted_text = "\n".join([f"  [bold]{k}:[/bold] {v}" for k, v in result.items()])
    else:
        formatted_text = str(result)

    console.print(Panel(
        formatted_text,
        title=title,
        border_style=border_style,
    ))
