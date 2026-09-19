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

    # Simple & stable yt_dlp options with original title
    ydl_opts = {
        'format': 'bestaudio/audio',
        'outtmpl': '%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
            # Oru vela extension mp3-ku change aagala naanga safe-ah convert panrom
            base, ext = os.path.splitext(filename)
            mp3_filename = base + ".mp3"
            
            if os.path.exists(filename) and filename != mp3_filename:
                os.rename(filename, mp3_filename)
                filename = mp3_filename
            elif not os.path.exists(filename) and os.path.exists(mp3_filename):
                filename = mp3_filename

            if os.path.exists(filename):
                response = send_file(filename, as_attachment=True, download_name=os.path.basename(filename))
                
                @response.call_on_close
                def cleanup():
                    try:
                        if os.path.exists(filename):
                            os.remove(filename)
                    except Exception as e:
                        print(f"Cleanup error: {e}")

                return response
            else:
                return render_template('index.html', message="Error: File could not be processed!")

    except Exception as e:
        return render_template('index.html', message=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
