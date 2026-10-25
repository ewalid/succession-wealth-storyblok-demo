"""Idempotent seed: folders, 6 offices, 15 real planners (public data from successionwealth.co.uk),
topic page, 2 articles, event, video page, Bristol + Leeds campaign pages.
Public source data was scraped once into data/planner_profiles.json (name, title, photo URL, bio, certs, contact)."""
import io, json, mimetypes, os, re, urllib.request, uuid, urllib.parse
from sb import *

HERE = os.path.dirname(os.path.abspath(__file__))
PROFILES = json.load(open(os.path.join(HERE, "data", "planner_profiles.json")))


def U(): return str(uuid.uuid4())
def rt(*paras):
    return {"type": "doc", "content": [{"type": "paragraph", "content": [{"type": "text", "text": p}]} for p in paras if p]}
def url_link(u):
    return {"fieldtype": "multilink", "linktype": "url", "url": u, "cached_url": u, "target": "_blank"} if u else {"fieldtype": "multilink", "linktype": "url", "url": "", "cached_url": ""}
def block(component, **kw): return {"_uid": U(), "component": component, **kw}

# ---------------- stories helpers ----------------
def find_story(full_slug):
    d = api("GET", f"stories?with_slug={urllib.parse.quote(full_slug)}")
    s = d.get("stories", [])
    return s[0] if s else None

FOLDERS = {}
def ensure_folder(slug, name, default_root=None):
    ex = find_story(slug)
    if ex:
        FOLDERS[slug] = ex["id"]; print("folder exists", slug, ex["id"]); return ex["id"]
    body = {"name": name, "slug": slug, "is_folder": True}
    if default_root: body["default_root"] = default_root
    s = api("POST", "stories", {"story": body})["story"]
    FOLDERS[slug] = s["id"]; print("folder created", slug, s["id"]); return s["id"]

def upsert_story(folder, slug, name, content, publish=True):
    full = f"{folder}/{slug}"
    ex = find_story(full)
    body = {"name": name, "slug": slug, "content": content}
    if ex:
        # keep existing _uid so the Visual Editor does not lose its place
        content["_uid"] = (api("GET", f"stories/{ex['id']}")["story"]["content"] or {}).get("_uid", U())
        s = api("PUT", f"stories/{ex['id']}", {"story": body, "publish": 1 if publish else 0})["story"]
        print(("updated " if publish else "updated(draft) ") + full, s["id"])
    else:
        content["_uid"] = U()
        body["parent_id"] = FOLDERS[folder]
        s = api("POST", "stories", {"story": body, "publish": 1 if publish else 0})["story"]
        print(("created+published " if publish else "created(draft) ") + full, s["id"])
    return s

