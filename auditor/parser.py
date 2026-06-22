def parse_requirements(filepath):
    packages = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            for sep in ["==", ">=", "~=", "<="]:
                if sep in line:
                    name, version = line.split(sep)
                    packages.append({"name": name.strip(), "version": version.strip()})
                    break
            else:
                packages.append({"name": line, "version": None})
    return packages
