"""Shared GTM snippets; run directly to update all published static HTML."""
from pathlib import Path
import re

HEAD = """<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-WJBB3K4Q');</script>
<!-- End Google Tag Manager -->"""
BODY = """<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-WJBB3K4Q"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->"""


def inject_gtm(html):
    """Insert once, preserving all existing page content."""
    for tag, snippet in (("head", HEAD), ("body", BODY)):
        if snippet not in html:
            html, count = re.subn(rf"<{tag}\b[^>]*>", lambda m: m[0] + "\n" + snippet,
                                  html, count=1, flags=re.I)
            if count != 1:
                raise ValueError(f"Missing <{tag}> in HTML")
    return html


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    pages = list(root.glob("*.html"))
    for directory in ("blog", "cases", "pl", "en"):
        pages.extend((root / directory).rglob("*.html"))
    for path in pages:
        original = path.read_text()
        updated = inject_gtm(original)
        if updated != original:
            path.write_text(updated)
    print(f"GTM integrated into {len(pages)} pages.")
