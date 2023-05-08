from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    playlist_url = request.form['playlist_url']
    target_service = request.form['target_service']
    
    # Perform the conversion logic here
    # You can use APIs or libraries specific to the target service to convert the playlist
    
    converted_playlist = f"Converted playlist from {playlist_url} to {target_service}"
    return render_template('result.html', converted_playlist=converted_playlist)

if __name__ == '__main__':
    app.run(debug=True)