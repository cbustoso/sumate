from rest_framework.renderers import JSONRenderer


class ApiRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code
        response = {
            "error": False,
            "code": status_code,
            "data": data,
            "message": None
        }

        if not str(status_code).startswith('2'):
            response["error"] = True
            response["data"] = ""
            
            try:
                response["message"] = data["detail"]
            except KeyError:
                response["message"] = data

        return super(ApiRenderer, self).render(response, accepted_media_type, renderer_context)
