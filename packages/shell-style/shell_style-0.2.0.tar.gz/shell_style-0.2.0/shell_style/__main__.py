from argparse import ArgumentParser as _ArgumentParser
from .models import Console as _Console, Table as _Table, ProgressBar as _ProgressBar
from .ssml import interpret

def _demo() -> None:
    console = _Console("Demo")
    console.write("<@fg_green>This is a demo of <@bold>Shell-Style<@stop>")
    console.write("Shell-Style supports most features needed for constructing TUIs, for example <@bold>bold<@stop>, <@italic>italic<@stop>, <@underline>underline<@stop>, and <@fg_blue>much more<@stop>!")
    console.write("It also has support for logging and <@bold>24-bit colors<@stop>")
    
    table = _Table(3)
    table.add_row("Working with", "tables", "has never been easier")
    table.add_row("Display information", "in a nice, tabular format", "with our table utilities")
    table.display()

    progress = _ProgressBar(10, delay=0.1, symbol="~")
    progress.run(style="fg_green")

def _process(type: str, input: str, output: str) -> None:
    mode = 0

    match type:
        case "ssml-to-ansi":
            mode = 0

        case "ssml-to-html":
            mode = 2

        case "ansi-to-ssml":
            mode = 1

        case "html-to-ssml":
            mode = 3

    with open(output, "w") as file:
        file.write(interpret(open(input, "r").read(), mode))

def _main() -> None:
    parser = _ArgumentParser(description="The Shell-Style CLI")
    parser.add_argument("-d", "--demo", action="store_true", help="Show a demo of Shell-Style's functionality")
    parser.add_argument("-i", "--input", type=str, help="The input file")
    parser.add_argument("-o", "--output", type=str, help="The output file")
    parser.add_argument("-t", "--type", type=str, choices=["ssml-to-ansi", "ssml-to-html", "ansi-to-ssml", "html-to-ssml"], help="The type of input and output")
    args = parser.parse_args()

    if args.demo:
        _demo()

    else:
        _process(args.type, args.input, args.output)

if __name__ == "__main__":
    _main()
