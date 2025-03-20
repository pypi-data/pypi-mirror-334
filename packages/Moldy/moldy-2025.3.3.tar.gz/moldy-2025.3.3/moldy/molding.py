import re
from pathlib import Path

from moldy.logging import log, Color

mold_include_re = re.compile("<!--\\s*Mold\\s*:\\s*([a-zA-Z0-9.\\\\/ _]+)\\s*-*-->")
mold_comment_re = re.compile("//.*\n")

def process_section(section: str):
    values = section.split("$$")

    name = values[0].strip()
    values = values[1:]
    kv_map = {}

    for string in values:
        kv = string.split("\n", maxsplit=1)
        if len(kv) == 1:
            kv_map[kv[0].strip()] = ""
        else:
            kv_map[kv[0].strip()] = kv[1].strip()

    kv_map["name"] = name

    return kv_map


def process_moldings(moldings: Path):
    string = moldings.read_text()
    string = mold_comment_re.sub("\n", string)
    sections = string.split("$$$$")
    sections = [s.strip() for s in sections]
    sections = [s for s in sections if s != ""]

    for s in sections:
        yield process_section(s)


def parse_moldable(file: Path):
    string = file.read_text()
    output = []
    index = 0

    for match in mold_include_re.finditer(string):
        span = match.span()
        output.append(string[index:span[0]])
        output.append((match.group(1),))
        index = span[1]

    if index < len(string):
        output.append(string[index:])
    return output


def apply_molding(template: list, molding: map, destination: str):
    output = ""

    for segment in template:
        if isinstance(segment, str):
            output += segment
            continue

        try:
            output += molding[segment[0]]
        except KeyError:
            log("Could not fulfil template because key ", Color(1), segment[0], Color(None),
                " has no value associated with it for name ", Color(1), molding["name"], Color(None))

    destination = destination.replace("$name", molding["name"])
    destination = destination.replace("!name", molding["name"])

    dest_file = Path(destination)
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    dest_file.touch(exist_ok=True)
    dest_file.write_text(output)


def mold(file: Path, moldings: Path, destination: str):
    template = parse_moldable(file)
    parsed_moldings = { molding["name"]: molding for molding in process_moldings(moldings)}

    if "default" in parsed_moldings:
        default_molding = {}
    else:
        default_molding = parsed_moldings["default"]
        del parsed_moldings["default"]

    for name, molding in parsed_moldings:
        for key, default_value in default_molding:
            if key not in molding:
                log("Placing default value for ", Color(5), key, Color(None), " as it is missing for ", Color(5), name, Color(None))
                molding[key] = default_value

    for _, molding in parsed_moldings:
        apply_molding(template, molding, destination)
