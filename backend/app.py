from flask import Flask

app = Flask(__name__)

@app.route("/")
def main():
    # Adding Bootstrap CDN link to the response
    bootstrap_link = '<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">'
    
    # Your HTML content
    html_content = "<p>Hello, World!</p>"
    
    # Combining Bootstrap CDN link and your HTML content
    complete_html = bootstrap_link + html_content

    return complete_html

if __name__ == "__main__":
    app.run(debug=True)
