import time
import requests

def check_cve(name, version, ecosystem="PyPI"):
    if version is None:
        return "UNVERIFIED"
    url = "https://api.osv.dev/v1/query"
    payload = {
        "version": version,
        "package": {"name": name, "ecosystem": ecosystem}
    }
    try:
        r = requests.post(url, json=payload, timeout=5)
        vulns = r.json().get("vulns", [])
        time.sleep(0.3)
        return [{"id": v["id"], "summary": v.get("summary", "")} for v in vulns]
    except requests.RequestException:
        return "ERROR"
