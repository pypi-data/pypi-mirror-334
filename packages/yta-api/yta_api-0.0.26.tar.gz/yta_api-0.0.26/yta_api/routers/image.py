from yta_image.generation.ai.generator import DefaultImageGenerator
from yta_image import Image
from yta_general_utils.temp import Temp
from yta_general_utils.downloader import Downloader
from fastapi.responses import FileResponse
from fastapi import APIRouter


PREFIX = 'image'

router = APIRouter(
    prefix = f'/{PREFIX}'
)

@router.get('/generate')
def route_generate_image(prompt: str):
    return FileResponse(
        DefaultImageGenerator().generate_image(
            prompt,
            Temp.create_filename('ai_image.png')
        ).output_filename
    )

@router.get('/edit')
def route_edit_image(image_url: str):
    # This is just a test to download an iamge, edit
    # it and return it as a file
    image = Image(Downloader.download_image(image_url, Temp.create_filename('image.png')))

    return FileResponse(
        image.filter.pixelate(16).output_filename
    )