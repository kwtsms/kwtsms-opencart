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

r = post(admin + '?route=marketplace/installer.upload&user_token=' + T, files={'file': ('kwtsms.ocmod.zip', open(zip_path, 'rb').read())})
print('upload:', r[:300])
if '"error"' in r:
    fail('upload error')

listing = get(admin + '?route=marketplace/installer.extension&user_token=' + T)
ids = re.findall(r'installer\.install&(?:amp;)?user_token=[0-9a-f]+&(?:amp;)?extension_install_id=(\d+)', listing)
print('installable ids:', ids)
if not ids:
    fail('uploaded extension not listed')
r = get(admin + '?route=marketplace/installer.install&user_token=' + T + '&extension_install_id=' + ids[-1])
print('install:', r[:300])
if '"error"' in r:
    fail('install error')

r = get(admin + '?route=extension/module.install&user_token=' + T + '&extension=kwtsms&code=kwtsms')
print('module install:', r[:300])
if '"error"' in r:
    fail('module install error')
print('OK')
