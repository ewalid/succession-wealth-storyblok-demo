"""Idempotent: create/update datasources + entries (specialisms, meeting-preferences, qualifications)."""
from sb import *

DATASOURCES = {
    "specialisms": ("Specialisms", [
        ("Retirement planning", "retirement-planning"),
        ("Inheritance tax planning", "inheritance-tax"),   # value matches planner-spec API example
        ("Pensions", "pensions"),
        ("Investments", "investments"),
        ("Later life planning", "later-life-planning"),
        ("Equity release", "equity-release"),
        ("Mortgages & protection", "mortgages-protection"),
        ("Business owners", "business-owners"),
        ("Divorce", "divorce"),
        ("Trusts & estate planning", "trusts-estate-planning"),
        ("Employee benefits", "employee-benefits"),
        ("Sports professionals", "sports-professionals"),
    ]),
    "meeting-preferences": ("Meeting preferences", [
        ("Home visit", "home"),
        ("Office", "office"),
        ("Digital (video or phone)", "digital"),
    ]),
    "qualifications": ("Qualifications", [
        ("Chartered Financial Planner", "chartered-financial-planner"),
        ("Certified Financial Planner (CFP)", "certified-financial-planner"),
        ("FPFS", "fpfs"),
        ("APFS", "apfs"),
        ("Chartered Wealth Manager", "chartered-wealth-manager"),
        ("CII Diploma", "cii-diploma"),
        ("CeMAP", "cemap"),
    ]),
}


def main():
    existing = {d["slug"]: d for d in api("GET", "datasources")["datasources"]}
    for slug, (name, entries) in DATASOURCES.items():
        if slug in existing:
            ds = existing[slug]
            print("exists", slug, ds["id"])
        else:
            ds = api("POST", "datasources", {"datasource": {"name": name, "slug": slug}})["datasource"]
            print("created", slug, ds["id"])
        have = {e["value"]: e for e in list_all(f"datasource_entries?datasource_id={ds['id']}", "datasource_entries")}
        for n, v in entries:
            if v in have:
                if have[v]["name"] != n:
                    api("PUT", f"datasource_entries/{have[v]['id']}", {"datasource_entry": {"name": n, "value": v, "datasource_id": ds["id"]}})
                    print("  updated", v)
            else:
                api("POST", "datasource_entries", {"datasource_entry": {"name": n, "value": v, "datasource_id": ds["id"]}})
                print("  +", v)


if __name__ == "__main__":
    main()
