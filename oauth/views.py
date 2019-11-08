from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


from oauth2_provider.views.generic import ProtectedResourceView


class ApiEndpoint(ProtectedResourceView):

    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')


@login_required
def secret_page(request, *args, **kwargs):
    return HttpResponse('Secret contents!', status=200)
