"""
FILE:      .github/ci/oc_install.py
CREATED:   2026-11-07 23:05 +03
TASK:      opencart CI install test (int-ci-matrix)
AUTHOR:    M Alhassoun
WHAT:      Drives a fresh OpenCart 4 admin over HTTP the way a merchant does: log in, upload kwtsms.ocmod.zip in
           Extensions > Installer, install it, then install the kwtsms module under Extensions > Modules.
           Prints each response (no secrets) and exits non-zero on any failure.
WHY:       OpenCart installs extensions only through its admin; this replaces a browser in CI.
USAGE:     python3 oc_install.py <base_url> <admin_user> <admin_password_file> <zip>
DEPENDS:   Python 3 standard library only.
"""
import http.cookiejar, json, re, sys, urllib.parse, urllib.request, uuid

base, user, pw_file, zip_path = sys.argv[1].rstrip('/'), sys.argv[2], sys.argv[3], sys.argv[4]
password = open(pw_file).read().strip()
jar = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))

def get(url):
    with op.open(url) as r:
        return r.read().decode('utf-8', 'replace')

def post(url, data=None, files=None):
    if files:
        b = uuid.uuid4().hex
        body = b''
        for k, v in (data or {}).items():
            body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n'.encode()
        for k, (name, content) in files.items():
            body += f'--{b}\r\nContent-Disposition: form-data; name="{k}"; filename="{name}"\r\nContent-Type: application/zip\r\n\r\n'.encode() + content + b'\r\n'
        body += f'--{b}--\r\n'.encode()
        req = urllib.request.Request(url, data=body, headers={'Content-Type': 'multipart/form-data; boundary=' + b})
    else:
        req = urllib.request.Request(url, data=urllib.parse.urlencode(data or {}).encode())
    with op.open(req) as r:
        return r.read().decode('utf-8', 'replace')

def fail(msg):
    print('FAIL:', msg); sys.exit(1)

admin = base + '/admin/index.php'
page = get(admin + '?route=common/login')
m = re.search(r'route=common/login\.login&(?:amp;)?login_token=([0-9a-f]+)', page)
if not m:
    fail('login form not found')
r = post(admin + '?route=common/login.login&login_token=' + m.group(1), {'username': user, 'password': password})
print('login:', r[:200].replace(password, '***'))
tok = re.search(r'user_token=([0-9a-f]+)', r)
if not tok:
    fail('no user_token after login')
T = tok.group(1)

# 2026-11-08 00:34 +03: REINSTALL=1 only uninstalls and reinstalls the module (settings must survive, task opencart-keep-settings).
import os
if os.environ.get('REINSTALL') == '1':
    page = get(admin + '?route=extension/kwtsms/module/kwtsms&user_token=' + T)
    print('settings page chars:', len(page))
    for act in ('uninstall', 'install'):
        r = get(admin + '?route=extension/module.' + act + '&user_token=' + T + '&extension=kwtsms&code=kwtsms')
        print('module ' + act + ':', r[:200])
        if '"error"' in r:
            fail('module ' + act + ' error')
    print('OK'); sys.exit(0)

r = post(admin + '?route=marketplace/installer.upload&user_token=' + T, files={'file': ('kwtsms.ocmod.zip', open(zip_path, 'rb').read())})
print('upload:', r[:300])
if '"error"' in r:
    fail('upload error')

ids = []
for route in ('marketplace/installer.list', 'marketplace/installer.extension', 'marketplace/installer'):
    listing = get(admin + '?route=' + route + '&user_token=' + T)
    rows = re.findall(r'<tr.*?</tr>', listing.replace('&amp;', '&'), re.S)
    ids = [i for row in rows if 'kwtsms' in row.lower() for i in re.findall(r'installer\.install&user_token=[0-9a-f]+&extension_install_id=(\d+)', row)]
    print('listing', route, 'chars', len(listing), 'ids', ids, '| kwtsms mentioned:', 'kwtsms' in listing)
    if ids:
        break
print('installable ids:', ids)
if not ids:
    fail('uploaded extension not listed')
url = admin + '?route=marketplace/installer.install&user_token=' + T + '&extension_install_id=' + ids[0]
for step in range(20):
    r = get(url)
    print('install step', step, ':', r[:200])
    if '"error"' in r:
        fail('install error')
    nxt = json.loads(r).get('next')
    if not nxt:
        break
    url = nxt.replace('\\/', '/')

r = get(admin + '?route=extension/module.install&user_token=' + T + '&extension=kwtsms&code=kwtsms')
print('module install:', r[:300])
if '"error"' in r:
    fail('module install error')
print('OK')
