import time
import requests

def check_cve(name, version, ecosystem="PyPI", retries=2):
    if version is None:
        return "UNVERIFIED"
    url = "https://api.osv.dev/v1/query"
    payload = {
        "version": version,
        "package": {"name": name, "ecosystem": ecosystem}
    }
    for attempt in range(retries):
        try:
            r = requests.post(url, json=payload, timeout=10)
            vulns = r.json().get("vulns", [])
            time.sleep(0.3)
            return [{"id": v["id"], "summary": v.get("summary", "")} for v in vulns]
        except requests.RequestException:
            if attempt < retries - 1:
                time.sleep(2)
            continue
    return "ERROR"
