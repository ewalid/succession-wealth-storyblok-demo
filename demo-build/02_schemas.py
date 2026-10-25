"""Idempotent: component group, nestable blocks, content types, presets, and extensions of
existing types (article-page: author/specialisms; default-page: allow planner blocks).
Redirect and every other existing component stay untouched."""
import uuid
from sb import *

NAVY, BRONZE = "#14213d", "#8b6f4b"   # navy + the bronze/gold used on successionwealth.co.uk (#8b6f4b)


# ---------- field helpers ----------
def f(type_, label, help_, **kw):
    d = {"type": type_, "display_name": label, "description": help_}
    d.update(kw)
    return d


def text(label, help_, **kw): return f("text", label, help_, **kw)
def textarea(label, help_, **kw): return f("textarea", label, help_, **kw)
def richtext(label, help_, **kw): return f("richtext", label, help_, **kw)
def number(label, help_, **kw): return f("number", label, help_, **kw)
def boolean(label, help_, **kw): return f("boolean", label, help_, **kw)
def image(label, help_, **kw): return f("asset", label, help_, filetypes=["images"], **kw)
def link(label, help_, **kw): return f("multilink", label, help_, allow_target_blank=True, asset_link_type=kw.pop("asset", False), email_link_type=kw.pop("email", False), **kw)
def ds_one(slug, label, help_, **kw): return f("option", label, help_, source="internal", datasource_slug=slug, **kw)
def ds_many(slug, label, help_, **kw): return f("options", label, help_, source="internal", datasource_slug=slug, **kw)
def inline_one(opts, label, help_, **kw): return f("option", label, help_, options=[{"name": n, "value": v} for n, v in opts], **kw)
def inline_many(opts, label, help_, **kw): return f("options", label, help_, options=[{"name": n, "value": v} for n, v in opts], **kw)
def story_one(ct, label, help_, **kw): return f("option", label, help_, source="internal_stories", filter_content_type=[ct], use_uuid=True, entry_appearance="card", **kw)
def story_many(ct, label, help_, **kw): return f("options", label, help_, source="internal_stories", filter_content_type=[ct], use_uuid=True, entry_appearance="card", **kw)
def bloks(label, help_, whitelist=None, **kw):
    d = f("bloks", label, help_, restrict_type="", restrict_components=bool(whitelist), **kw)
    if whitelist:
        d["component_whitelist"] = whitelist
    return d
def seo_field(): return bloks("SEO", "Optional. Add one 'SEO settings' block to override the page title, description and social image.", ["seo_meta"], maximum=1)


def build_schema(items):
    """items: list of (name, field) or ('__tab__', label, [names]) -> schema with positions + tabs"""
    schema, pos = {}, 0
    for it in items:
        if it[0] == "__tab__":
            schema[f"tab-{uuid.uuid5(uuid.NAMESPACE_URL, it[1])}"] = {"type": "tab", "display_name": it[1], "keys": it[2], "pos": pos}
        else:
            schema[it[0]] = {**it[1], "pos": pos}
        pos += 1
    return schema


def tabs(*groups):
    """groups: (label, [(name, field)...]) -> flattened items with tabs first then fields (tabs reference keys)."""
    items = []
    for label, flds in groups:
        items.append(("__tab__", label, [n for n, _ in flds]))
    for _, flds in groups:
        items += flds
    return items


# ---------- component upsert ----------
_comps = {}
def comps():
    if not _comps:
        for c in list_all("components", "components"):
            _comps[c["name"]] = c
    return _comps


def upsert_component(name, display_name, schema, **extra):
    body = {"name": name, "display_name": display_name, "schema": schema, **extra}
    ex = comps().get(name)
    if ex:
        c = api("PUT", f"components/{ex['id']}", {"component": body})["component"]
        print("updated component", name, c["id"])
    else:
        c = api("POST", "components", {"component": body})["component"]
        print("created component", name, c["id"])
    _comps[name] = c
    return c


