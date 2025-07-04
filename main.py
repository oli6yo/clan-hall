from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/..."  # Udskift med din rigtige webhook

@app.route("/api", methods=["POST"])
def api():
    try:
        data = request.get_json(force=True)
        print("✅ Modtaget data:", data)

        if data and "members" in data:
            for member in data["members"]:
                name = member.get("name", "Unknown")
                rank = member.get("rank", "Unknown")
                send_to_discord(name, rank)
        else:
            print("⚠️ Data er ikke som forventet:", data)

        return jsonify({"status": "received"}), 200

    except Exception as e:
        print("❌ Fejl ved behandling af request:", e)
        return jsonify({"status": "error", "message": str(e)}), 400


def send_to_discord(name, rank):
    content = f"📢 **{name}** joined the clan as **{rank}**!"
    payload = {"content": content}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
        print("📨 Discord respons:", response.status_code)
        print("🧾 Discord svar:", response.text)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"❌ Fejl ved sending til Discord: {e}")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

