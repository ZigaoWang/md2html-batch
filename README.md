# MD2HTML - Markdown to HTML Converter (Batch Edition)

## Overview

MD2HTML is a powerful and user-friendly tool for converting Markdown files to HTML in batch mode. This tool supports syntax highlighting, custom CSS styling, and generates an index page for easy navigation. The project is ideal for creating personal blogs, documentation sites, or any other static web content from Markdown files.

## Features

- **Batch Conversion**: Converts multiple Markdown files to HTML in one go.
- **Custom CSS Styling**: Supports light and dark mode themes.
- **Syntax Highlighting**: Uses Pygments for beautiful code highlighting.
- **Copy Button for Code Blocks**: Adds a copy button to code blocks for easy copying.
- **MathJax Support**: Automatically includes MathJax for rendering mathematical notations.
- **Index Page Generation**: Creates an index page listing all converted HTML files.
- **Folder Structure Option**: Option to organize HTML files into folders for clean URLs.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/ZigaoWang/md2html-batch.git
   cd md2html-batch
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your Markdown files in the `input` folder.

2. Run the script:
   ```bash
   python main.py
   ```

3. Follow the prompts to choose your preferences:
   - **Mode**: Choose between light and dark mode for CSS styling.
   - **Site Name**: Enter a name for your site, which will appear as the title of the index page.
   - **Use Folders**: Decide whether to use folders for clean URLs.

4. The converted HTML files will be generated in the `output` folder, with an `index.html` file for navigation.

## Customization

- **CSS Styles**: Modify `style_light.css` and `style_dark.css` to customize the appearance of your HTML files.

## Example

Here's an example of how to convert Markdown files:

1. Place your `.md` files in the `input` folder.
2. Run `python main.py`.
3. Enter your preferences when prompted.
4. The HTML files will be generated in the `output` folder.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Credits

Made with 💜 by [Zigao Wang](https://zigao.wang).

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## Acknowledgements

- [Markdown](https://daringfireball.net/projects/markdown/)
- [BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/)
- [Pygments](https://pygments.org/)
- [MathJax](https://www.mathjax.org/)

## Contact

For any questions or suggestions, please open an issue or contact [Zigao Wang](mailto:a@zigao.wang).