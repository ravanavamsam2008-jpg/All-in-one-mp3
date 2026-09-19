from flask import Flask, render_template, request, send_file
import yt_dlp
import os

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_audio():
    url = request.form.get('url')
    if not url:
        return render_template('index.html', message="Please enter a valid URL!")

    # Android storage-ku safe-aana filename-ah convert panra options
    ydl_opts = {
        'format': 'bestaudio/audio',
        'outtmpl': '%(id)s.mp3',
        'restrictfilenames': True,  # Special characters and spaces-ah remove pannidum
        'noplaylist': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video info-va extract panrom
            info = ydl.extract_info(url, download=True)
            filename = info.get('id') + '.mp3'
            
            # File-a user-oda browser-ku send panrom
            response = send_file(filename, as_attachment=True)
            
            # File send aanathum server folder-la irundhu delete panra function
            @response.call_on_close
            def cleanup():
                try:
                    if os.path.exists(filename):
                        os.remove(filename)
                except Exception as e:
                    print(f"Cleanup error: {e}")

            return response

    except Exception as e:
        return render_template('index.html', message=f"Error: {str(e)}")

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
