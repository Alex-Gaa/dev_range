#C:\Users\Developer\PycharmProjects\devrange\children\urls.py
from django.urls import path

from .views import (
    ChildListCreateView,
    AcceptInviteView,
    ChildInviteDetailView,
    ChildDetailView,
    ResetChildPasswordView,
)

urlpatterns = [

    # CHILDREN CRUD
    path(
        "",
        ChildListCreateView.as_view()
    ),
    path(
        "invite/<uuid:token>/",
            ChildInviteDetailView.as_view()
    ),
    # INVITE ACCEPT
    path(
        "accept-invite/",
        AcceptInviteView.as_view()
    ),
    path("<int:pk>/", ChildDetailView.as_view()),
    path(
        "<int:pk>/reset-password/",
        ResetChildPasswordView.as_view()
    ),
]