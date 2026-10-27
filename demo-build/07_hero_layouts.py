"""SW · Home hero — four layouts + presets + /hero-layouts showcase.

Usage:
  python 07_hero_layouts.py schemas   # schema + presets + default preset
  python 07_hero_layouts.py page      # publish /hero-layouts showcase
  python 07_hero_layouts.py all
"""
from __future__ import annotations

import copy
import sys
import uuid

from sb import api

COMPONENT_ID = 234922588961656


def opt(name, value):
    return {"name": name, "value": value}


def update_schema():
    hero = api("GET", f"components/{COMPONENT_ID}")["component"]
    schema = copy.deepcopy(hero["schema"])
    schema["layout"] = {
        "type": "option",
        "display_name": "Layout",
        "description": "How the hero sits on the page. Swap layouts without losing your copy or media.",
        "options": [
            opt("Dark card on photo (Succession)", "overlay_card"),
            opt("Centered card on photo", "overlay_center"),
            opt("Split — text + media", "split"),
            opt("Full-bleed text on media", "full_bleed"),
        ],
        "default_value": "overlay_card",
        "exclude_empty_option": True,
        "pos": -2,
    }
    schema["media_position"] = {
        "type": "option",
        "display_name": "Media side",
        "description": "Only for Split layout.",
        "options": [
            opt("Media on the right", "right"),
            opt("Media on the left", "left"),
        ],
        "default_value": "right",
        "exclude_empty_option": True,
        "pos": -1.5,
        "conditional_settings": [{
            "rule_match": "any",
            "rule_conditions": [{
                "validated_object": {"type": "field", "field_key": "layout", "field_attr": "value"},
                "validation": "not_equals",
                "value": "split",
            }],
            "modifications": [{"display": "hide"}],
        }],
    }
    schema["tab_layout"] = {
        "type": "tab",
        "display_name": "Layout & media",
        "keys": ["layout", "media_position", "media_type", "image", "video"],
        "pos": -3,
    }
    schema["tab_content"] = {
        "type": "tab",
        "display_name": "Content",
        "keys": [
            "headline", "intro",
            "primary_cta_label", "primary_cta_link",
            "secondary_cta_label", "secondary_cta_link",
        ],
        "pos": -2.5,
    }
    api("PUT", f"components/{COMPONENT_ID}", {"component": {
        "name": hero["name"],
        "display_name": hero.get("display_name") or "SW · Home hero",
        "description": (
            "Home hero with four layouts: Succession dark card, centered card, "
            "split text+media, or full-bleed text on media. Media can be image or video."
        ),
        "is_root": hero.get("is_root"),
        "is_nestable": hero.get("is_nestable"),
        "component_group_uuid": hero.get("component_group_uuid"),
        "schema": schema,
    }})
    print("schema updated")
    return schema, hero


def ensure_presets(schema, hero, image=None):
    def base(**overrides):
        content = {
            "_uid": str(uuid.uuid4()),
            "component": "sw-hero",
            "layout": "overlay_card",
            "media_type": "image",
            "media_position": "right",
            "headline": "Helping you build and protect your wealth",
            "intro": (
                "Independent financial advice for every stage of life — "
                "with a planner who takes the time to understand you."
            ),
            "primary_cta_label": "Book a meeting",
            "primary_cta_link": {
                "url": "#lead-form", "linktype": "url",
                "fieldtype": "multilink", "cached_url": "#lead-form",
            },
            "secondary_cta_label": "Explore solutions",
            "secondary_cta_link": {
                "url": "/planners", "linktype": "url",
                "fieldtype": "multilink", "cached_url": "/planners",
            },
        }
        if image:
            content["image"] = image
        content.update(overrides)
        return content

    wanted = [
        ("Dark card on photo (Succession)", base(layout="overlay_card")),
        ("Centered card on photo", base(layout="overlay_center")),
        ("Split — text + media", base(layout="split", media_position="right")),
        ("Full-bleed text on media", base(layout="full_bleed")),
    ]
    existing = {
        p["name"]: p
        for p in api("GET", "presets/").get("presets", [])
        if p.get("component_id") == COMPONENT_ID
    }
    default_id = None
    for name, content in wanted:
        if name in existing:
            print("preset exists", name)
            if name.startswith("Dark card"):
                default_id = existing[name]["id"]
            continue
        r = api("POST", "presets/", {"preset": {
            "name": name,
            "component": "sw-hero",
            "component_id": COMPONENT_ID,
            "preset": content,
        }})
        pid = r.get("preset", {}).get("id")
        print("preset created", name, pid)
        if name.startswith("Dark card"):
            default_id = pid

    if default_id:
        api("PUT", f"components/{COMPONENT_ID}", {"component": {
            "name": hero["name"],
            "display_name": hero.get("display_name") or "SW · Home hero",
            "preset_id": default_id,
            "schema": schema,
            "is_nestable": hero.get("is_nestable"),
            "is_root": hero.get("is_root"),
            "component_group_uuid": hero.get("component_group_uuid"),
            "description": hero.get("description") or "",
        }})
        print("default preset", default_id)


