from fastapi import FastAPI
import uvicorn
from scraping.naukri import find_candidates_naukri
import json
from scraping.linkedin import find_candidates_linkedin

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.api_route("/get_naukri_candidates", methods=["GET", "POST"])
def get_naukri_candidates():
    filename = "jd.json"
    try:
        with open(filename, "r") as f:
            jd = json.load(f)
    except Exception:
        jd = {}
    candidates = find_candidates_naukri(jd, max_results=20) if jd else []
    return {"candidates": candidates}


@app.api_route("/get_linkedin_candidates", methods=["GET", "POST"])
def get_linkedin_candidates():
    filename = "jd.json"
    try:
        with open(filename, "r") as f:
            jd = json.load(f)
    except Exception:
        jd = {}
    candidates = find_candidates_linkedin(jd, max_results=20) if jd else []
    return {"candidates": candidates}


@app.api_route("/post_on_naukri", methods=["GET", "POST"])
def post_on_naukri():
    return {"message": "Posted on Naukri successfully"}


@app.api_route("/post_on_zoho", methods=["GET", "POST"])
def post_on_zoho():
    return {"message": "Posted on Zoho Recruit successfully"}


@app.api_route("/search_candidates_ats", methods=["GET", "POST"])
def post_on_ats_search():
    return {"message": "Posted on ATS Search successfully"}


@app.api_route("/post_on_hiring_ai", methods=["GET", "POST"])
def post_on_hiring_ai():
    return {"message": "Posted on Hiring AI successfully"}


@app.api_route("/reach_candidates_on_linkedin", methods=["GET", "POST"])
def reach_candidates_on_linkedin():
    return {"message": "Reached on LinkedIn successfully"}


@app.api_route("/get_candidates_from_naukri", methods=["GET", "POST"])
def get_candidates_from_naukri():
    return {"emails": ["harshareddygaddam21@gmail.com", "harshareddygaddam21@gmail.com"]}


@app.api_route("/get_candidates_data", methods=["GET", "POST"])
def get_jd_data():
    cand_file = "candidate.json"
    try:
        with open(cand_file, "r") as f:
            candidate = json.load(f)
    except Exception:
        candidate = {}
    
    jd_file = "jd.json"
    try:
        with open(jd_file, "r") as f:
            jd = json.load(f)
    except Exception:
        jd = {}
    
    return {"candidate": candidate, "jd": jd}



@app.api_route("/get_jd_data", methods=["GET", "POST"])
def get_jb_data():
    cand_file = "candidate.json"
    try:
        with open(cand_file, "r") as f:
            candidate = json.load(f)
    except Exception:
        candidate = {}
    
    jd_file = "jd.json"
    try:
        with open(jd_file, "r") as f:
            jd = json.load(f)
    except Exception:
        jd = {}
    
    return {"candidate": candidate, "jd": jd}

#http://host.docker.internal:8000
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)