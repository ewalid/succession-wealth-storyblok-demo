"""Read-only check through the Content Delivery API, using the repo's STORYBLOK_TOKEN (never printed)."""
import json, re, urllib.request, urllib.parse
from sb import *
env = open("../.env").read()
tok = re.search(r'^STORYBLOK_TOKEN="?([^"\n]+)', env, re.M).group(1)
def cdn(q, ver="published"):
    return json.load(urllib.request.urlopen(f"https://api.storyblok.com/v2/cdn/stories?{q}&version={ver}&token={tok}"))
def uid(slug): return cdn(f"by_slugs={slug}")["stories"][0]["uuid"]
leeds = uid("offices/leeds")
d = cdn(f"content_type=planner&filter_query[office][in]={leeds}&filter_query[active][is]=true&resolve_relations=planner.office")
print("Leeds planners:", [s["name"] for s in d["stories"]], "| office resolved:", d["stories"][0]["content"]["office"]["name"] if isinstance(d["stories"][0]["content"]["office"], dict) else "NO (uuid only)", "| rels:", len(d["rels"]))
print("IHT specialists:", [s["name"] for s in cdn("content_type=planner&filter_query[specialisms][any_in_array]=inheritance-tax")["stories"]])
print("Leeds + pensions:", [s["name"] for s in cdn(f"content_type=planner&filter_query[specialisms][any_in_array]=pensions&filter_query[office][in]={leeds}")["stories"]])
a = cdn("by_slugs=articles/inheritance-tax-planning-five-questions&resolve_relations=article-page.author")["stories"][0]
print("Article author:", a["content"]["author"]["name"] if isinstance(a["content"]["author"], dict) else a["content"]["author"])
print("Published campaigns:", [s["full_slug"] for s in cdn("starts_with=campaigns/")["stories"]], "| draft:", [s["full_slug"] for s in cdn("starts_with=campaigns/", "draft")["stories"]])
print("Redirects untouched:", [s["full_slug"] for s in cdn("starts_with=redirects/", "draft")["stories"]])
