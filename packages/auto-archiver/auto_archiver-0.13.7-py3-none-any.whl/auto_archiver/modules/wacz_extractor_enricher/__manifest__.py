{
    "name": "WACZ Enricher (and Extractor)",
    "type": ["enricher", "extractor"],
    "entry_point": "wacz_extractor_enricher::WaczExtractorEnricher",
    "requires_setup": True,
    "dependencies": {
        "python": ["loguru", "jsonlines", "warcio"],
        # TODO?
        "bin": ["docker"],
    },
    "configs": {
        "profile": {
            "default": None,
            "help": "browsertrix-profile (for profile generation see https://github.com/webrecorder/browsertrix-crawler#creating-and-using-browser-profiles).",
        },
        "docker_commands": {"default": None, "help": "if a custom docker invocation is needed"},
        "timeout": {"default": 120, "help": "timeout for WACZ generation in seconds", "type": "int"},
        "extract_media": {
            "default": False,
            "type": "bool",
            "help": "If enabled all the images/videos/audio present in the WACZ archive will be extracted into separate Media and appear in the html report. The .wacz file will be kept untouched.",
        },
        "extract_screenshot": {
            "default": True,
            "type": "bool",
            "help": "If enabled the screenshot captured by browsertrix will be extracted into separate Media and appear in the html report. The .wacz file will be kept untouched.",
        },
        "socks_proxy_host": {
            "default": None,
            "help": "SOCKS proxy host for browsertrix-crawler, use in combination with socks_proxy_port. eg: user:password@host",
        },
        "socks_proxy_port": {
            "default": None,
            "type": "int",
            "help": "SOCKS proxy port for browsertrix-crawler, use in combination with socks_proxy_host. eg 1234",
        },
        "proxy_server": {"default": None, "help": "SOCKS server proxy URL, in development"},
    },
    "description": """
    Creates .WACZ archives of web pages using the `browsertrix-crawler` tool, with options for media extraction and screenshot saving.
    [Browsertrix-crawler](https://crawler.docs.browsertrix.com/user-guide/) is a headless browser-based crawler that archives web pages in WACZ format.

    ### Features
    - Archives web pages into .WACZ format using Docker or direct invocation of `browsertrix-crawler`.
    - Supports custom profiles for archiving private or dynamic content.
    - Extracts media (images, videos, audio) and screenshots from the archive, optionally adding them to the enrichment pipeline.
    - Generates metadata from the archived page's content and structure (e.g., titles, text).

    ### Notes
    - Requires Docker for running `browsertrix-crawler` .
    - Configurable via parameters for timeout, media extraction, screenshots, and proxy settings.
    """,
}
