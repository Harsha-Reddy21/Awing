import os
import json
import sys
import urllib.parse
import urllib.request
from dotenv import load_dotenv

load_dotenv()


def build_query(jd: dict) -> str:
    parts = ['site:linkedin.com/in', f'"{jd.get("jobTitle","")}"']
    skills = jd.get("skillsRequired", [])
    parts += [f'"{s}"' for s in skills]

    loc = jd.get("location", {}) or {}
    loc_terms = [loc.get("city"), loc.get("state"), loc.get("country")]
    loc_terms = [t for t in loc_terms if t]
    if loc_terms:
        parts.append("(" + " OR ".join([f'"{t}"' for t in loc_terms]) + ")")

    exp = jd.get("experienceRequired", {}) or {}
    miny, maxy = exp.get("minYears"), exp.get("maxYears")
    if isinstance(miny, int) and isinstance(maxy, int) and maxy >= miny:
        years = " OR ".join([f'"{y} years"' for y in range(miny, maxy + 1)])
        parts.append("(" + years + ")")

    if "Bachelor" in (jd.get("education") or ""):
        parts.append('("Bachelor" OR "B.E" OR "BTech" OR "B.Sc" OR "BS")')

    # Reduce job postings/recruiter noise
    parts += ["-jobs", "-job", "-hiring", "-recruiter", "-recruitment", "-careers"]
    return " ".join([p for p in parts if p.strip()])


def _serpapi_search(query: str, num: int = 20) -> dict:
    api_key = os.getenv("SERP_API_KEY")
    if not api_key:
        raise ValueError("SERP_API_KEY missing. Add it to your .env")

    params = {
        "engine": "google",
        "q": query,
        "hl": "en",
        "num": min(max(num, 1), 100),
        "api_key": api_key,
    }
    url = "https://serpapi.com/search.json?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _parse_candidates(serp: dict) -> list:
    results = serp.get("organic_results") or []
    out = []
    for r in results:
        title = r.get("title") or ""
        link = r.get("link")
        snippet = r.get("snippet") or ""
        name = title.split(" - ")[0].split(" | ")[0].strip()
        if link and "linkedin.com/in" in link:
            out.append({
                "name": name,
                "title": title,
                "profile_url": link,
                "summary": snippet,
            })
    return out


def find_candidates(job_description: dict, max_results: int = 20) -> list:
    q = build_query(job_description)
    serp = _serpapi_search(q, num=max_results)
    return _parse_candidates(serp)


if __name__ == "__main__":
    # Usage: echo '<JD JSON>' | python scraping/linkedin.py
    filename = "jd.json"
    try:
        with open(filename, "r") as f:
            jd = json.load(f)
    except Exception:
        jd = {}
    candidates = find_candidates(jd, max_results=20) if jd else []
    print(json.dumps({
        "query": build_query(jd) if jd else "",
        "candidates": candidates
    }, ensure_ascii=False, indent=2))