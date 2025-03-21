import re
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from rich.progress import track

BASE_URL = "https://proceedings.neurips.cc"


@dataclass(frozen=True)
class Paper:
    id: str
    title: str
    authors: list[str]
    url: str
    pdf_url: str
    abstract: str
    year: int
    is_dataset_and_benchmark_track: bool

    def to_serializable(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "authors": self.authors,
            "url": self.url,
            "pdf_url": self.pdf_url,
            "abstract": self.abstract,
            "year": self.year,
            "is_dataset_and_benchmark_track": self.is_dataset_and_benchmark_track,
        }


def extract_id_from_paper_url(url: str) -> str:
    result = re.search(r"^.*hash\/([a-zA-Z0-9]*)-.*\.html$", url)
    if result:
        return result.group(1)
    else:
        raise ValueError("ID not found")


def get_paper_abstract(url: str) -> str:
    soup = BeautifulSoup(requests.get(url).content, "html.parser")
    after_abstract = False
    for tag in soup.find("body").find_all(True):
        if tag.text == "Abstract":
            after_abstract = True
            continue
        if after_abstract and (tag.text != ""):
            return tag.text
    return ""


def get_publication_list(year: int) -> list[Paper]:
    soup = BeautifulSoup(
        requests.get(
            f"https://proceedings.neurips.cc/paper_files/paper/{year}"
        ).content,
        "html.parser",
    )

    papers = []
    for paper_li in track(
        soup.find_all(
            "li", class_=["conference", "datasets_and_benchmarks_track", "none"]
        ),
        description=f"Downloading and parsing {year}'s proceeding.",
    ):
        paper_link = paper_li.find("a")

        paper_url = urljoin(BASE_URL, paper_link["href"])
        paper_id = extract_id_from_paper_url(paper_url)
        paper_title = paper_link.text

        authors: list[str] = paper_li.find("i").text.split(", ")
        is_dataset_and_benchmark_track = (
            "datasets_and_benchmarks_track" in paper_li["class"]
        )

        pdf_url = (
            f"https://proceedings.neurips.cc/paper_files/paper/2024/file/{paper_id}-Paper-Conference.pdf"
            if not is_dataset_and_benchmark_track
            else f"https://proceedings.neurips.cc/paper_files/paper/2024/file/{paper_id}-Paper-Datasets_and_Benchmarks_Track.pdf"
        )
        paper_abstract = get_paper_abstract(paper_url)

        paper = Paper(
            id=paper_id,
            title=paper_title,
            authors=authors,
            url=paper_url,
            pdf_url=pdf_url,
            abstract=paper_abstract,
            year=year,
            is_dataset_and_benchmark_track=is_dataset_and_benchmark_track,
        )
        papers.append(paper)

    return papers
