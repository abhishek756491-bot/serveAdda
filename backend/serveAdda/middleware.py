from django.http import JsonResponse
from .models import Tenant

class TenantMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Admin panel aur auth routes par tenant check bypass karein
        if request.path.startswith('/admin/') or request.path.startswith('/serveAdda/auth/'):
            return self.get_response(request)

        # Header se tenant_id (subdomain_slug) nikalein
        tenant_id = request.headers.get('X-Tenant-ID')
        
        if tenant_id:
            try:
                request.tenant = Tenant.objects.get(subdomain_slug=tenant_id)
            except Tenant.DoesNotExist:
                return JsonResponse({'error': 'Invalid Tenant ID. Agency not found.'}, status=400)
        else:
            # Agar header nahi hai, toh bad request return karein (except public routes)
            request.tenant = None

        response = self.get_response(request)
        return response