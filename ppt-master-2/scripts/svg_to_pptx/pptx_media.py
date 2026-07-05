"""SVG to PNG conversion for Office compatibility mode."""

from __future__ import annotations

import hashlib
import shutil
import tempfile
from pathlib import Path

# SVG to PNG library detection
# Prefer CairoSVG (better quality), fall back to svglib, then browser capture.
PNG_RENDERER: str | None = None
PLAYWRIGHT_OK = False

try:
    import cairosvg
    PNG_RENDERER = 'cairosvg'
except (ImportError, OSError):
    try:
        from svglib.svglib import svg2rlg
        from reportlab.graphics import renderPM
        PNG_RENDERER = 'svglib'
    except (ImportError, OSError):
        pass

if PNG_RENDERER is None:
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        PLAYWRIGHT_OK = True
        PNG_RENDERER = 'playwright'
    except Exception:
        pass


def get_png_renderer_info() -> tuple[str | None, str, str | None]:
    """Get PNG renderer status information.

    Returns:
        (renderer_name, status_text, install_hint) tuple.
    """
    if PNG_RENDERER == 'cairosvg':
        return ('cairosvg', '(full gradient/filter support)', None)
    elif PNG_RENDERER == 'svglib':
        return ('svglib', '(some gradients may be lost)',
                'Install cairosvg for better results: pip install cairosvg')
    elif PNG_RENDERER == 'playwright':
        return ('playwright', '(browser screenshot fallback)', None)
    else:
        return (None, '(not installed)',
                'Install via: pip install cairosvg or pip install svglib reportlab')


def convert_svg_to_png(
    svg_path: Path,
    png_path: Path,
    width: int | None = None,
    height: int | None = None,
) -> bool:
    """Convert SVG to PNG using the available renderer.

    Args:
        svg_path: SVG file path.
        png_path: Output PNG file path.
        width: Output width in pixels.
        height: Output height in pixels.

    Returns:
        Whether the conversion was successful.
    """
    if PNG_RENDERER is None:
        return False

    try:
        if PNG_RENDERER == 'cairosvg':
            cairosvg.svg2png(
                url=str(svg_path),
                write_to=str(png_path),
                output_width=width,
                output_height=height,
            )
            return True

        elif PNG_RENDERER == 'svglib':
            drawing = svg2rlg(str(svg_path))
            if drawing is None:
                print(f"  Warning: Unable to parse SVG ({svg_path.name})")
                return False
            renderPM.drawToFile(
                drawing,
                str(png_path),
                fmt="PNG",
                configPIL={'quality': 95},
            )
            return True

        elif PNG_RENDERER == 'playwright' and PLAYWRIGHT_OK:
            from playwright.sync_api import sync_playwright  # type: ignore

            svg = svg_path.read_text(encoding='utf-8', errors='ignore')
            page_html = (
                "<!doctype html><html><head><meta charset='utf-8'>"
                "<style>html,body{margin:0;width:100%;height:100%;overflow:hidden;background:white;}"
                "svg{display:block;width:100%;height:100%;}"
                "</style></head><body>"
                f"{svg}"
                "</body></html>"
            )
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True, channel='msedge')
                page = browser.new_page(
                    viewport={'width': width or 1280, 'height': height or 720},
                    device_scale_factor=1,
                )
                page.set_content(page_html, wait_until='load')
                page.screenshot(path=str(png_path), full_page=True)
                browser.close()
            return png_path.is_file()

    except Exception as e:
        print(f"  Warning: SVG to PNG conversion failed ({svg_path.name}): {e}")
        return False

    return False


def _cache_key(svg_path: Path, width: int | None, height: int | None) -> str:
    h = hashlib.sha256()
    with open(svg_path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            h.update(chunk)
    return f"{h.hexdigest()}_{width or 0}x{height or 0}_{PNG_RENDERER or 'none'}"


def convert_svg_to_png_cached(
    svg_path: Path,
    png_path: Path,
    width: int | None = None,
    height: int | None = None,
    cache_dir: Path | None = None,
) -> bool:
    """Cache-aware SVG→PNG conversion.

    Returns True on success (cache hit or fresh render). Cache key bakes in
    SVG content hash + size + renderer name; switching renderers invalidates
    naturally. Failures are never cached.
    """
    if cache_dir is None:
        return convert_svg_to_png(svg_path, png_path, width, height)

    if PNG_RENDERER is None:
        return False

    try:
        key = _cache_key(svg_path, width, height)
    except OSError as e:
        print(f"  Warning: Failed to hash SVG ({svg_path.name}): {e}")
        return convert_svg_to_png(svg_path, png_path, width, height)

    cached = cache_dir / f"{key}.png"
    if cached.is_file():
        try:
            shutil.copy(cached, png_path)
            return True
        except OSError as e:
            print(f"  Warning: Cache copy failed, re-rendering ({svg_path.name}): {e}")

    cache_dir.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_name = tempfile.mkstemp(suffix='.png', dir=str(cache_dir))
    tmp_path = Path(tmp_name)
    import os
    os.close(tmp_fd)

    ok = convert_svg_to_png(svg_path, tmp_path, width, height)
    if not ok:
        try:
            tmp_path.unlink()
        except OSError:
            pass
        return False

    try:
        os.replace(tmp_path, cached)
    except OSError:
        try:
            tmp_path.unlink()
        except OSError:
            pass

    try:
        shutil.copy(cached, png_path)
        return True
    except OSError as e:
        print(f"  Warning: Cache copy failed ({svg_path.name}): {e}")
        return False
