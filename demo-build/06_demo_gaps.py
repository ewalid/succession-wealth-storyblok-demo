"""Close the demo-test gaps (UC1 hide nav, UC5 events hub, UC9 onward journey, UC10 topic hub,
UC11 tracking fields, UC13 redirect, UC8 starter cleanup). Idempotent; additive schema changes only.
Usage: python3 06_demo_gaps.py schemas | content"""
import sys, uuid
from sb import *
import importlib
s02 = importlib.import_module("02_schemas")
from importlib import import_module
text, textarea, richtext, number, boolean, image, link = s02.text, s02.textarea, s02.richtext, s02.number, s02.boolean, s02.image, s02.link
ds_one, ds_many, inline_one, inline_many, story_one, bloks, f = s02.ds_one, s02.ds_many, s02.inline_one, s02.inline_many, s02.story_one, s02.bloks, s02.f
build_schema, tabs, upsert_component, comps, ensure_group, seo_field = s02.build_schema, s02.tabs, s02.upsert_component, s02.comps, s02.ensure_group, s02.seo_field
NAVY, BRONZE = s02.NAVY, s02.BRONZE

CONTENT_TYPES = [("Articles", "article-page"), ("Videos", "video_page"), ("Events", "event")]


def add_fields(name, new_fields, tab_key_label=None):
    """Append new fields to an existing component without touching existing ones. Optionally add them to a new tab."""
    c = api("GET", f"components/{comps()[name]['id']}")["component"]   # fresh fetch before write
    sch = c["schema"]
    added = []
    p = max(v.get("pos", 0) for v in sch.values()) + 1
    for key, fld in new_fields:
        if key not in sch:
            sch[key] = {**fld, "pos": p}
            p += 1
            added.append(key)
    if tab_key_label and added:
        tk = f"tab-{uuid.uuid5(uuid.NAMESPACE_URL, name + tab_key_label)}"
        if tk in sch:
            sch[tk]["keys"] = list(dict.fromkeys(sch[tk]["keys"] + added))
        else:
            sch[tk] = {"type": "tab", "display_name": tab_key_label, "keys": added, "pos": p}
    if added:
        api("PUT", f"components/{c['id']}", {"component": {"schema": sch}})
    print(name, "added", added or "nothing (already there)")


def onward_field():
    return bloks("Onward journey", "Optional. Add one 'Onward journey' block to suggest what to read, watch or attend next.", ["onward_journey"], maximum=1)


