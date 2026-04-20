class GappVersion {
  // ERR_CONT_01105

  static const core_version = '2.8.4';
  static const api_version = '1.0.0';

  // Al compilar, Android extraerá 2066502 e iOS extraerá 2066500
  static const android_version = '(2.0665.02)'; // version de flavor distinta, va dos versiones más adelantada que en el caso de Android
  static const apple_version = '(2.0665.00)';

  static const prefs_ver = 10;
}