# ---------------- assets ----------------
def get_or_upload_asset(slug, src_url):
    from PIL import Image
    d = api("GET", f"assets?search={slug}&per_page=25")
    for a in d.get("assets", []):
        if f"/{slug}." in a["filename"] or a["filename"].rsplit("/", 1)[-1].startswith(slug + "."):
            return a
    req = urllib.request.Request(src_url, headers={"User-Agent": "Mozilla/5.0"})
    raw = urllib.request.urlopen(req).read()
    im = Image.open(io.BytesIO(raw)); w, h = im.size
    ext = {"PNG": "png", "JPEG": "jpg", "WEBP": "webp"}.get(im.format, "png")
    fname = f"{slug}.{ext}"
    a = api("POST", "assets", {"filename": fname, "size": f"{w}x{h}", "validate_upload": 1})
    boundary = "----sb" + uuid.uuid4().hex
    buf = io.BytesIO()
    for k, v in a["fields"].items():
        buf.write(f'--{boundary}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode())
    ctype = mimetypes.guess_type(fname)[0] or "application/octet-stream"
    buf.write(f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{fname}"\r\nContent-Type: {ctype}\r\n\r\n'.encode())
    buf.write(raw); buf.write(f"\r\n--{boundary}--\r\n".encode())
    r = urllib.request.Request(a["post_url"], data=buf.getvalue(), headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}, method="POST")
    urllib.request.urlopen(r).read()
    api("GET", f"assets/{a['id']}/finish_upload")
    print("  uploaded asset", fname, a["id"])
    return api("GET", f"assets/{a['id']}")

def asset_value(a, alt):
    return {"id": a["id"], "alt": alt, "name": "", "focus": "", "title": alt, "source": "", "filename": a["filename"], "copyright": "", "fieldtype": "asset", "meta_data": {"alt": alt, "title": alt}, "is_external_url": False}

# ---------------- data ----------------
OFFICES = {  # real addresses/phones from successionwealth.co.uk/contact-us; lat/lng approximate
    "leeds": dict(name="Leeds", address="The Pinnacle\n67 Albion Street\nLeeds", postcode="LS1 5AA", lat="53.7985", lng="-1.5444", phone="0113 390 8010"),
    "bristol": dict(name="Bristol", address="Whitefriars\nLewins Mead\nBristol", postcode="BS1 2NT", lat="51.4587", lng="-2.5961", phone="0117 927 6026"),
    "london": dict(name="London", address="1 Carey Lane\nLondon", postcode="EC2V 8AE", lat="51.5155", lng="-0.0951", phone="0203 696 6800"),
    "edinburgh": dict(name="Edinburgh", address="132 Calton Road\nEdinburgh", postcode="EH8 8JQ", lat="55.9525", lng="-3.1724", phone="0131 557 0777"),
    "birmingham": dict(name="Birmingham", address="60 Church Street\nBirmingham", postcode="B3 2DJ", lat="52.4829", lng="-1.8985", phone="0121 212 9212"),
    "belfast": dict(name="Belfast", address="Avenue House, 1st Floor\n42-44 Rosemary Street\nBelfast", postcode="BT1 1QE", lat="54.6021", lng="-5.9282", phone="028 9023 0696"),
}
OFFICE_INTRO = {
    "leeds": "Our Leeds office is in The Pinnacle on Albion Street, in the centre of the city. Our local wealth planners help clients across Leeds and the surrounding area, and can meet you in the office, at home or online.",
    "bristol": "Our Bristol office is at Whitefriars on Lewins Mead, close to the city centre. Our local wealth planners can meet you in the office, at home or online.",
    "london": "Our London office is at 1 Carey Lane in the City of London. Our London wealth planners can meet you in the office or online.",
    "edinburgh": "Our Edinburgh office is on Calton Road, a short walk from Waverley station. Our Scottish wealth planners can meet you in the office, at home or online.",
    "birmingham": "Our Birmingham office, on Church Street, is home to our head office and a team of local wealth planners. They can meet you in the office, at home or online.",
    "belfast": "Our Belfast office is on the first floor of Avenue House on Rosemary Street. Our Northern Ireland wealth planners can meet you in the office, at home or online.",
}

# slug -> (office, specialisms, qualifications, meeting prefs, radius). Specialisms are drawn from each planner's public bio
# where it names them; the rest, plus meeting preferences and radius, are DEMO-ASSIGNED (not published by the firm).
PLAN = {
    "james-tollefson": ("leeds", ["retirement-planning", "inheritance-tax", "investments"], ["chartered-financial-planner", "fpfs"], ["home", "office", "digital"], 25),
    "jon-noake": ("leeds", ["trusts-estate-planning", "inheritance-tax", "later-life-planning"], ["chartered-financial-planner", "apfs"], ["office", "digital"], 15),
    "katy-calvert": ("leeds", ["retirement-planning", "pensions"], ["apfs"], ["home", "office", "digital"], 30),
    "denica-arthur": ("bristol", ["retirement-planning", "investments"], ["cii-diploma"], ["home", "office", "digital"], 20),
    "paul-mcmullan": ("bristol", ["mortgages-protection", "investments"], ["cii-diploma", "cemap"], ["home", "office"], 12),
    "jin-hira": ("bristol", ["investments", "mortgages-protection", "employee-benefits"], ["cii-diploma", "cemap"], ["office", "digital"], 10),
    "hugo-clay": ("london", ["retirement-planning", "investments"], ["chartered-financial-planner", "fpfs", "apfs"], ["office", "digital"], 10),
    "bhavisha-soni": ("london", ["retirement-planning", "inheritance-tax", "trusts-estate-planning"], ["chartered-financial-planner", "apfs", "cii-diploma"], ["home", "office", "digital"], 20),
    "alison-james": ("edinburgh", ["retirement-planning", "inheritance-tax"], ["fpfs"], ["home", "office", "digital"], 25),
    "malcolm-reid": ("edinburgh", ["retirement-planning", "pensions", "investments"], ["chartered-financial-planner", "apfs"], ["office", "digital"], 15),
    "louis-murray": ("edinburgh", ["investments", "sports-professionals"], ["cii-diploma"], ["home", "digital"], 35),
    "sean-rebbetts": ("birmingham", ["pensions", "retirement-planning"], ["chartered-financial-planner"], ["office", "digital"], 18),
    "tim-bartley": ("birmingham", ["business-owners", "retirement-planning", "employee-benefits"], ["chartered-financial-planner", "fpfs"], ["home", "office", "digital"], 30),
    "andrew-mccoll": ("belfast", ["retirement-planning", "investments", "later-life-planning"], ["chartered-financial-planner", "apfs"], ["home", "office"], 20),
    "colin-watson": ("belfast", ["business-owners", "investments", "trusts-estate-planning"], ["apfs", "chartered-wealth-manager"], ["home", "office", "digital"], 40),
}


def short(p):
    s = re.sub(r"\s+", " ", p).strip()
    if len(s) <= 200: return s
    sents = re.split(r"(?<=[.!?])\s+", s)
    out = sents[0]
    if len(out) > 220:
        out = out[:200].rsplit(" ", 1)[0] + "…"
    elif len(sents) > 1 and len(out) + len(sents[1]) < 200:
        out += " " + sents[1]
    return out


def main():
    # ----- folders -----
    for slug, name, root in [("offices", "Offices", "office"), ("planners", "Planners", "planner"), ("campaigns", "Campaigns", "campaign-page"),
                              ("topics", "Topics", "default-page"), ("events", "Events", "event"), ("videos", "Videos", "video_page")]:
        ensure_folder(slug, name, root)
    FOLDERS["articles"] = find_story("articles")["id"]

    # ----- offices -----
    office = {}
    for slug, o in OFFICES.items():
        content = {"component": "office", "name": o["name"], "intro": rt(OFFICE_INTRO[slug]), "address": o["address"], "postcode": o["postcode"],
                   "lat": o["lat"], "lng": o["lng"], "phone": o["phone"], "map_style": "brand", "pinned_planners": [], "body": [], "seo": []}
        office[slug] = upsert_story("offices", slug, o["name"], content)

    # ----- planners -----
    planner = {}
    for slug, (off, specs, quals, prefs, radius) in PLAN.items():
        p = PROFILES[slug]
        first, last = p["name"].split(" ", 1)
        asset = get_or_upload_asset(f"planner-{slug}", p["img"])
        paras = [x for chunk in p["bio"] for x in chunk.split("\n\n") if x.strip()]
        paras = [x.strip().strip('"') if x.strip().startswith('"') else x.strip() for x in paras]
        content = {"component": "planner", "first_name": first, "last_name": last, "photo": asset_value(asset, p["name"]), "job_title": p["title"],
                   "qualifications": quals, "specialisms": specs, "office": office[off]["uuid"], "meeting_preferences": prefs,
                   "home_visit_radius_miles": str(radius), "phone": p["tel"], "email": p["email"],
                   "fca_register_url": url_link(p["fca"]), "short_bio": short(paras[0]) if paras else "", "bio": rt(*paras),
                   "active": True, "seo": []}
        planner[slug] = upsert_story("planners", slug, p["name"], content)

    # pin one planner on Bristol (Leeds left empty for the live "pin" demo moment)
    b = office["bristol"]; bc = api("GET", f"stories/{b['id']}")["story"]["content"]
    bc["pinned_planners"] = [planner["denica-arthur"]["uuid"]]
    api("PUT", f"stories/{b['id']}", {"story": {"content": bc}, "publish": 1}); print("pinned Denica Arthur on offices/bristol")

    # ----- topic page -----
    iht = "inheritance-tax"
    topic_body = [
        block("hero-section-simple", eyebrow="Planning", headline="Inheritance tax planning", layout="stacked", text_alignment="left", buttons=[], image=None,
              text="Careful planning can help you pass more of your wealth to the people you care about. Talk to a planner who specialises in it.",
              background_color="white", secondary_background_color="primary-background", preserve_image_aspect_ratio=True, image_decoration=False),
        block("text-section", eyebrow="", headline=[block("headline-segment", text="Why plan for inheritance tax?", highlight="")], text_alignment="left", buttons=[], background_color="white",
              text=rt("Inheritance tax can reduce what you leave behind if it is not considered early. Our planners look at your whole picture, including pensions, property, trusts and gifting, so that your wishes are met.",
                      "Tax treatment depends on your individual circumstances and may change in future. This page is for general information and is not advice.")),
        block("planner_grid", title="Planners who specialise in inheritance tax planning", mode="by_specialism", specialism=iht, sort="az", limit="3", planners=[], office=""),
        block("planner_finder", title="Find the right planner for you", intro="Enter your postcode to find a planner near you.", preset_specialism=iht, default_preference="", max_results="3"),
    ]
    upsert_story("topics", "inheritance-tax-planning", "Inheritance tax planning",
                 {"component": "default-page", "meta_title": "Inheritance tax planning | Succession Wealth",
                  "meta_description": "Speak to a Succession Wealth planner who specialises in inheritance tax planning.", "body": topic_body})

    # ----- articles (author -> planner) -----
    sample = api("GET", "stories/234213853633293")["story"]["content"]
    def article(slug, name, author, specs, paras):
        c = {"component": "article-page", "headline": name, "image": sample.get("image") or {}, "text": rt(*paras), "categories": [], "call_to_action": [],
             "meta_title": name, "meta_description": paras[0][:155], "author": planner[author]["uuid"], "specialisms": specs}
        return upsert_story("articles", slug, name, c)
    article("inheritance-tax-planning-five-questions", "Inheritance tax planning: five questions to ask early", "alison-james", ["inheritance-tax", "retirement-planning"],
            ["Inheritance tax is easier to plan for when you start early. These are the questions we suggest every family asks.",
             "What is my estate worth today, including property and pensions? Who do I want to benefit, and when? Are my wills and any trusts up to date? Could gifting during my lifetime help? Who will act as my executors?",
             "Illustrative demo article. Tax treatment depends on individual circumstances and may change. This is not advice."])
    article("retirement-income-before-you-stop-work", "Retirement income: what to think about before you stop work", "katy-calvert", ["retirement-planning", "pensions"],
            ["The few years before retirement are a good time to turn a pot of savings into a plan for income.",
             "Consider your essential spending, which pensions you hold and when you can take them, and how long your money needs to last. A cashflow forecast can show how different choices play out.",
             "Illustrative demo article. The value of investments can fall as well as rise. This is not advice."])

    # ----- event (hosts -> planners) -----
    upsert_story("events", "retirement-income-evening-leeds", "Retirement income evening, Leeds",
                 {"component": "event", "title": "Retirement income evening, Leeds", "start": "2026-11-19 18:30", "end": "2026-11-19 20:00",
                  "location": "Leeds office, The Pinnacle, 67 Albion Street", "booking_url": url_link(""),
                  "description": rt("An informal evening on turning your savings into a retirement income, with time for questions. Illustrative demo event."),
                  "hosts": [planner["katy-calvert"]["uuid"], planner["james-tollefson"]["uuid"]], "specialisms": ["retirement-planning", "pensions"], "seo": []})

    # ----- video page (featured_planners -> planners) -----
    upsert_story("videos", "inheritance-tax-explained", "Inheritance tax explained",
                 {"component": "video_page", "title": "Inheritance tax explained",
                  "description": rt("A short introduction to inheritance tax planning. Illustrative demo video page: add a video in the editor."),
                  "featured_planners": [planner["alison-james"]["uuid"]], "specialisms": ["inheritance-tax"], "seo": []})

    # ----- campaign pages (Bristol published, Leeds left as DRAFT for the Save vs Publish beat) -----
    def campaign(off_slug, publish):
        o = OFFICES[off_slug]
        body = [block("planner_grid", title=f"Your {o['name']} planners", mode="by_office", office=office[off_slug]["uuid"], sort="pinned_then_az", limit="3", planners=[], specialism=""),
                block("office_map", office=office[off_slug]["uuid"], planner="", show_directions=True),
                block("lead_form", headline="Ready for a conversation?", intro="There is no pressure and no obligation, just a confidential chat to understand your goals.",
                      form_mode="native", fields=["first_name", "surname", "email", "phone", "postcode"], submit_label="Request a conversation")]
        return upsert_story("campaigns", f"{off_slug}-retirement-planning", f"{o['name']} retirement planning",
                            {"component": "campaign-page", "headline": f"Retirement planning in {o['name']}",
                             "intro": f"Speak to a local {o['name']} wealth planner about your retirement goals.", "office": office[off_slug]["uuid"],
                             "utm_campaign": f"{off_slug}-retirement-planning", "body": body, "seo": []}, publish=publish)
    campaign("bristol", True)
    campaign("leeds", False)

    print("\nOFFICES:", ", ".join(f"offices/{s}" for s in OFFICES))
    print("PLANNERS:", ", ".join(f"planners/{s}" for s in PLAN))


if __name__ == "__main__":
    main()
