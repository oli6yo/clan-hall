from flask import Flask, request, jsonify
import requests
import json

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1390452061723955240/1-ymXdkl552bfpT8M8szpRlTBdX48GE33SVEkJ0nHCcCz3_SXLDvwTVXYSW2WyHY8p9m"  # ← Udskift med din egen

@app.route("/api", methods=["POST"])
def api():
    try:
        data = request.get_json(force=True)
        print("📥 Modtaget data:")
        print(json.dumps(data, indent=2))  # 🔍 LOG ALT

        # Du kan evt. validere client_id og secret her
        client_id = data.get("client_id", "")
        client_secret = data.get("client_secret", "")
        print("🔑 Client ID:", client_id)
        print("🗝️ Client Secret:", client_secret)

        if "members" in data:
            for member in data["members"]:
                name = member.get("name", "Unknown")
                rank = member.get("rank", "Unknown")
                send_to_discord(name, rank)
        else:
            print("⚠️ Ingen 'members' fundet i data")
        return jsonify({"status": "received"}), 200

    except Exception as e:
        print("❌ Fejl:", e)
        return jsonify({"status": "error", "message": str(e)}), 400


def send_to_discord(name, rank):
    content = f"📢 **{name}** joined the clan as **{rank}**!"
    payload = {"content": content}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print("✅ Discord response:", response.status_code)
        print("📨 Discord svar:", response.text)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Fejl ved sending til Discord: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

