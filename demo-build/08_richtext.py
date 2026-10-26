"""Switch intro/body copy fields from textarea to rich text and migrate every stored string
(stories + presets) to a rich-text doc so the editor shows the existing copy.
Idempotent. Drafts in progress are migrated in the draft only (never published over).
Usage: python3 08_richtext.py"""
from sb import *

FIELDS = {
    "sw-split": ["body"],
    "sw-guides": ["intro"],
    "campaign-page": ["intro"],
    "lead_form": ["intro", "thank_you_message"],
    "events_hub": ["intro"],
    "planner_finder": ["intro"],
    "topic-hub": ["intro"],
}


def to_doc(text):
    paras = []
    for block in [b for b in text.replace("\r\n", "\n").split("\n\n") if b.strip()]:
        content = []
        for i, line in enumerate(block.split("\n")):
            if i:
                content.append({"type": "hard_break"})
            if line:
                content.append({"type": "text", "text": line})
        paras.append({"type": "paragraph", "content": content})
    return {"type": "doc", "content": paras or [{"type": "paragraph"}]}


def migrate(node):
    """Convert string values in place; returns number of fields converted."""
    n = 0
    if isinstance(node, dict):
        for key in FIELDS.get(node.get("component"), []):
            if isinstance(node.get(key), str):
                node[key] = to_doc(node[key]) if node[key].strip() else ""
                n += 1
        for v in node.values():
            n += migrate(v)
    elif isinstance(node, list):
        for v in node:
            n += migrate(v)
    return n


def schemas():
    comps = {c["name"]: c for c in list_all("components", "components")}
    for name, keys in FIELDS.items():
        c = api("GET", f"components/{comps[name]['id']}")["component"]   # fresh fetch before write
        changed = []
        for k in keys:
            f = c["schema"][k]
            if f["type"] != "richtext":
                f["type"] = "richtext"
                f.pop("default_value", None)   # a string default is invalid for rich text
                f.pop("max_length", None)
                changed.append(k)
        if changed:
            api("PUT", f"components/{c['id']}", {"component": {"schema": c["schema"]}})
        print(f"schema {name}: {changed or 'already rich text'}")


def stories():
    for s in list_all("stories", "stories", extra="&story_only=1"):
        full = api("GET", f"stories/{s['id']}")["story"]   # fresh fetch before write
        n = migrate(full["content"])
        if not n:
            continue
        publish = bool(full.get("published")) and not full.get("unpublished_changes")
        api("PUT", f"stories/{full['id']}", {"story": full, "publish": 1 if publish else 0})
        print(f"story {full['full_slug']}: {n} field(s) {'published' if publish else 'saved as draft'}")


def presets():
    for p in api("GET", "presets")["presets"]:
        full = api("GET", f"presets/{p['id']}")["preset"]
        if migrate(full.get("preset") or {}):
            # keep picker image/icon/description: send every field back, not just the content
            keep = {k: full[k] for k in ("name", "component_id", "preset", "image", "icon", "color", "description") if full.get(k) is not None}
            api("PUT", f"presets/{p['id']}", {"preset": keep})
            print("preset", full["name"])


if __name__ == "__main__":
    schemas()
    stories()
    presets()
