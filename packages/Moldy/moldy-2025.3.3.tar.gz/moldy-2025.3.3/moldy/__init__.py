import argparse
from pathlib import Path

from moldy.logging import log, Color
from moldy.molding import mold


def command_entry_point():
    try:
        run_moldy()
    except KeyboardInterrupt:
        pass


def traverse_files(root: Path, file: Path, destination: str):
    if file.is_dir():
        for subfile in file.iterdir():
            traverse_files(root, subfile, destination)
        return

    if not file.name.endswith(".mold"):
        return

    template_file = file.with_name(file.name.removesuffix(".mold"))

    if not template_file.exists():
        log("Orphaned .mold file: ", Color(1), file.resolve(), Color(None))

    destination = destination.replace("$path", str(template_file.relative_to(root)))
    destination = destination.replace("!path", str(template_file.relative_to(root)))

    log("Molding ", Color(2), template_file, Color(None), " into ", Color(2), destination, Color(None))
    mold(template_file, file, destination)


def run_moldy():
    parser = argparse.ArgumentParser(
        prog="moldy",
        description="I needed a quick templating engine for generating translated versions of files"
    )
    parser.add_argument("PATH")
    parser.add_argument("DESTINATION")
    args = parser.parse_args()

    traverse_files(Path(args.PATH), Path(args.PATH), args.DESTINATION)
