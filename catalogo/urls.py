from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.lista_obras, name='lista_obras'),
    path('nueva/', views.nueva_obra, name='nueva_obra'),
    path('compositores/', views.lista_compositores, name='lista_compositores'),
    path('compositores/<int:compositor_id>/', views.detalle_compositor, name='detalle_compositor'),
    path('compositores/nuevo/', views.nuevo_compositor, name='nuevo_compositor'),
    path('compositores/<int:compositor_id>/eliminar/', views.eliminar_compositor, name='eliminar_compositor'),
    path('registro/', views.registro, name='registro'),
    path('login/', LoginView.as_view(template_name='catalogo/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='lista_obras'), name='logout'),
    path('<int:obra_id>/', views.detalle_obra, name='detalle_obra'),
    path('<int:obra_id>/editar/', views.editar_obra, name='editar_obra'),
    path('rocola/', views.vista_rocola, name='rocola'),
    path('obra/<int:obra_id>/reportar/', views.crear_reporte, name='crear_reporte'),
    path('admin-panel/reportes/', views.bandeja_reportes, name='bandeja_reportes'),
]