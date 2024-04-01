from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def index():
    # Set the user agent to iPhone
    user_agent = ('Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) '
                  'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 '
                  'Mobile/15E148 Safari/604.1')

    # URL to load within the iframe
    url_to_load = 'https://shorturl.at/euyC6'

    # Create headers with the custom user agent and additional header
    headers = {
        'User-Agent': user_agent,
        'X-Powered-By': 'NIHAL ✨'
    }

    # Fetch the content of the URL using the provided user agent
    response = requests.get(url_to_load, headers=headers)

    # Render the template with the content loaded in the iframe
    return render_template('index.html', iframe_content=response.content)

if __name__ == '__main__':
    app.run(debug=True)
