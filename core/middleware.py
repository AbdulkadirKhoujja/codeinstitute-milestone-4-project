class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if not request.path.startswith("/admin/"):
            response["Content-Security-Policy"] = (
                "default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; form-action 'self' https://checkout.stripe.com"
            )
        response["Referrer-Policy"] = "same-origin"
        if request.user.is_authenticated:
            response["Cache-Control"] = "private, no-store"
        return response
