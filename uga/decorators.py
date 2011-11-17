from functools import wraps
import urlparse
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.conf import settings


def require_cms_permissions(view_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.current_page.has_view_permission(request):
            return view_func(request, *args, **kwargs)
        path = request.build_absolute_uri()
        # If the login url is the same scheme and net location then just
        # use the path as the "next" url.
        login_scheme, login_netloc = urlparse.urlparse(login_url or
                                                    settings.LOGIN_URL)[:2]
        current_scheme, current_netloc = urlparse.urlparse(path)[:2]
        if ((not login_scheme or login_scheme == current_scheme) and
            (not login_netloc or login_netloc == current_netloc)):
            path = request.get_full_path()
        from django.contrib.auth.views import redirect_to_login
        return redirect_to_login(path, login_url, redirect_field_name)
    return _wrapped_view


