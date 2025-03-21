from argparse import ArgumentParser
import sienna
from pathlib import Path

from neurips_downloader.core import get_publication_list


def run():
    parser = ArgumentParser()
    parser.add_argument(
        "--years",
        "-y",
        type=int,
        nargs="+",
        required=True,
        help="Year to download the proceeding of.",
    )
    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        required=True,
        help="Directory to save the results.",
    )
    args = parser.parse_args()

    years: list[int] = args.years
    output_dir: Path = Path(args.output_dir)

    if not output_dir.exists():
        raise ValueError(f"{output_dir} does not exist):")

    for year in years:
        papers = get_publication_list(year)
        serialized_papers = [p.to_serializable() for p in papers]
        sienna.save(serialized_papers, output_dir / f"neurips.{year}.jsonl")


if __name__ == "__main__":
    run()
