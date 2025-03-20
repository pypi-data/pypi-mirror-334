#!/usr/bin/env python3
"""
slid.py

A terminal-based slide presentation tool that renders Markdown files
as beautiful slides in your terminal using the Rich library.

Usage:
    python slid.py <markdown_file> [--author <author_name>]

Example:
    python slid.py my_presentation.md --author "John Doe"

Features:
    - Navigate slides with arrow keys
    - Execute bash and Python code blocks by typing "r <code_block_number>"
    - Copy code blocks to clipboard with "c <code_block_number>"
    - Open URLs with "r url" or copy URLs with "c url"
    - Beautiful rich formatting
    - Support for Markdown-formatted links [text](url)

Requirements:
    pip install rich readchar pyperclip
"""

import os
import sys
import argparse
import time
import re
import subprocess
import tempfile
import webbrowser
from pathlib import Path
import readchar
import pyperclip  # For clipboard functionality

from rich.console import Console
from rich.syntax import Syntax
from rich.markdown import Markdown
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rich.align import Align
from rich.table import Table
from rich.console import Group


class MarkdownSlides:
    def __init__(self, markdown_file, author=None):
        """Initialize the slides application."""
        self.markdown_file = markdown_file
        self.file_name = Path(markdown_file).stem
        self.author = author or os.getenv("USER", "Presenter")
        self.slides = []
        self.current_slide = 0
        self.console = Console()
        self.last_key = None  # Track the last key pressed
        self.theme = {
            "background": "deep_sky_blue4",
            "foreground": "white",
            "accent": "cyan",
            "title": "bright_white",
            "code_output": "green",
            "error": "red",
            "url": "blue underline",
        }
        self.code_blocks = (
            []
        )  # Will store tuples of (slide_index, global_idx, slide_idx, language, code)
        self.urls = {}  # Will store URLs for each slide
        self.last_block_index = {}  # Track the last block index used per slide

    def parse_slides(self):
        """Parse the markdown file into individual slides."""
        try:
            with open(self.markdown_file, "r", encoding="utf-8") as file:
                content = file.read()

            # Split content by the slide separator (---), but only when it's on its own line
            # This prevents splitting inside code blocks that contain ---
            slides = []
            current_slide = ""
            in_code_block = False

            for line in content.splitlines():
                # Track if we're inside a code block
                if line.startswith("```"):
                    in_code_block = not in_code_block

                # Only split at --- when it's on its own line and not in a code block
                if line.strip() == "---" and not in_code_block:
                    if current_slide.strip():  # Only add non-empty slides
                        slides.append(current_slide.strip())
                    current_slide = ""
                else:
                    current_slide += line + "\n"

            # Add the last slide if it's not empty
            if current_slide.strip():
                slides.append(current_slide.strip())

            self.slides = slides

            if not self.slides:
                raise ValueError("No slides found in the markdown file.")

            # Extract title from the first slide if it starts with a # heading
            title_line = (
                self.slides[0].splitlines()[0] if self.slides[0].splitlines() else ""
            )
            if title_line.startswith("#"):
                self.title = title_line.lstrip("#").strip()
            else:
                self.title = self.file_name.replace("_", " ").title()

            # Parse code blocks and URLs from all slides
            self.extract_code_blocks()
            self.extract_urls()

        except FileNotFoundError:
            print(f"Error: File '{self.markdown_file}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error parsing markdown file: {e}")
            sys.exit(1)

    def extract_code_blocks(self):
        """Extract executable code blocks from slides with sequential numbering."""
        code_block_pattern = re.compile(r"```(python|bash|sh)(.*?)```", re.DOTALL)

        # Reset code blocks and last block index tracking
        self.code_blocks = []
        self.last_block_index = {}
        global_block_index = 0

        for slide_index, slide_content in enumerate(self.slides):
            # Find all code blocks in this slide
            matches = code_block_pattern.finditer(slide_content)
            slide_block_index = 1  # Start numbering from 1 for each slide

            for match in matches:
                language = match.group(1)
                # Strip leading/trailing whitespace and extract code
                code = match.group(2).strip()

                if language == "sh":
                    language = "bash"  # Normalize shell language names

                if code and language in ("python", "bash"):
                    # Store code block with slide-specific index and global index
                    self.code_blocks.append(
                        (
                            slide_index,
                            global_block_index,
                            slide_block_index,
                            language,
                            code,
                        )
                    )
                    global_block_index += 1
                    slide_block_index += 1

            # Store the last used block index for this slide
            if slide_block_index > 1:  # If there were any blocks
                self.last_block_index[slide_index] = slide_block_index - 1
            else:
                self.last_block_index[slide_index] = 0

            # Update the slide content to include code block numbers
            updated_content = slide_content

            # Replace each code block with a numbered version
            for i, (s_idx, g_idx, s_block_idx, lang, _) in enumerate(self.code_blocks):
                if s_idx == slide_index:
                    old_block = f"```{lang}"
                    new_block = f"```{lang} [#{s_block_idx}]"
                    # Only replace the first occurrence that hasn't been replaced yet
                    updated_content = updated_content.replace(old_block, new_block, 1)

            # Update the slide content with numbered code blocks
            self.slides[slide_index] = updated_content

    def extract_urls(self):
        """Extract URLs from slides, including Markdown format links, continuing numbering from code blocks."""
        # Pattern for standard URLs
        raw_url_pattern = re.compile(r"https?://\S+")

        # Pattern for Markdown links [text](url)
        md_link_pattern = re.compile(r"\[(.*?)\]\((https?://[^)]+)\)")

        # Reset the URLs dict
        self.urls = {}

        for slide_index, slide_content in enumerate(self.slides):
            # Find all URLs in this slide
            raw_urls = raw_url_pattern.findall(slide_content)
            md_links = md_link_pattern.findall(slide_content)

            # Process raw URLs first (but exclude those that are part of markdown links)
            filtered_raw_urls = []
            for url in raw_urls:
                # Check if this URL is part of a markdown link
                is_in_md_link = False
                for _, md_url in md_links:
                    if url.startswith(md_url) or md_url.startswith(url):
                        is_in_md_link = True
                        break

                if not is_in_md_link:
                    filtered_raw_urls.append(url)

            # Extract just the URLs from markdown links
            md_urls = [url for _, url in md_links]

            # Combine all URLs (raw URLs that aren't in markdown links + markdown link URLs)
            all_urls = filtered_raw_urls + md_urls

            if all_urls:
                # Get the last block index used for this slide, defaulting to 0 if none
                start_idx = self.last_block_index.get(slide_index, 0) + 1

                # Store URLs for this slide with slide-specific indices continuing from code blocks
                self.urls[slide_index] = []
                for i, url in enumerate(all_urls, start_idx):
                    # Store as (url_index, url)
                    self.urls[slide_index].append((i, url))

    def create_slide_layout(self):
        """Create the layout for each slide."""
        layout = Layout()

        # Split the layout into header, content, and footer
        layout.split(
            Layout(name="header", size=3),
            Layout(name="content"),
            Layout(name="footer", size=3),
        )

        return layout

    def render_header(self):
        """Render the slide header with just the presentation name."""
        presentation_name = Path(self.markdown_file).stem.replace("_", " ")

        return Panel(
            Align.center(
                Text(presentation_name, style=f"bold {self.theme['title']}"),
            ),
            style=self.theme["background"],
            border_style=self.theme["accent"],
        )

    def render_footer(self):
        """Render the slide footer with author name and slide number."""
        footer_table = Table.grid(expand=True)
        footer_table.add_column()
        footer_table.add_column(justify="right")

        # Add info about code execution if there are code blocks in this slide
        code_blocks_in_slide = [
            b for b in self.code_blocks if b[0] == self.current_slide
        ]
        urls_in_slide = self.urls.get(self.current_slide, [])

        footer_info = f"🙂 {self.author}"

        if code_blocks_in_slide or urls_in_slide:
            commands = []
            if code_blocks_in_slide or urls_in_slide:
                commands.append("'r #' to run code/URL")
                commands.append("'c #' to copy code/URL")

            footer_info = f"🙂 {self.author} | " + " | ".join(commands)

        author_text = Text(footer_info, style=self.theme["foreground"])

        slide_count = Text(
            f"{self.current_slide + 1}/{len(self.slides)} 📄",
            style=self.theme["foreground"],
        )

        footer_table.add_row(author_text, slide_count)

        return Panel(
            footer_table,
            style=self.theme["background"],
            border_style=self.theme["accent"],
        )

    def render_content(self, markdown_text):
        """Render the slide content."""
        # Create markdown object first
        md = Markdown(markdown_text)

        # Get the content with markdown as a layout element
        content = Align.center(md)

        # Add code block and URL hints if present, with unified numbering
        current_slide_blocks = [
            b for b in self.code_blocks if b[0] == self.current_slide
        ]
        urls_in_slide = self.urls.get(self.current_slide, [])

        if current_slide_blocks or urls_in_slide:
            hints = []
            all_items = []

            # Combine code blocks and URLs in order of their numbers
            for _, _, slide_block_idx, lang, _ in current_slide_blocks:
                all_items.append(("code", slide_block_idx, lang))

            for url_idx, url in urls_in_slide:
                all_items.append(("url", url_idx, url))

            # Sort by index to ensure they appear in numerical order
            all_items.sort(key=lambda x: x[1])

            # Create a single hints section with all runnable/copyable items
            if all_items:
                hint_text = Text(
                    "\nRunnable items on this slide:\n", style="italic dim grey70"
                )

                for item_type, idx, info in all_items:
                    if item_type == "code":
                        item_info = Text(f"#{idx}: ", style="grey74")
                        lang_info = Text(
                            f"Code block ({info})\n", style="italic grey70"
                        )
                        hint_text.append(item_info)
                        hint_text.append(lang_info)
                    else:  # URL
                        item_info = Text(f"#{idx}: ", style="grey74")
                        url_text = Text(f"{info}\n", style=self.theme["url"])
                        hint_text.append(item_info)
                        hint_text.append(url_text)

                hints.append(hint_text)

            # Create a compound layout with markdown and hints
            content = Group(md, *hints)

        return Panel(
            content,
            style=self.theme["background"],
            border_style=self.theme["accent"],
            padding=(1, 2),
        )

    def display_slide(self, slide_index):
        """Display a single slide."""
        self.current_slide = slide_index

        # Clear the console
        self.console.clear()

        # Create the layout
        layout = self.create_slide_layout()

        # Populate the layout
        layout["header"].update(self.render_header())
        layout["content"].update(self.render_content(self.slides[slide_index]))
        layout["footer"].update(self.render_footer())

        # Render the layout
        self.console.print(layout)

    def get_key(self):
        """Get a key press, including special keys like arrows."""
        key = readchar.readkey()

        # Handle arrow keys
        arrow_keys = {
            "\x1b[A": "up",
            "\x1b[B": "down",
            "\x1b[C": "right",
            "\x1b[D": "left",
        }

        return arrow_keys.get(key, key)

    def get_command(self):
        """Get a command from the user (for longer input like 'r 1' or 'c 1')."""
        # Create a prompt at the bottom of the screen
        terminal_height = os.get_terminal_size().lines
        terminal_width = os.get_terminal_size().columns

        # Move cursor to bottom of screen
        sys.stdout.write(f"\033[{terminal_height-1};1H")
        sys.stdout.write("\033[K")  # Clear the line

        # Change the prompt based on the last key pressed
        if self.last_key == "r":
            sys.stdout.write("> r ")
        elif self.last_key == "c":
            sys.stdout.write("> c ")
        else:
            sys.stdout.write("> ")

        sys.stdout.flush()

        # Get user input
        command = input()

        # Clear the command line
        sys.stdout.write("\033[K")
        sys.stdout.flush()

        return command

    def handle_url_command(self, is_copy=False):
        """Handle URL commands (open or copy)."""
        urls = self.urls.get(self.current_slide, [])

        if not urls:
            self.console.clear()
            self.console.print("[bold red]No URLs found on this slide.[/]")
            self.console.print(
                "\n\n[italic]Press any key to return to the presentation...[/]"
            )
            readchar.readkey()
            return

        # If there's only one URL, use it; otherwise, let the user choose
        if len(urls) == 1:
            url_idx, url = urls[0]
            if is_copy:
                self.copy_to_clipboard(url, "URL")
            else:
                self.open_url(url)
        else:
            # Display list of URLs
            self.console.clear()
            self.console.print("[bold cyan]Multiple URLs found on this slide:[/]\n")

            for idx, url in urls:
                self.console.print(f"[bold]{idx}.[/] {url}")

            self.console.print("\n[bold yellow]Enter the number of the URL:[/]")
            choice = input("> ")

            try:
                idx = int(choice)
                url_match = next((url for url_idx, url in urls if url_idx == idx), None)
                if url_match:
                    if is_copy:
                        self.copy_to_clipboard(url_match, "URL")
                    else:
                        self.open_url(url_match)
                else:
                    raise ValueError("Invalid selection")
            except ValueError:
                self.console.print("[bold red]Invalid selection.[/]")
                self.console.print(
                    "\n\n[italic]Press any key to return to the presentation...[/]"
                )
                readchar.readkey()

    def open_url(self, url):
        """Open a URL in the web browser without showing intermediate screen."""
        try:
            # Simply open the URL without displaying any intermediate screen
            webbrowser.open(url)

            # No need to wait for a keypress or show a message
            # Just return to continue the presentation flow
        except Exception as e:
            self.console.clear()
            self.console.print(f"[bold red]Error opening URL: {str(e)}[/]")
            self.console.print(
                "\n\n[italic]Press any key to return to the presentation...[/]"
            )
            readchar.readkey()

    def execute_code_block(self, slide_block_number):
        """Execute a code block by its slide-specific index."""
        # Find code blocks for the current slide
        current_slide_blocks = [
            b for b in self.code_blocks if b[0] == self.current_slide
        ]

        # Find the block with the matching slide-specific index
        block = next(
            (b for b in current_slide_blocks if b[2] == slide_block_number), None
        )

        if not block:
            # If not a code block, check if it's a URL
            urls_in_slide = self.urls.get(self.current_slide, [])
            url_match = next(
                (url for idx, url in urls_in_slide if idx == slide_block_number), None
            )

            if url_match:
                # If it matches a URL, open it
                self.open_url(url_match)
                return
            else:
                # Neither a code block nor a URL
                self.console.clear()
                self.console.print(
                    f"[bold red]Error: Item #{slide_block_number} not found on this slide.[/]"
                )
                self.console.print(
                    "\n\n[italic]Press any key to return to the presentation...[/]"
                )
                readchar.readkey()
                return

        slide_index, _, _, language, code = block

        # Execute the code based on language
        if language == "python":
            self.execute_python(code)
        elif language == "bash":
            self.execute_bash(code)
        else:
            self.console.clear()
            self.console.print(
                f"[bold red]Error: Unsupported language '{language}'.[/]"
            )
            self.console.print(
                "\n\n[italic]Press any key to return to the presentation...[/]"
            )
            readchar.readkey()

    def copy_code_block(self, slide_block_number):
        """Copy a code block to the clipboard by its slide-specific index."""
        # Find code blocks for the current slide
        current_slide_blocks = [
            b for b in self.code_blocks if b[0] == self.current_slide
        ]

        # Find the block with the matching slide-specific index
        block = next(
            (b for b in current_slide_blocks if b[2] == slide_block_number), None
        )

        if not block:
            # If not a code block, check if it's a URL
            urls_in_slide = self.urls.get(self.current_slide, [])
            url_match = next(
                (url for idx, url in urls_in_slide if idx == slide_block_number), None
            )

            if url_match:
                # If it matches a URL, copy it
                self.copy_to_clipboard(url_match, "URL")
                return
            else:
                # Neither a code block nor a URL
                self.console.clear()
                self.console.print(
                    f"[bold red]Error: Item #{slide_block_number} not found on this slide.[/]"
                )
                self.console.print(
                    "\n\n[italic]Press any key to return to the presentation...[/]"
                )
                readchar.readkey()
                return

        slide_index, _, _, language, code = block
        self.copy_to_clipboard(code, f"Code Block #{slide_block_number} ({language})")

    def copy_to_clipboard(self, text, description):
        """Copy text to clipboard silently without showing confirmation."""
        try:
            # Copy the text to the clipboard
            pyperclip.copy(text)

            # Show a minimal status message at the bottom of the screen
            terminal_height = os.get_terminal_size().lines
            terminal_width = os.get_terminal_size().columns

            # Move cursor to bottom of screen and clear line
            sys.stdout.write(f"\033[{terminal_height-1};1H")
            sys.stdout.write("\033[K")  # Clear the line

            # Brief notification that disappears automatically
            sys.stdout.write("\033[32mCopied to clipboard\033[0m")  # Green text
            sys.stdout.flush()

            # Wait briefly then clear the message
            time.sleep(0.8)
            sys.stdout.write("\033[K")  # Clear the line
            sys.stdout.flush()

        except Exception as e:
            # Show error briefly at bottom of screen
            terminal_height = os.get_terminal_size().lines
            terminal_width = os.get_terminal_size().columns

            sys.stdout.write(f"\033[{terminal_height-1};1H")
            sys.stdout.write("\033[K")  # Clear the line
            sys.stdout.write(
                f"\033[31mError copying to clipboard: {str(e)}\033[0m"
            )  # Red text
            sys.stdout.flush()

            time.sleep(1.5)
            sys.stdout.write("\033[K")  # Clear the line
            sys.stdout.flush()

    def execute_python(self, code):
        """Execute Python code and stream the output."""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(
                suffix=".py", mode="w", delete=False
            ) as temp:
                temp.write(code)
                temp_name = temp.name

            self.console.clear()
            self.console.print(
                Panel(
                    f"[bold cyan]Executing Python Code:[/]\n\n{code}",
                    title="Code Block",
                    border_style="cyan",
                )
            )
            self.console.print("\n[bold green]Output:[/]\n")

            # Execute the code and stream output
            process = subprocess.Popen(
                [sys.executable, temp_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
            )

            # Stream stdout in real-time
            for line in process.stdout:
                self.console.print(line, end="")

            process.wait(timeout=10)

            # Display stderr if there was an error
            if process.returncode != 0:
                self.console.print("\n[bold red]Error:[/]\n", end="")
                for line in process.stderr:
                    self.console.print(line, end="")

            # Remove the temporary file
            os.unlink(temp_name)

            self.console.print(
                "\n\n[italic]Press any key to return to the presentation...[/]"
            )
            readchar.readkey()

        except subprocess.TimeoutExpired:
            self.console.print(
                "\n[bold red]Error: Execution timed out after 10 seconds.[/]"
            )
            self.console.print(
                "\n\n[italic]Press any key to return to the presentation...[/]"
            )
            readchar.readkey()
        except Exception as e:
            self.console.print(f"\n[bold red]Error: {str(e)}[/]")
            self.console.print(
                "\n\n[italic]Press any key to return to the presentation...[/]"
            )
            readchar.readkey()

    def execute_bash(self, code):
        """Execute bash code and stream the output."""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(
                suffix=".sh", mode="w", delete=False
            ) as temp:
                temp.write(code)
                temp_name = temp.name

            # Make the script executable
            os.chmod(temp_name, 0o755)

            self.console.clear()
            self.console.print(
                Panel(
                    f"[bold cyan]Executing Bash Code:[/]\n\n{code}",
                    title="Code Block",
                    border_style="cyan",
                )
            )
            self.console.print("\n[bold green]Output:[/]\n")

            # Execute the code and stream output
            process = subprocess.Popen(
                ["/bin/bash", temp_name],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,  # Line buffered
            )

            # Stream stdout in real-time
            for line in process.stdout:
                self.console.print(line, end="")

            process.wait(timeout=10)

            # Display stderr if there was an error
            if process.returncode != 0:
                self.console.print("\n[bold red]Error:[/]\n", end="")
                for line in process.stderr:
                    self.console.print(line, end="")

            # Remove the temporary file
            os.unlink(temp_name)

            self.console.print(
                "\n\n[italic]Press any key to return to the presentation...[/]"
            )
            readchar.readkey()

        except subprocess.TimeoutExpired:
            self.console.print(
                "\n[bold red]Error: Execution timed out after 10 seconds.[/]"
            )
            self.console.print(
                "\n\n[italic]Press any key to return to the presentation...[/]"
            )
            readchar.readkey()
        except Exception as e:
            self.console.print(f"\n[bold red]Error: {str(e)}[/]")
            self.console.print(
                "\n\n[italic]Press any key to return to the presentation...[/]"
            )
            readchar.readkey()

    def run_presentation(self):
        """Run the slide presentation."""
        self.parse_slides()

        self.console.clear()
        self.console.print(
            Align.center(
                Text(
                    f"\n\nslid.py: {self.title}\n\n",
                    style=f"bold {self.theme['title']}",
                )
            )
        )
        self.console.print(
            Align.center(
                Text(
                    "Navigation:\n"
                    "→ or 'n': Next slide\n"
                    "← or 'p': Previous slide\n"
                    "↑/↓: Also navigate slides\n"
                    "Number keys: Jump to slide\n"
                    "Press 'r' then type a number: Run code block or open URL\n"
                    "Press 'r url': Select from multiple URLs to open\n"
                    "Press 'c' then type a number: Copy code or URL to clipboard\n"
                    "Press 'c url': Select from multiple URLs to copy\n"
                    "'q': Quit presentation\n\n"
                    "Press any key to start...",
                    style=self.theme["foreground"],
                )
            )
        )

        # Wait for user input to start
        readchar.readkey()

        slide_index = 0
        while True:
            self.display_slide(slide_index)

            key = self.get_key()

            if key == "q":
                break
            elif key == "r":  # Run code or open URL
                self.last_key = "r"  # Store the last key
                command = self.get_command()

                if command.strip().lower() == "url":
                    self.handle_url_command(is_copy=False)
                    self.display_slide(slide_index)  # Redisplay the slide
                else:
                    try:
                        # Convert the input to a number
                        block_index = int(command.strip())
                        self.execute_code_block(block_index)
                        self.display_slide(slide_index)  # Redisplay the slide
                    except ValueError:
                        # Just redisplay the slide if input was invalid
                        self.display_slide(slide_index)

            elif key == "c":  # Copy code or URL
                self.last_key = "c"  # Store the last key
                command = self.get_command()

                if command.strip().lower() == "url":
                    self.handle_url_command(is_copy=True)
                    self.display_slide(slide_index)  # Redisplay the slide
                else:
                    try:
                        # Convert the input to a number
                        block_index = int(command.strip())
                        self.copy_code_block(block_index)
                        self.display_slide(slide_index)  # Redisplay the slide
                    except ValueError:
                        # Just redisplay the slide if input was invalid
                        self.display_slide(slide_index)

            elif key in (
                "n",
                "right",
                "down",
                " ",
                "\r",
            ):  # Next slide (right arrow, down arrow, space, or Enter)
                slide_index = min(slide_index + 1, len(self.slides) - 1)
            elif key in ("p", "left", "up"):  # Previous slide (left arrow, up arrow)
                slide_index = max(slide_index - 1, 0)
            elif key.isdigit():  # Jump to specific slide
                target = int(key) - 1
                if 0 <= target < len(self.slides):
                    slide_index = target

        # End presentation
        self.console.clear()
        self.console.print(
            Align.center(
                Text(
                    "\n\nPresentation ended.\nThank you!\n\n",
                    style=f"bold {self.theme['title']}",
                )
            )
        )


def main():
    """Parse command line arguments and run the presentation."""
    parser = argparse.ArgumentParser(
        description="Terminal-based Markdown slides presenter"
    )
    parser.add_argument(
        "markdown_file", help="Path to the markdown file containing slides"
    )
    parser.add_argument("--author", help="Name of the presenter/author", default=None)

    args = parser.parse_args()

    slides = MarkdownSlides(args.markdown_file, args.author)
    slides.run_presentation()


if __name__ == "__main__":
    main()
