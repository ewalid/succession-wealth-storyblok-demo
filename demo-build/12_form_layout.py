"""Form blok: per-field widths (full/two-thirds/half/third/quarter + start new row), layout tab
(stacked, image beside, image behind), heading/intro, presets, and a showcase forms/contact-us. Idempotent.
Usage: python3 12_form_layout.py"""
import uuid
from sb import *

IMG = {"id": 234970118355388, "filename": "https://a.storyblok.com/f/296113342540964/603516b670/lp-first-meeting.jpg",
       "alt": "Modern office building exterior", "fieldtype": "asset", "name": "", "focus": "", "title": "", "copyright": ""}


def opt(name, value): return {"name": name, "value": value}
def u(): return str(uuid.uuid4())
def doc(*paras): return {"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": p}]} for p in paras]}
def choice(label, value): return {"component": "field-option", "_uid": u(), "label": label, "value": value}


def field(label, name, ftype="text", width="full", required=False, new_row=False, options=None, **kw):
    return {"component": "form-field", "_uid": u(), "label": label, "name": name, "field_type": ftype, "width": width,
            "is_required": required, "start_new_row": new_row, "options": options or [], "placeholder": "", "autocomplete": "", "rows": "4", **kw}


FORM_NEW = {
    "headline": {"type": "text", "display_name": "Heading"},
    "intro": {"type": "richtext", "display_name": "Intro text"},
    "success_message": {"type": "text", "display_name": "Thank-you message", "description": "Shown after the form is sent"},
    "layout": {"type": "option", "display_name": "Layout", "default_value": "stacked", "exclude_empty_option": True, "options": [
        opt("Form only", "stacked"), opt("Image beside the form", "image_side"), opt("Image behind the form", "image_background")]},
    "side_image": {"type": "asset", "display_name": "Image", "filetypes": ["images"]},
    "image_position": {"type": "option", "display_name": "Image side", "default_value": "right", "exclude_empty_option": True,
                       "options": [opt("Right", "right"), opt("Left", "left")]},
    "background": {"type": "option", "display_name": "Background", "default_value": "cream", "exclude_empty_option": True, "options": [
        opt("Cream", "cream"), opt("White", "white"), opt("Dark", "dark"), opt("Bronze", "bronze")]},
    "form_width": {"type": "option", "display_name": "Form width", "default_value": "medium", "exclude_empty_option": True,
                   "description": "Used when there is no image beside the form",
                   "options": [opt("Narrow", "narrow"), opt("Medium", "medium"), opt("Wide", "wide")]},
    "card": {"type": "boolean", "display_name": "Put the form on a white card"},
    "button_align": {"type": "option", "display_name": "Button", "default_value": "left", "exclude_empty_option": True,
                     "options": [opt("Left", "left"), opt("Centred", "center"), opt("Full width", "full")]},
}
CONTENT_KEYS = ["headline", "intro", "fields", "button_text", "success_message"]
LAYOUT_KEYS = ["layout", "side_image", "image_position", "background", "form_width", "card", "button_align"]

CONTACT = {
    "component": "form", "headline": "Talk to a planner", "button_text": "Request a call back",
    "intro": doc("Tell us a little about you and a planner from your nearest office will be in touch within one working day."),
    "success_message": "Thank you. A planner will call you within one working day.",
    "layout": "image_side", "side_image": IMG, "image_position": "right", "background": "cream", "form_width": "medium",
    "card": False, "button_align": "left",
    "fields": [
        field("First name", "first_name", width="half", required=True, autocomplete="given-name"),
        field("Surname", "surname", width="half", required=True, autocomplete="family-name"),
        field("Email", "email", "email", width="two_thirds", required=True),
        field("Postcode", "postcode", width="third", required=True, autocomplete="postal-code"),
        field("Phone", "phone", "tel", width="half"),
        field("Best time to call", "best_time", "select", width="half", options=[
            choice("Morning", "morning"), choice("Afternoon", "afternoon"), choice("Evening", "evening")]),
        field("How would you like to meet?", "meeting", "radio", options=[
            choice("At home", "home"), choice("At our office", "office"), choice("By video", "digital")]),
        field("What would you like to talk about?", "message", "textarea"),
        field("I agree to Succession Wealth contacting me about my enquiry", "consent", "checkbox", required=True),
    ],
}
SIGNUP = {
    "component": "form", "headline": "Get our weekly insights", "button_text": "Sign up",
    "intro": doc("Market updates and planning ideas from our planners, once a week."),
    "success_message": "You're subscribed. Look out for our next email.",
    "layout": "stacked", "background": "dark", "form_width": "narrow", "card": False, "button_align": "full",
    "fields": [
        field("First name", "first_name", width="half", required=True),
        field("Email", "email", "email", width="half", required=True),
    ],
}


