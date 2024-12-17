from flask import Flask, request, render_template_string
import subprocess
import os

app = Flask(__name__)

# HTML template for the web interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>GeoWiFi - Search WiFi Locations</title>
</head>
<body>
    <h1>GeoWiFi Tool</h1>
    <form method="POST" action="/">
        <label for="search_type">Search Type:</label>
        <select name="search_type" id="search_type">
            <option value="bssid">BSSID</option>
            <option value="ssid">SSID</option>
        </select>
        <br><br>
        <label for="query">Enter BSSID or SSID:</label>
        <input type="text" id="query" name="query" required>
        <br><br>
        <label for="output">Output Format:</label>
        <select name="output" id="output">
            <option value="json">JSON</option>
            <option value="map">Map</option>
        </select>
        <br><br>
        <input type="submit" value="Search">
    </form>
    <hr>
    <div>
        <h3>Results:</h3>
        <pre>{{ results }}</pre>
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    results = ""
    if request.method == "POST":
        search_type = request.form["search_type"]
        query = request.form["query"]
        output = request.form["output"]

        # Construct the GeoWiFi command
        command = f"python3 geowifi.py -s {search_type} {query} -o {output}"

        try:
            # Execute the command and capture the output
            result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            results = result
        except subprocess.CalledProcessError as e:
            results = f"Error: {e.output}"

    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == "__main__":
    # Run the app on localhost at port 5000
    app.run(debug=True, host="127.0.0.1", port=5000)
