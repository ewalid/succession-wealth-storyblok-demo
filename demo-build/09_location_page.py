"""Location landing page template (mirrors successionwealth.co.uk/financial-advice-<city>, campaign MK26-665).
Content type `location-page` + section blocks (lp-*) + presets + a full-page default preset,
then the Leeds and Bristol pages. Copy uses {city} / {phone} / {address} tokens filled from the Office.
Usage: python3 09_location_page.py schemas | content"""
import sys, uuid, importlib
from sb import *

s02 = importlib.import_module("02_schemas")
text, textarea, richtext, boolean, image, link, inline_one, story_one, bloks, f = (
    s02.text, s02.textarea, s02.richtext, s02.boolean, s02.image, s02.link, s02.inline_one, s02.story_one, s02.bloks, s02.f)
build_schema, tabs, upsert_component, comps, ensure_group, seo_field = (
    s02.build_schema, s02.tabs, s02.upsert_component, s02.comps, s02.ensure_group, s02.seo_field)
NAVY, BRONZE = s02.NAVY, s02.BRONZE

TOKENS_HELP = " You can type {city}, {phone} or {address}: they are filled in from the page's Office."
ASSETS = {"leeds_hero": 234970101643702, "bristol_hero": 234970105371064, "leeds_map": 234970109942201,
          "bristol_map": 234970113628602, "first_meeting": 234970118355388, "fees": 234970121402814}
SECTION_BLOCKS = ["lp-text", "lp-office", "lp-image-card", "lp-testimonial", "lp-trust",
                  "lead_form", "planner_grid", "office_map", "youtube-video", "faq-section", "onward_journey"]


# ---------------- rich text helpers ----------------
def para(t): return {"type": "paragraph", "content": [{"type": "text", "text": t}]} if t else {"type": "paragraph"}
def h3(t): return {"type": "heading", "attrs": {"level": 3}, "content": [{"type": "text", "text": t}]}
def ul(items): return {"type": "bullet_list", "content": [{"type": "list_item", "content": [para(i)]} for i in items]}
def doc(*nodes): return {"type": "doc", "content": [n if isinstance(n, dict) else para(n) for n in nodes]}
def uid(): return str(uuid.uuid4())
def cta(label, href=""):
    return {"cta_label": label, "cta_link": {"id": "", "url": href, "linktype": "url", "fieldtype": "multilink", "cached_url": href}}


# ---------------- copy (from the live Leeds/Bristol pages, city tokenised) ----------------
HERO_BODY = doc(
    "Based in and around {city}, our team of independent financial advisers provide thoughtful and holistic whole-of-market advice to individuals with £250,000 or more in total across pension and investment savings. This tailored advice helps clients make informed financial decisions and navigate life with confidence.",
    "Whether you're planning for retirement, looking to preserve and pass on your wealth, investing for the future or seeking greater financial certainty, we'll take the time to understand what's important to you and create a plan that reflects your goals.",
    "Realise your financial goals and prepare for life's most important moments.")

NATIONAL = {"component": "lp-text", "headline": "Local advice backed by national strength", "image_position": "none", "background": "white",
            "body": doc("Our team of independent financial advisers in {city} take the time to understand your unique circumstances, goals and aspirations.",
                        "While you'll benefit from a dedicated local adviser, you'll also have access to the expertise and resources of a nationwide network of more than 190 highly qualified financial advisers. Whether you prefer to meet at home or visit our {city} office, we're here in a way that works for you.",
                        "As an Associate Firm of the Personal Finance Society, the UK's leading professional body for financial advisers, we are committed to maintaining the highest standards of professionalism, ethics and client care. Our focus is on building long-term relationships based on trust, understanding and personalised advice.",
                        "We're also supported by the strength and stability of Aviva Group. Combined with our independent approach, this means we're free to recommend solutions from across the whole market, helping you feel confident that your wealth is working towards the future you want for yourself and your family."),
            **cta("Why choose us", "/about")}
OFFICE = {"component": "lp-office", "headline": "Our nearest office to you", "map_type": "interactive",
          "body": doc("As part of your local community, we provide personalised advice designed to support you through life's changing priorities and financial decisions."),
          **cta("Book a free consultation")}
EXPECT = {"component": "lp-image-card", "headline": "What you can expect", "card_position": "right",
          "body": doc("Taking the first step towards independent financial advice doesn't need to be complicated. Your first meeting is a chance to discuss your goals, priorities and any questions you may have. There's no cost, obligation or pressure. We'll take the time to understand your circumstances, answer your questions, explain how we can help, outline next steps and provide a clear explanation of our fees."),
          **cta("Your first meeting", "/contact")}
