from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1390452061723955240/1-ymXdk1552bfpT8M8szpRlTBdX48GE33VEkJ0nHCcCz3_SXLDwvTVXYSW2WyHY8p9m"

@app.route("/", methods=["GET"])
def index():
    return "Clan Halls API is live."

@app.route("/api/activity", methods=["POST"])
def handle_activity():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        message = f"**Activity Report**\n```{data}```"
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/members", methods=["POST"])
def handle_members():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        members = data.get("members", [])
        member_list = "\n".join([f"- {m}" for m in members])
        message = f"**Member List Report**\n```{member_list}```"
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/settings", methods=["POST"])
def handle_settings():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        settings_message = "\n".join([f"{key}: {value}" for key, value in data.items()])
        message = f"**Settings Report**\n```{settings_message}```"
        requests.post(DISCORD_WEBHOOK_URL, json={"content": message})
        return jsonify({"status": "ok"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)
