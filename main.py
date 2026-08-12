from flask import Flask, request, send_file
import img2pdf
import io
import base64

app = Flask(__name__)

@app.route('/merge', methods=['POST'])
def merge_images():
    try:
        image_bytes_list = []

        # Новый формат: JSON с base64-строками (его шлёт обновлённый сборщик)
        if request.is_json:
            data = request.get_json(force=True)
            for item in data.get('images', []):
                image_bytes_list.append(base64.b64decode(item['data']))
        # Старый формат: multipart/form-data (оставлен для совместимости)
        else:
            files = request.files.getlist("images")
            image_bytes_list = [f.read() for f in files]

        if not image_bytes_list:
            return "Нет изображений в запросе", 400

        # Склеиваем в один PDF без потери качества (lossless), как и раньше
        pdf_bytes = img2pdf.convert(image_bytes_list)

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