TESTIMONIAL = {"component": "lp-testimonial", "headline": "Why our clients choose local planners", "link_label": "Read more verified client reviews",
               "link": {"id": "", "url": "https://www.vouchedfor.co.uk", "linktype": "url", "fieldtype": "multilink", "cached_url": "https://www.vouchedfor.co.uk", "target": "_blank"},
               "quote": "[My planner] is a financial adviser that genuinely listens to what your aims and objectives are. His independent professional advice is invaluable. You are able to plan ahead with confidence.",
               "attribution": "Verified client review", **cta("Book a free consultation")}
FEES = {"component": "lp-text", "headline": "Clear and transparent fees", "image_position": "left", "background": "white",
        "body": doc("We believe financial advice should be straightforward and easy to understand. That's why we're open and transparent about our fees from the very beginning.",
                    "Your first meeting with us is at our expense and comes with no obligation. If you decide to move forward, we'll clearly explain our charges, what they cover and the value you can expect to receive at every stage.",
                    "Our goal is to help you make confident financial decisions, with complete clarity over costs, services and the benefits of the advice you receive."),
        **cta("Our fees", "/pricing")}
INDEPENDENT = {"component": "lp-text", "headline": "A truly independent approach", "image_position": "none", "background": "cream",
               "body": doc("As an independent financial advice firm, we're free to recommend solutions from across the whole market, selecting those that best meet your individual circumstances, goals and long-term aspirations.",
                           "We work with clients who have £250,000 or more in pension and investment assets, helping them make informed financial decisions with confidence. Whether you're planning for retirement, preserving wealth for future generations or seeking greater financial certainty, we'll create a personalised plan designed around what's important to you.",
                           h3("Our areas of expertise include:"),
                           ul(["Inheritance, estate and trust planning – helping you preserve and pass on your wealth in line with your wishes",
                               "Savings and investment planning – helping your money work towards your long-term goals",
                               "Pensions and retirement planning – creating a strategy for the retirement lifestyle you want",
                               "Financial protection – helping protect your family, business and financial future",
                               "Mortgages and equity release – supporting major life decisions with tailored borrowing solutions"])),
               **cta("Our full range of services", "/services")}
TRUST = {"component": "lp-trust", "items": [
    {"component": "lp-trust-item", "provider": "Trustpilot", "rating": "Rated Excellent",
     "description": "Rated Excellent on Trustpilot, our clients have reviewed us highly and which parts of our service they praise and would recommend."},
    {"component": "lp-trust-item", "provider": "VouchedFor", "rating": "4.8★",
     "description": "4.8★ rating on VouchedFor, an independent service that lets you find, rate and review financial advisers across the UK."}]}
PLANNERS = {"component": "planner_grid", "title": "Meet your {city} planners", "mode": "by_office", "sort": "pinned_then_az", "limit": "3"}


def asset(key):
    a = api("GET", f"assets/{ASSETS[key]}")
    return {"id": a["id"], "alt": a.get("alt") or "", "name": "", "focus": a.get("focus") or "", "title": a.get("title") or "",
            "source": "", "filename": a["filename"], "copyright": "", "fieldtype": "asset", "meta_data": a.get("meta_data") or {},
            "is_external_url": False}


def lead_form():
    """Re-use the live 'Ready for a conversation?' preset content so the page form matches the rest of the site."""
    lf = comps()["lead_form"]
    presets = [p for p in api("GET", "presets")["presets"] if p["component_id"] == lf["id"]]
    base = next((p for p in presets if p["name"] == "Conversation (Succession)"), presets[0] if presets else None)
    content = dict(api("GET", f"presets/{base['id']}")["preset"]["preset"]) if base else {"component": "lead_form"}
    content.update({"component": "lead_form", "headline": "Ready for a conversation?", "mailchimp_tags": "paid-search, location-lp, {city}"})
    return content


def with_uids(node):
    if isinstance(node, dict):
        out = {k: with_uids(v) for k, v in node.items()}
        if "component" in out:
            out["_uid"] = uid()
        return out
    if isinstance(node, list):
        return [with_uids(v) for v in node]
    return node


