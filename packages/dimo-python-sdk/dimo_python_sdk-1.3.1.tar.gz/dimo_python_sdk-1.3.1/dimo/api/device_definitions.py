from dimo.errors import check_type
from dimo.errors import check_optional_type


class DeviceDefinitions:

    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def decode_vin(self, developer_jwt: str, country_code: str, vin: str) -> dict:
        check_type("developer_jwt", developer_jwt, str)
        check_type("country_code", country_code, str)
        check_type("vin", vin, str)
        body = {
            "countryCode": country_code,
            "vin": vin,
        }
        response = self._request(
            "POST",
            "DeviceDefinitions",
            "/device-definitions/decode-vin",
            headers=self._get_auth_headers(developer_jwt),
            data=body,
        )
        return response

    def search_device_definitions(
        self,
        query=None,
        make_slug=None,
        model_slug=None,
        year=None,
        page=None,
        page_size=None,
    ):
        check_optional_type("query", query, str)
        check_optional_type("make_slug", make_slug, str)
        check_optional_type("model_slug", model_slug, str)
        check_optional_type("year", year, int)
        check_optional_type("page", page, int)
        check_optional_type("page_size", page_size, int)
        params = {
            "query": query,
            "makeSlug": make_slug,
            "modelSlug": model_slug,
            "year": year,
            "page": page,
            "pageSize": page_size,
        }
        response = self._request(
            "GET",
            "DeviceDefinitions",
            "/device-definitions/search",
            params=params,
        )
        return response
