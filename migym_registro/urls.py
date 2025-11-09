from django.contrib import admin
from django.urls import path, include
from aplications.home.views import IndexView, AboutView
from django.contrib.auth import views as auth_views
from core.views import CustomLoginView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', IndexView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),

    path('login/', CustomLoginView.as_view(template_name='home/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),

    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path("ocupacion/", include("aplications.ocupacion.urls", namespace="ocupacion")),
    path('socios/', include(('aplications.socios.urls', 'socios'), namespace='socios')),
    path('pagos/', include(('aplications.pagos.urls', 'pagos'), namespace='pagos')),
    path('rutina/', include('aplications.rutina.urls')),
    path('configuracion/', include('aplications.configuracion.urls')),

    path("usuarios/", include("aplications.usuarios.urls")),
    path('ckeditor5/', include('django_ckeditor_5.urls')),
]



