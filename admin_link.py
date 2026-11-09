"""Create a personal admin link for https://pitch.ateno.co/admin/ (no email needed).

Usage: python3 admin_link.py            # prints a new link and saves it to .admin-link (not in git)
       python3 admin_link.py --revoke   # delete all admin keys and admin browsers first (old links stop working)

Open the link in a browser and confirm the admin email; that browser stays admin until you "Sign out this browser".
Needs gcloud logged in to an owner account of the project.
"""
import hashlib, json, pathlib, secrets, subprocess, sys, urllib.request

PROJECT, HOST, ADMIN = "ateno-pitch", "pitch.ateno.co", "glsvyatoslav@gmail.com"
DOCS = f"https://firestore.googleapis.com/v1/projects/{PROJECT}/databases/(default)/documents"
access = subprocess.run(["gcloud", "auth", "print-access-token"], capture_output=True, text=True, check=True).stdout.strip()
H = {"Authorization": f"Bearer {access}", "Content-Type": "application/json", "x-goog-user-project": PROJECT}

def call(method, url, body=None):
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body is not None else None, method=method, headers=H)
    return json.loads(urllib.request.urlopen(req).read() or b"{}")

if "--revoke" in sys.argv:
    for coll in ("adminKeys", "admins"):
        for d in call("GET", f"{DOCS}/{coll}?pageSize=300").get("documents", []):
            call("DELETE", f"https://firestore.googleapis.com/v1/{d['name']}")
    print("old admin links and admin browsers removed")

token = secrets.token_urlsafe(24)
key = hashlib.sha256(f"{token}:{ADMIN}".encode()).hexdigest()
call("PATCH", f"{DOCS}/adminKeys/{key}", {"fields": {"note": {"stringValue": "created by admin_link.py"}}})
link = f"https://{HOST}/admin/#k={token}"
pathlib.Path(__file__).with_name(".admin-link").write_text(link + "\n")
print(link)