def full_body(map_key=None, fees=True):
    office = dict(OFFICE)
    if map_key:
        office.update({"map_type": "image", "map_image": asset(map_key)})
    fees_blk = dict(FEES, image=asset("fees")) if fees else FEES
    return with_uids([NATIONAL, office, PLANNERS, dict(EXPECT, image=asset("first_meeting")), TESTIMONIAL, fees_blk, INDEPENDENT, lead_form(), TRUST])


# ---------------- schemas ----------------
def schemas():
    grp = ensure_group("location page")["uuid"]
    ctaf = [("cta_label", text("Button label", "Optional. Leave empty for no button.")),
            ("cta_link", link("Button link", "Optional. Leave empty to scroll to the form on this page."))]
    bg = ("background", inline_one([("White", "white"), ("Cream", "cream")], "Background", "Section background colour.", default_value="white"))

    upsert_component("lp-text", "Text section", build_schema([
        ("headline", text("Heading", "Section heading." + TOKENS_HELP)),
        ("body", richtext("Text", "Paragraphs, sub-headings and bullet lists." + TOKENS_HELP)),
        ("image", image("Image (optional)", "Shown beside the text. Leave empty for a text-only section.")),
        ("image_position", inline_one([("No image", "none"), ("Image on the left", "left"), ("Image on the right", "right")], "Image position", "Where the image sits next to the text.", default_value="none")),
        bg, *ctaf]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="headline")

    upsert_component("lp-office", "Nearest office", build_schema([
        ("headline", text("Heading", "Section heading.", default_value="Our nearest office to you")),
        ("body", richtext("Text", "Shown under the address. The address comes from the page's Office automatically." + TOKENS_HELP)),
        ("map_type", inline_one([("Interactive map (from the office location)", "interactive"), ("Map image", "image")], "Map", "Interactive needs nothing else. Map image uses the picture below.", default_value="interactive")),
        ("map_image", image("Map image", "Only used when Map is 'Map image'.")),
        *ctaf]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="headline")

    upsert_component("lp-image-card", "Image with card", build_schema([
        ("image", image("Background image", "Full-width photo behind the card.")),
        ("headline", text("Heading", "Card heading." + TOKENS_HELP)),
        ("body", richtext("Text", "Card text." + TOKENS_HELP)),
        ("card_position", inline_one([("Left", "left"), ("Right", "right"), ("Centre", "center")], "Card position", "Where the white card sits on the photo.", default_value="right")),
        *ctaf]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="headline")

    upsert_component("lp-testimonial", "Client testimonial", build_schema([
        ("headline", text("Heading", "Section heading.", default_value="Why our clients choose local planners")),
        ("link_label", text("Reviews link label", "Optional link under the heading.")),
        ("link", link("Reviews link", "Where the reviews link goes, e.g. VouchedFor.")),
        ("quote", textarea("Quote", "The client quote.")),
        ("attribution", text("Attribution", "Who said it, e.g. 'Verified client review'.")),
        *ctaf]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="headline")

    upsert_component("lp-trust-item", "Review rating", build_schema([
        ("provider", text("Provider", "e.g. Trustpilot or VouchedFor.")),
        ("rating", text("Rating", "e.g. 'Rated Excellent' or '4.8★'.")),
        ("description", textarea("Text", "One sentence about the rating.")),
    ]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE, preview_field="provider")

    upsert_component("lp-trust", "Review ratings", build_schema([
        ("items", bloks("Ratings", "Add one rating per review site.", ["lp-trust-item"], maximum=4)),
    ]), is_nestable=True, is_root=False, component_group_uuid=grp, color=BRONZE)

    upsert_component("location-page", "Location landing page", build_schema(tabs(
        ("Hero", [
            ("office", story_one("office", "Office", "The one field that localises the page: city name, phone, address, map and local planners all come from this office. Change it and the whole page moves to that city.")),
            ("headline", text("Headline", "Main headline." + TOKENS_HELP, default_value="Independent financial advice in {city}")),
            ("hero_body", richtext("Intro", "Text in the hero card." + TOKENS_HELP)),
            ("hero_image", image("Hero image", "City photo behind the hero card. Recommended 2000 x 1000px.")),
            ("tracking_phone", text("Campaign tracking phone (optional)", "Call-tracking number for this campaign, e.g. 0113 417 0957. Leave empty to show the office phone.")),
            ("cta_label", text("Button label", "Hero button text.", default_value="Book a free consultation")),
            ("cta_link", link("Button link", "Optional. Leave empty to scroll to the form on this page.")),
        ]),
        ("Page sections", [
            ("body", bloks("Page sections", "The sections below the hero. Only location-page blocks are available, so every city page stays on-brand.", SECTION_BLOCKS)),
        ]),
        ("Compliance & tracking", [
            ("compliance_code", text("Financial promotion reference", "Compliance approval code shown at the bottom of the page, e.g. MK26-665.")),
            ("utm_campaign", text("Campaign name for tracking", "Added to form submissions, e.g. 'mk26-665-leeds'.")),
            ("hide_navigation", boolean("Hide site navigation", "Paid-search pages usually hide the menu so visitors stay on the page and the form.", default_value=True)),
            ("seo", seo_field()),
        ]),
    )), is_root=True, is_nestable=False, color=NAVY, preview_field="headline")
    presets()


def presets():
    existing = {(p["name"], p["component_id"]): p for p in api("GET", "presets")["presets"]}

    def put(cname, pname, content, default=False):
        cid = comps()[cname]["id"]
        body = {"name": pname, "component_id": cid, "preset": with_uids(content)}
        ex = existing.get((pname, cid))
        p = api("PUT", f"presets/{ex['id']}", {"preset": body})["preset"] if ex else api("POST", "presets", {"preset": body})["preset"]
        print("preset", cname, "·", pname)
        if default:
            api("PUT", f"components/{cid}", {"component": {"preset_id": p["id"]}})

    put("lp-text", "Local advice backed by national strength", NATIONAL, default=True)
    put("lp-text", "Clear and transparent fees (image left)", dict(FEES, image=asset("fees")))
    put("lp-text", "A truly independent approach (with list)", INDEPENDENT)
    put("lp-office", "Nearest office · interactive map", OFFICE, default=True)
    put("lp-office", "Nearest office · map image", dict(OFFICE, map_type="image"))
    put("lp-image-card", "What you can expect", dict(EXPECT, image=asset("first_meeting")), default=True)
    put("lp-testimonial", "Why our clients choose local planners", TESTIMONIAL, default=True)
    put("lp-trust", "Trustpilot + VouchedFor", TRUST, default=True)
    put("location-page", "Location landing page (full)", {
        "component": "location-page", "headline": "Independent financial advice in {city}", "hero_body": HERO_BODY,
        "cta_label": "Book a free consultation", "hide_navigation": True, "body": full_body()}, default=True)


# ---------------- content ----------------
def content():
    offices = {s["slug"]: s["uuid"] for s in api("GET", "stories?starts_with=offices/&per_page=50&story_only=1")["stories"]}
    folder = api("GET", "stories?with_slug=locations&folder_only=1")["stories"]
    if folder:
        fid = folder[0]["id"]
    else:
        fid = api("POST", "stories", {"story": {"name": "Location landing pages", "slug": "locations", "is_folder": True, "default_root": "location-page"}})["story"]["id"]
        print("created folder locations/")
    pages = [("leeds", "Financial advice Leeds", "0113 417 0957", "leeds_hero", "leeds_map"),
             ("bristol", "Financial advice Bristol", "", "bristol_hero", "bristol_map")]
    for city, name, phone, hero, mp in pages:
        slug = f"financial-advice-{city}"
        c = {"component": "location-page", "office": offices[city], "headline": "Independent financial advice in {city}",
             "hero_body": HERO_BODY, "hero_image": asset(hero), "tracking_phone": phone, "cta_label": "Book a free consultation",
             "body": full_body(mp), "compliance_code": "MK26-665", "utm_campaign": f"mk26-665-{city}", "hide_navigation": True,
             "seo": with_uids([{"component": "seo_meta", "title": f"Financial Adviser {city.title()} | IFA {city.title()} | Independent Financial Advice",
                                "description": f"Independent, whole-of-market financial advice in {city.title()} for individuals with £250,000 or more in pensions and investments. Book a free consultation.",
                                "noindex": False}])}
        ex = api("GET", f"stories?with_slug=locations/{slug}")["stories"]
        if ex:
            full = api("GET", f"stories/{ex[0]['id']}")["story"]
            if full.get("unpublished_changes"):
                print("  ! draft in progress on", slug, "- skipped"); continue
            full["content"] = c
            api("PUT", f"stories/{full['id']}", {"story": full, "publish": 1})
            print("updated", full["full_slug"])
        else:
            s = api("POST", "stories", {"story": {"name": name, "slug": slug, "parent_id": fid, "content": c}, "publish": 1})["story"]
            print("created", s["full_slug"])


if __name__ == "__main__":
    {"schemas": schemas, "content": content}[sys.argv[1]]()
