def calculate_risk(cve_results, typo_result, meta_result):
    # Typosquatting always overrides to HIGH — most dangerous signal
    if typo_result:
        return "HIGH"

    # Any confirmed CVEs → HIGH
    if isinstance(cve_results, list) and cve_results:
        return "HIGH"

    # Yanked latest version → HIGH
    if meta_result.get("yanked"):
        return "HIGH"

    # Abandoned (>4 years) → MEDIUM
    days = meta_result.get("days_since_update")
    if days is not None and days > 1460:  # 4 years
        return "MEDIUM"

    # Stale (>2 years) → MEDIUM
    if days is not None and days > 730:   # 2 years
        return "MEDIUM"

    # Unverified version (no pin) → MEDIUM
    if cve_results == "UNVERIFIED":
        return "MEDIUM"

    return "LOW"
