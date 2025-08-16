from urllib.parse import urlparse

class HtmxLoginRequiredMiddleware():

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if(request.headers.get("HX-Request") == "true" and response.status_code == 302):
            print("HTMX request from unauthed user")
            ref_header = request.headers.get("Referer", "")
            if ref_header:
                referer = urlparse(ref_header)
                querystring = f"?next={referer.path}"
            else:
                querystring = ""
            redirect = urlparse(response['location'])
            response.status_code = 204
            response.headers["HX-Redirect"] = f"{redirect.path}{querystring}"
        return response