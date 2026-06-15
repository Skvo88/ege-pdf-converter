from flask import Flask, request, send_file
import img2pdf
import io

app = Flask(__name__)

@app.route('/merge', methods=['POST'])
def merge_images():
    try:
        # Извлекаем присланные картинки из запроса
        files = request.files.getlist("images")
        image_bytes_list = [f.read() for f in files]
        
        # Склеиваем их в один PDF без потери качества (lossless)
        pdf_bytes = img2pdf.convert(image_bytes_list)
        
        # Отправляем готовый PDF-файл обратно в Google Apps Script
        return send_file(
            io.BytesIO(pdf_bytes),
            mimetype='application/pdf',
            as_attachment=True,
            download_name='assembly.pdf'
        )
    except Exception as e:
        return str(e), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
