"""One-off: copy images and files from the old Weebly site into this repo.

Run from the repository root on a network where mackinderlab.weebly.com loads
(for example York, or on mobile data):

    python3 scripts/download_assets.py

People photos and three research images could not be located automatically.
Save those by hand from the old site (right click, Save image as) into the
paths listed at the end of this script's output.
"""

import urllib.request
from pathlib import Path

BASE = "https://mackinderlab.weebly.com/uploads/8/9/4/6/89460500/"
ROOT = Path(__file__).resolve().parent.parent

FILES = {
    # Research
    "1476820484.png": "assets/images/research/interaction-network.png",
    # CyanoTag figures
    "cyanotagpipeline_orig.png": "assets/images/cyanotag/cyanotagpipeline_orig.png",
    "librarystats-jun2024_orig.png": "assets/images/cyanotag/librarystats-jun2024_orig.png",
    "imaging-cyanotag-alldata-june2024_orig.png": "assets/images/cyanotag/imaging-cyanotag-alldata-june2024_orig.png",
    "expression-cyanotag-alldata-june2024_orig.png": "assets/images/cyanotag/expression-cyanotag-alldata-june2024_orig.png",
    "s3-fullinteractome-26feb2024_orig.png": "assets/images/cyanotag/s3-fullinteractome-26feb2024_orig.png",
    # Downloads
    "cyanotagmethods_v1p4_ajperin_19jun2024.pdf": "assets/files/cyanotagmethods_v1p4_ajperin_19jun2024.pdf",
    "cyanotag_cloningprimerdesigns_3apr2024.xlsx": "assets/files/cyanotag_cloningprimerdesigns_3apr2024.xlsx",
    "cyanotag_bsai_eblockdesigns_3apr2024.xlsx": "assets/files/cyanotag_bsai_eblockdesigns_3apr2024.xlsx",
    "cyanotagalldata_june2024_ajp.xlsx": "assets/files/cyanotagalldata_june2024_ajp.xlsx",
    "np_2017_mackinder.pdf": "assets/files/np_2017_mackinder.pdf",
    # News photos
    "gaurav_orig.jpg": "assets/images/news/gaurav_orig.jpg",
    "mld8_orig.jpg": "assets/images/news/mld8_orig.jpg",
    "whatsapp-image-2025-03-09-at-15-38-08_orig.jpeg": "assets/images/news/whatsapp-image-2025-03-09-at-15-38-08_orig.jpeg",
    "pottery_orig.jpg": "assets/images/news/pottery_orig.jpg",
    "published/kakaotalk-20231119-103129304-02.jpg": "assets/images/news/kakaotalk-20231119-103129304-02.jpg",
    "kakaotalk-20231002-231129475_orig.jpg": "assets/images/news/kakaotalk-20231002-231129475_orig.jpg",
    "20211203-mackinder-lab-christmas-party-forage_orig.jpg": "assets/images/news/20211203-mackinder-lab-christmas-party-forage_orig.jpg",
    "20210929-irina-farewell-lunch_orig.jpg": "assets/images/news/20210929-irina-farewell-lunch_orig.jpg",
    "20210819-pubtrip-jamie-last-day_orig.jpg": "assets/images/news/20210819-pubtrip-jamie-last-day_orig.jpg",
    "210527-mackinder-lab-members_orig.jpg": "assets/images/news/210527-mackinder-lab-members_orig.jpg",
    "abi-and-dom-civil-partnership-celebration_orig.jpg": "assets/images/news/abi-and-dom-civil-partnership-celebration_orig.jpg",
    "lab-pubtrip_orig.jpg": "assets/images/news/lab-pubtrip_orig.jpg",
    "published/james-poster-prize.jpg": "assets/images/news/james-poster-prize.jpg",
    "published/onyou-baby.jpg": "assets/images/news/onyou-baby.jpg",
    "img-20181114-114443_orig.jpg": "assets/images/news/img-20181114-114443_orig.jpg",
    "published/20180423-170130.jpg": "assets/images/news/20180423-170130.jpg",
    "published/img-4622.jpg": "assets/images/news/img-4622.jpg",
    "image0_orig.jpeg": "assets/images/news/image0_orig.jpeg",
    "201204-algaeandchristmas_orig.jpg": "assets/images/news/201204-algaeandchristmas_orig.jpg",
    "screenshot-2019-12-12-at-12-31-45_orig.png": "assets/images/news/screenshot-2019-12-12-at-12-31-45_orig.png",
    "20181220-113424-1_orig.jpg": "assets/images/news/20181220-113424-1_orig.jpg",
    "published/img-4619.jpg": "assets/images/news/img-4619.jpg",
    "published/whatsapp-image-2025-03-09-at-15-38-08-1.jpeg": "assets/images/news/whatsapp-image-2025-03-09-at-15-38-08-1.jpeg",
}

MANUAL = [
    "assets/images/research/pyrenoid-em.jpg  (Research page: deep-etch EM of the pyrenoid)",
    "assets/images/research/tagged-colonies.jpg  (Research page: robot-picked colonies)",
    "assets/images/research/cyanobacteria-mneongreen.jpg  (Research page: mNeonGreen cyanobacteria)",
    "assets/images/people/<first-last>.jpg  (one per person, e.g. luke-mackinder.jpg; names match the files in _people/)",
]


PAGES = {
    "people": "https://mackinderlab.weebly.com/people.html",
    "research": "https://mackinderlab.weebly.com/research.html",
    "home": "https://mackinderlab.weebly.com/",
}


def scrape():
    """Save every uploaded image on the People, Research and Home pages, in page order,
    with a list (assets/images/weebly/index.txt) of filename and nearby text."""
    import html as htmlmod
    import re
    lines = []
    for page, url in PAGES.items():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        text = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
        for n, m in enumerate(re.finditer(r'<img[^>]+src="([^"]*?/uploads/[^"]+)"[^>]*>', text)):
            src = htmlmod.unescape(m.group(1)).split("?")[0]
            if src.startswith("//"):
                src = "https:" + src
            elif src.startswith("/"):
                src = "https://mackinderlab.weebly.com" + src
            alt = re.search(r'alt="([^"]*)"', m.group(0))
            after = re.sub(r"<[^>]+>", " ", text[m.end(): m.end() + 600])
            after = " ".join(htmlmod.unescape(after).split())[:120]
            name = f"{page}-{n:02d}-" + src.rsplit("/", 1)[-1]
            out = ROOT / "assets/images/weebly" / name
            out.parent.mkdir(parents=True, exist_ok=True)
            try:
                r = urllib.request.urlopen(urllib.request.Request(src, headers={"User-Agent": "Mozilla/5.0"}), timeout=60)
                out.write_bytes(r.read())
            except Exception as exc:
                print(f"FAILED {src}: {exc}")
                continue
            lines.append(f"{name}\talt={alt.group(1) if alt else ''}\tnext={after}")
            print(f"saved  {name}")
    (ROOT / "assets/images/weebly/index.txt").write_text("\n".join(lines) + "\n")


def main():
    for src, dest in FILES.items():
        out = ROOT / dest
        if out.exists():
            print(f"skip   {dest}")
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        try:
            req = urllib.request.Request(BASE + src, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=60) as r:
                out.write_bytes(r.read())
            print(f"saved  {dest}")
        except Exception as exc:
            print(f"FAILED {dest}: {exc}")
    if not (ROOT / "assets/images/weebly/index.txt").exists():
        scrape()
    print("\nSave these by hand from the old site:")
    for m in MANUAL:
        print("  " + m)


if __name__ == "__main__":
    main()
