# ai-repo

apt repository + download page for **[Artificially Inteligent](https://github.com/LuBart08/ArtificiallyInteligent)**.

**Live:** https://lubart08.github.io/ai-repo/

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

In **Sileo**, **Zebra** or **Cydia**: *Settings → Add Source* → `https://lubart08.github.io/ai-repo/`

### One-tap buttons (URL schemes)

| Button | URL | Handled by |
|---|---|---|
| `+ Add to Cydia` | `cydia://url/?source=<repo-url, percent-encoded>` | Cydia; **Sileo too** — it registers the `cydia` scheme and decodes `?source=` (see `Sileo/AppDelegate.swift`) |
| `+ Add to Sileo` | `sileo://source/<repo-url>` | Sileo (`host == "source"` → prefilled Add-Source dialog) |

Zebra declares only `zbra://` and its handler is still a `// TODO` in
`URLController.swift`, so there is no one-tap path for it — use the manual
*Add Source* route above.

The package shows up under **Tweaks** as *Artificially Inteligent*.

## Direct install (SSH)

```sh
curl -LO https://lubart08.github.io/ai-repo/debs/com.rg.artificiallyinteligient_1.0.0-3+debug_iphoneos-arm.deb
dpkg -i com.rg.artificiallyinteligient_1.0.0-3+debug_iphoneos-arm.deb
sbreload
```

## Regenerating the index

```sh
python3 build.py   # after replacing the .deb in debs/
```
