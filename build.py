#!/usr/bin/env python3
"""Generate an apt (Cydia/Sileo/Zebra) repository + download page for the .deb."""
import datetime
import gzip
import hashlib
import html
import os

REPO_DIR = os.path.expanduser("~/build/ai-repo")
DEB_NAME = "com.rg.artificiallyinteligient_1.0.0-3+debug_iphoneos-arm.deb"
DEB_PATH = os.path.join(REPO_DIR, "debs", DEB_NAME)
PAGES_URL = "https://lubart08.github.io/ai-repo/"
GITHUB_REPO = "https://github.com/LuBart08/ai-repo"
PROJECT_REPO = "https://github.com/LuBart08/ArtificiallyInteligent"
RELEASE_URL = "https://github.com/LuBart08/ArtificiallyInteligent/releases/tag/v1.0.0-3%2Bdebug"

with open(DEB_PATH, "rb") as f:
    blob = f.read()

size = len(blob)
md5 = hashlib.md5(blob).hexdigest()
sha1 = hashlib.sha1(blob).hexdigest()
sha256 = hashlib.sha256(blob).hexdigest()

# metadata taken from `dpkg-deb -f`, with the fork owner as maintainer
# (upstream control still has the "Your Name" / example.com placeholders)
DESC = ("A lightweight AI chatbot client for legacy jailbroken iOS devices (iOS 4.0+). "
        "Includes a SpringBoard long-press overlay, a Settings.app pane, and a standalone "
        "app (with a artificiallyinteligent:// URL scheme and a cross-tweak "
        "Darwin-notification API for other tweaks to call into). Connect to "
        "OpenAI-compatible APIs, Ollama, VoidAI, or custom providers.")
ENTRY = f"""Package: com.rg.artificiallyinteligient
Name: Artificially Inteligent
Version: 1.0.0-3+debug
Architecture: iphoneos-arm
Maintainer: LuBart08 <LuBart08@users.noreply.github.com>
Author: ivanisgood52
Section: Tweaks
Depends: mobilesubstrate | com.saurik.substrate.safemode, firmware (>= 4.0), preferenceloader
Homepage: {PROJECT_REPO}
Installed-Size: 468
Filename: debs/{DEB_NAME}
Size: {size}
MD5sum: {md5}
SHA1: {sha1}
SHA256: {sha256}
Description: {DESC}
"""

# ---- Packages / Packages.gz -------------------------------------------------
with open(os.path.join(REPO_DIR, "Packages"), "w") as f:
    f.write(ENTRY)
with open(os.path.join(REPO_DIR, "Packages.gz"), "wb") as f:
    with gzip.GzipFile(fileobj=f, mode="wb", mtime=0) as g:
        g.write(ENTRY.encode())

# ---- Release ----------------------------------------------------------------
now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
release = f"""Origin: Artificially Inteligent
Label: Artificially Inteligent
Suite: stable
Codename: stable
Date: {now}
Architectures: iphoneos-arm
Components: main
Description: AI chatbot client for jailbroken iOS 4.0+ — apt repository
Homepage: {PROJECT_REPO}
"""
with open(os.path.join(REPO_DIR, "Release"), "w") as f:
    f.write(release)

# ---- index.html -------------------------------------------------------------
def card(title, body):
    return f'<div class="card"><h2>{title}</h2>{body}</div>'


download_card = card("Download", f"""
  <a class="btn" href="debs/{html.escape(DEB_NAME)}">⬇ Download .deb</a>
  <p class="meta">{size:,} bytes &middot; <code>iphoneos-arm</code> &middot; v1.0.0-3+debug</p>
  <p class="meta">Also on the
    <a href="{RELEASE_URL}">GitHub release page</a>.</p>""")

add_card = card("Add this repo to your package manager", f"""
  <p>Sileo, Zebra and Cydia all understand this repository:</p>
  <div class="copyrow">
    <code id="repourl">{PAGES_URL}</code>
    <button onclick="navigator.clipboard.writeText('{PAGES_URL}');this.textContent='Copied ✓'">Copy</button>
  </div>
  <p class="meta">Settings → <em>Add Source</em> → paste the URL above. The package appears
  under <strong>Tweaks</strong> as <em>Artificially Inteligent</em>.</p>""")

install_card = card("Or install over SSH", f"""
  <pre><code>curl -LO {PAGES_URL}debs/{html.escape(DEB_NAME)}
dpkg -i {html.escape(DEB_NAME)}
sbreload   <span class="cmt"># or: killall -9 SpringBoard</span></code></pre>""")

deps_card = card("Details", f"""
  <table>
    <tr><th>Package</th><td><code>com.rg.artificiallyinteligient</code></td></tr>
    <tr><th>Version</th><td><code>1.0.0-3+debug</code></td></tr>
    <tr><th>Architecture</th><td><code>iphoneos-arm</code> (armv7 tier)</td></tr>
    <tr><th>Minimum iOS</th><td>4.0</td></tr>
    <tr><th>Depends</th><td><code>mobilesubstrate | com.saurik.substrate.safemode</code>,
        <code>firmware (&ge; 4.0)</code>, <code>preferenceloader</code></td></tr>
    <tr><th>Installed size</th><td>468 KiB</td></tr>
    <tr><th>MD5</th><td><code class="hash">{md5}</code></td></tr>
    <tr><th>SHA256</th><td><code class="hash">{sha256}</code></td></tr>
  </table>""")

