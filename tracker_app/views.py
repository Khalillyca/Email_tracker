from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.http import HttpResponse
 
 
@api_view(["GET", "POST"])
@permission_classes([AllowAny])
def email_tracker(request):
    print("METHOD:", request.method)
    print("QUERY:", request.GET)
    print("BODY:", request.body.decode())
 
    token = request.GET.get("validationToken")
    if token:
        return HttpResponse(token, content_type="text/plain")
 
    return HttpResponse("ok")