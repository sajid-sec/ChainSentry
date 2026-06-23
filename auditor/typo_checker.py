import Levenshtein

def load_known_packages(filepath="data/known_packages.txt"):
    with open(filepath) as f:
        return [line.strip().lower() for line in f if line.strip()]

def check_typosquatting(name, known_packages, threshold=2):
    if len(name) < 4:
        return None
    name_lower = name.lower()
    for known in known_packages:
        if known == name_lower:
            return None  # exact match = legitimate
        dist = Levenshtein.distance(name_lower, known)
        if dist <= threshold:
            return {"similar_to": known, "distance": dist}
    return None
