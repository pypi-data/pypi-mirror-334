import functools
import re
from typing import Any, Optional

from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from scrapling.defaults import AsyncFetcher, StealthyFetcher

from scrapling_fetch_mcp._markdownify import _CustomMarkdownify


class UrlFetchRequest(BaseModel):
    url: str = Field(..., description="URL to fetch")
    mode: str = Field(
        "basic", description="Fetching mode (basic, stealth, or max-stealth)"
    )
    format: str = Field("markdown", description="Output format (html or markdown)")
    max_length: int = Field(
        5000,
        description="Maximum number of characters to return.",
        gt=0,
        lt=1000000,
        title="Max Length",
    )
    start_index: int = Field(
        0,
        description="On return output starting at this character index, useful if a previous fetch was truncated and more context is required.",
        ge=0,
        title="Start Index",
    )
    search_pattern: str = Field(
        None,
        description="Regular expression pattern to search for in the content",
    )
    context_chars: int = Field(
        200,
        description="Number of characters to include before and after each match",
        ge=0,
    )


class UrlFetchResponse(BaseModel):
    content: str
    metadata: "UrlFetchResponse.Metadata" = Field(
        default_factory=lambda: UrlFetchResponse.Metadata(),
        description="Metadata about the content retrieval",
    )

    class Metadata(BaseModel):
        total_length: int
        retrieved_length: int
        is_truncated: bool
        percent_retrieved: float
        start_index: Optional[int] = None
        match_count: Optional[int] = None


async def browse_url(request: UrlFetchRequest) -> Any:
    if request.mode == "basic":
        return await AsyncFetcher.get(request.url, stealthy_headers=True)
    elif request.mode == "stealth":
        return await StealthyFetcher.async_fetch(
            request.url, headless=True, network_idle=True
        )
    elif request.mode == "max-stealth":
        return await StealthyFetcher.async_fetch(
            request.url,
            headless=True,
            block_webrtc=True,
            network_idle=True,
            disable_resources=False,
            block_images=False,
        )
    else:
        raise ValueError(f"Unknown mode: {request.mode}")


def _extract_content(page, request) -> str:
    is_markdown = request.format == "markdown"
    return _html_to_markdown(page.html_content) if is_markdown else page.html_content


def _html_to_markdown(html: str) -> str:
    soup = BeautifulSoup(html, "lxml")
    for script in soup(["script", "style"]):
        script.extract()
    body_elm = soup.find("body")
    return _CustomMarkdownify().convert_soup(body_elm if body_elm else soup)


def _search_content(
    content: str, pattern: str, context_chars: int = 200
) -> tuple[str, int]:
    try:
        matches = list(re.compile(pattern).finditer(content))
        if not matches:
            return "", 0
        chunks = [
            (
                max(0, match.start() - context_chars),
                min(len(content), match.end() + context_chars),
            )
            for match in matches
        ]
        merged_chunks = functools.reduce(
            lambda acc, chunk: (
                [*acc[:-1], (acc[-1][0], max(acc[-1][1], chunk[1]))]
                if acc and chunk[0] <= acc[-1][1]
                else [*acc, chunk]
            ),
            chunks,
            [],
        )
        result_sections = [content[start:end] for start, end in merged_chunks]
        return "\n...\n".join(result_sections), len(matches)
    except re.error as e:
        return f"ERROR: Invalid regex pattern: {str(e)}", 0


def _search_req(
    full_content: str, request: UrlFetchRequest
) -> tuple[str, UrlFetchResponse.Metadata]:
    original_length = len(full_content)
    matched_content, match_count = _search_content(
        full_content, request.search_pattern, request.context_chars
    )
    if not matched_content:
        return "", UrlFetchResponse.Metadata(
            total_length=original_length,
            retrieved_length=0,
            is_truncated=False,
            percent_retrieved=0,
            match_count=0,
        )
    truncated_content = matched_content[: request.max_length]
    is_truncated = len(matched_content) > request.max_length
    metadata = UrlFetchResponse.Metadata(
        total_length=original_length,
        retrieved_length=len(truncated_content),
        is_truncated=is_truncated,
        percent_retrieved=round((len(truncated_content) / original_length) * 100, 2)
        if original_length > 0
        else 100,
        match_count=match_count,
    )
    return truncated_content, metadata


def _regular_req(
    full_content: str, request: UrlFetchRequest
) -> tuple[str, UrlFetchResponse.Metadata]:
    total_length = len(full_content)
    truncated_content = full_content[
        request.start_index : request.start_index + request.max_length
    ]
    is_truncated = total_length > (request.start_index + request.max_length)
    metadata = UrlFetchResponse.Metadata(
        total_length=total_length,
        retrieved_length=len(truncated_content),
        is_truncated=is_truncated,
        percent_retrieved=round((len(truncated_content) / total_length) * 100, 2)
        if total_length > 0
        else 100,
        start_index=request.start_index,
    )
    return truncated_content, metadata


async def fetch_url(request: UrlFetchRequest) -> UrlFetchResponse:
    page = await browse_url(request)
    full_content = _extract_content(page, request)
    content, metadata = (
        _search_req(full_content, request)
        if request.search_pattern
        else _regular_req(full_content, request)
    )
    return UrlFetchResponse(content=content, metadata=metadata)
