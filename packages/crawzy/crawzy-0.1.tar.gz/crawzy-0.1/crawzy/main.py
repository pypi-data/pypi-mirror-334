import argparse
import os
import re
import time
from urllib.parse import urljoin, urlparse
import requests
from bs4 import BeautifulSoup
import shutil
from colorama import Fore, Style, init
import trafilatura

VISITED = set()

DEFAULT_HTML_DIR = ".output/html"
DEFAULT_TEXT_DIR = "output"

init(autoreset=True)


HTML_DIR = "output/html"
TEXT_DIR = "output/text"
os.makedirs(TEXT_DIR, exist_ok=True)


def extract_text(file_path):
    """Extracts clean text from an HTML file."""
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return trafilatura.extract(html_content)


def normalize_url(url):
    """Normalize URL by removing repeated language paths and trailing slashes."""
    parsed = urlparse(url)
    path = re.sub(r"(/tr)+", "/tr", parsed.path)
    normalized_url = f"{parsed.scheme}://{parsed.netloc}{path}".rstrip("/")
    return normalized_url


def crawl(url, domain):
    """Recursively crawl internal links of a domain."""
    os.makedirs(DEFAULT_HTML_DIR, exist_ok=True)
    url = normalize_url(url)
    if url in VISITED or urlparse(url).netloc != domain:
        return

    VISITED.add(url)

    try:
        HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        file_name = os.path.join(
            DEFAULT_HTML_DIR, url.replace("https://", "").replace("/", "_") + ".html"
        )

        with open(file_name, "w", encoding="utf-8") as f:
            f.write(response.text)

        print(f"{Fore.GREEN}{Style.BRIGHT} {url}")
        for link in soup.find_all("a", href=True):
            new_url = urljoin(url, link["href"])
            new_url = normalize_url(new_url)
            # Skip if it's a duplicate, external, or malformed link
            if new_url not in VISITED and urlparse(new_url).netloc == domain:
                time.sleep(1)
                crawl(new_url, domain)

    except requests.RequestException as e:
        print(f"{Fore.RED}Error: {e}")


def extract(text_dir):
    """Extract text from the crawled HTML files."""
    print(f"{Fore.CYAN}Extracting text from HTML files...\n")

    if not os.path.exists(text_dir):
        os.makedirs(text_dir)

    for html_file in os.listdir(DEFAULT_HTML_DIR):
        text = extract_text(os.path.join(DEFAULT_HTML_DIR, html_file))
        if text:
            file_name = html_file.replace(".html", ".txt")
            with open(
                os.path.join(text_dir, file_name),
                "w",
                encoding="utf-8",
            ) as f:
                f.write(text)
    print(f"{Fore.BLUE}{Style.BRIGHT}Text files are located at {text_dir}")


def cleanup():
    """Clean up the HTML directory after text extraction."""
    if os.path.exists(DEFAULT_HTML_DIR):
        shutil.rmtree(DEFAULT_HTML_DIR)
        os.rmdir(os.path.dirname(DEFAULT_HTML_DIR))


def main():
    # Set up the argument parser
    parser = argparse.ArgumentParser(
        description="A command-line web crawler and text extractor.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("domain", type=str, help="Domain to crawl (e.g., website.com)")
    parser.add_argument(
        "--output",
        "-o",
        type=str,
        default=DEFAULT_TEXT_DIR,
        help="Directory to save the extracted text files",
    )

    # Parse the arguments
    args = parser.parse_args()

    try:
        # Start the crawling process
        print(
            f"{Fore.BLUE}Crawling {args.domain}... {Style.BRIGHT}(Press CTRL + C to stop at any time)"
        )
        print(f"{Fore.MAGENTA}Scraped URLs will be listed below:")
        crawl(f"https://{args.domain}", args.domain)
    except KeyboardInterrupt:
        print(
            f"\n{Fore.YELLOW}Crawling interrupted by user. Moving to the next step..."
        )

    # Proceed to text extraction and cleanup
    try:
        print()
        extract(args.output)
    except Exception as e:
        print(f"Unable to extract text from files: {e}")
    finally:
        cleanup()