def schemas():
    grp = ensure_group("planners")["uuid"]

    upsert_component("onward_journey", "Onward journey", build_schema([
        ("title", text("Heading", "Heading above the cards.", default_value="Where to go next")),
        ("mode", inline_one([("Latest content, chosen automatically", "latest"), ("Pick content by hand", "pinned")], "How to choose content",
                            "Latest: fills itself with the newest content matching the topic/author below, so it stays fresh as new content is published. Pick: you choose and order each item.",
                            default_value="latest")),
        ("items", f("options", "Pinned content (pick mode)", "Only used in 'Pick content by hand'. Choose articles, videos or events and drag to order.",
                    source="internal_stories", filter_content_type=[ct for _, ct in CONTENT_TYPES], use_uuid=True, entry_appearance="card")),
        ("topic", ds_one("specialisms", "Topic (latest mode)", "Only show content tagged with this topic. Leave empty for any topic.")),
        ("author", story_one("planner", "Planner (latest mode)", "Only show content written, hosted or featuring this planner. Leave empty for any planner.")),
        ("content_types", inline_many(CONTENT_TYPES, "Content types (latest mode)", "Which kinds of content to include. Leave empty for all.")),
        ("limit", number("Number of cards", "How many cards to show.", default_value="3")),
        ("open_in_new_tab", boolean("Open links in a new tab", "Tick to open the cards in a new browser tab.", default_value=False)),
    ]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="title")

    upsert_component("events_hub", "Events hub", build_schema([
        ("title", text("Heading", "Heading above the upcoming events.", default_value="Upcoming events")),
        ("intro", textarea("Intro text", "Optional short text under the heading.")),
        ("topic", ds_one("specialisms", "Only events on this topic (optional)", "Leave empty to list every event.")),
        ("show_past", boolean("Show past events", "Events move to 'Past events' automatically once their date has passed.", default_value=True)),
        ("past_limit", number("Maximum past events", "How many past events to list.", default_value="3")),
    ]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="title")

    upsert_component("topic-hub", "Topic hub", build_schema(tabs(
        ("Topic", [
            ("title", text("Hub title", "Main headline, e.g. 'Autumn Budget 2026'.")),
            ("intro", textarea("Intro text", "One or two sentences under the headline.")),
            ("hero_image", image("Hero image", "Optional banner image. Recommended 1600 x 700px.")),
            ("topic", ds_one("specialisms", "Topic", "The one field that drives the hub: planners, the finder, latest content and events for this topic are added automatically.")),
            ("body", bloks("Extra sections", "Optional sections shown after the automatic ones. Use any block.", None)),
        ]),
        ("Automatic sections", [
            ("show_planners", boolean("Show planners for this topic", "Lists every active planner tagged with the topic.", default_value=True)),
            ("show_finder", boolean("Show 'Find the right planner'", "The finder opens with this topic already selected.", default_value=True)),
            ("show_content", boolean("Show latest articles and videos", "Newest content tagged with the topic.", default_value=True)),
            ("show_events", boolean("Show upcoming events", "Upcoming events tagged with the topic.", default_value=True)),
        ]),
        ("SEO", [("seo", seo_field())]),
    )), is_root=True, is_nestable=False, color=NAVY, preview_field="title")

    add_fields("campaign-page", [
        ("hide_navigation", boolean("Hide site navigation", "Tick for paid campaign pages: hides the menu and footer links so visitors stay on the page and the form. The logo stays.", default_value=False)),
    ], "Campaign settings")
    # allow video + onward journey blocks on campaign pages (additive to the whitelist)
    c = api("GET", f"components/{comps()['campaign-page']['id']}")["component"]
    wl = c["schema"]["body"]["component_whitelist"]
    extra = [b for b in ["youtube-video", "onward_journey"] if b not in wl]
    if extra:
        c["schema"]["body"]["component_whitelist"] = wl + extra
        api("PUT", f"components/{c['id']}", {"component": {"schema": c["schema"]}})
    print("campaign-page body whitelist +", extra)

    add_fields("event", [
        ("hide_from_hub", boolean("Hide from events hub", "Tick for client-only events: the page still works by direct link but is not listed on the events hub.", default_value=False)),
        ("office", story_one("office", "Office (for the map)", "Optional. For in-person events at an office, pick it to show a map with directions.")),
        ("onward", onward_field()),
    ], "Hub, map & next steps")
    add_fields("article-page", [("onward", onward_field())])
    add_fields("video_page", [("onward", onward_field())])
    add_fields("planner", [("onward", onward_field())], "Onward journey")
    add_fields("site-config", [
        ("gtm_id", text("Google Tag Manager container ID", "e.g. GTM-ABC1234. GA4, Hotjar, LinkedIn and Meta tags are then managed in Tag Manager without a deploy.")),
        ("ga4_id", text("GA4 measurement ID", "Optional, e.g. G-XXXXXXX. Only needed if GA4 is not loaded through Tag Manager.")),
        ("linkedin_partner_id", text("LinkedIn Insight partner ID", "Optional, for LinkedIn ads retargeting.")),
        ("meta_pixel_id", text("Meta pixel ID", "Optional, for Facebook/Instagram ads retargeting.")),
    ], "Tracking")


# ---------------- content ----------------
def story_by_slug(slug):
    r = api("GET", f"stories?with_slug={slug}")["stories"]
    return api("GET", f"stories/{r[0]['id']}")["story"] if r else None


def save(story, publish=True):
    if story.get("unpublished_changes") and publish:
        print("  ! draft in progress on", story["full_slug"], "- saving without publish")
        publish = False
    api("PUT", f"stories/{story['id']}", {"story": story, "publish": 1 if publish else 0, "force_update": 1})
    print("  saved", story["full_slug"], "(published)" if publish else "(draft)")


def create(parent_slug, name, slug, content, startpage=False):
    ex = story_by_slug(f"{parent_slug}/{slug}") if not startpage else None
    if ex:
        ex["content"] = {**ex["content"], **content}
        save(ex)
        return ex
    parent = api("GET", f"stories?with_slug={parent_slug}&folder_only=1")["stories"][0]
    if startpage:
        for s in api("GET", f"stories?starts_with={parent_slug}/&per_page=100")["stories"]:
            if s.get("is_startpage"):
                full = api("GET", f"stories/{s['id']}")["story"]
                full["content"] = {**full["content"], **content}
                save(full)
                return full
    body = {"name": name, "slug": slug, "parent_id": parent["id"], "content": content, "is_startpage": startpage}
    s = api("POST", "stories", {"story": body, "publish": 1})["story"]
    print("  created", s["full_slug"])
    return s


def uid():
    return str(uuid.uuid4())


def rt(*paras):
    return {"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": p}]} for p in paras]}


def onward(**kw):
    return [{"_uid": uid(), "component": "onward_journey", "title": "Where to go next", "mode": "latest", "limit": "3", **kw}]


def url_link(u):
    return {"id": "", "url": u, "linktype": "url", "fieldtype": "multilink", "cached_url": u}


