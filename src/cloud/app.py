import fastapi

from cloud import api as cloud_api
from cloud import constants as cloud_constants

app = fastapi.FastAPI(
    title=cloud_constants.APP_TITLE,
    description=cloud_constants.APP_DESCRIPTION,
)
app.include_router(cloud_api.router)
