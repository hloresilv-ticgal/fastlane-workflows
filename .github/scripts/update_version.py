import re
import os

DART_FILE = 'lib/gapp_version.dart'
CHANGELOG_FILE = 'changelog.md'

def main():
    # 1. LEER EL ARCHIVO DART
    with open(DART_FILE, 'r', encoding='utf-8') as f:
        dart_content = f.read()

    # Buscar la versión (ej. '2.8.4')
    version_match = re.search(r"static const version = '([\d\.]+)';", dart_content)
    if not version_match:
        print("No se encontró la versión en el archivo dart.")
        return
    current_version = version_match.group(1)
    version_clean = current_version.replace('.', '') # '2.8.4' -> '284'

    # Buscar el build (ej. '(2.0673.00)')
    build_match = re.search(r"static const build = '\(2\.(\d{4})\.00\)';", dart_content)
    if not build_match:
        print("No se encontró el build en el archivo dart.")
        return
    current_build_num = int(build_match.group(1))

    # Incrementar el build
    new_build_num = current_build_num + 1
    new_build_str = f"{new_build_num:04d}" # Convierte 674 -> 0674
    full_new_issue = f"0000{new_build_str[-3:]}" # Asegura formato 0000674

    # Actualizar contenido dart
    new_build_text = f"static const build = '(2.{new_build_str}.00)';"
    dart_content = dart_content.replace(build_match.group(0), new_build_text)

    with open(DART_FILE, 'w', encoding='utf-8') as f:
        f.write(dart_content)
    print(f"Dart actualizado: Build {current_build_num} -> {new_build_num}")

    # 2. ACTUALIZAR EL CHANGELOG
    with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f:
        changelog_content = f.read()

    # Vamos a buscar el span gris del NUEVO número y reemplazarlo por el enlace
    # Patrón a buscar: <span style="color:grey">0000675 |</span> (o sin el pipe al final)
    # Reemplazo: [0000675](#284-0000675) |

    target_span = f'<span style="color:grey">{full_new_issue} |</span>'
    target_span_end = f'<span style="color:grey">{full_new_issue} </span>'

    replacement = f'[{full_new_issue}](#{version_clean}-{full_new_issue}) |'
    replacement_end = f'[{full_new_issue}](#{version_clean}-{full_new_issue}) '

    if target_span in changelog_content:
        changelog_content = changelog_content.replace(target_span, replacement)
    elif target_span_end in changelog_content:
        changelog_content = changelog_content.replace(target_span_end, replacement_end)
    else:
        print(f"ADVERTENCIA: No se encontró el espacio para {full_new_issue} en el Changelog. Revisa si necesitas añadir más líneas grises.")

    with open(CHANGELOG_FILE, 'w', encoding='utf-8') as f:
        f.write(changelog_content)
    print(f"Changelog actualizado con la issue {full_new_issue}.")

if __name__ == "__main__":
    main()