def ensure_group(name):
    for g in api("GET", "component_groups")["component_groups"]:
        if g["name"] == name:
            return g
    g = api("POST", "component_groups", {"component_group": {"name": name}})["component_group"]
    print("created group", name)
    return g


# ---------- definitions ----------
def main():
    grp = ensure_group("planners")["uuid"]
    seo_grp = ensure_group("SEO")["uuid"]

    # ===== nestable blocks =====
    upsert_component("seo_meta", "SEO settings", build_schema([
        ("title", text("SEO title", "Shown in search results and the browser tab. Aim for 50-60 characters. Leave empty to use the page title.")),
        ("description", textarea("SEO description", "Shown under the title in search results. Aim for 140-160 characters. Leave empty to use the page intro.")),
        ("og_image", image("Social share image", "Image shown when the page is shared on LinkedIn, Facebook or WhatsApp. Recommended 1200 x 630px.")),
        ("noindex", boolean("Hide from search engines", "Tick to stop search engines listing this page (adds noindex). Leave unticked for normal pages.", default_value=False)),
    ]), is_nestable=True, is_root=False, component_group_uuid=seo_grp, color=NAVY)

    upsert_component("planner_card", "Planner card", build_schema([
        ("planner", story_one("planner", "Planner", "Pick the planner to show. The photo, name, title, specialisms and office all come from their profile, so there is nothing to retype.")),
        ("cta_label", text("Button label", "Text on the button that opens the planner's profile.", default_value="Meet your planner")),
        ("show_specialisms", boolean("Show specialisms", "Show the planner's specialisms as small tags on the card.", default_value=True)),
        ("show_office", boolean("Show office", "Show the office the planner is based in.", default_value=True)),
    ]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="cta_label")

    upsert_component("planner_grid", "Planner grid", build_schema([
        ("title", text("Heading", "Optional heading above the grid, e.g. 'Meet our Leeds planners'. Leave empty for no heading.")),
        ("mode", inline_one([("Pick planners by hand", "manual"), ("All planners in an office", "by_office"), ("All planners with a specialism", "by_specialism")],
                            "How to choose planners", "Manual: you choose each planner. By office / By specialism: the grid fills itself, so new planners appear automatically and anyone unpublished or set to inactive disappears.",
                            default_value="manual")),
        ("planners", story_many("planner", "Planners (manual mode)", "Only used when 'How to choose planners' is 'Pick planners by hand'. Pick and order the planners to show.")),
        ("office", story_one("office", "Office (by office mode)", "Only used for 'All planners in an office'. Planners pinned on that office show first.")),
        ("specialism", ds_one("specialisms", "Specialism (by specialism mode)", "Only used for 'All planners with a specialism'. Every active planner tagged with it appears automatically.")),
        ("sort", inline_one([("Pinned first, then A-Z", "pinned_then_az"), ("A-Z by last name", "az")], "Order", "Pinned first uses the pinned planners from the office page, then lists everyone else A-Z.", default_value="pinned_then_az")),
        ("limit", number("Maximum planners", "Maximum number of planners to show. Leave empty to show everyone.", default_value="6")),
    ]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="title")

    upsert_component("planner_finder", "Find the right planner", build_schema([
        ("title", text("Heading", "Heading of the finder.", default_value="Find the right planner for you")),
        ("intro", textarea("Intro text", "Short text above the form. Say what the visitor needs to enter.", default_value="Tell us where you are and what you need help with, and we will show you the planners who can help.")),
        ("preset_specialism", ds_one("specialisms", "Pre-select a topic (optional)", "Use this on topic pages: the finder opens with this topic already ticked. Leave empty on general pages.")),
        ("default_preference", inline_one([("No preference", ""), ("Home visit", "home"), ("Office", "office"), ("Digital (video or phone)", "digital")],
                                          "Default meeting preference", "Which meeting type is selected when the finder opens. Visitors can change it.", default_value="")),
        ("max_results", number("Number of results", "How many planners to show in the results.", default_value="3")),
    ]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="title")

    upsert_component("office_map", "Office map", build_schema([
        ("office", story_one("office", "Office", "The office to show on the map. Its address and coordinates come from the office page.")),
        ("planner", story_one("planner", "Show home-visit radius for planner (optional)", "Optional. Pick a planner to draw their home-visit radius as a circle around the office. Leave empty for just the office pin.")),
        ("show_directions", boolean("Show 'Get directions' button", "Adds a button that opens Google Maps directions to the office.", default_value=True)),
    ]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="office")

    upsert_component("lead_form", "Lead form", build_schema([
        ("headline", text("Heading", "Heading above the form.", default_value="Ready for a conversation?")),
        ("intro", textarea("Intro text", "Reassuring text under the heading.", default_value="There is no pressure and no obligation, just a confidential chat to understand your goals.")),
        ("form_mode", inline_one([("Built-in form", "native"), ("Mailchimp embed", "mailchimp")], "Form type", "Built-in form uses the fields you tick below. Mailchimp embed uses the audience form ID.", default_value="native")),
        ("fields", inline_many([("First name", "first_name"), ("Surname", "surname"), ("Email", "email"), ("Phone", "phone"), ("Postcode", "postcode"),
                                 ("Investment and pension value", "investment_value"), ("Where did you hear about us?", "heard_about")],
                                "Fields to show", "Tick the questions to ask (built-in form only). Name and email are always asked.")),
        ("mailchimp_form_id", text("Mailchimp form ID", "Only for the Mailchimp embed. Paste the form ID provided by the marketing team.")),
        ("mailchimp_tags", text("Mailchimp tags", "Optional. Comma-separated tags added to every lead from this form, e.g. 'paid-search, leeds'.")),
        ("submit_label", text("Button label", "Text on the submit button.", default_value="Request a conversation")),
        ("thank_you_message", textarea("Thank-you message", "Shown after the form is sent, if no thank-you page is chosen.", default_value="Thank you. We will be in touch to arrange a convenient time.")),
        ("thank_you_page", link("Thank-you page", "Optional. Send visitors to this page after submitting.")),
        ("privacy_url", link("Privacy policy link", "Linked from the consent checkbox.")),
        ("hidden_fields_note", f("section", "Tracking (automatic)", "The page, template, planner, office and UTM parameters are added to every submission automatically so the leads can be attributed. Nothing to fill in here.")),
    ]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="headline")

    # ===== content types =====
    upsert_component("office", "Office", build_schema(tabs(
        ("Office", [
            ("name", text("Office name", "Public name of the office, e.g. 'Leeds'.")),
            ("intro", richtext("About this office", "A short welcome to the office and the area it covers.")),
            ("hero_image", image("Hero image", "Optional photo of the office or the city. Recommended 1600 x 700px.")),
            ("pinned_planners", story_many("planner", "Pinned planners", "Planners shown first on this office page. Everyone else is listed A-Z automatically.")),
        ]),
        ("Location", [
            ("address", textarea("Address", "Full postal address, one line per row.")),
            ("postcode", text("Postcode", "Used for the map and directions, e.g. 'LS1 5AA'.")),
            ("lat", number("Latitude", "Decimal latitude, e.g. 53.7950. Used by the map and the planner finder.")),
            ("lng", number("Longitude", "Decimal longitude, e.g. -1.5470. Used by the map and the planner finder.")),
            ("map_style", inline_one([("On-brand (no businesses or ads)", "brand")], "Map style", "Visual style of the map.", default_value="brand")),
            ("phone", text("Phone", "Main office phone number.")),
            ("email", text("Email", "Optional. Main office email address.")),
        ]),
        ("Extra content & SEO", [
            ("body", bloks("Extra sections", "Optional extra sections shown below the planners.", None)),
            ("seo", seo_field()),
        ]),
    )), is_root=True, is_nestable=False, color=NAVY, preview_field="name")

    upsert_component("planner", "Planner", build_schema(tabs(
        ("Profile", [
            ("first_name", text("First name", "Planner's first name.")),
            ("last_name", text("Last name", "Planner's last name. Used for A-Z ordering.")),
            ("photo", image("Photo", "Headshot. Square or portrait, at least 800px wide.")),
            ("job_title", text("Job title", "e.g. 'Chartered Wealth Planner'.")),
            ("short_bio", textarea("Short bio (for cards)", "One or two sentences shown on planner cards. Around 160 characters works best.")),
            ("bio", richtext("Full bio", "Full biography shown on the planner's profile page.")),
            ("video", link("Intro video (optional)", "Optional. Upload a video or paste a YouTube/Vimeo link.", asset=True)),
        ]),
        ("Expertise & office", [
            ("qualifications", ds_many("qualifications", "Qualifications", "Tick every qualification the planner holds.")),
            ("specialisms", ds_many("specialisms", "Specialisms", "Topics the planner can help with. This is what puts them on topic pages and in finder results automatically.")),
            ("office", story_one("office", "Office", "The office the planner is based in. They appear on that office page automatically.")),
            ("meeting_preferences", ds_many("meeting-preferences", "Meeting preferences", "How the planner can meet clients. Used by the planner finder.")),
            ("home_visit_radius_miles", number("Home visit radius (miles)", "How far from the office the planner will travel to visit clients at home. Drawn as a circle on the map.")),
        ]),
        ("Contact & booking", [
            ("phone", text("Phone", "Planner's direct phone number.")),
            ("email", text("Email", "Planner's email address.")),
            ("fca_register_url", link("FCA register link", "Link to the planner's entry on the FCA register.")),
            ("booking_url", link("Booking link", "Optional booking page, e.g. Microsoft Bookings. If empty, the lead form is used.")),
        ]),
        ("Visibility & SEO", [
            ("active", boolean("Active", "Untick when a planner leaves or is on leave. They disappear from every list, even if the entry is still published.", default_value=True)),
            ("seo", seo_field()),
        ]),
    )), is_root=True, is_nestable=False, color=NAVY, preview_field="last_name")

    campaign_blocks = [b for b in ["hero-section-simple", "hero-section", "banner", "text-section", "image-text-section",
                                   "testimonials-section", "faq-section", "logo-section", "button"] if b in comps()]
    campaign_blocks += ["lead_form", "planner_grid", "office_map"]
    upsert_component("campaign-page", "Campaign page", build_schema(tabs(
        ("Campaign", [
            ("headline", text("Headline", "Main headline at the top of the page.")),
            ("intro", textarea("Intro text", "Short supporting text under the headline.")),
            ("hero_image", image("Hero image", "Main image at the top of the page.")),
            ("office", story_one("office", "Office", "The local office this campaign targets. Address, map and planners come from the office page.")),
            ("body", bloks("Page sections", "Add campaign sections here. Only approved campaign blocks are available, so the page stays on-brand and compliant.", campaign_blocks)),
        ]),
        ("Tracking & SEO", [
            ("utm_campaign", text("Campaign name for tracking", "Added to form submissions so leads can be attributed, e.g. 'bristol-retirement-q4'.")),
            ("seo", seo_field()),
        ]),
    )), is_root=True, is_nestable=False, color=BRONZE, preview_field="headline")

    upsert_component("event", "Event", build_schema(tabs(
        ("Event", [
            ("title", text("Event title", "Name of the event.")),
            ("start", f("datetime", "Start", "Date and time the event starts.")),
            ("end", f("datetime", "End", "Optional. Date and time the event ends.")),
            ("location", text("Location", "Venue name and town, or 'Online'.")),
            ("image", image("Image", "Main image for the event.")),
            ("description", richtext("Description", "What the event is about and who it is for.")),
            ("booking_url", link("Booking link", "Where visitors register for the event.")),
        ]),
        ("Hosts & topics", [
            ("hosts", story_many("planner", "Hosts", "Planners hosting the event. Their photo and profile are shown automatically.")),
            ("specialisms", ds_many("specialisms", "Topics", "Topics covered. Used to show this event on topic pages.")),
            ("seo", seo_field()),
        ]),
    )), is_root=True, is_nestable=False, color=NAVY, preview_field="title")

    upsert_component("video_page", "Video page", build_schema(tabs(
        ("Video", [
            ("title", text("Video title", "Title of the video.")),
            ("video", link("Video", "Upload a video or paste a YouTube/Vimeo link.", asset=True)),
            ("thumbnail", image("Thumbnail", "Optional cover image shown before the video plays.")),
            ("description", richtext("Description", "Text shown alongside the video.")),
        ]),
        ("Planners & topics", [
            ("featured_planners", story_many("planner", "Featured planners", "Planners who appear in the video. Their cards are shown on the page automatically.")),
            ("specialisms", ds_many("specialisms", "Topics", "Topics covered. Used to show this video on topic pages.")),
            ("seo", seo_field()),
        ]),
    )), is_root=True, is_nestable=False, color=NAVY, preview_field="title")

    # ===== extend existing types (additive only) =====
    art = comps()["article-page"]
    sch = art["schema"]
    if "author" not in sch:
        p = max(v.get("pos", 0) for v in sch.values()) + 1
        sch["author"] = {**story_one("planner", "Author", "Optional. The planner who wrote this article. If empty, or if the planner is inactive or unpublished, the byline falls back to 'Succession Wealth'."), "pos": p}
        sch["specialisms"] = {**ds_many("specialisms", "Topics", "Topics covered. Used to show this article on topic pages."), "pos": p + 1}
        api("PUT", f"components/{art['id']}", {"component": {"schema": sch}})
        print("extended article-page with author + specialisms")
    else:
        print("article-page already extended")

    dp = comps()["default-page"]
    sch = dp["schema"]
    wl = sch["body"].setdefault("component_group_whitelist", [])
    if grp not in wl:
        wl.append(grp)
        api("PUT", f"components/{dp['id']}", {"component": {"schema": sch}})
        print("default-page body now allows planner blocks")
    else:
        print("default-page already allows planner blocks")

    # ===== presets (+ default) =====
    existing = {(p["name"], p["component_id"]): p for p in api("GET", "presets")["presets"]}
    PRESETS = {
        "planner_card": [("Planner card", {"cta_label": "Meet your planner", "show_specialisms": True, "show_office": True})],
        "planner_grid": [("Planners in an office", {"title": "Meet our planners", "mode": "by_office", "sort": "pinned_then_az", "limit": "6"}),
                         ("Planners by specialism", {"title": "Planners who can help", "mode": "by_specialism", "sort": "az", "limit": "3"})],
        "planner_finder": [("Find the right planner", {"title": "Find the right planner for you",
                                                       "intro": "Tell us where you are and what you need help with, and we will show you the planners who can help.",
                                                       "default_preference": "", "max_results": "3"})],
    }
    for cname, plist in PRESETS.items():
        cid = comps()[cname]["id"]
        first_id = None
        for pname, vals in plist:
            body = {"name": pname, "component_id": cid, "preset": {"_uid": str(uuid.uuid5(uuid.NAMESPACE_URL, "preset-" + pname)), "component": cname, **vals}}
            ex = existing.get((pname, cid))
            if ex:
                p = api("PUT", f"presets/{ex['id']}", {"preset": body})["preset"]
            else:
                p = api("POST", "presets", {"preset": body})["preset"]
                print("created preset", pname, p["id"])
            first_id = first_id or p["id"]
        api("PUT", f"components/{cid}", {"component": {"preset_id": first_id}})
        print("default preset set for", cname, first_id)


if __name__ == "__main__":
    main()
