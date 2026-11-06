<picture>
  <source media="(prefers-color-scheme: dark)" srcset=".github/assets/readme-header-dark.png">
  <img alt="kwtSMS: SMS gateway for Kuwait" src=".github/assets/readme-header-light.png">
</picture>

# kwtSMS for OpenCart

[![OpenCart](https://img.shields.io/badge/OpenCart-4.x-blue?logo=opencart)](https://www.opencart.com/index.php?route=marketplace/extension&filter_search=kwtsms)
[![PHP](https://img.shields.io/badge/PHP-8.0%2B-777BB4?logo=php&logoColor=white)](https://php.net)
[![Release](https://img.shields.io/github/v/release/kwtsms/kwtsms-opencart)](https://github.com/kwtsms/kwtsms-opencart/releases)
[![License](https://img.shields.io/badge/License-GPL--3.0-green)](https://www.gnu.org/licenses/gpl-3.0.html)

Send order updates, checkout OTP codes, abandoned cart reminders and SMS campaigns from your OpenCart store, through
kwtSMS, the Kuwaiti SMS gateway. Free.

kwtSMS delivers to Zain, Ooredoo, stc and Virgin in Kuwait and to more than 200 countries, with your own Sender ID,
free API testing and credits that do not expire.

## Features

### Order Notifications
- **Customer SMS on status change**: configurable per-status, with per-status template overrides
- **Admin paid order alerts**: SMS when a new paid order arrives
- **Admin problem order alerts**: SMS on cancelled, refunded, or other problem statuses
- **Per-status custom templates**: different message for Shipped vs Processing vs Cancelled

### COD OTP Verification
- **Phone verification at checkout** for Cash on Delivery orders
- Prevents fake COD orders with one-time code verification
- Configurable code length, expiry, resend cooldown
- Rate limiting per phone and per IP
- Bootstrap 5 modal injected into checkout page

### Abandoned Cart Recovery
- **Cron-based detection** of abandoned carts
- Sends SMS reminder after configurable delay (default: 1 hour)
- One SMS per cart (dedup via cart hash, no spam)
- Configurable max sends per cron run

### Bulk SMS Campaigns
- **Send to all customers**, specific customer groups, or custom phone numbers
- Campaign preview with recipient count and credit estimate
- Campaign history log with results tracking

### Event Alerts
- **Customer welcome SMS** on new registration
- **Admin new customer alert**
- **Admin low stock alert** with global threshold, once-per-product logic
- **Admin new product review alert**
- **Admin return request alert**

### OTP on Login and Registration
- **Phone verification on customer registration**
- **Two-factor authentication on customer login** via SMS
- Configurable per feature (enable/disable independently)

### Core
- **7-tab admin UI**: Dashboard, Campaigns, Settings, Gateway, Templates, Logs, Help
- **Gateway login/logout/reload** with live API connection
- **Test Gateway**: send test SMS through the full pipeline (supports multiple numbers)
- **24 message templates**: EN + AR, editable with reset-to-default
- **SMS log**: full audit trail with filters, pagination, clear
- **Debug log**: internal flow tracing (normalize, verify, clean, send)
- **Dashboard**: SMS analytics (sent/failed/skipped) and system status
- **Daily cron sync**: balance, sender IDs, coverage
- **Phone normalization**: local numbers, Arabic digits, +/00 prefix stripping, default country code
- **Per-country phone validation**: number length and mobile prefix checks via kwtsms-php library
- **Bulk SMS**: auto-batching for 200+ recipients with ERR013 backoff
- **Coverage check**: skips countries not in account coverage

## Requirements

- OpenCart 4.0.2.x or later, PHP 8.0 or later with curl and json.
- A kwtSMS account (free test account, no papers): https://www.kwtsms.com/cportal/signup/

## Installation

### From OpenCart Marketplace (recommended)

1. Go to [OpenCart Marketplace](https://www.opencart.com/index.php?route=marketplace/extension&filter_search=kwtsms) and search for "kwtSMS"
2. Download the extension
3. In your OpenCart Admin, go to **Extensions > Installer** and upload the .ocmod.zip file
4. Go to **Extensions > Extensions**, select **Modules** from the dropdown
5. Find **kwtSMS - SMS Gateway** and click the green **+** (Install) button
6. Click the blue **pencil** (Edit) button to configure

### From GitHub

1. Download the latest release from [GitHub Releases](https://github.com/kwtsms/kwtsms-opencart/releases)
2. Extract the zip, the `extension/kwtsms/` directory contains the extension files
3. Copy the `kwtsms/` folder to your OpenCart installation's `extension/` directory
4. In your OpenCart Admin, go to **Extensions > Extensions**, select **Modules**
5. Find **kwtSMS - SMS Gateway** and click Install, then Edit

## Setup

1. **Gateway** tab: enter the API username and password of your kwtSMS account (not your mobile number) and click
   **Login**.
2. **Settings** tab: the extension starts with sensible defaults; turn on test mode for a first try.
3. **Templates** tab: adjust the English and Arabic messages.
4. Use **Test Gateway** to send a test message through the full pipeline, then turn test mode off.

Test mode messages are not delivered, but their credits are held until you delete them from the Sending Queue in your
kwtSMS account.

## Placeholders

| Placeholder | Available In | Description |
|---|---|---|
| `{order_id}` | Order, Admin | Order number |
| `{customer_name}` | All | Customer full name |
| `{order_status}` | Order | Current order status |
| `{order_total}` | Order, Admin, Cart | Total with currency |
| `{store_name}` | All | Store name |
| `{date}` | All | Current date and time |
| `{customer_email}` | Customer, Admin | Customer email |
| `{customer_phone}` | Admin | Customer phone |
| `{product_name}` | Stock, Review, Return | Product name |
| `{product_model}` | Stock | Product model/SKU |
| `{product_quantity}` | Stock | Current stock level |
| `{stock_threshold}` | Stock | Configured threshold |
| `{rating}` | Review | Review rating (1-5) |
| `{return_reason}` | Return | Return reason |
| `{otp_code}` | OTP | Verification code |
| `{expiry_minutes}` | OTP | Code validity |
| `{products_summary}` | Cart | Product names in cart |

## Arabic

Every template comes in English and Arabic and the admin screens are translated. Arabic SMS are sent as Unicode: one
SMS page holds 70 Arabic characters, against 160 English ones.

## FAQ

**Which username do I use?** The API username and password of your kwtSMS account, not your mobile number.

**Why do test messages not arrive?** Test mode queues messages without delivering them. Turn it off in Settings.

**What is a Sender ID?** The name shown as the sender on the phone. See the
[Sender ID help](https://www.kwtsms.com/sender-id-help.html).

## Technical Details

- 20 PHP files + 3 Twig templates
- 8 database tables
- 9 OpenCart events
- 2 cron jobs (daily sync + abandoned cart)
- 24 SMS templates (EN + AR)
- 7 admin tabs

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Support

Help: https://www.kwtsms.com/support.html | FAQ: https://www.kwtsms.com/faq/ |
API: [developers](https://www.kwtsms.com/developers.html), [API reference](https://www.kwtsms.com/api-documentation.html) |
[Issues](https://github.com/kwtsms/kwtsms-opencart/issues)

## Security

See [SECURITY.md](SECURITY.md).

## License

GPL-3.0-or-later, (c) kwtSMS (BoxLink Center). See https://www.gnu.org/licenses/gpl-3.0.html.
