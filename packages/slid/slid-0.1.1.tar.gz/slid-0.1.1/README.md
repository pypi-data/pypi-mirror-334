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
pip install slid
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

## AI

This tool was generated using AI, with the next prompt:

> create python tool to show slides in the terminal, (similar to "slides") but using Rich, Python library. the idea is take a Markdown File, find the key “---\”n and split the file in slides, use a beautiful color schema, and you can add at the bottom, the name of the users and the name of the slides (markdown name) and in the other side you can add the number of the slides such us (1/14 for example). allow run "bash" and "python" cells/Code Block, if you can write "r 1" run the cell 1. Also allow to copy the blocks and URL in the links using the command “c”, for example if in one slide you have 1 bash block and 2 links, you can run “c 3”, to copy the 2nd link or “r 2” to open the 1st link in the slide. For move between the slides, the user can user the arrow keys (next and previous), the enter key, or the space key (for next), up key (beginning), down key (last slide).

Ussing [aider](https://aider.chat) agent in [BeeAI](https://beeai.dev) platform
