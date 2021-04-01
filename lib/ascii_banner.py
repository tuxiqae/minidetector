from pyfiglet import Figlet


def print_ascii_banner(banner: str) -> None:
    custom_fig = Figlet(font='doom')
    print(custom_fig.renderText(banner))
