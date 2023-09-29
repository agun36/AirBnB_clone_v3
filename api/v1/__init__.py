from flask import Blueprint

app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Import your views here
from api.v1.views import *
