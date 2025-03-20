class Telemetry:
    def __init__(self, dimo_instance):
        self.dimo = dimo_instance

    # Primary query method
    def query(self, query, vehicle_jwt):
        return self.dimo.query("Telemetry", query, token=vehicle_jwt)
    
    def available_signals(self, vehicle_jwt: str, token_id: int) -> dict:
        query = """
        query getAvailableSignals($tokenId: Int!) {
            availableSignals (tokenId: $tokenId)
        }
        """
        variables = {"tokenId": token_id}
        
        return self.dimo.query(
            "Telemetry", query, token=vehicle_jwt, variables=variables
        )

    # Sample query - get signals latest
    def get_signals_latest(self, vehicle_jwt: str, token_id: int) -> dict:
        query = """
        query GetSignalsLatest($tokenId: Int!) {
            signalsLatest(tokenId: $tokenId){
                powertrainTransmissionTravelledDistance{
                    timestamp
                    value
                }
                exteriorAirTemperature{
                    timestamp
                    value
                }
                speed {
                    timestamp
                    value
                }
                powertrainType{
                    timestamp
                    value
                }
            }
        }
        """
        variables = {"tokenId": token_id}

        return self.dimo.query(
            "Telemetry", query, token=vehicle_jwt, variables=variables
        )

    # Sample query - daily signals from autopi
    def get_daily_signals_autopi(
        self, vehicle_jwt: str, token_id: int, start_date: str, end_date: str
    ) -> dict:
        query = """
        query GetDailySignalsAutopi($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
            signals(
                tokenId: $tokenId,
                interval: "24h",
                from: $startDate, 
                to: $endDate,
                filter: {
                    source: "autopi"
                })
                {
                    speed(agg: MED)
                    powertrainType(agg: RAND)
                    powertrainRange(agg: MIN) 
                    exteriorAirTemperature(agg: MAX)
                    chassisAxleRow1WheelLeftTirePressure(agg: MIN)
                    timestamp
                }
            }
            """
        variables = {"tokenId": token_id, "startDate": start_date, "endDate": end_date}

        return self.dimo.query(
            "Telemetry", query, token=vehicle_jwt, variables=variables
        )

    # Sample query - daily average speed of a specific vehicle
    def get_daily_average_speed(
        self, vehicle_jwt: str, token_id: int, start_date: str, end_date: str
    ) -> dict:
        query = """
        query GetDailyAverageSpeed($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
         signals (
            tokenId: $tokenId,
            from: $startDate,
            to: $endDate,
            interval: "24h"
            )
        {
            timestamp
            avgSpeed: speed(agg: AVG)
        }
        }
        """
        variables = {"tokenId": token_id, "startDate": start_date, "endDate": end_date}

        return self.dimo.query(
            "Telemetry", query, token=vehicle_jwt, variables=variables
        )

    # Sample query - daily max speed of a specific vehicle
    def get_daily_max_speed(
        self, vehicle_jwt: str, token_id: int, start_date: str, end_date: str
    ) -> dict:
        query = """
        query GetMaxSpeed($tokenId: Int!, $startDate: Time!, $endDate: Time!) {
            signals(
                tokenId: $tokenId,
                from: $startDate,
                to: $endDate,
                interval: "24h"
            )
        {
            timestamp
            maxSpeed: speed(agg: MAX)
        }
        }
        """
        variables = {"tokenId": token_id, "startDate": start_date, "endDate": end_date}

        return self.dimo.query(
            "Telemetry", query, token=vehicle_jwt, variables=variables
        )

    # Sample query - get the VIN of a specific vehicle
    def get_vehicle_vin_vc(self, vehicle_jwt: str, token_id: str) -> dict:
        query = """
        query GetVIN($tokenId: Int!) {
            vinVCLatest (tokenId: $tokenId) {
                vin
            }
        }"""
        variables = {"tokenId": token_id}

        return self.dimo.query(
            "Telemetry", query, token=vehicle_jwt, variables=variables
        )

    def get_vin(self, vehicle_jwt: str, token_id: int):
        try:
            attestation_response = self.dimo.attestation.create_vin_vc(
                vehicle_jwt=vehicle_jwt, token_id=token_id
            )
            if (
                attestation_response["message"]
                == "VC generated successfully. Retrieve using the provided GQL URL and query parameter."
            ):
                query = """
                query GetLatestVinVC($tokenId: Int!) {
                    vinVCLatest(tokenId: $tokenId) {
                        vin
                    }
                }
                """
                variables = {"tokenId": token_id}

                return self.dimo.query(
                    "Telemetry", query, token=vehicle_jwt, variables=variables
                )
            else:
                return "There was an error generating a VIN VC. Please check your credentials and try again."

        except Exception as error:
            raise Exception(f"Error getting VIN: {str(error)}")
