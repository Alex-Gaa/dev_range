from django.urls import path

from .views import (
    ChildListCreateView,
    AcceptInviteView, ChildInviteDetailView,
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
]