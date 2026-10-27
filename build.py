"""Inject plan.json into template.html -> preventif-2026.html (artifact page)
and preventif-2026-standalone.html (full document for opening the file directly)."""
import json
import pathlib
import sys

here = pathlib.Path(__file__).parent
plan = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
tpl = (here / "template.html").read_text(encoding="utf-8")
data = json.dumps(plan, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
assert tpl.count("__PLAN_JSON__") == 1
page = tpl.replace("__PLAN_JSON__", data)
out = here / "preventif-2026.html"
out.write_text(page, encoding="utf-8")
print(out, out.stat().st_size, "bytes")

# Same skeleton the artifact host adds, so a local copy renders in standards mode.
skeleton = (
    '<!doctype html><html lang="fr"><head><meta charset="utf-8">'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
    "<style>:root{color-scheme:light;box-sizing:border-box;padding-top:env(safe-area-inset-top,0px);"
    "padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px -apple-system,BlinkMacSystemFont,sans-serif}"
    "img{max-width:100%}[hidden]{display:none!important}</style></head><body>\n"
)
standalone = here / "preventif-2026-standalone.html"
standalone.write_text(skeleton + page + "\n</body></html>\n", encoding="utf-8")
print(standalone, standalone.stat().st_size, "bytes")