def content():
    leeds_campaign = story_by_slug("campaigns/leeds-retirement-planning")
    leeds_event = story_by_slug("events/retirement-income-evening-leeds")
    offices = {s["slug"]: s["uuid"] for s in api("GET", "stories?starts_with=offices/&per_page=100")["stories"]}
    planners = {s["slug"]: s["uuid"] for s in api("GET", "stories?starts_with=planners/&per_page=100")["stories"]}

    print("UC13 redirect")
    r = story_by_slug("redirects/redirect-1-services-landing-page") or story_by_slug("redirects/retired-manchester-campaign")
    r["name"], r["slug"] = "Retired: Manchester retirement campaign", "retired-manchester-campaign"
    r["content"] = {**r["content"], "Type": "301", "oldURL": url_link("/campaigns/manchester-retirement-planning"),
                    "newURL": {"id": leeds_campaign["uuid"], "url": "", "linktype": "story", "fieldtype": "multilink", "cached_url": leeds_campaign["full_slug"]},
                    "ToInternalStory": leeds_campaign["uuid"], "FromInternalStory": ""}
    save(r)

    print("UC5 events")
    create("events", "Autumn Budget 2026: live webinar", "autumn-budget-2026-webinar", {
        "component": "event", "title": "Autumn Budget 2026: live webinar", "start": "2026-11-27 12:30", "end": "2026-11-27 13:15",
        "location": "Online", "description": rt("Our planners unpack what the Autumn Budget means for your pensions, investments and inheritance tax plans, and answer your questions live."),
        "booking_url": url_link("https://www.gotomeeting.com/webinar"), "hosts": [planners["alison-james"]],
        "specialisms": ["inheritance-tax", "pensions"], "hide_from_hub": False, "onward": onward(topic="inheritance-tax")})
    create("events", "Pension planning seminar, Bristol", "pension-planning-seminar-bristol", {
        "component": "event", "title": "Pension planning seminar, Bristol", "start": "2026-10-15 18:30", "end": "2026-10-15 20:00",
        "location": "Bristol office", "office": offices.get("bristol", ""), "description": rt("An evening on making the most of your pension before and after you stop work."),
        "hosts": [planners["jon-noake"]] if "jon-noake" in planners else [], "specialisms": ["pensions", "retirement-planning"], "hide_from_hub": False})
    create("events", "Client briefing: Autumn Budget (clients only)", "client-briefing-autumn-budget", {
        "component": "event", "title": "Client briefing: Autumn Budget", "start": "2026-12-02 08:00", "end": "2026-12-02 09:00",
        "location": "London office", "office": offices.get("london", ""), "description": rt("A private breakfast briefing for existing clients."),
        "hosts": [planners["alison-james"]], "specialisms": ["inheritance-tax"], "hide_from_hub": True})
    ev = story_by_slug("events/retirement-income-evening-leeds")
    ev["content"] = {**ev["content"], "office": offices.get("leeds", ""), "hide_from_hub": False}
    ev["content"].setdefault("onward", onward(topic="retirement-planning"))
    save(ev)
    create("events", "Events", "index", {"component": "default-page", "meta_title": "Events | Succession Wealth",
                                         "meta_description": "Seminars and webinars with Succession Wealth planners.",
                                         "body": [{"_uid": uid(), "component": "events_hub", "title": "Upcoming events",
                                                   "intro": "Join our planners in person or online. Events move to 'Past events' automatically.",
                                                   "show_past": True, "past_limit": "3"}]}, startpage=True)

    print("UC9 onward journeys")
    a = story_by_slug("articles/inheritance-tax-planning-five-questions")
    a["content"]["onward"] = onward(topic="inheritance-tax", title="More on inheritance tax")
    save(a)
    a = story_by_slug("articles/retirement-income-before-you-stop-work")
    a["content"]["onward"] = onward(topic="retirement-planning", title="More on retirement planning")
    save(a)
    v = story_by_slug("videos/inheritance-tax-explained")
    v["content"]["onward"] = onward(mode="pinned", title="Read and watch next",
                                    items=[a["uuid"], story_by_slug("events/autumn-budget-2026-webinar")["uuid"]])
    save(v)
    p = story_by_slug("planners/alison-james")
    p["content"]["onward"] = onward(author=p["uuid"], title="Articles and events with Alison")
    save(p)

    print("UC10 topic hub")
    create("topics", "Autumn Budget 2026", "autumn-budget-2026", {
        "component": "topic-hub", "title": "Autumn Budget 2026", "topic": "inheritance-tax",
        "intro": "What the Budget means for your pensions, investments and inheritance tax plans, and the planners who can help you act on it.",
        "show_planners": True, "show_finder": True, "show_content": True, "show_events": True, "body": []})

    print("UC8 unpublish starter articles")
    keep = {"retirement-income-before-you-stop-work", "inheritance-tax-planning-five-questions"}
    for s in api("GET", "stories?starts_with=articles/&per_page=100&story_only=1")["stories"]:
        if s["slug"] not in keep and not s.get("is_startpage") and s.get("published"):
            api("GET", f"stories/{s['id']}/unpublish")
            print("  unpublished", s["full_slug"])

    print("Governance: compliance stage")
    for st in api("GET", "workflow_stages")["workflow_stages"]:
        if st["name"] == "Reviewing":
            api("PUT", f"workflow_stages/{st['id']}", {"workflow_stage": {"name": "Compliance review", "workflow_id": st.get("workflow_id")}})
            print("  renamed Reviewing -> Compliance review")


if __name__ == "__main__":
    {"schemas": schemas, "content": content}[sys.argv[1]]()
