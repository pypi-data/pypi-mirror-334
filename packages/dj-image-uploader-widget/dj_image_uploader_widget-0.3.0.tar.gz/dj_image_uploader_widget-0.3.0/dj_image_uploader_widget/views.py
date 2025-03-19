from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .utils.oss import upload_to_oss


@require_POST
@login_required
def upload_view(request):
    try:
        image_file = request.FILES["image"]
        oss_url = upload_to_oss(image_file, request.user.id)
        return JsonResponse({"url": oss_url})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)
