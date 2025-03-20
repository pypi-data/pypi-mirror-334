"""HTML to Markdown conversion functionality.

This module provides functions for fetching web content and converting it to Markdown.
Key features include:
- URL validation and HTML fetching with proper error handling
- HTML to Markdown conversion using html2text
- Support for content filtering with CSS selectors
- Table of contents generation
- Removal of excessive blank lines (compact mode)
- Removal of zero-width spaces and other invisible characters

The main entry point is the `convert_url_to_markdown` function, which handles
the entire process from fetching a URL to producing clean Markdown output.
"""

import io
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

import html2text
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


@dataclass
class WebdownConfig:
    """Configuration options for HTML to Markdown conversion.

    This class centralizes all configuration options for the conversion process,
    making it easier to manage and extend the functionality.

    Attributes:
        Basic options:

        * url: URL of the web page to convert (required for URL-based conversion)
        * include_links: Whether to include hyperlinks (True) or plain text (False)
        * include_images: Whether to include images (True) or exclude them (False)
        * include_toc: Whether to generate table of contents
        * css_selector: CSS selector to extract specific content (e.g., "main")
        * compact_output: Whether to remove excessive blank lines
        * body_width: Maximum line length for wrapping (0 for no wrapping)
        * show_progress: Whether to display a progress bar during download

        Advanced HTML2Text options:

        * single_line_break: Whether to use single line breaks (True) or double (False)
        * protect_links: Whether to protect links from line wrapping with brackets
        * images_as_html: Whether to keep images as HTML rather than Markdown syntax
        * unicode_snob: Whether to use Unicode characters instead of ASCII equivalents
        * tables_as_html: Whether to keep tables as HTML rather than Markdown syntax
        * emphasis_mark: Character to use for emphasis (usually underscore '_')
        * strong_mark: Character to use for strong emphasis (usually asterisks '**')
        * default_image_alt: Default alt text to use when images don't have any
        * pad_tables: Whether to add padding spaces for table alignment
        * wrap_list_items: Whether to wrap list items to the body_width
    """

    # Basic options
    url: Optional[str] = None
    include_links: bool = True
    include_images: bool = True
    include_toc: bool = False
    css_selector: Optional[str] = None
    compact_output: bool = False
    body_width: int = 0
    show_progress: bool = False

    # Advanced HTML2Text options
    single_line_break: bool = False
    protect_links: bool = False
    images_as_html: bool = False
    unicode_snob: bool = False
    tables_as_html: bool = False  # Equivalent to bypass_tables in html2text
    emphasis_mark: str = "_"
    strong_mark: str = "**"
    default_image_alt: str = ""
    pad_tables: bool = False
    wrap_list_items: bool = False


class WebdownError(Exception):
    """Exception for webdown errors.

    This exception class is used for all errors raised by the webdown package.
    The error type is indicated by a descriptive message and can be
    distinguished by checking the message content.

    Error types include:

    * URL format errors (when the URL doesn't follow standard format)
    * Network errors (connection issues, timeouts, HTTP errors)
    * Parsing errors (issues with processing the HTML content)
    """

    pass


def validate_url(url: str) -> bool:
    """Validate URL format.

    Args:
        url: URL to validate

    Returns:
        True if valid, False otherwise

    >>> validate_url('https://example.com')
    True
    >>> validate_url('not_a_url')
    False
    """
    parsed = urlparse(url)
    return bool(parsed.scheme and parsed.netloc)


def fetch_url(url: str, show_progress: bool = False) -> str:
    """Fetch HTML content from URL with optional progress bar.

    Args:
        url: URL to fetch
        show_progress: Whether to display a progress bar during download

    Returns:
        HTML content as string

    Raises:
        WebdownError: If URL is invalid or cannot be fetched
    """
    if not validate_url(url):
        raise WebdownError(f"Invalid URL format: {url}")

    try:
        # Stream the response to show download progress
        if show_progress:
            # First make a HEAD request to get the content length
            head_response = requests.head(url, timeout=5)
            head_response.raise_for_status()
            total_size = int(head_response.headers.get("content-length", 0))

            # Now make the GET request with stream=True
            response = requests.get(url, timeout=10, stream=True)
            response.raise_for_status()

            # Create a buffer to store the content
            content = io.StringIO()

            # Create a progress bar
            with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                unit_divisor=1024,
                desc=f"Downloading {url.split('/')[-1] or 'webpage'}",
                disable=not show_progress,
            ) as progress_bar:
                # Decode each chunk and update the progress bar
                for chunk in response.iter_content(
                    chunk_size=1024, decode_unicode=True
                ):
                    if chunk:
                        progress_bar.update(len(chunk.encode("utf-8")))
                        content.write(chunk)

            return content.getvalue()
        else:
            # Regular request without progress bar
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return str(response.text)
    except requests.exceptions.Timeout:
        raise WebdownError(f"Connection timed out while fetching {url}")
    except requests.exceptions.ConnectionError:
        raise WebdownError(f"Connection error while fetching {url}")
    except requests.exceptions.HTTPError as e:
        raise WebdownError(f"HTTP error {e.response.status_code} while fetching {url}")
    except requests.exceptions.RequestException as e:
        raise WebdownError(f"Error fetching {url}: {str(e)}")


