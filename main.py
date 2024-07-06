import os
from datetime import datetime
import markdown
from jinja2 import Environment, FileSystemLoader

TEMPLATE_DIR = 'templates'
ENTRY_DIR = 'entries'
HTML_DIR = 'html'

env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))


def create_entry():
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f"{date_str}.md"
    filepath = os.path.join(ENTRY_DIR, filename)

    if os.path.exists(filepath):
        print(f"Entry for {date_str} already exists.")
        return

    with open(filepath, 'w') as file:
        file.write(f"# Journal Entry for {date_str}\n\n")

    print(f"Created new entry: {filename}")


def list_entries():
    entries = sorted(os.listdir(ENTRY_DIR))
    for entry in entries:
        print(entry)
    return entries


def convert_to_html(entry):
    try:
        with open(os.path.join(ENTRY_DIR, entry), 'r') as file:
            md_content = file.read()

        html_content = markdown.markdown(md_content)
        template = env.get_template('journal_template.html')
        rendered_html = template.render(content=html_content, title=entry.replace('.md', ''))

        output_file = entry.replace('.md', '.html')
        output_path = os.path.join(HTML_DIR, output_file)

        with open(output_path, 'w') as file:
            file.write(rendered_html)

        print(f"Converted {entry} to HTML: {output_file}")
    except FileNotFoundError:
        print(f"Error: The file {entry} does not exist.")


def generate_index(entries):
    entry_list = [
        {"title": entry.replace('.md', ''), "link": entry.replace('.md', '.html')}
        for entry in entries
    ]
    template = env.get_template('index_template.html')
    rendered_html = template.render(entries=entry_list)

    with open(os.path.join(HTML_DIR, 'index.html'), 'w') as file:
        file.write(rendered_html)

    print("Generated index.html")


def generate_site():
    entries = list_entries()
    for entry in entries:
        convert_to_html(entry)
    generate_index(entries)


def main():
    os.makedirs(ENTRY_DIR, exist_ok=True)
    os.makedirs(HTML_DIR, exist_ok=True)

    while True:
        print("--------------------------------------------------")
        print("Choose an option:")
        print("1. Create a new journal entry")
        print("2. List journal entries")
        print("3. Convert an entry to HTML")
        print("4. Generate the entire site")
        print("5. Exit")
        print("--------------------------------------------------")

        choice = input("Enter your choice: ")

        if choice == '1':
            create_entry()
        elif choice == '2':
            list_entries()
        elif choice == '3':
            entry = input("Enter the entry filename (e.g., 2024-07-01.md): ")
            convert_to_html(entry)
        elif choice == '4':
            generate_site()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
