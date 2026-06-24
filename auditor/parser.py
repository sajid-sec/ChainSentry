import re

def parse_requirements(filepath):
    packages = []
    with open(filepath) as f:
        for line in f:
            line = line.strip()

            if not line or line.startswith("#"):
                continue
            if line.startswith("-"):
                continue
            if not re.match(r'^[A-Za-z0-9]', line):
                continue

            found = False
            # Check >= ~= <= BEFORE == to avoid matching == inside markers
            for sep in [">=", "~=", "<=", "=="]:
                if sep in line:
                    name, rest = line.split(sep, 1)
                    version = rest.split(";")[0].split(",")[0].strip()
                    packages.append({"name": name.strip(), "version": version})
                    found = True
                    break

            if not found:
                clean = line.split(";")[0].strip()
                if re.match(r'^[A-Za-z0-9][A-Za-z0-9._-]*$', clean):
                    packages.append({"name": clean, "version": None})

    return packages
