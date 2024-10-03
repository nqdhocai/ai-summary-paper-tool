from datetime import datetime
from time import mktime
from aicore import summarize_text

import arxiv

# Construct the default API client.
client = arxiv.Client()

# Search for the 10 most recent articles matching the keyword "quantum."
search = arxiv.Search(
    query="quantum",
    max_results=5,
    sort_by=arxiv.SortCriterion.SubmittedDate
)

results = list(client.results(search))


class ArxivModel:
    def __init__(self, arxiv_url, title, abstract, pdf_url, authors, published_time, tag):
        self.arxiv_url = arxiv_url
        self.title = title
        self.abstract = abstract
        self.pdf_url = pdf_url
        self.authors = authors
        self.published_time = published_time
        self.tag = tag


class SearchEngine:
    def __init__(self, client=arxiv.Client()):
        self.client = client

    def search(self, query="cat:cs.CV+OR+cat:cs.AI+OR+cat:cs.LG+OR+cat:cs.CL+OR+cat:cs.NE+OR+cat:stat.ML",
               max_results=100):
        results = list(arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.SubmittedDate
        ))

        papers = [
            ArxivModel(
                arxiv_url=result["arxiv_url"],
                title=result["title"].replace("\n", "").replace("  ", " "),
                abstract=result["summary"].replace("\n", "").replace("  ", " "),
                pdf_url=result["pdf_url"],
                authors=", ".join(result["authors"])[:800],
                published_time=datetime.fromtimestamp(mktime(result["updated_parsed"])),
                tag=" | ".join([x["term"] for x in result["tags"]]),
            )
            for result in results
        ]
        return papers

class SearchUI:
    def __init__(self, search=SearchEngine()):
        self.search = search

    def _get_papers(self, urls):
        #TODO tai paper
        pass
    def _delete_paper(self, file_path):
        #TODO xoa file sau khi da tom tat xong
        pass
    def _summary(self, file_path):
        #TODO sau khi tai ve thi tien hanh upload len gg api va tom tat
        pass
    def app(self):
        #TODO hien thi giao dien
        pass