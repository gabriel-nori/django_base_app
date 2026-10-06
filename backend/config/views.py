from django.views.decorators.http import require_safe
from django.http import FileResponse, Http404
from django.conf import settings


@require_safe
def spa_index(request, *args, **kwargs):
    """Serve the SPA entrypoint so the frontend router can handle the path."""
    index_file = settings.SPA_DIR / "index.html"
    if not index_file.is_file():
        raise Http404("SPA build not found. Check SPA_DIR.")

    response = FileResponse(open(index_file, "rb"), content_type="text/html")
    # index.html must always be revalidated so new deploys are picked up
    response["Cache-Control"] = "no-cache"
    return response
