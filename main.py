from flask import Flask, jsonify
import requests
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, origins=["https://chatnlearnai.com"])

@app.route('/start-demo', methods=['GET'])
def start_demo():
    try:
        url = "https://tavusapi.com/v2/conversations"

        payload = {
            "replica_id": "r9d30b0e55ac",
            "persona_id": "p6b0e7541d3f",
            "conversation_name": "Science - States of Matter",
            "conversational_context": "You’re having a video conversation with a student specifically for an Integrated Science learning session about the States of Matter...",
            "custom_greeting": "Hi there! We're going to talk about the states of matter. Can you tell me what the three states of matter are?",
            "properties": {
                "max_call_duration": 180,
                "participant_left_timeout": 2,
                "participant_absent_timeout": 60,
                "enable_recording": True,
                "enable_closed_captions": True,
                "language": "english",
                "recording_s3_bucket_name": "conversation-recordings",
                "recording_s3_bucket_region": "us-east-1",
                "aws_assume_role_arn": ""
            }
        }
        
        api_key = os.getenv("tavus_api_key")
        
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        response_json = response.json()

        conversation_url = response_json.get("conversation_url")
        if conversation_url:
            return jsonify({"url": conversation_url})
        else:
            return jsonify({"error": "No conversation URL returned"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
