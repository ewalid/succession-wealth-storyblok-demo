"""Campaign hero: layouts + image / uploaded video / YouTube media. Additive only:
the existing hero_image field is left byte-for-byte as it was (its focal point keeps working).
Usage: python3 07_campaign_hero.py"""
import importlib
from sb import *

g = importlib.import_module("06_demo_gaps")
text, inline_one, link, f, add_fields = g.text, g.inline_one, g.link, g.f, g.add_fields


def show_when(field_key, *values):
    """Hide this field unless field_key has one of values (conditional field, new fields only)."""
    return [{"modifications": [{"display": "hide"}], "rule_match": "all",
             "rule_conditions": [{"validation": "not_equal", "value": v, "field_key": field_key} for v in values]}]


LAYOUTS = [("Overlay card (text box over the image)", "overlay_card"),
           ("Split: text left, media right", "split"),
           ("Full-bleed, centred text", "centered"),
           ("Text only (no media)", "text_only"),
           ("Compact strip", "compact")]

add_fields("campaign-page", [
    ("hero_layout", inline_one(LAYOUTS, "Hero layout",
                               "How the top of the page looks. Overlay card is the default. Text only ignores the media.",
                               default_value="overlay_card")),
    ("hero_media_type", inline_one([("Image", "image"), ("Video (upload)", "video"), ("YouTube video", "youtube")],
                                   "Hero media", "Show the hero image, an uploaded video, or a YouTube film.", default_value="image")),
    ("hero_video", f("asset", "Hero video (upload)", "MP4, ideally under 15 MB. Plays muted on a loop. The hero image is used as the poster.",
                     filetypes=["videos"], conditional_settings=show_when("hero_media_type", "video"))),
    ("hero_youtube", text("YouTube link", "Paste the YouTube link or video ID, e.g. https://www.youtube.com/watch?v=abc123.",
                          conditional_settings=show_when("hero_media_type", "youtube"))),
    ("hero_cta_label", text("Hero button label", "Optional. Leave empty for no button.", default_value="Request a conversation")),
    ("hero_cta_link", link("Hero button link", "Optional. Leave empty to scroll to the lead form on this page.")),
], "Hero")
