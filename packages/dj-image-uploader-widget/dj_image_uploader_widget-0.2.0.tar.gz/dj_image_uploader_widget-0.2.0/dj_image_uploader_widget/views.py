from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .oss import upload_to_oss, decode_base64_image

@require_POST
@login_required
def upload_image(request):
    try:
        image_file = request.FILES['image']

        oss_url = upload_to_oss(
            image_file,
            user_id=request.user.id
        )
        return JsonResponse({'url': oss_url})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)