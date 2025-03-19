from yta_general_utils.downloader import Downloader
from yta_general_utils.web.tiktok.downloader import download_tiktok_video
from yta_general_utils.temp import Temp
from fastapi.responses import FileResponse
from fastapi import APIRouter


PREFIX = 'download'

router = APIRouter(
    prefix = f'/{PREFIX}'
)

@router.get('/tiktok')
def route_download_tiktok(url: str):
    # TODO: Review this, please
    # TODO: This must be done within Downloader.download_tiktok
    output_filename = Temp.create_filename('tiktokvideo.mp4')
    
    return FileResponse(
        download_tiktok_video(url, output_filename).filename
    )