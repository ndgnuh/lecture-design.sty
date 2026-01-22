import dataclasses
import re
from argparse import ArgumentParser
from dataclasses import dataclass
from io import StringIO
from os import path

INPUT = re.compile(r"\\input{([^{}]+)}")
REQUIRE_PACKAGE = re.compile(r"\\RequirePackage{(.+)}")
REQUIRE_PACKAGE_OPT = re.compile(r"\\RequirePackage\[(.*)\]{(.+)}")


class Element:
    pass


@dataclass(eq=True, frozen=True)
class UsePackage(Element):
    name: str
    options: str = ""

    def render(self) -> str:
        if self.options:
            return r"\RequirePackage[%s]{%s}" % (self.options, self.name)
        else:
            return r"\RequirePackage{%s}" % self.name


@dataclass
class Text(Element):
    content: str


@dataclass
class Input(Element):
    src: str


def parse_entrypoint(content: str) -> list[Element]:
    segments = []
    i, n = 0, len(content)

    buffer = StringIO()

    def commit_buffer():
        if buffer.tell() > 0:
            segments.append(Text(buffer.getvalue()))
            buffer.seek(0)
            buffer.truncate(0)

    while i < n:
        c = content[i]
        if c == "\\":

            rest = content[i:]

            # Check for \input
            m = re.match(INPUT, rest)
            if m:
                commit_buffer()
                segments.append(Input(m.group(1)))
                i = i + len(m.group(0))
                continue

            # Check for \RequirePackage
            m = re.match(REQUIRE_PACKAGE, rest)
            if m:
                commit_buffer()
                segments.append(UsePackage(name=m.group(1)))
                i = i + len(m.group(0))
                continue

            # Check for \RequirePackage with options
            m = re.match(REQUIRE_PACKAGE_OPT, rest)
            if m:
                commit_buffer()
                segments.append(UsePackage(name=m.group(2), options=m.group(1)))
                i = i + len(m.group(0))
                continue

            buffer.write(c)
        else:
            buffer.write(c)

        i = i + 1
    commit_buffer()
    return segments


# Include all the subsequent inputs
def resolve(content: str, base_dir: str) -> str:
    segments = parse_entrypoint(content)
    buffer = StringIO()
    for segment in segments:
        match segment:
            case Input(src=src_file):
                src_file = path.join(base_dir, src_file)
                with open(src_file, "r", encoding="utf-8") as infile:
                    input_content = infile.read()
                included_content = resolve(input_content, base_dir)
                buffer.write(included_content)
            case Text(content=text):
                buffer.write(text)
            case UsePackage() as pkg:
                buffer.write(pkg.render())
            case _:
                raise ValueError(f"Unknown segment type: {segment}")
    return buffer.getvalue()


def build(input_file: str, output_file: str) -> None:
    with open(input_file, "r", encoding="utf-8") as infile:
        content = infile.read()

    # Simulate some build process (e.g., minification, bundling, etc.)
    base_dir = path.dirname(input_file)
    content = resolve(content, base_dir)
    segments = parse_entrypoint(content)

    # Sort segments so that UsePackage comes first
    # And preserve the order of other segments
    # sorted_segments = []
    #
    # for seg in segments:
    #     if isinstance(seg, UsePackage) and seg not in sorted_segments:
    #         sorted_segments.append(seg)
    # for seg in segments:
    #     if not isinstance(seg, UsePackage):
    #         sorted_segments.append(seg)
    # segments = sorted_segments

    with open(output_file, "w", encoding="utf-8") as buffer:
        for segment in segments:
            match segment:
                case Text(content=text):
                    buffer.write(text)
                case Input(src=src_file):
                    src_file = path.join(base_dir, src_file)
                    with open(src_file, "r", encoding="utf-8") as infile:
                        built_content = infile.read()
                    buffer.write("%% Included from %s\n" % src_file)
                    buffer.write(built_content)
                case UsePackage() as pkg:
                    buffer.write(pkg.render())
                    buffer.write("\n")

    with open(output_file, "r", encoding="utf-8") as buffer:
        content = buffer.read()

    with open(output_file, "w", encoding="utf-8") as buffer:
        content = re.sub(r"\n{2,}", "\n\n", content)
        buffer.write(content)
    print(f"Built {output_file} from {input_file}")


def main():
    arg_parser = ArgumentParser(description="Build script for the project.")
    arg_parser.add_argument("entryfile", type=str, help="Main template file")
    arg_parser.add_argument(
        "-o", "--output", type=str, help="Output template file", default=None
    )
    args = arg_parser.parse_args()

    input_file = args.entryfile
    name, ext = path.splitext(input_file)
    output_file = None
    match args.output:
        case None:
            output_file = f"{name}.bundled{ext}"
        case _:
            output_file = args.output

    build(input_file, output_file)


if __name__ == "__main__":
    main()
