import os
import argparse
import markdown
from bs4 import BeautifulSoup
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter


def print_logo():
    logo = r"""
   __  ______    ___    __ __________  _____ 
  /  |/  / _ \  |_  |  / // /_  __/  |/  / / 
 / /|_/ / // / / __/  / _  / / / / /|_/ / /__
/_/  /_/____/ /____/ /_//_/ /_/ /_/  /_/____/
    """
    print("--------------------------------------------------")
    print(logo)
    print("MD2HTML - Markdown to HTML Converter")
    print("Made with 💜 by Zigao Wang.")
    print("This project is licensed under MIT License.")
    print("GitHub Repo: https://github.com/ZigaoWang/md2html/")
    print("--------------------------------------------------")


def convert_md_to_html(md_text, light_mode=True):
    html = markdown.markdown(md_text,
                             extensions=['fenced_code', 'tables', 'toc', 'footnotes', 'attr_list', 'md_in_html'])
    soup = BeautifulSoup(html, 'html.parser')

    for code in soup.find_all('code'):
        parent = code.parent
        if parent.name == 'pre':
            language = code.get('class', [''])[0].replace('language-', '') or 'text'
            lexer = get_lexer_by_name(language, stripall=True)
            formatter = HtmlFormatter(style='default' if light_mode else 'monokai')
            highlighted_code = highlight(code.string, lexer, formatter)
            code.replace_with(BeautifulSoup(highlighted_code, 'html.parser'))

            copy_button_html = f'''
            <div class="code-header">
                <span class="language-label">{language}</span>
                <button class="copy-button" onclick="copyCode(this)">
                    <svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon">
                        <path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path>
                        <path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path>
                    </svg>
                </button>
            </div>
            '''
            parent.insert_before(BeautifulSoup(copy_button_html, 'html.parser'))

    return soup.prettify()


def add_custom_style(html_content, css_content=None):
    styled_html = f"<style>{css_content}</style>\n{html_content}" if css_content else html_content

    footer = """
    <footer>
        <p>Powered by <a href="https://github.com/ZigaoWang/md2html/">MD2HTML</a> by <a href="https://zigao.wang">Zigao Wang</a></p>
    </footer>
    """

    copy_button_script = """
    <script>
    function copyCode(button) {
        const code = button.closest('.code-header').nextElementSibling.innerText;
        navigator.clipboard.writeText(code).then(() => {
            button.innerHTML = '<svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-check"><path fill-rule="evenodd" d="M13.78 3.22a.75.75 0 0 1 0 1.06l-7.5 7.5a.75.75 0 0 1-1.06 0l-3.5-3.5a.75.75 0 0 1 1.06-1.06L6 10.44l7.22-7.22a.75.75 0 0 1 1.06 0z"></path></svg>';
            setTimeout(() => { 
                button.innerHTML = '<svg aria-hidden="true" height="16" viewBox="0 0 16 16" version="1.1" width="16" data-view-component="true" class="octicon octicon-copy js-clipboard-copy-icon"><path d="M0 6.75C0 5.784.784 5 1.75 5h1.5a.75.75 0 0 1 0 1.5h-1.5a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-1.5a.75.75 0 0 1 1.5 0v1.5A1.75 1.75 0 0 1 9.25 16h-7.5A1.75 1.75 0 0 1 0 14.25Z"></path><path d="M5 1.75C5 .784 5.784 0 6.75 0h7.5C15.216 0 16 .784 16 1.75v7.5A1.75 1.75 0 0 1 14.25 11h-7.5A1.75 1.75 0 0 1 5 9.25Zm1.75-.25a.25.25 0 0 0-.25.25v7.5c0 .138.112.25.25.25h7.5a.25.25 0 0 0 .25-.25v-7.5a.25.25 0 0 0-.25-.25Z"></path></svg>';
            }, 2000);
        });
    }
    </script>
    """

    mathjax_script = """
    <script>
    (function () {
        var script = document.createElement('script');
        script.type = 'text/javascript';
        script.src = 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js';
        document.head.appendChild(script);
    })();
    </script>
    """

    return styled_html + footer + copy_button_script + mathjax_script


def batch_convert_md_to_html(entries_folder, output_folder, site_name, light_mode=True, use_folders=True):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    css_path = 'style_light.css' if light_mode else 'style_dark.css'
    css_content = ""
    if os.path.isfile(css_path):
        with open(css_path, 'r', encoding='utf-8') as css_file:
            css_content = css_file.read()

    md_files = [f for f in os.listdir(entries_folder) if f.endswith('.md')]
    md_files.sort()

    for md_file in md_files:
        md_file_path = os.path.join(entries_folder, md_file)
        with open(md_file_path, 'r', encoding='utf-8') as file:
            md_text = file.read()

        html = convert_md_to_html(md_text, light_mode=light_mode)
        html_with_style = add_custom_style(html, css_content)

        if use_folders:
            html_folder_name = md_file.replace('.md', '')
            html_folder_path = os.path.join(output_folder, html_folder_name)
            os.makedirs(html_folder_path, exist_ok=True)
            html_file_path = os.path.join(html_folder_path, 'index.html')
        else:
            html_file_name = md_file.replace('.md', '.html')
            html_file_path = os.path.join(output_folder, html_file_name)

        with open(html_file_path, 'w', encoding='utf-8') as html_file:
            html_file.write(html_with_style)

        print(f"Converted {md_file} to {html_file_path}")

    index_content = f"""
    <html>
    <head>
        <title>{site_name}</title>
        <style>{css_content}</style>
    </head>
    <body>
        <h1>{site_name}</h1>
        <ul>
    """

    for md_file in md_files:
        if use_folders:
            html_file = md_file.replace('.md', '') + '/'
        else:
            html_file = md_file.replace('.md', '.html')
        index_content += f'<li><a href="{html_file}">{md_file.replace(".md", "")}</a></li>\n'

    index_content += """
        </ul>
        <footer>
            <p>Powered by <a href="https://github.com/ZigaoWang/md2html/">MD2HTML</a> by <a href="https://zigao.wang">Zigao Wang</a></p>
        </footer>
    </body>
    </html>
    """

    index_file_path = os.path.join(output_folder, 'index.html')
    with open(index_file_path, 'w', encoding='utf-8') as index_file:
        index_file.write(index_content)

    print(f"Generated index.html in {output_folder}")


def main():
    print_logo()
    mode = input("Choose the mode (light/dark): ").strip().lower()
    site_name = input("Enter the name of the site: ").strip()
    use_folders = input("Do you want to use folders for URLs? (yes/no): ").strip().lower() == 'yes'

    light_mode = mode == 'light'

    entries_folder = 'input'
    output_folder = 'output'

    batch_convert_md_to_html(entries_folder, output_folder, site_name, light_mode=light_mode, use_folders=use_folders)


if __name__ == "__main__":
    main()