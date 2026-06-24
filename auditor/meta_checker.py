import requests
from datetime import datetime, timezone

def get_pypi_metadata(name):
    try:
        r = requests.get(f"https://pypi.org/pypi/{name}/json", timeout=10)
        if r.status_code != 200:
            return {"error": "not_found"}
        data = r.json()
        info = data.get("info", {})

        # Author — try multiple fields
        author = (info.get("author") or
                  info.get("author_email") or
                  info.get("maintainer") or
                  "unknown")

        # Last release date across all versions
        releases = data.get("releases", {})
        dates = []
        for version_files in releases.values():
            for f in version_files:
                upload_time = f.get("upload_time")
                if upload_time:
                    dates.append(datetime.fromisoformat(upload_time))
        last_updated = max(dates).replace(tzinfo=timezone.utc) if dates else None
        days_since_update = (datetime.now(timezone.utc) - last_updated).days if last_updated else None

        # Yanked — check LATEST version only, not all history
        latest_version = info.get("version")
        latest_files = releases.get(latest_version, [])
        yanked = any(f.get("yanked", False) for f in latest_files)

        return {
            "author": author,
            "home_page": info.get("home_page") or info.get("project_url") or "",
            "days_since_update": days_since_update,
            "yanked": yanked
        }
    except requests.RequestException:
        return {"error": "request_failed"}