def html_to_markdown(
    html: str,
    include_links: bool = True,
    include_images: bool = True,
    include_toc: bool = False,
    css_selector: Optional[str] = None,
    compact_output: bool = False,
    body_width: int = 0,
    # Advanced HTML2Text options
    single_line_break: bool = False,
    protect_links: bool = False,
    images_as_html: bool = False,
    unicode_snob: bool = False,
    tables_as_html: bool = False,
    emphasis_mark: str = "_",
    strong_mark: str = "**",
    default_image_alt: str = "",
    pad_tables: bool = False,
    wrap_list_items: bool = False,
    # Config object support
    config: Optional[WebdownConfig] = None,
) -> str:
    """Convert HTML to Markdown with various formatting options.

    This function takes HTML content and converts it to Markdown format.
    It provides many options to customize the output, from basic features like
    link/image handling to advanced formatting options.

    You can provide individual parameters or use a WebdownConfig object.
    If a config object is provided, it takes precedence over individual parameters.

    Args:
        Basic options:

        * html: HTML content to convert as a string
        * include_links: Whether to include hyperlinks (True) or convert to plain text
        * include_images: Whether to include images (True) or exclude them (False)
        * include_toc: Whether to generate table of contents based on headings
        * css_selector: CSS selector to extract specific content (e.g., "main")
        * compact_output: Whether to remove excessive blank lines in the output
        * body_width: Maximum line length for text wrapping (0 for no wrapping)

        Advanced HTML2Text options:

        * single_line_break: Whether to use single line breaks instead of double
        * protect_links: Whether to protect links from line wrapping with brackets
        * images_as_html: Whether to keep images as HTML rather than Markdown syntax
        * unicode_snob: Whether to use Unicode characters instead of ASCII equivalents
        * tables_as_html: Whether to keep tables as HTML rather than Markdown format
        * emphasis_mark: Character to use for emphasis (default: "_")
        * strong_mark: Character to use for strong emphasis (default: "**")
        * default_image_alt: Default alt text for images without alt attributes
        * pad_tables: Whether to add padding spaces for table alignment
        * wrap_list_items: Whether to wrap list items to the body_width

        Config object support:

        * config: A WebdownConfig object containing all configuration options.
          If provided, all other parameters are ignored.

    Returns:
        A string containing the converted Markdown content

    Examples:
        >>> html = "<h1>Title</h1><p>Content with <a href='#'>link</a></p>"
        >>> print(html_to_markdown(html))
        # Title

        Content with [link](#)

        >>> print(html_to_markdown(html, include_links=False))
        # Title

        Content with link

        >>> print(html_to_markdown(html, body_width=40))
        # Title

        Content with [link](#)
    """
    # Extract specific content by CSS selector if provided
    if css_selector:
        soup = BeautifulSoup(html, "html.parser")
        selected = soup.select(css_selector)
        if selected:
            html = "".join(str(element) for element in selected)

    # Use config object if provided, otherwise use individual parameters
    if config is not None:
        # Override parameters with config values
        include_links = config.include_links
        include_images = config.include_images
        include_toc = config.include_toc
        css_selector = config.css_selector
        compact_output = config.compact_output
        body_width = config.body_width
        single_line_break = config.single_line_break
        protect_links = config.protect_links
        images_as_html = config.images_as_html
        unicode_snob = config.unicode_snob
        tables_as_html = config.tables_as_html
        emphasis_mark = config.emphasis_mark
        strong_mark = config.strong_mark
        default_image_alt = config.default_image_alt
        pad_tables = config.pad_tables
        wrap_list_items = config.wrap_list_items

    # Configure html2text
    h = html2text.HTML2Text()

    # Basic options
    h.ignore_links = not include_links
    h.ignore_images = not include_images
    h.body_width = body_width  # User-defined line width

    # Advanced options
    h.single_line_break = single_line_break
    h.protect_links = protect_links
    h.images_as_html = images_as_html
    h.unicode_snob = unicode_snob
    h.bypass_tables = tables_as_html  # Note: bypass_tables is the opposite of md tables
    h.emphasis_mark = emphasis_mark
    h.strong_mark = strong_mark
    h.default_image_alt = default_image_alt
    h.pad_tables = pad_tables
    h.wrap_list_items = wrap_list_items

    markdown = h.handle(html)

    # Post-process the markdown
    import re

    # Remove zero-width spaces and other invisible characters
    markdown = re.sub(r"[\u200B\u200C\u200D\uFEFF]", "", markdown)

    # Post-process to remove excessive blank lines if requested
    if compact_output:
        # Replace 3 or more consecutive newlines with just 2
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    # Add table of contents if requested
    if include_toc:
        headings = re.findall(r"^(#{1,6})\s+(.+)$", markdown, re.MULTILINE)

        if headings:
            toc = ["# Table of Contents\n"]
            for markers, title in headings:
                level = len(markers) - 1  # Adjust for 0-based indentation
                indent = "  " * level
                link = title.lower().replace(" ", "-")
                # Clean the link of non-alphanumeric characters
                link = re.sub(r"[^\w-]", "", link)
                toc.append(f"{indent}- [{title}](#{link})")

            markdown = "\n".join(toc) + "\n\n" + markdown

    # The return type is explicitly str, so we ensure it's returned as a string
    return str(markdown)


