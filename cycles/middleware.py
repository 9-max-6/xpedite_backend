from django.utils.deprecation import MiddlewareMixin
from cycles.models import SuperCycle

class SuperCycleMiddleware(MiddlewareMixin):
    """
    Middleware to check for the 'supercycle' parameter in all incoming requests
    and set it to the latest SuperCycle if not provided. It also attaches the
    supercycle object to the request for use in views.
    """
    
    def process_request(self, request):
        # Check if the 'supercycle' query parameter is missing
        supercycle_id = request.GET.get('supercycle', None)
        supercycle = None

        if supercycle_id:
            # Try to retrieve the SuperCycle object based on the provided supercycle ID
            try:
                supercycle = SuperCycle.objects.get(id=supercycle_id)
            except SuperCycle.DoesNotExist:
                pass
        else:
            try:
            # If no supercycle parameter is provided, use the latest SuperCycle
                supercycle = SuperCycle.objects.order_by('-created_at').first()
            except SuperCycle.DoesNotExist:
                return None

        
        # Attach the supercycle object to the request
        request.supercycle = supercycle

        return None
