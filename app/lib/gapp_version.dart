class GappVersion {
  static const coreVersion = '2.8.4'; // Versión leída del pubspec.yaml
  static const apiVersion = '1.0.0';  // Preparado para el futuro

  // FORMATO: (X . CORE_BUILD . FLAVOR_BUILD)
  // Al compilar, Android extraerá 2067302 e iOS extraerá 2067300
  static const android_version = '(2.0673.02)';
  static const apple_version = '(2.0673.00)';

  static const prefs_ver = 10;
}