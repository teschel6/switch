from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
import readchar
from typing import Optional, List

from switch.datatypes import UserConfig, Reference


def get_key() -> str:
    """Simple cross-platform key reading using readchar"""
    key = readchar.readkey()

    if key == readchar.key.UP:
        return "up"
    elif key == readchar.key.DOWN:
        return "down"
    elif key in (readchar.key.ENTER, readchar.key.CR, readchar.key.LF):
        return "enter"
    elif key in (readchar.key.BACKSPACE, readchar.key.DELETE):
        return "backspace"

    return key


def control_hint() -> Text:
    """Make a styled control hint"""
    hint = Text()
    hint.append("↑ / ↓", style="bold green")
    hint.append(" select ", style="bold bright_white")
    hint.append("^C", style="bold green")
    hint.append(" exit ", style="bold bright_white")

    return hint


def select_project(config: UserConfig) -> Optional[Reference]:
    """Interactive project selector with filtering"""
    console = Console()
    selected_index = 0
    filter_text = ""

    def get_filtered_projects() -> List[Reference]:
        """Return projects that match the filter"""
        if not filter_text:
            return config.projects
        return [p for p in config.projects if filter_text.lower() in p.name.lower()]

    def render_ui() -> None:
        """Render the current state of the UI"""
        filtered = get_filtered_projects()

        table = Table(box=None, show_header=False)
        table.add_column("selected", justify="left", style="blue", no_wrap=True)
        table.add_column("name", justify="left", style="blue", no_wrap=True)
        table.add_column("directory", justify="left")
        table.add_column("id", justify="left", style="bright_black")

        for i, ref in enumerate(filtered):
            if i == selected_index:
                table.add_row(
                    ">", ref.name, ref.directory, ref.id, style="black on white"
                )
            else:
                table.add_row(" ", ref.name, ref.directory, ref.id)

        if not filtered:
            table.add_row("", "No matching projects", "", "", style="bright_black")

        table_panel = Panel(
            table,
            title="[bold]Projects[/bold]",
            height=20,
            subtitle=control_hint(),
            subtitle_align="left",
            border_style="magenta",
        )

        prompt_panel = Panel(
            f"> {filter_text}█",
            title="[bold]Filter[/bold]",
            border_style="magenta",
        )

        console.clear()
        console.print()
        console.print(table_panel)
        console.print(prompt_panel)

    try:
        # Main interaction loop
        while True:
            render_ui()
            filtered = get_filtered_projects()

            # Ensure selected_index is valid
            if filtered and selected_index >= len(filtered):
                selected_index = len(filtered) - 1
            if selected_index < 0:
                selected_index = 0

            key = get_key()

            if key == "up":
                if filtered and selected_index > 0:
                    selected_index -= 1
            elif key == "down":
                if filtered and selected_index < len(filtered) - 1:
                    selected_index += 1
            elif key == "backspace":
                if filter_text:
                    filter_text = filter_text[:-1]
                    selected_index = 0
            elif key == "esc":
                return None
            elif key and len(key) == 1 and key.isprintable():
                filter_text += key
                selected_index = 0
            elif key == "enter":
                console.clear()
                if filtered:
                    return filtered[selected_index]
                return None
    except KeyboardInterrupt:
        return None