def convert_url_to_markdown(
    url_or_config: str | WebdownConfig,
    include_links: bool = True,
    include_images: bool = True,
    include_toc: bool = False,
    css_selector: Optional[str] = None,
    compact_output: bool = False,
    body_width: int = 0,
    show_progress: bool = False,
) -> str:
    """Convert a web page to markdown.

    This function accepts either a URL string or a WebdownConfig object.
    If a URL string is provided, the remaining parameters are used for configuration.
    If a WebdownConfig object is provided, all other parameters are ignored.

    Args:
        * url_or_config: URL of the web page or a WebdownConfig object
        * include_links: Whether to include hyperlinks (ignored if config provided)
        * include_images: Whether to include images (ignored if config provided)
        * include_toc: Generate table of contents (ignored if config provided)
        * css_selector: CSS selector for extraction (ignored if config provided)
        * compact_output: Whether to remove blank lines (ignored if config provided)
        * body_width: Maximum line length for text wrapping (ignored if config provided)
        * show_progress: Whether to display a progress bar (ignored if config provided)

    Returns:
        Markdown content

    Raises:
        WebdownError: If URL is invalid or cannot be fetched

    Examples:
        # Using individual parameters (backward compatible)
        markdown = convert_url_to_markdown(
            "https://example.com",
            include_toc=True,
            show_progress=True
        )

        # Using config object (new approach)
        config = WebdownConfig(
            url="https://example.com",
            include_toc=True,
            show_progress=True
        )
        markdown = convert_url_to_markdown(config)
    """
    # Determine if we're using a config object or URL string
    if isinstance(url_or_config, WebdownConfig):
        config = url_or_config
        if config.url is None:
            raise WebdownError("URL must be provided in the config object")
        url = config.url
        include_links = config.include_links
        include_images = config.include_images
        include_toc = config.include_toc
        css_selector = config.css_selector
        compact_output = config.compact_output
        body_width = config.body_width
        show_progress = config.show_progress
    else:
        # Using the traditional parameter-based approach
        url = url_or_config

    html = fetch_url(url, show_progress=show_progress)

    if isinstance(url_or_config, WebdownConfig):
        # Pass the config object to html_to_markdown
        return html_to_markdown(html, config=config)
    else:
        # Use individual parameters
        return html_to_markdown(
            html,
            include_links=include_links,
            include_images=include_images,
            include_toc=include_toc,
            css_selector=css_selector,
            compact_output=compact_output,
            body_width=body_width,
        )
