"""Build a corpus: either from local .txt files or by scraping a website politely."""
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import requests
from bs4 import BeautifulSoup


def load_local_corpus(path):
    """Read every .txt file in a folder; the file name is the document title."""
    docs = []
    for file in sorted(Path(path).glob("*.txt")):
        text = file.read_text(encoding="utf-8").strip()
        if text:
            docs.append({"title": file.stem, "url": None, "text": text})
    return docs


def _allowed_by_robots(url, user_agent):
    parsed = urlparse(url)
    parser = RobotFileParser(f"{parsed.scheme}://{parsed.netloc}/robots.txt")
    try:
        parser.read()
    except Exception:
        return False  # if robots.txt cannot be read, do not scrape
    return parser.can_fetch(user_agent, url)


def _get(url, user_agent):
    try:
        response = requests.get(url, headers={"User-Agent": user_agent}, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.RequestException as error:
        print(f"Could not fetch {url}: {error}")
        return None


def extract_links(html, base_url, selector, limit):
    soup = BeautifulSoup(html, "html.parser")
    links = []
    for tag in soup.select(selector):
        link = urljoin(base_url, tag["href"])
        if urlparse(link).netloc == urlparse(base_url).netloc and link not in links:
            links.append(link)
        if len(links) >= limit:
            break
    return links


def extract_article(html, title_selector, content_selector):
    """Return (title, text) from an article page; (None, None) if nothing found."""
    soup = BeautifulSoup(html, "html.parser")
    title_tag = soup.select_one(title_selector)
    paragraphs = [p.get_text(" ", strip=True) for p in soup.select(content_selector)]
    text = " ".join(p for p in paragraphs if p)
    title = title_tag.get_text(strip=True) if title_tag else None
    return (title, text) if title and text else (None, None)


def scrape_corpus(source):
    """Scrape up to `max_articles` articles from `source['url']`, respecting robots.txt."""
    ua = source["user_agent"]
    if not _allowed_by_robots(source["url"], ua):
        print("robots.txt does not allow scraping this URL (or could not be read). Aborting.")
        return []
    home = _get(source["url"], ua)
    if not home:
        return []
    docs = []
    for link in extract_links(home, source["url"], source["article_link_selector"], source["max_articles"]):
        if not _allowed_by_robots(link, ua):
            continue
        time.sleep(source["delay_seconds"])
        html = _get(link, ua)
        if not html:
            continue
        title, text = extract_article(html, source["title_selector"], source["content_selector"])
        if title:
            docs.append({"title": title, "url": link, "text": text})
    return docs
