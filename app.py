import os
import redis
from flask import Flask

# Create the Flask web application instance
app = Flask(__name__)

# --- Database Connection ---
# Use environment variables for flexible configuration.
# Default to 'localhost' if the REDIS_HOST variable is not set.
redis_host = os.environ.get('REDIS_HOST', 'localhost')

# Connect to our Redis instance.
# The decode_responses=True argument makes sure Redis returns strings, not bytes.
db = redis.Redis(host=redis_host, port=6379, decode_responses=True)


# --- Application Routes ---
@app.route('/')
def index():
    """
    This is the main view for our application.
    It increments the 'views' counter in Redis and displays the result.
    """
    try:
        # The .incr() method is atomic, making it safe for multiple requests.
        # It increments the value of a key by one. If the key does not exist,
        # it is set to 0 before performing the operation.
        views = db.incr('views')
    except redis.exceptions.ConnectionError as e:
        # If we can't connect to Redis, return an error message.
        # This makes the app more robust.
        return f"<h1>Error: Could not connect to Redis.</h1><p>{e}</p>", 500

    # Return the view count to the user.
    return f"<h1>Welcome!</h1><p>This page has been viewed {views} times.</p>"

if __name__ == "__main__":
    # Run the app on port 5000, accessible from any network interface.
    app.run(host="0.0.0.0", port=5000, debug=True)
