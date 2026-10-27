"""Inject plan.json into template.html:
  preventif-2026.html             claude.ai page
  preventif-2026-standalone.html  offline copy (full document, data kept in the browser)
  index.html                      Firebase version for GitHub Pages (only with --firebase)

python build.py plan.json [--firebase firebase-config.json] [--seed seed.json] [--app-url URL] [--moved]
"""
import argparse
import json
import pathlib

ARTIFACT_URL = "https://claude.ai/artifact/MLPhKdrM3Rn6cdioj1UZRQ"

ap = argparse.ArgumentParser()
ap.add_argument("plan")
ap.add_argument("--firebase", help="Firebase web config (JSON) -> also writes index.html")
ap.add_argument("--seed", help="data taken over from the claude.ai app on the first manager login")
ap.add_argument("--app-url", default=ARTIFACT_URL, help="address people should use (links in the pages)")
ap.add_argument("--moved", action="store_true", help="claude.ai page: say the app has moved to --app-url")
ap.add_argument("--preview", action="store_true", help="without --firebase: index.html as a read-only preview")
a = ap.parse_args()

here = pathlib.Path(__file__).parent
read = lambda f: json.loads(pathlib.Path(f).read_text(encoding="utf-8-sig"))
js = lambda o: json.dumps(o, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
plan = read(a.plan)
tpl = (here / "template.html").read_text(encoding="utf-8")
assert tpl.count("__PLAN_JSON__") == 1 and tpl.count("__BUILD_JSON__") == 1


def page(build):
    return tpl.replace("__PLAN_JSON__", js(plan)).replace("__BUILD_JSON__", js(build))


def write(name, text):
    out = here / name
    out.write_text(text, encoding="utf-8")
    print(out, out.stat().st_size, "bytes")


write("preventif-2026.html", page({"firebase": None, "seed": None, "appUrl": a.app_url, "moved": a.moved}))

# Same skeleton the artifact host adds, so a local copy renders in standards mode.
def skeleton(head=""):
    return (
        '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' + head +
        "<style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);"
        "padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}"
        "img{max-width:100%}[hidden]{display:none!important}</style></head><body>\n"
    )


offline = {"firebase": None, "seed": None, "appUrl": a.app_url, "moved": False}
write("preventif-2026-standalone.html", skeleton() + page(offline) + "\n</body></html>\n")

if a.firebase or a.preview:
    fb = ({"firebase": read(a.firebase), "seed": read(a.seed) if a.seed else None, "appUrl": a.app_url, "moved": False} if a.firebase
          else {"firebase": None, "seed": None, "appUrl": a.app_url, "moved": False, "preview": True})
    write("index.html", skeleton('<link rel="icon" href="site/preventif.ico">') + page(fb) + "\n</body></html>\n")
