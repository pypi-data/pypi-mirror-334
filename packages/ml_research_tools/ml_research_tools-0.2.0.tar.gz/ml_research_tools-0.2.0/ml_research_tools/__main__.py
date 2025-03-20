import argparse
import sys
import logging

from .tex.latex_improver import main as latex_grammar
from .exp.wandb_downloader import main as wandb_downloader

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

tools = {
    "latex-grammar": latex_grammar,
    "wandb-downloader": wandb_downloader,
}

def main():
    parser = argparse.ArgumentParser("ml_research_tools", add_help=False)
    parser.add_argument("tool", choices=list(tools.keys()) + ["help"], help="select tool, use <tool> --help for more info")
    args, next_args = parser.parse_known_args()

    match args.tool:
        case _ if args.tool in tools:
            return tools[args.tool](next_args)
        case "help":
            parser.print_help()
            return 0
        case _:
            raise RuntimeError(f"Unknown tool: {args.tool}")


if __name__ == "__main__":
    sys.exit(main())
