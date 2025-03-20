# slid

A terminal-based presentation tool that turns Markdown files into beautiful interactive slides with code execution capabilities. 

![Terminal Slides Screenshot](assets/screen.jpeg)

## Features

- ✨ Beautiful terminal-based presentation slides
- 🖼️ Renders Markdown with rich formatting
- ⌨️ Simple keyboard navigation (arrow keys or keyboard shortcuts)
- 🔄 Automatic slide detection using "---" separator
- 💻 Execute Python and Bash code blocks directly within the presentation
- 📋 Copy code blocks to clipboard with a single command
- 🌐 Open URLs directly from the presentation
- 🎨 Elegant color scheme and formatting

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/slid.py.git
cd slid.py
pip install .
```

or

```bash
pip install git+https://github.com/ismaelfaro/slid.py.git
```

## Usage

```bash
slid your_presentation.md
```

```bash
slid your_presentation.md --author "Your Name"
```

## Navigation

- **→** or **n**: Next slide
- **←** or **p**: Previous slide
- **↑/↓**: Also navigate slides
- **Number keys**: Jump to specific slide
- **r**: Run code block (followed by block number) or open URL (followed by "url")
- **c**: Copy code to clipboard (followed by block number)
- **q**: Quit presentation

## Code Execution

Code blocks are automatically detected and numbered for each slide. When on a slide with code:

1. Python and Bash/Shell code blocks are automatically detected
2. Press **r** followed by the block number to execute (e.g., **r 1**)
3. Output is displayed in real-time
4. Press any key to return to the presentation

## Opening URLs

You can open URLs directly from the presentation:

1. Press **r** followed by "url" (e.g., **r url**)
2. The default web browser will open with the URL from the slide
3. The presentation continues to display while the browser opens

## Clipboard Function

To copy code to your clipboard:

1. Press **c** followed by the block number (e.g., **c 1**)
2. A confirmation will display that the code was copied
3. Press any key to return to the presentation

## License

Apache License 2.0

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.