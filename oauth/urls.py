from django.urls import re_path, include
import oauth2_provider.views as oauth2_views
from django.conf import settings
from .views import ApiEndpoint, secret_page

# OAuth2 provider endpoints
oauth2_endpoint_views = [
    re_path(r'^authorize/$', oauth2_views.AuthorizationView.as_view(), name="authorize"),
    re_path(r'^token/$', oauth2_views.TokenView.as_view(), name="token"),
    re_path(r'^revoke-token/$', oauth2_views.RevokeTokenView.as_view(), name="revoke-token"),
]

if settings.DEBUG:
    # OAuth2 Application Management endpoints
    oauth2_endpoint_views += [
        re_path(r'^applications/$', oauth2_views.ApplicationList.as_view(), name="list"),
        re_path(r'^applications/register/$', oauth2_views.ApplicationRegistration.as_view(), name="register"),
        re_path(r'^applications/(?P<pk>\d+)/$', oauth2_views.ApplicationDetail.as_view(), name="detail"),
        re_path(r'^applications/(?P<pk>\d+)/delete/$', oauth2_views.ApplicationDelete.as_view(), name="delete"),
        re_path(r'^applications/(?P<pk>\d+)/update/$', oauth2_views.ApplicationUpdate.as_view(), name="update"),
    ]

    # OAuth2 Token Management endpoints
    oauth2_endpoint_views += [
        re_path(r'^authorized-tokens/$', oauth2_views.AuthorizedTokensListView.as_view(), name="authorized-token-list"),
        re_path(r'^authorized-tokens/(?P<pk>\d+)/delete/$', oauth2_views.AuthorizedTokenDeleteView.as_view(),
                name="authorized-token-delete"),
    ]

urlpatterns = [
    # OAuth 2 endpoints:
    re_path(r'^o/', include((oauth2_endpoint_views, 'oauth'), namespace="oauth2_provider")),
    re_path(r'^api/hello', ApiEndpoint.as_view()),  # an example resource endpoint
    re_path(r'^secret$', secret_page, name='secret'),  # an example resource endpoint
]
