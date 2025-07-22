from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

@app.route("/text2png", methods=["POST"])
def text2png():
    data = request.json
    text = data.get("text", "ที่ได้เจอนั้น")
    font_size = int(data.get("font_size", 48))
    font_path = "NotoSansThai.ttf"  # ชื่อไฟล์ฟอนต์ (ใส่ในโฟลเดอร์เดียวกับ app.py)
    color = data.get("color", "white")  # สามารถส่งสีข้อความได้

    if not os.path.exists(font_path):
        return {"error": "Font not found"}, 404

    font = ImageFont.truetype(font_path, font_size)
    dummy_img = Image.new("RGBA", (1, 1))
    draw_dummy = ImageDraw.Draw(dummy_img)
    bbox = draw_dummy.textbbox((0, 0), text, font=font)
    width = bbox[2] - bbox[0]
    height = bbox[3] - bbox[1]
    padding = 20

    image = Image.new("RGBA", (width + padding, height + padding), (0, 0, 0, 0))  # โปร่งใส
    draw = ImageDraw.Draw(image)
    draw.text((padding // 2, padding // 2), text, font=font, fill=color)

    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype="image/png", as_attachment=False, download_name="text.png")

@app.route("/", methods=["GET"])
def hello():
    return "Text2PNG API - พร้อมใช้!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
