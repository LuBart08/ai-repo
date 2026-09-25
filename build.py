#!/usr/bin/env python3
"""Generate an apt (Cydia/Sileo/Zebra) repository + plain-HTML download page.

Outputs (all in this directory):
  Packages, Packages.gz, Release   -> apt index for Sileo / Zebra / Cydia
  index.html                       -> plain HTML page (no CSS, no JavaScript)
  README.md                        -> repo documentation

`styled.html` is a static alternative page kept in git; it is not touched here.
"""
import datetime
import gzip
import hashlib
import html
import os

REPO_DIR = os.path.expanduser("~/build/ai-repo")
DEB_NAME = "com.rg.artificiallyinteligient_1.0.0-3+debug_iphoneos-arm.deb"
DEB_PATH = os.path.join(REPO_DIR, "debs", DEB_NAME)
PAGES_URL = "https://lubart08.github.io/ai-repo/"
PROJECT_REPO = "https://github.com/LuBart08/ArtificiallyInteligent"
UPSTREAM_REPO = "https://github.com/ivanisgoodatcoding52/ArtificiallyInteligent"
RELEASE_URL = "https://github.com/LuBart08/ArtificiallyInteligent/releases/tag/v1.0.0-3%2Bdebug"

with open(DEB_PATH, "rb") as f:
    blob = f.read()

size = len(blob)
md5 = hashlib.md5(blob).hexdigest()
sha1 = hashlib.sha1(blob).hexdigest()
sha256 = hashlib.sha256(blob).hexdigest()
e = html.escape

DESC = ("A lightweight AI chatbot client for legacy jailbroken iOS devices (iOS 4.0+). "
        "Includes a SpringBoard long-press overlay, a Settings.app pane, and a standalone "
        "app (with a artificiallyinteligent:// URL scheme and a cross-tweak "
        "Darwin-notification API for other tweaks to call into). Connect to "
        "OpenAI-compatible APIs, Ollama, VoidAI, or custom providers.")

# ---- Packages / Packages.gz -------------------------------------------------
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
with open(os.path.join(REPO_DIR, "Packages"), "w") as f:
    f.write(ENTRY)
with open(os.path.join(REPO_DIR, "Packages.gz"), "wb") as f:
    with gzip.GzipFile(fileobj=f, mode="wb", mtime=0) as g:
        g.write(ENTRY.encode())

# ---- Release ----------------------------------------------------------------
now = datetime.datetime.now(datetime.timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
with open(os.path.join(REPO_DIR, "Release"), "w") as f:
    f.write(f"""Origin: Artificially Inteligent
Label: Artificially Inteligent
Suite: stable
Codename: stable
Date: {now}
Architectures: iphoneos-arm
Components: main
Description: AI chatbot client for jailbroken iOS 4.0+ — apt repository
Homepage: {PROJECT_REPO}
""")

# ---- index.html (plain HTML: no CSS, no JavaScript) -------------------------
page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="apt repository and download page for Artificially Inteligent, an AI chatbot client for jailbroken iOS 4.0+.">
<title>Artificially Inteligent — repo</title>
</head>
<body>

<h1>Artificially Inteligent</h1>

<p>
A lightweight AI chatbot client for legacy jailbroken iOS devices (iOS 4.0+).
SpringBoard overlay, Settings pane and standalone app &mdash; all native
Objective-C, no web views.
</p>

<p>
Version <b>1.0.0-3+debug</b> &middot;
Architecture <b>iphoneos-arm</b> (armv7) &middot;
Minimum iOS <b>4.0</b> &middot;
Licence <b>MIT</b>
</p>

<hr>

<h2>Download</h2>

<p>
<a href="debs/{e(DEB_NAME)}">{e(DEB_NAME)}</a>
({size:,} bytes)
</p>

<p>
The same file is attached to the
<a href="{RELEASE_URL}">GitHub release</a>.
</p>

<h2>Add this repository to your package manager</h2>

<p>Works with Sileo, Zebra and Cydia:</p>

<pre>{PAGES_URL}</pre>

<p>
Settings &rarr; <i>Add Source</i> &rarr; paste the URL above.
The package then appears under <b>Tweaks</b> as <b>Artificially Inteligent</b>.
</p>

<h2>Or install over SSH</h2>

<pre>curl -LO {PAGES_URL}debs/{e(DEB_NAME)}
dpkg -i {e(DEB_NAME)}
sbreload</pre>

<h2>Package details</h2>

<table border="1" cellpadding="6" cellspacing="0">
<tr><th align="left">Package</th><td><code>com.rg.artificiallyinteligient</code></td></tr>
<tr><th align="left">Version</th><td><code>1.0.0-3+debug</code></td></tr>
<tr><th align="left">Architecture</th><td><code>iphoneos-arm</code> (armv7 tier)</td></tr>
<tr><th align="left">Minimum iOS</th><td>4.0</td></tr>
<tr><th align="left">Installed size</th><td>468 KiB</td></tr>
<tr><th align="left">Download size</th><td>{size:,} bytes</td></tr>
<tr><th align="left">Depends</th><td><code>mobilesubstrate | com.saurik.substrate.safemode</code>,
<code>firmware (&gt;= 4.0)</code>, <code>preferenceloader</code></td></tr>
<tr><th align="left">MD5</th><td><code>{md5}</code></td></tr>
<tr><th align="left">SHA1</th><td><code>{sha1}</code></td></tr>
<tr><th align="left">SHA256</th><td><code>{sha256}</code></td></tr>
</table>

<h2>Repository files</h2>

<ul>
<li><a href="Packages">Packages</a> &mdash; apt package index</li>
<li><a href="Packages.gz">Packages.gz</a> &mdash; gzipped index (what package managers fetch)</li>
<li><a href="Release">Release</a> &mdash; repository metadata</li>
<li><a href="debs/">debs/</a> &mdash; the packages themselves</li>
<li><a href="styled.html">styled.html</a> &mdash; same page, with styling</li>
</ul>

<h2>Links</h2>

<ul>
<li><a href="{PROJECT_REPO}">Source code (fork)</a> &mdash; README, build tiers, cross-tweak bridge API</li>
<li><a href="{UPSTREAM_REPO}">Upstream repository</a></li>
<li><a href="https://github.com/LuBart08/ai-repo">This repository (ai-repo)</a></li>
</ul>

<hr>

<p>
MIT licensed &middot; built with Theos &middot; served by GitHub Pages
</p>

</body>
</html>
"""
with open(os.path.join(REPO_DIR, "index.html"), "w") as f:
    f.write(page)

# ---- README.md --------------------------------------------------------------
with open(os.path.join(REPO_DIR, "README.md"), "w") as f:
    f.write(f"""# ai-repo

apt repository + download page for **[Artificially Inteligent]({PROJECT_REPO})**.

**Live:** {PAGES_URL}

## Contents

| File | Purpose |
|---|---|
| `index.html` | Download page — plain HTML, no CSS, no JavaScript |
| `styled.html` | Same page with styling (static alternative, kept as-is) |
| `Packages` / `Packages.gz` | apt package index (flat repo layout) |
| `Release` | Repo metadata read by package managers |
| `debs/*.deb` | The packages |
| `build.py` | Regenerates `Packages`, `Packages.gz`, `Release`, `index.html`, `README.md` |

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
""")

print("size   :", size)
print("md5    :", md5)
print("sha256 :", sha256)
for n in ("Packages", "Packages.gz", "Release", "index.html", "README.md"):
    p = os.path.join(REPO_DIR, n)
    print(f"  {n:14s} {os.path.getsize(p):>8} bytes")
