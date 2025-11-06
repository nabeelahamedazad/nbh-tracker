from flask import Flask, request, Response
from datetime import datetime
import base64, threading
import gspread
from google.oauth2.service_account import Credentials

# === CONFIG ===
SHEET_ID = "1T2wYwxgMbuV2K_zRpEKELmSGA89igw6ARL8mYsjrXAc"  # 👈 your sheet ID
SHEET_NAME = "Sheet17"  # 👈 change if needed
TRACK_COL = "H"         # 👈 Tracking column
# =================

# transparent pixel
PIXEL = base64.b64decode("R0lGODlhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs=")

# Google Sheets auth (using service account)
creds = Credentials.from_service_account_file("service_account.json", scopes=[
    "https://www.googleapis.com/auth/spreadsheets"
])
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

app = Flask(__name__)

def update_tracking(row, status):
    try:
        sheet.update_acell(f"{TRACK_COL}{row}", status)
        print(f"✅ Updated row {row}: {status}")
    except Exception as e:
        print("⚠️ Error updating sheet:", e)

@app.route("/track")
def track():
    row = request.args.get("row")
    if not row:
        return Response(PIXEL, mimetype="image/gif")
    status = f"Opened on {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}"
    threading.Thread(target=update_tracking, args=(row, status), daemon=True).start()
    return Response(PIXEL, mimetype="image/gif")

@app.route("/")
def home():
    return "✅ NBH Email Tracker is Live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
