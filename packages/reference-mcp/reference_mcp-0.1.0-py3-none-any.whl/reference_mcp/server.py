import itertools

import httpx
from mcp.server.fastmcp import FastMCP
from scholarly import scholarly

mcp = FastMCP("CiteMCP", "Get citation data from CiteAs and Google Scholar")


@mcp.tool()
def get_citeas_data(resource: str) -> str:
    """Retrieve BibTeX-formatted citation for the specified `resource` (e.g., DOI, URL, keyword) from the CiteAs"""
    response = httpx.get(f"https://api.citeas.org/product/{resource}?email=default@example.com")
    response.raise_for_status()
    data = response.json()
    return next((export["export"] for export in data["exports"] if export["export_name"] == "bibtex"), None)


@mcp.tool()
def get_scholar_data(query: str, results: int = 2) -> str:
    """Retrieve `results` BibTeX-formatted citations for publications matching the `query` from the Google Scholar"""
    pubs = scholarly.search_pubs(query)
    return "\n".join(scholarly.bibtex(pub) for pub in itertools.islice(pubs, results))


def main():
    mcp.run()
