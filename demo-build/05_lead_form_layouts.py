#!/usr/bin/env python3
"""Expand lead_form with layout options and create marketer presets."""
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MT = [l.split("=", 1)[1].strip().strip('"') for l in open(Path.home() / "dev/darwin/storyblok.env") if l.startswith("STORYBLOK_MANAGEMENT_TOKEN=")][0]
SPACE = 296113342540964
COMP_ID = 234227299840376


def api(method, path, body=None):
    data = None if body is None else json.dumps(body).encode()
    req = urllib.request.Request(
        f"https://mapi.storyblok.com/v1/spaces/{SPACE}{path}",
        data=data,
        method=method,
        headers={"Authorization": MT, "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        return json.load(r)


def opt(name, value):
    return {"name": name, "value": value}


schema = {
    "tab_content": {
        "type": "tab",
        "display_name": "Content",
        "keys": [
            "layout",
            "headline",
            "intro",
            "form_mode",
            "fields",
            "extra_fields",
            "submit_label",
            "thank_you_message",
            "thank_you_page",
            "privacy_url",
        ],
        "pos": 0,
    },
    "tab_style": {
        "type": "tab",
        "display_name": "Layout & style",
        "keys": [
            "background",
            "background_image",
            "side_image",
            "image_position",
            "form_width",
            "field_columns",
            "show_attribution_preview",
        ],
        "pos": 1,
    },
    "tab_mailchimp": {
        "type": "tab",
        "display_name": "Mailchimp",
        "keys": ["mailchimp_form_id", "mailchimp_tags", "hidden_fields_note"],
        "pos": 2,
    },
    "layout": {
        "type": "option",
        "display_name": "Layout",
        "description": "How the form sits on the page. Pick a look that fits the section — you can change this later without losing your fields.",
        "options": [
            opt("Stacked card (classic)", "stacked"),
            opt("Split with image", "split_image"),
            opt("Dark conversation panel", "dark_panel"),
            opt("Two-column fields, wide", "two_column_wide"),
            opt("Compact campaign strip", "compact"),
            opt("Full-bleed on image", "full_bleed"),
        ],
        "default_value": "dark_panel",
        "exclude_empty_option": True,
        "pos": 3,
    },
    "headline": {
        "type": "text",
        "display_name": "Heading",
        "description": "Main heading above the form.",
        "default_value": "Ready for a conversation?",
        "pos": 4,
    },
    "intro": {
        "type": "textarea",
        "display_name": "Intro text",
        "description": "Short reassuring line under the heading.",
        "default_value": "There is no pressure and no obligation — just a confidential chat to understand your goals.",
        "pos": 5,
    },
    "form_mode": {
        "type": "option",
        "display_name": "Form type",
        "description": "Built-in form uses the fields below. Mailchimp embed uses the form ID from marketing.",
        "options": [
            opt("Built-in form", "native"),
            opt("Mailchimp embed", "mailchimp"),
        ],
        "default_value": "native",
        "exclude_empty_option": True,
        "pos": 6,
    },
    "fields": {
        "type": "options",
        "display_name": "Standard fields",
        "description": "Tick the questions to ask. First name, surname and email are always shown for the built-in form.",
        "options": [
            opt("First name", "first_name"),
            opt("Surname", "surname"),
            opt("Email", "email"),
            opt("Phone", "phone"),
            opt("Postcode", "postcode"),
            opt("Investment and pension value", "investment_value"),
            opt("Where did you hear about us?", "heard_about"),
        ],
        "default_value": "first_name,surname,email,phone,postcode,investment_value,heard_about",
        "pos": 7,
    },
    "extra_fields": {
        "type": "bloks",
        "display_name": "Extra custom fields",
        "description": "Optional. Add extra questions with the Form field block (select, checkbox, etc.).",
        "restrict_components": True,
        "component_whitelist": ["form-field"],
        "pos": 8,
    },
    "submit_label": {
        "type": "text",
        "display_name": "Button label",
        "default_value": "Request a conversation",
        "pos": 9,
    },
    "thank_you_message": {
        "type": "textarea",
        "display_name": "Thank-you message",
        "default_value": "Thank you. We will be in touch to arrange a convenient time.",
        "pos": 10,
    },
    "thank_you_page": {
        "type": "multilink",
        "display_name": "Thank-you page",
        "description": "Optional. Send visitors here after submitting instead of showing the message.",
        "pos": 11,
    },
    "privacy_url": {
        "type": "multilink",
        "display_name": "Privacy policy link",
        "pos": 12,
    },
    "background": {
        "type": "option",
        "display_name": "Background",
        "description": "Section background. Text colour adjusts automatically for contrast.",
        "options": [
            opt("Cream", "cream"),
            opt("White", "white"),
            opt("Navy", "navy"),
            opt("Bronze", "bronze"),
            opt("Image", "image"),
        ],
        "default_value": "navy",
        "exclude_empty_option": True,
        "pos": 13,
    },
    "background_image": {
        "type": "asset",
        "display_name": "Background image",
        "description": "Used when Background = Image, or for the Full-bleed layout.",
        "filetypes": ["images"],
        "pos": 14,
        "conditional_settings": [
            {
                "rule_match": "any",
                "rule_conditions": [
                    {
                        "validated_object": {"type": "field", "field_key": "background", "field_attr": "value"},
                        "validation": "not_equals",
                        "value": "image",
                    },
                    {
                        "validated_object": {"type": "field", "field_key": "layout", "field_attr": "value"},
                        "validation": "not_equals",
                        "value": "full_bleed",
                    },
                ],
                "modifications": [{"display": "hide"}],
            }
        ],
    },
    "side_image": {
        "type": "asset",
        "display_name": "Side image",
        "description": "Photo shown next to the form in the Split with image layout.",
        "filetypes": ["images"],
        "pos": 15,
        "conditional_settings": [
            {
                "rule_match": "any",
                "rule_conditions": [
                    {
                        "validated_object": {"type": "field", "field_key": "layout", "field_attr": "value"},
                        "validation": "not_equals",
                        "value": "split_image",
                    }
                ],
                "modifications": [{"display": "hide"}],
            }
        ],
    },
    "image_position": {
        "type": "option",
        "display_name": "Image position",
        "description": "Which side the photo sits on (Split layout only).",
        "options": [opt("Image on the right", "right"), opt("Image on the left", "left")],
        "default_value": "right",
        "pos": 16,
        "conditional_settings": [
            {
                "rule_match": "any",
                "rule_conditions": [
                    {
                        "validated_object": {"type": "field", "field_key": "layout", "field_attr": "value"},
                        "validation": "not_equals",
                        "value": "split_image",
                    }
                ],
                "modifications": [{"display": "hide"}],
            }
        ],
    },
    "form_width": {
        "type": "option",
        "display_name": "Form width",
        "options": [
            opt("Narrow", "narrow"),
            opt("Medium", "medium"),
            opt("Wide", "wide"),
        ],
        "default_value": "medium",
        "exclude_empty_option": True,
        "pos": 17,
    },
    "field_columns": {
        "type": "option",
        "display_name": "Field columns",
        "description": "One column is easier on mobile. Two columns packs more into a wide form.",
        "options": [opt("One column", "1"), opt("Two columns", "2")],
        "default_value": "2",
        "exclude_empty_option": True,
        "pos": 18,
    },
    "show_attribution_preview": {
        "type": "boolean",
        "display_name": "Show attribution preview",
        "description": "In the Visual Editor, show the hidden page / planner / UTM fields that are sent with every lead. Off on the live site unless you leave this on for a demo.",
        "default_value": True,
        "pos": 19,
    },
    "mailchimp_form_id": {
        "type": "text",
        "display_name": "Mailchimp form ID",
        "description": "Only for Mailchimp embed. Paste the form ID from marketing.",
        "pos": 20,
        "conditional_settings": [
            {
                "rule_match": "any",
                "rule_conditions": [
                    {
                        "validated_object": {"type": "field", "field_key": "form_mode", "field_attr": "value"},
                        "validation": "not_equals",
                        "value": "mailchimp",
                    }
                ],
                "modifications": [{"display": "hide"}],
            }
        ],
    },
    "mailchimp_tags": {
        "type": "text",
        "display_name": "Mailchimp tags",
        "description": "Optional. Comma-separated tags, e.g. paid-search, leeds.",
        "pos": 21,
        "conditional_settings": [
            {
                "rule_match": "any",
                "rule_conditions": [
                    {
                        "validated_object": {"type": "field", "field_key": "form_mode", "field_attr": "value"},
                        "validation": "not_equals",
                        "value": "mailchimp",
                    }
                ],
                "modifications": [{"display": "hide"}],
            }
        ],
    },
    "hidden_fields_note": {
        "type": "section",
        "display_name": "Tracking (automatic)",
        "description": "Page, template, planner, office and UTM parameters are added to every submission automatically. CAPTCHA and unsubmitted-form storage are frontend work for Kyan.",
        "pos": 22,
    },
}

comp = api("GET", f"/components/{COMP_ID}")["component"]
comp["schema"] = schema
comp["display_name"] = "Lead form"
comp["description"] = "Lead capture with layout options. Built-in fields or Mailchimp embed. Attribution fields are filled automatically."
api("PUT", f"/components/{COMP_ID}", {"component": {"schema": schema, "display_name": "Lead form", "description": comp["description"]}})
print("schema updated")

# Presets
presets = [
    {
        "name": "Dark conversation panel",
        "preset": {
            "layout": "dark_panel",
            "background": "navy",
            "form_width": "medium",
            "field_columns": "2",
            "form_mode": "native",
            "headline": "Ready for a conversation?",
            "intro": "There is no pressure and no obligation — just a confidential chat to understand your goals.",
            "fields": ["first_name", "surname", "email", "phone", "postcode", "investment_value", "heard_about"],
            "submit_label": "Request a conversation",
            "thank_you_message": "Thank you. We will be in touch to arrange a convenient time.",
            "show_attribution_preview": True,
            "component": "lead_form",
        },
    },
    {
        "name": "Split with lifestyle image",
        "preset": {
            "layout": "split_image",
            "background": "cream",
            "image_position": "right",
            "form_width": "wide",
            "field_columns": "2",
            "form_mode": "native",
            "headline": "Book a meeting with a local planner",
            "intro": "Tell us a little about yourself and we will match you with the right person.",
            "fields": ["first_name", "surname", "email", "phone", "postcode", "investment_value"],
            "submit_label": "Book a meeting",
            "thank_you_message": "Thanks — a planner will be in touch shortly.",
            "show_attribution_preview": True,
            "component": "lead_form",
        },
    },
    {
        "name": "Compact campaign strip",
        "preset": {
            "layout": "compact",
            "background": "bronze",
            "form_width": "wide",
            "field_columns": "2",
            "form_mode": "native",
            "headline": "Start the conversation",
            "intro": "Share your details and we will call you back.",
            "fields": ["first_name", "surname", "email", "phone", "postcode"],
            "submit_label": "Get in touch",
            "thank_you_message": "Thank you — we will call you back.",
            "show_attribution_preview": False,
            "component": "lead_form",
        },
    },
    {
        "name": "Wide two-column questionnaire",
        "preset": {
            "layout": "two_column_wide",
            "background": "cream",
            "form_width": "wide",
            "field_columns": "2",
            "form_mode": "native",
            "headline": "Tell us what matters to you",
            "intro": "The more we know, the better we can prepare for your first meeting.",
            "fields": ["first_name", "surname", "email", "phone", "postcode", "investment_value", "heard_about"],
            "submit_label": "Submit details",
            "thank_you_message": "Thank you for sharing that. We will be in touch.",
            "show_attribution_preview": True,
            "component": "lead_form",
        },
    },
    {
        "name": "Stacked cream card",
        "preset": {
            "layout": "stacked",
            "background": "cream",
            "form_width": "narrow",
            "field_columns": "1",
            "form_mode": "native",
            "headline": "Request a call back",
            "intro": "Leave your details and a member of the team will ring you.",
            "fields": ["first_name", "surname", "email", "phone", "postcode"],
            "submit_label": "Request a call",
            "thank_you_message": "Thank you — we will call you soon.",
            "show_attribution_preview": True,
            "component": "lead_form",
        },
    },
    {
        "name": "Mailchimp embed",
        "preset": {
            "layout": "stacked",
            "background": "white",
            "form_width": "medium",
            "field_columns": "1",
            "form_mode": "mailchimp",
            "headline": "Stay informed",
            "intro": "Join our mailing list for market updates and planning tips.",
            "fields": [],
            "mailchimp_form_id": "DEMO-MAILCHIMP-FORM-ID",
            "mailchimp_tags": "website, demo",
            "submit_label": "Subscribe",
            "thank_you_message": "You are subscribed.",
            "show_attribution_preview": False,
            "component": "lead_form",
        },
    },
]

# Delete old presets for this component if any
existing = api("GET", f"/presets/?component_id={COMP_ID}").get("presets") or []
for p in existing:
    try:
        api("DELETE", f"/presets/{p['id']}")
        print("deleted preset", p.get("name"))
    except Exception as e:
        print("skip delete", e)

first_id = None
for p in presets:
    body = {"preset": {"name": p["name"], "component_id": COMP_ID, "preset": p["preset"]}}
    created = api("POST", "/presets/", body)["preset"]
    print("created preset", created["id"], p["name"])
    if first_id is None:
        first_id = created["id"]

if first_id:
    api("PUT", f"/components/{COMP_ID}", {"component": {"preset_id": first_id}})
    print("default preset set", first_id)

print("done")
