####################################################################################################

from pyramid.response import Response
from pyramid.view import view_config
from ocr import readDigits

####################################################################################################

@view_config(route_name="home", renderer="home.pt")
def home_view(request):
    return { }


@view_config(route_name="ocr", renderer="json", request_method="POST")
def ocr_view(request):
    "Read number from LCD display and return as JSON object"

    try:
        number = readDigits(request.POST["image"].file)
        return {"success": True, "result": number}
    except Exception as e:
        return {"success": False, "message": str(e)}

####################################################################################################