from dimo.errors import check_type


class Attestation:
    def __init__(self, request_method, get_auth_headers):
        self._request = request_method
        self._get_auth_headers = get_auth_headers

    def create_vin_vc(self, vehicle_jwt: str, token_id: int) -> dict:
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        params = {"force": True}
        url = f"/v1/vc/vin/{token_id}"
        return self._request(
            "POST",
            "Attestation",
            url,
            params=params,
            headers=self._get_auth_headers(vehicle_jwt),
        )

    def create_pom_vc(self, vehicle_jwt: str, token_id: int) -> dict:
        check_type("vehicle_jwt", vehicle_jwt, str)
        check_type("token_id", token_id, int)
        url = f"/v1/vc/pom/{token_id}"
        return self._request(
            "POST", "Attestation", url, headers=self._get_auth_headers(vehicle_jwt)
        )
