import json, os, sys
import pyfiglet
from libgen_api import LibgenSearch 

from rich import box
from rich.text import Text
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from rich.markdown import Markdown

libgen = LibgenSearch()
console = Console()

def clear_console() -> None:
    """
    Clear terminal & print title, rendered using Figlet.
    """

    os.system("cls" if os.name == "nt" else "clear")
    console_width = os.get_terminal_size().columns
    header_title = pyfiglet.figlet_format("G a i a", font="roman").rstrip("\n ") + "\n"
    header_subtitle = "the terminal-living libgen browser"
    header_text = Text(header_title + "\n" + header_subtitle, justify="center")
    header = Panel(header_text, style="bold green", expand=True)
    console.print(header)
    print("\n")

def show_results(response: list, query: str, query_type: str) -> str:
    """
    Display LibGen API results.
    """

    clear_console()
    fields = ["Title", "Author", "Year", "Extension"]
    results = []

    # only take desired fields
    for item in response:
        result = dict()
        for field in fields:
            result[field] = item[field]
        results.append(result)

    # truncate titles & authors
    '''
    max_length = 32
    for result in results:
        title, author = result["Title"], result["Author"]
        if len(title) > max_length:
            result["Title"] = title[:(max_length - 3)] + "..."
        if len(author) > max_length:
            result["Author"] = title[:(max_length - 3)] + "..."
    '''

    results_table = Table(title=f"Results for \"{query}\"", box=box.ROUNDED, expand=True)
    results_table.add_column("No.")
    results_table.add_column("Title", style="bold green")
    results_table.add_column("Author", style="cyan")
    results_table.add_column("Year")
    results_table.add_column("Extension")

    for i in range(len(results)):
        result = results[i]
        results_table.add_row(str(i+1), result["Title"], result["Author"], result["Year"], result["Extension"])

    if len(results):
        console.print(results_table, justify="center")
        print()
        entry = input("Which entry would you like to download? > ").lower().strip()
        show_entry(entry, response, results_table)
    else:
        return "[bold red]No results found![/bold red]"

    
def show_entry(entry: str, response: list, results_table: Table) -> None:
    """
    Show more information about a specific entry.
    """
    clear_console()
    if entry.isdigit() and (int(entry) - 1) in list(range(len(response))):
        item = response[int(entry) - 1]

        entry_table = Table(title=f"Information on Item {entry}", box=box.ROUNDED)
        entry_table.add_column("Detail")
        entry_table.add_column("Description", style="bold green")
        for key in item.keys():
            entry_table.add_row(*[key, item[key]])

        console.print(entry_table, justify="center")

        confirmation = input("Download (yes/no)? ").lower().strip()
        if confirmation == "yes":
            print()
            download_links = libgen.resolve_download_links(item)
            
            os.system(f'wget {next(iter(download_links.values()))}')
            
            farewell = Text("Thank you for using Gaia.\nHappy reading!", style="bold yellow")
            console.print(farewell, justify="center")
        else:
            clear_console()
            console.print(results_table, justify="center")
            entry = input("> ").lower().strip()
            show_entry(entry, response, results_table)
    else:
        main()

def command_handler(command: str):
    if command == ".help":
        clear_console()
        to_print = "[bold green]This is Gaia![/bold green]\n"
        to_print += "Gaia is a Library Genesis browser that lives [green]entirely in your terminal[/green].\n"
        to_print += "• To start searching, either type 'title' or 'author' when prompted for your query type.\n"
        to_print += "• Afterwards, input your search query and wait as Gaia fetches a table of results for you.\n"
        to_print += "• When presented with the table, input the number of any entry to see its details.\n"
        to_print += "• If you've found the book you're looking for, type 'yes' to download it.\n"
        to_print += "Happy reading!"
        return to_print
    elif command == ".exit":
        console.print(Text("See you next time!", style="bold yellow"), justify="center")
        sys.exit()
    else:
        return "[bold red]Invalid command![/bold red]"

ACCEPTED_QUERY_TYPES = ["title", "author"]

def query_handler(query_type: str):
    if query_type.startswith("."):
        return command_handler(query_type)

    if query_type not in ACCEPTED_QUERY_TYPES:
        return "[bold red]Invalid query type![/bold red]"
    
    if query_type == "title":
        title = input("Title of book? ")
        with console.status("Searching for your title..."):
            response = libgen.search_title(title)
        res = show_results(response, title, "Title")
    elif query_type == "author":
        author = input("Name of author? ")
        with console.status("Searching for your author..."):
            response = libgen.search_author(author)
        res = show_results(response, author, "Author")

    return res

def main_loop():
    accepted_query_types = ["title", "author"]
    history = None
    
    while True:
        if history:
            console.print(history)

        query_type = input(f"Insert query type ({'/'.join(accepted_query_types)}): ").strip()
        history = query_handler(query_type)

        clear_console()

def main():
    try:
        clear_console()
        console.print(Align("Welcome to Gaia!", align="center"), style="bold green")
        console.print(Align("Enter '.help' to see instructions, and enter '.exit' to quit the browser.", align="center"))
        console.print(Align("To get started, try searching something below.", align="center"))
        console.print()
        main_loop()
    except KeyboardInterrupt:
        print()
        console.print(Text("Thanks for using Gaia!", style="bold yellow"), justify="center")
        sys.exit()
    
if __name__ == "__main__":
    main()