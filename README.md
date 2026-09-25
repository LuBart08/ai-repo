# ai-repo

apt repository + download page for **[Artificially Inteligent](https://github.com/LuBart08/ArtificiallyInteligent)**.

**Live:** https://lubart08.github.io/ai-repo/

## Contents

| File | Purpose |
|---|---|
| `index.html` | Human-facing download page (this site) |
| `Packages` / `Packages.gz` | apt package index (flat repo layout) |
| `Release` | Repo metadata read by package managers |
| `debs/*.deb` | The packages |
| `build.py` | Regenerates `Packages`, `Packages.gz`, `Release` and `index.html` |

## Adding as a source

In **Sileo**, **Zebra** or **Cydia**: *Settings → Add Source* → `https://lubart08.github.io/ai-repo/`

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
