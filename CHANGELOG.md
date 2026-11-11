# Changelog

## [Unreleased]

### Changed
- Settings, templates, gateway login, campaigns and SMS log are kept when the module is uninstalled.

## [1.1.1] - 2026-11-07

### Added
- Integration name and version sent with requests.

### Changed
- Bundled kwtsms-php library updated.
- GPL-3.0 LICENSE file added.
- Release file renamed `kwtsms.ocmod.zip`; the README explains how to upgrade without losing settings.
- Tested on OpenCart 4.1.0.4.

## [1.1.0] - 2026-04-09

### Added
- Per-status SMS templates with reset to default.
- Customer welcome SMS and admin alerts for new customers, low stock, product reviews and returns.
- COD OTP verification, OTP on login and registration.
- Abandoned cart SMS recovery.
- Bulk SMS campaigns with preview and history.
- More settings and a country code dropdown.

### Changed
- Test gateway and dashboard improved.
- Tab order and sender ID dropdown refined.
- Bug fixes.

## [1.0.0] - 2026-04-05

### Added
- Initial release.
- SMS notifications on order status changes (customer and admin).
- Gateway login and test gateway.
- English and Arabic templates.
- SMS and debug logs.
- Dashboard with SMS analytics.
- Order status toggles, phone normalization and coverage check.
- Bulk SMS batching.
- Daily sync.