links_card = card("Links", f"""
  <ul class="links">
    <li><a href="{PROJECT_REPO}">Source code (fork)</a> — README, build tiers, bridge API</li>
    <li><a href="https://github.com/ivanisgoodatcoding52/ArtificiallyInteligent">Upstream repository</a></li>
    <li><a href="{PAGES_URL}Packages">Packages index</a> &middot;
        <a href="{PAGES_URL}Packages.gz">Packages.gz</a> &middot;
        <a href="{PAGES_URL}Release">Release</a></li>
  </ul>""")

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Artificially Inteligent — repo</title>
<meta name="description" content="apt repository for Artificially Inteligent, an AI chatbot client for jailbroken iOS 4.0+.">
<style>
  :root {{
    --bg: #0d1117; --panel: #161b22; --border: #30363d;
    --fg: #e6edf3; --muted: #8b949e; --accent: #58a6ff; --green: #3fb950;
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0; background: var(--bg); color: var(--fg);
    font: 16px/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
  }}
  .wrap {{ max-width: 860px; margin: 0 auto; padding: 48px 20px 80px; }}
  h1 {{ font-size: 2rem; margin: 0 0 4px; }}
  h2 {{ font-size: 1.05rem; margin: 0 0 14px; color: var(--accent); text-transform: uppercase; letter-spacing: .05em; }}
  .tagline {{ color: var(--muted); margin: 0 0 28px; }}
  .badges {{ margin-bottom: 28px; }}
  .card {{
    background: var(--panel); border: 1px solid var(--border);
    border-radius: 10px; padding: 20px 22px; margin-bottom: 16px;
  }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
  code {{
    background: #0b0f14; border: 1px solid var(--border); border-radius: 5px;
    padding: 1px 6px; font: 13px/1.5 ui-monospace, SFMono-Regular, Menlo, monospace;
  }}
  pre {{ background: #0b0f14; border: 1px solid var(--border); border-radius: 8px;
        padding: 14px; overflow-x: auto; }}
  pre code {{ background: none; border: 0; padding: 0; }}
  .cmt {{ color: var(--muted); }}
  .btn {{
    display: inline-block; background: var(--green); color: #04150a; font-weight: 600;
    padding: 11px 22px; border-radius: 8px; font-size: 1rem;
  }}
  .btn:hover {{ text-decoration: none; filter: brightness(1.1); }}
  .meta {{ color: var(--muted); font-size: .9rem; }}
  .copyrow {{ display: flex; gap: 10px; align-items: center; flex-wrap: wrap; margin: 10px 0; }}
  .copyrow code {{ flex: 1 1 320px; padding: 9px 12px; font-size: .95rem; }}
  .copyrow button {{
    background: #21262d; color: var(--fg); border: 1px solid var(--border);
    border-radius: 7px; padding: 9px 16px; cursor: pointer; font-size: .9rem;
  }}
  .copyrow button:hover {{ background: #30363d; }}
  table {{ width: 100%; border-collapse: collapse; font-size: .93rem; }}
  th, td {{ text-align: left; padding: 7px 8px; border-bottom: 1px solid var(--border); vertical-align: top; }}
  th {{ color: var(--muted); font-weight: 600; width: 160px; }}
  tr:last-child th, tr:last-child td {{ border-bottom: 0; }}
  .hash {{ word-break: break-all; }}
  .links {{ margin: 0; padding-left: 18px; }}
  .links li {{ margin: 6px 0; }}
  footer {{ color: var(--muted); font-size: .85rem; margin-top: 30px; text-align: center; }}
</style>
</head>
<body>
<div class="wrap">
  <h1>Artificially Inteligent</h1>
  <p class="tagline">A lightweight AI chatbot client for legacy jailbroken iOS devices (iOS 4.0+) —
     SpringBoard overlay, Settings pane, standalone app.</p>
  <p class="badges">
    <img alt="version" src="https://img.shields.io/badge/version-1.0.0--3%2Bdebug-blue">
    <img alt="ios" src="https://img.shields.io/badge/iOS-4.0%2B-lightgrey">
    <img alt="arch" src="https://img.shields.io/badge/arch-iphoneos--arm-orange">
    <img alt="license" src="https://img.shields.io/badge/license-MIT-green">
  </p>
  {download_card}
  {add_card}
  {install_card}
  {deps_card}
  {links_card}
  <footer>MIT licensed &middot; built with Theos &middot; served by GitHub Pages</footer>
</div>
</body>
</html>
"""
with open(os.path.join(REPO_DIR, "index.html"), "w") as f:
    f.write(page)

# ---- README.md --------------------------------------------------------------
readme = f"""# ai-repo

apt repository + download page for **[Artificially Inteligent]({PROJECT_REPO})**.

**Live:** {PAGES_URL}

## Contents

| File | Purpose |
|---|---|
| `index.html` | Human-facing download page (this site) |
| `Packages` / `Packages.gz` | apt package index (flat repo layout) |
| `Release` | Repo metadata read by package managers |
| `debs/*.deb` | The packages |
| `build.py` | Regenerates `Packages`, `Packages.gz`, `Release` and `index.html` |

## Adding as a source

In **Sileo**, **Zebra** or **Cydia**: *Settings → Add Source* → `{PAGES_URL}`

The package shows up under **Tweaks** as *Artificially Inteligent*.

## Direct install (SSH)

```sh
curl -LO {PAGES_URL}debs/{DEB_NAME}
dpkg -i {DEB_NAME}
sbreload
```

## Regenerating the index

```sh
python3 build.py   # after replacing the .deb in debs/
```
"""
with open(os.path.join(REPO_DIR, "README.md"), "w") as f:
    f.write(readme)

print("size   :", size)
print("md5    :", md5)
print("sha256 :", sha256)
for n in ("Packages", "Packages.gz", "Release", "index.html", "README.md"):
    p = os.path.join(REPO_DIR, n)
    print(f"  {n:14s} {os.path.getsize(p):>8} bytes")
