import re
import os

DART_FILE = 'lib/gapp_core.dart'
CHANGELOG_FILE = 'changelog.md'

def main():
    # 1. ACTUALIZAR GAPP_CORE.DART
    with open(DART_FILE, 'r', encoding='utf-8') as f:
        dart_content = f.read()

    # Buscar la versión semántica (Ej: 2.8.4)
    version_match = re.search(r"static const coreVersion = '([\d\.]+)';", dart_content)
    if not version_match:
        print("No se encontró 'coreVersion' en gapp_core.dart")
        return
    current_version = version_match.group(1)
    version_clean = current_version.replace('.', '') # '2.8.4' -> '284'

    # Expresión regular para encontrar la estructura (X.YYYY.ZZ) en android y apple
    # Grupo 1: prefijo (ej. '(2.')
    # Grupo 2: Core Build (ej. '0673')
    # Grupo 3: sufijo / flavor (ej. '.02)')
    regex_pattern = r"(\(\d+\.)(\d{4})(\.\d{2}\))"

    # Buscamos el core actual basándonos en la primera coincidencia (asumimos que android y apple tienen el mismo core)
    match = re.search(regex_pattern, dart_content)
    if not match:
        print("No se encontró el formato (X.YYYY.ZZ) en el archivo dart.")
        return

    current_core_build = int(match.group(2))
    new_core_build = current_core_build + 1
    new_core_str = f"{new_core_build:04d}" # Convierte 674 en '0674'

    # Función para reemplazar solo el bloque central YYYY en todas las coincidencias
    def replacer(m):
        return f"{m.group(1)}{new_core_str}{m.group(3)}"

    dart_content = re.sub(regex_pattern, replacer, dart_content)

    with open(DART_FILE, 'w', encoding='utf-8') as f:
        f.write(dart_content)
    print(f"Core Build actualizado en Dart: {current_core_build} -> {new_core_build}")

    # 2. ACTUALIZAR CHANGELOG.MD
    with open(CHANGELOG_FILE, 'r', encoding='utf-8') as f:
        changelog_content = f.read()

    # Formateamos para que tenga 7 dígitos igual que en tu changelog: '0000674'
    # Como new_core_str tiene 4 (ej '0674'), le añadimos '000' delante
    full_new_issue = f"000{new_core_str}"

    target_span = f'<span style="color:grey">{full_new_issue} |</span>'
    target_span_end = f'<span style="color:grey">{full_new_issue} </span>'

    replacement = f'[{full_new_issue}](#{version_clean}-{full_new_issue}) |'
    replacement_end = f'[{full_new_issue}](#{version_clean}-{full_new_issue}) '

    if target_span in changelog_content:
        changelog_content = changelog_content.replace(target_span, replacement)
    elif target_span_end in changelog_content:
        changelog_content = changelog_content.replace(target_span_end, replacement_end)
    else:
        print(f"ADVERTENCIA: No se encontró el span gris para {full_new_issue} en el Changelog.")

    with open(CHANGELOG_FILE, 'w', encoding='utf-8') as f:
        f.write(changelog_content)
    print(f"Changelog actualizado con el issue {full_new_issue}.")

if __name__ == "__main__":
    main()