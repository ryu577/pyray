from io import BytesIO


def get_image_bytes(img):
    with BytesIO() as data:
        img.save(data, "PNG")
        return data.getvalue()
