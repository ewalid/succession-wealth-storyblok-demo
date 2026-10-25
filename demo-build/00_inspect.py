from sb import *
for c in list_all("components", "components"):
    print("COMP", c["id"], c["name"], "root" if c.get("is_root") else "", "nest" if c.get("is_nestable") else "", len(c.get("schema", {})))
print("DS", [(d["id"], d["slug"]) for d in api("GET", "datasources")["datasources"]])
for s in list_all("stories", "stories", extra="&story_only=false"):
    print("STORY", s["id"], s["full_slug"], "folder" if s["is_folder"] else "", s.get("content_type") or "", "pub" if s["published"] else "draft")
print("PRESETS", [(p["id"], p["name"], p["component_id"]) for p in api("GET", "presets")["presets"]])
print("GROUPS", [(g["id"], g["name"]) for g in api("GET", "component_groups")["component_groups"]])
