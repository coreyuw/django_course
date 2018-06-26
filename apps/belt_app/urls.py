from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.createUser),
    url(r'^dashboard$', views.dashboard),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^addtrip$', views.addtrip),
    url(r'^update$', views.update),
    url(r'^view/(?P<trip_id>\d+)$', views.view, name="my_view"),
    url(r'^cancel/(?P<trip_id>\d+)$', views.cancel, name="my_cancel"),
    url(r'^delete/(?P<trip_id>\d+)$', views.delete, name="my_delete"),
    url(r'^join/(?P<trip_id>\d+)$', views.join, name="my_join"),
    # url(r'^users/myaccount/(?P<user_id>\d+)$', views.edit, name='my_edit'),
    # url(r'^users/update$', views.update, name='my_update'),
    # url(r'^add_quote$', views.add, name="my_add"),
    # url(r'^user/(?P<user_id>\d+)$', views.show, name='my_show'),
    # url(r'^like/(?P<quote_id>\d+)$', views.like, name="my_like"),
    # url(r'^delete/(?P<quote_id>\d+)$', views.delete, name="my_delete")
    # url(r'^users$', views.index, name='my_index'),
    # url(r'^users/new$', views.new, name='my_new'),
    # url(r'^users/create$', views.create, name='my_create'),
    # url(r'^users/(?P<user_id>\d+)$', views.show, name='my_show'),
    # url(r'^users/(?P<user_id>\d+)/edit$', views.edit, name='my_edit'),
    # url(r'^users/update$',views.update, name='my_update'),
    # url(r'^users/(?P<user_id>\d+)/destroy$', views.destroy, name='my_delete')
]