def home_image():
    stories = api("GET", "stories?with_slug=home&per_page=5")["stories"]
    if not stories:
        return None
    home = api("GET", f"stories/{stories[0]['id']}")["story"]
    for b in home["content"].get("body") or []:
        if b.get("component") == "sw-hero" and b.get("image"):
            return b["image"]
    return None


def publish_page():
    image = home_image()

    def hero_blok(layout, media_position="right", headline=None):
        blok = {
            "_uid": str(uuid.uuid4()),
            "component": "sw-hero",
            "layout": layout,
            "media_type": "image",
            "media_position": media_position,
            "headline": headline or "Helping you build and protect your wealth",
            "intro": "Independent financial advice for every stage of life.",
            "primary_cta_label": "Book a meeting",
            "primary_cta_link": {
                "url": "#lead-form", "linktype": "url",
                "fieldtype": "multilink", "cached_url": "#lead-form",
            },
            "secondary_cta_label": "Explore solutions",
            "secondary_cta_link": {
                "url": "/planners", "linktype": "url",
                "fieldtype": "multilink", "cached_url": "/planners",
            },
        }
        if image:
            blok["image"] = image
        return blok

    content = {
        "component": "default-page",
        "body": [
            {
                "_uid": str(uuid.uuid4()),
                "component": "text-section",
                "headline": [{
                    "_uid": str(uuid.uuid4()),
                    "component": "headline-segment",
                    "text": "Home hero layouts",
                    "as": "h1",
                }],
                "text": (
                    "Four layouts on the same SW · Home hero block. "
                    "Change Layout in the Visual Editor — copy and media stay put."
                ),
            },
            hero_blok("overlay_card", headline="1 · Dark card on photo (Succession)"),
            hero_blok("overlay_center", headline="2 · Centered card on photo"),
            hero_blok("split", "right", headline="3 · Split — text + media"),
            hero_blok("full_bleed", headline="4 · Full-bleed text on media"),
        ],
    }
    found = api("GET", "stories?with_slug=hero-layouts&per_page=5")["stories"]
    if found:
        sid = found[0]["id"]
        api("PUT", f"stories/{sid}", {
            "story": {"name": "Hero layouts", "slug": "hero-layouts", "content": content},
            "force_update": "1",
            "publish": 1,
        })
        print("page updated", sid)
    else:
        r = api("POST", "stories/", {
            "story": {
                "name": "Hero layouts",
                "slug": "hero-layouts",
                "parent_id": 0,
                "content": content,
            },
            "publish": 1,
        })
        print("page created", r.get("story", {}).get("full_slug"))


def main():
    cmd = (sys.argv[1] if len(sys.argv) > 1 else "all").lower()
    if cmd in ("schemas", "all"):
        schema, hero = update_schema()
        ensure_presets(schema, hero, home_image())
    if cmd in ("page", "all"):
        publish_page()


if __name__ == "__main__":
    main()
