"""
Welcome to Youtube Autonomous API Module.

Please, take a look at this project to get inspiration:
https://github.com/htbrandao/fastemplate/blob/master/fastemplate/__init__.py

These other resources are gold:
https://github.com/mjhea0/awesome-fastapi
"""
from yta_api.dependencies import is_authorized_with_api_key
from yta_api.routers import audio, image
from yta_general_utils.programming.env import Environment
from yta_general_utils.temp import Temp
from fastapi import FastAPI, Depends

# import uvicorn
# import os


Environment.load_current_project_dotenv()
Temp.clean_folder()

app = FastAPI(dependencies = [
    Depends(is_authorized_with_api_key)
])

# Include routers here
app.include_router(audio.router)
app.include_router(image.router)

# if __name__ == '__init__.py':
#     # Apparently this is the way to run it in Vercel:
#     # https://stackoverflow.com/questions/78425424/how-can-you-specify-python-runtime-version-in-vercel
#     uvicorn.run(
#         '__init__:app',
#         host = '0.0.0.0',
#         port = int(os.get('PORT', 8000)),
#         reload = True
#     )

"""
Instructions:
- You can run the server with 'fastapi dev yta_api.__init__.py'

Issues:
- This library needs the 'typer' library, which uses 
the 'click' library in a newer version than the required
by 'manim' library. So we need to reinstall the 'typer'
each time we reinstall 'manim'.
"""