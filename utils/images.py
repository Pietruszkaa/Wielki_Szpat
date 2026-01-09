from io import BytesIO
from petpetgif import petpet
from PIL import Image, ImageOps

async def generate_petpet_gif(member) -> BytesIO:
    avatar_bytes = await member.display_avatar.read()

    source = BytesIO(avatar_bytes)
    dest = BytesIO()

    petpet.make(source, dest)
    dest.seek(0)

    return dest

async def generate_grayscale_avatar(member) -> BytesIO:
    avatar_bytes = await member.display_avatar.read()
    img = Image.open(BytesIO(avatar_bytes)).convert("RGB")
    gray = ImageOps.grayscale(img)

    output = BytesIO()
    gray.save(output, format="PNG")
    output.seek(0)

    return output
