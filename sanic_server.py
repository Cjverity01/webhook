from sanic import Sanic
from sanic.response import json
import asyncio
from multiprocessing import Queue

app = Sanic("GoogleFormWebhook")

# Create a queue to hold form submissions
application_queue = Queue()

@app.post("/webhook")
async def webhook(request):
    data = request.json
    # Extract application details from the POST request
    applicant_name = data.get("applicant_name", "Unknown")
    application_details = data.get("application_details", "No details provided.")
    timestamp = data.get("timestamp", "Unknown time")

    # Add the application data to the queue
    application_queue.put({
        "name": applicant_name,
        "details": application_details,
        "timestamp": timestamp
    })

    # Acknowledge the webhook
    return json({"status": "received"}, status=200)

# Function to share the queue with the Discord bot
def get_application_queue():
    return application_queue

# Run the Sanic server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=9098)
