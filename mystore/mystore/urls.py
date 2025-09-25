from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/', include('elements.urls', namespace='elements')),

    # Login y Logout
    path('accounts/login/', auth_views.LoginView.as_view(template_name='elements/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(next_page='/store/'), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)