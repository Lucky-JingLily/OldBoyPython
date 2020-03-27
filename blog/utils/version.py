from rest_framework.versioning import BaseVersioning

class ParamVersion(BaseVersioning):
    def determine_version(self, request, *args, **kwargs):
        version = request.query_params.get("version")
        print(version)
        return version