from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

https://discord.com/api/webhooks/1390452061723955240/1-ymXdkl552bfpT8M8szpRlTBdX48GE33SVEkJ0nHCcCz3_SXLDvwTVXYSW2WyHY8p9m
@app.route("/api", methods=["POST"])
def api():
    data = request.get_json()

    # Hvis dataen er korrekt struktureret
    if data and "members" in data:
        for member in data["members"]:
            name = member.get("name", "Unknown")
            rank = member.get("rank", "Unknown")
            send_to_discord(name, rank)

    return jsonify({"status": "received"})

def send_to_discord(name, rank):
    content = f"🧙‍♂️ **{name}** joined the clan as **{rank}**!"
    payload = {"content": content}
    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
print(response.status_code)
print(response.status_code)
print(response.text)  # <- Tilføj denne linje

        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error sending to Discord: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
