from django.urls import path
from passwordkeeper.views import index_view, add_view, decrypt_password

urlpatterns = [
    path('index', index_view),
    path('add/', add_view),
    path('decrypt/<int:id>', decrypt_password, name='decrypt_password')
]
