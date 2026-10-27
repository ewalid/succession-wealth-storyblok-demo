"""Two presets per page type (content type), first one = default for new pages. Idempotent.
Usage: python3 10_page_presets.py"""
import importlib
from sb import *

lp = importlib.import_module("09_location_page")
doc, para, h3, ul, with_uids, comps, asset = lp.doc, lp.para, lp.h3, lp.ul, lp.with_uids, lp.comps, lp.asset


def h2(t): return {"type": "heading", "attrs": {"level": 2}, "content": [{"type": "text", "text": t}]}
def url(u): return {"id": "", "url": u, "linktype": "url", "fieldtype": "multilink", "cached_url": u}
def onward(**kw): return [{"component": "onward_journey", "title": "Where to go next", "mode": "latest", "limit": "3", **kw}]


def form(headline="Ready for a conversation?", **kw):
    f = lp.lead_form()
    f.update({"headline": headline, "mailchimp_tags": "paid-search", **kw})   # {city} is only filled on location pages
    return f


PRESETS = {
    "campaign-page": [
        ("Paid search campaign (form-led)", {
            "headline": "Retirement planning near you", "intro": doc("Speak to a local wealth planner about your retirement goals. No cost, no obligation."),
            "hero_layout": "overlay_card", "hero_media_type": "image", "hero_cta_label": "Book a free consultation",
            "hide_navigation": True, "body": [{"component": "planner_grid", "title": "Your local planners", "mode": "by_office", "sort": "pinned_then_az", "limit": "3"}, form()]}),
        ("Topic campaign with video (split)", {
            "headline": "Plan your inheritance tax early", "intro": doc("A short film from our planners, then book a conversation with a specialist."),
            "hero_layout": "split", "hero_media_type": "youtube", "hero_cta_label": "Talk to a specialist",
            "hide_navigation": True, "body": [{"component": "planner_grid", "title": "Inheritance tax specialists", "mode": "by_specialism", "specialism": "inheritance-tax", "sort": "az", "limit": "3"}, form(layout="compact")]}),
    ],
    "location-page": [
        ("Location page (short: hero, office, form)", {
            "headline": "Independent financial advice in {city}", "hero_body": lp.HERO_BODY, "cta_label": "Book a free consultation", "hide_navigation": True,
            "compliance_code": "", "body": [lp.OFFICE, lp.PLANNERS, form(mailchimp_tags="paid-search, location-lp, {city}"), lp.TRUST]}),
    ],
    "planner": [
        ("Chartered Wealth Planner", {
            "job_title": "Chartered Wealth Planner", "active": True, "home_visit_radius_miles": "25",
            "qualifications": ["chartered-financial-planner"], "specialisms": ["retirement-planning", "inheritance-tax", "investments"],
            "meeting_preferences": ["home", "office", "digital"],
            "short_bio": "Helps clients plan for retirement and pass on their wealth with confidence.",
            "bio": doc("[First name] is a Chartered Wealth Planner based in our [office] office, helping individuals and families plan for retirement and pass on their wealth.", "Every relationship starts with a conversation about what matters most: your family, your plans and the life you want to lead. [First name] then builds a financial plan around those goals and reviews it with you every year.", "Outside work: add a line about hobbies or community here."),
            "onward": onward(title="Articles and events with this planner")}),
        ("Specialist adviser (office and digital only)", {
            "job_title": "Employee Benefits Consultant", "active": True, "home_visit_radius_miles": "0",
            "qualifications": ["cii-diploma"], "specialisms": ["employee-benefits", "business-owners"], "meeting_preferences": ["office", "digital"],
            "short_bio": "Advises business owners on pensions and benefits for their teams.",
            "bio": doc("[First name] works with employers and business owners.", "Write two or three sentences about their specialism.")}),
    ],
    "office": [
        ("Regional office", {
            "intro": doc("Welcome to our [city] office. Our planners meet clients here, at home or by video."),
            "map_style": "brand", "body": [form()]}),
        ("Office by appointment only", {
            "intro": doc("Meetings at this office are by appointment only. Our planners can also visit you at home or meet by video."),
            "map_style": "brand", "body": [{"component": "planner_finder", "title": "Find the right planner for you", "default_preference": "home", "max_results": "3"}]}),
    ],
    "event": [
        ("In-person seminar", {
            "title": "[Topic] seminar, [City]", "location": "[City] office", "hide_from_hub": False,
            "description": doc("An evening with our planners on [topic]. Refreshments from 6pm, talk at 6:30pm, questions after."),
            "specialisms": ["retirement-planning"], "onward": onward(topic="retirement-planning")}),
        ("Online webinar", {
            "title": "[Topic]: live webinar", "location": "Online", "hide_from_hub": False,
            "description": doc("A 45-minute live webinar with our planners, with time for your questions. Register to receive the joining link."),
            "booking_url": url("https://www.gotomeeting.com/webinar"), "specialisms": ["inheritance-tax"]}),
    ],
    "video_page": [
        ("Planner explainer", {
            "title": "[Topic] explained",
            "description": doc("One of our planners explains [topic] in under five minutes, and what to do next."),
            "specialisms": ["inheritance-tax"], "onward": onward(topic="inheritance-tax", title="Read and watch next")}),
        ("Client story", {
            "title": "How we helped [client first name] plan their retirement",
            "description": doc("A client describes their goals, how their planner helped, and what changed."),
            "specialisms": ["retirement-planning"], "onward": onward(topic="retirement-planning")}),
    ],
    "topic-hub": [
        ("Topic hub (everything)", {
            "title": "[Topic]", "intro": doc("Everything you need to know about [topic], and the planners who can help."),
            "show_planners": True, "show_finder": True, "show_content": True, "show_events": True}),
        ("News hub (content and events only)", {
            "title": "[Event, e.g. Autumn Budget]", "intro": doc("Our latest analysis and upcoming events on [event]."),
            "show_planners": False, "show_finder": False, "show_content": True, "show_events": True}),
    ],
    "Redirect": [
        ("Permanent redirect (301)", {"Type": "301"}),
        ("Temporary redirect (302)", {"Type": "302"}),
    ],
    "article-page": [
        ("Planner guide", {
            "headline": "[Question your client asks]",
            "text": doc("Start with the answer in one or two sentences.", h2("What it means for you"), "Explain the impact in plain English.",
                        h2("What to do next"), ul(["First step", "Second step", "When to speak to a planner"])),
            "onward": onward(title="Related reading")}),
        ("Short news update", {
            "headline": "[What changed]",
            "text": doc("What changed and when, in two sentences.", "Who it affects and what they should do."),
            "onward": onward(title="More updates")}),
    ],
}


def main():
    existing = {(p["name"], p["component_id"]): p for p in api("GET", "presets")["presets"]}
    for cname, plist in PRESETS.items():
        cid = comps()[cname]["id"]
        first = None
        for pname, values in plist:
            body = {"name": pname, "component_id": cid, "preset": with_uids({"component": cname, **values})}
            ex = existing.get((pname, cid))
            p = api("PUT", f"presets/{ex['id']}", {"preset": body})["preset"] if ex else api("POST", "presets", {"preset": body})["preset"]
            first = first or p["id"]
            print(f"{cname:15} · {pname}")
        if cname != "location-page":   # location-page keeps 'Location landing page (full)' as default
            api("PUT", f"components/{cid}", {"component": {"preset_id": first}})
    # verify
    allp = api("GET", "presets")["presets"]
    for cname in PRESETS:
        c = api("GET", f"components/{comps()[cname]['id']}")["component"]
        names = [p["name"] for p in allp if p["component_id"] == c["id"]]
        default = next((p["name"] for p in allp if p["id"] == c.get("preset_id")), None)
        print(f"VERIFY {cname:15} {len(names)} presets, default = {default}")


if __name__ == "__main__":
    main()
