"""UC10: audio/podcast block, topic-hub hero style options, Extra sections limited to on-brand blocks. Idempotent.
Usage: python3 11_hub_audio_style.py"""
import uuid
from sb import *

HUB_BLOCKS = ["lp-text", "lp-image-card", "lp-testimonial", "lp-trust", "youtube-video", "audio_clip",
              "faq-section", "planner_grid", "lead_form", "onward_journey", "events_hub"]


def opt(name, value): return {"name": name, "value": value}


AUDIO_SCHEMA = {
    "label": {"type": "text", "pos": 0, "display_name": "Label", "default_value": "Listen", "description": "Small line above the title, e.g. Podcast"},
    "title": {"type": "text", "pos": 1, "display_name": "Title"},
    "description": {"type": "textarea", "pos": 2, "display_name": "Description"},
    "audio": {"type": "asset", "pos": 3, "display_name": "Audio file", "filetypes": ["audio"], "description": "Upload an MP3, or use a podcast link below"},
    "podcast_url": {"type": "multilink", "pos": 4, "display_name": "Podcast link", "description": "Spotify, Apple Podcasts or SoundCloud episode URL"},
    "duration": {"type": "text", "pos": 5, "display_name": "Duration", "description": "e.g. 24 min"},
}

HERO_FIELDS = {
    "hero_layout": {"type": "option", "display_name": "Hero layout", "default_value": "overlay", "options": [
        opt("Photo behind text", "overlay"), opt("Text beside photo", "split"), opt("Colour block, no photo", "text_only")]},
    "hero_background": {"type": "option", "display_name": "Background colour", "default_value": "dark", "options": [
        opt("Dark", "dark"), opt("Bronze", "bronze"), opt("Cream (dark text)", "cream")]},
    "hero_overlay": {"type": "option", "display_name": "Overlay strength", "default_value": "strong",
                     "description": "How much the colour covers the photo. Stronger = more readable.", "options": [
        opt("Strong", "strong"), opt("Medium", "medium"), opt("Light", "light"), opt("None", "none")]},
    "hero_text_align": {"type": "option", "display_name": "Text alignment", "default_value": "left", "options": [
        opt("Left", "left"), opt("Centre", "center")]},
}


def main():
    comps_ = {c["name"]: c for c in api("GET", "components")["components"]}

    # 1. audio_clip block
    body = {"name": "audio_clip", "display_name": "Audio / podcast", "is_nestable": True, "is_root": False, "schema": AUDIO_SCHEMA}
    if "audio_clip" in comps_:
        audio = api("PUT", f"components/{comps_['audio_clip']['id']}", {"component": body})["component"]
    else:
        audio = api("POST", "components", {"component": body})["component"]
    presets = api("GET", "presets")["presets"]
    pbody = {"name": "Podcast episode", "component_id": audio["id"], "preset": {
        "component": "audio_clip", "_uid": str(uuid.uuid4()), "label": "Podcast",
        "title": "[Episode title]", "description": "Our planners discuss [topic] and what it means for you.", "duration": "20 min"}}
    ex = next((p for p in presets if p["component_id"] == audio["id"] and p["name"] == "Podcast episode"), None)
    p = api("PUT", f"presets/{ex['id']}", {"preset": pbody})["preset"] if ex else api("POST", "presets", {"preset": pbody})["preset"]
    api("PUT", f"components/{audio['id']}", {"component": {"preset_id": p["id"]}})

    # 2. topic-hub: fresh fetch, add hero fields in their own tab, restrict Extra sections
    hub = api("GET", f"components/{comps_['topic-hub']['id']}")["component"]
    schema = hub["schema"]
    top = max(v.get("pos", 0) for v in schema.values())
    for i, (k, v) in enumerate(HERO_FIELDS.items()):
        schema[k] = {**v, "pos": top + 2 + i}
    tab = next((k for k, v in schema.items() if v.get("type") == "tab" and v.get("display_name") == "Hero style"), None)
    if not tab:
        schema[f"tab-{uuid.uuid4()}"] = {"type": "tab", "display_name": "Hero style", "keys": list(HERO_FIELDS), "pos": top + 1}
    schema["body"].update({"restrict_components": True, "restrict_type": "", "component_whitelist": HUB_BLOCKS})
    api("PUT", f"components/{hub['id']}", {"component": {"schema": schema}})

    # verify
    hub = api("GET", f"components/{hub['id']}")["component"]
    print("VERIFY body", hub["schema"]["body"]["restrict_components"], hub["schema"]["body"]["component_whitelist"])
    print("VERIFY hero fields", [k for k in HERO_FIELDS if k in hub["schema"]])
    print("VERIFY audio_clip", audio["id"], "default preset", p["name"])


if __name__ == "__main__":
    main()
