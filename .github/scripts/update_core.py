import re
import os

DART_FILE = 'lib/gapp_core.dart'
CHANGELOG_FILE = 'changelog.md'

def main():
    with open(DART_FILE, 'r', encoding='utf-8') as f:
        dart_content = f.read()

    version_match = re.search(r"static const coreVersion = '([\d\.]+)';", dart_content)
    current_version = version_match.group(1)
    version_clean = current_version.replace('.', '')

    regex_pattern = r"(\(\d+\.)(\d{4})(\.\d{2}\))"
    match = re.search(regex_pattern, dart_content)

    current_core_build = int(match.group(2))
    new_core_build = current_core_build + 1
    new_core_str = f"{new_core_build:04d}"

    def replacer(m):
        return f"{m.group(1)}{new_core_str}{m.group(3)}"

    dart_content = re.sub(regex_pattern, replacer, dart_content)

    with open(DART_FILE, 'w', encoding='utf-8') as f:
        f.write(dart_content)
    print(f"Core Build actualizado en Dart: {current_core_build} -> {new_core_build}")

    with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f:
        changelog_content = f.read()

    full_new_issue = f"000{new_core_str}"

    target_span = f'<span style="color:grey">{full_new_issue} |</span>'
    replacement = f'[{full_new_issue}](#{version_clean}-{full_new_issue}) |'

    if target_span in changelog_content:
        changelog_content = changelog_content.replace(target_span, replacement)

    with open(CHANGELOG_FILE, 'w', encoding='utf-8') as f:
        f.write(changelog_content)
    print(f"Changelog actualizado con el issue {full_new_issue}.")

if __name__ == "__main__":
    main()