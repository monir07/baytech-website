from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.views.generic import TemplateView


@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request: Request) -> Response:
    data = {
        'message': 'tax calculation api service',
        'method': request.method
    }
    return Response(data={'message': data}, status=status.HTTP_200_OK)


class HomePageView(TemplateView):
    template_name = "home.html"


from django.http import HttpResponse
from django.template import loader


def reference_page(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    template = loader.get_template('pages/' + load_template)
    return HttpResponse(template.render(context, request))