def main():
    comps_ = {c["name"]: c for c in api("GET", "components")["components"]}

    # form-field: more widths + start new row (fresh fetch)
    ff = api("GET", f"components/{comps_['form-field']['id']}")["component"]
    sch = ff["schema"]
    sch["width"]["options"] = [opt("Full width", "full"), opt("Two thirds", "two_thirds"), opt("Half", "half"),
                               opt("One third", "third"), opt("Quarter", "quarter")]
    sch["width"]["description"] = ("Fields sit side by side until the row is full (e.g. Half + Half, or Two thirds + One third). "
                                   "On phones every field is full width. In the Lead form only Full and Half apply.")
    top = max(v.get("pos", 0) for v in sch.values())
    # Choices stays optional: text fields hide it, and a checkbox without choices is a single tick box.
    sch["options"]["required"] = False
    sch["options"]["description"] = "For dropdown, radio or checkbox lists: add one choice per option. Leave a checkbox empty for a single tick box (e.g. consent)."
    sch.setdefault("start_new_row", {"type": "boolean", "display_name": "Start on a new row", "pos": top + 1})
    api("PUT", f"components/{ff['id']}", {"component": {"schema": sch}})

    # form: new fields in Content / Layout tabs (fresh fetch)
    fm = api("GET", f"components/{comps_['form']['id']}")["component"]
    sch = fm["schema"]
    top = max(v.get("pos", 0) for v in sch.values())
    for i, (k, v) in enumerate(FORM_NEW.items()):
        sch.setdefault(k, {**v, "pos": top + 3 + i})
    for name, keys, pos in (("Content", CONTENT_KEYS, -2), ("Layout", LAYOUT_KEYS, top + 1)):
        tab = next((k for k, v in sch.items() if v.get("type") == "tab" and v.get("display_name") == name), None) or f"tab-{u()}"
        sch[tab] = {"type": "tab", "display_name": name, "keys": keys, "pos": pos}
    sch["fields"]["display_name"] = sch["fields"].get("display_name") or "Fields"
    sch["button_text"]["display_name"] = sch["button_text"].get("display_name") or "Button label"
    api("PUT", f"components/{fm['id']}", {"component": {"display_name": "Form", "schema": sch}})

    # presets for new forms; first = default
    presets = api("GET", "presets")["presets"]
    first = None
    for pname, content in (("Contact form with image", CONTACT), ("Newsletter sign-up (dark)", SIGNUP)):
        body = {"name": pname, "component_id": fm["id"], "preset": {**content, "_uid": u()}}
        ex = next((p for p in presets if p["component_id"] == fm["id"] and p["name"] == pname), None)
        p = api("PUT", f"presets/{ex['id']}", {"preset": body})["preset"] if ex else api("POST", "presets", {"preset": body})["preset"]
        first = first or p["id"]
    api("PUT", f"components/{fm['id']}", {"component": {"preset_id": first}})

    # showcase stories (skip if someone has unsaved draft edits)
    for sid, content in ((234213853637402, CONTACT), (234213853637405, SIGNUP)):
        st = api("GET", f"stories/{sid}")["story"]
        if st.get("unpublished_changes"):
            print("SKIP draft in progress:", st["full_slug"]); continue
        api("PUT", f"stories/{sid}", {"story": {"content": {**content, "_uid": st["content"]["_uid"]}}, "publish": 1})
        print("updated + published", st["full_slug"])

    # verify
    st = api("GET", "stories/234213853637402")["story"]
    print("VERIFY contact-us", st["content"]["layout"], [(f["label"], f["width"]) for f in st["content"]["fields"]])
    fm = api("GET", f"components/{fm['id']}")["component"]
    print("VERIFY form tabs", [v["display_name"] for v in fm["schema"].values() if v.get("type") == "tab"], "default preset", first)


if __name__ == "__main__":
    main()
