import requests
from .utils import (
    get_addresses_info,
    get_emails_info,
    get_phones_info,
)
from .config import get_API_config
from .data_models import Transaction, Loan, Lien, Foreclosure, Mortgage, Person


class API:
    def __init__(self, session, data):
        self.session = session
        self.DATA = data
        (
            self.zillow_base_url,
            self.zillow_username,
            self.zillow_password,
            self.propstream_base_url,
            self.propstream_username,
            self.propstream_password,
            self.propstream_login_url,
            self.tracers_base_url,
            self.tracers_username,
            self.tracers_password,
        ) = get_API_config()

        session.authenticate()

    def _get_headers(self, service):
        headers = (
            {
                "X-RapidAPI-Host": self.zillow_username,
                "X-RapidAPI-Key": self.zillow_password,
            }
            if service == "zillow"
            else {
                "accept": "application/json",
                "content-type": "application/json",
                "galaxy-ap-name": self.tracers_username,
                "galaxy-ap-password": self.tracers_password,
                "galaxy-search-type": "BackgroundReport",
            }
        )
        return headers

    def _parse_lot_size(self, data):
        lot_size = data.get("resoFacts", {}).get("lotSize")
        return float(lot_size.split()[0].replace(",", "")) if lot_size else None

    def _person_search(self, payload):
        url = self.tracers_base_url
        headers = self._get_headers("tracers")
        response = requests.post(url, json=payload, headers=headers)
        return response.json()

    def _parse_propstream_result(self, result):
        json_array = result["properties"][0]
        transactions = json_array.get("transactions", [])
        loans = json_array.get("activeLoans", [])
        liens = json_array.get("liens", [])
        mortgages = json_array.get("mortgages", [])
        foreclosures = json_array.get("foreclosures", [])
        owners = self._extract_owners(json_array)
        property_data = {
            "propstream_address": json_array["address"].get("streetAddress"),
            "propstream_unit": json_array["address"].get("unitNumber"),
            "propstream_city": json_array["address"].get("cityName"),
            "propstream_state": json_array["address"].get("stateCode"),
            "propstream_zip": json_array["address"].get("zip"),
            "county": json_array["address"].get("countyName"),
            "latitude": json_array.get("latitude"),
            "longitude": json_array.get("longitude"),
            "mailing_address": json_array.get("mailAddress", {}).get("streetAddress"),
            "mailing_city": json_array.get("mailAddress", {}).get("cityName"),
            "mailing_state": json_array.get("mailAddress", {}).get("stateCode"),
            "mailing_zip": json_array.get("mailAddress", {}).get("zip"),
            "est_remaining_balance": json_array.get("openMortgageBalance", 0),
            "property_type": json_array.get("landUse"),
            "vacant": json_array.get("vacant"),
            "owner_occupied": json_array.get("owner_occupied"),
            "occupancy": json_array.get("occupancy"),
            "owners": owners,
            "transactions": [
                Transaction(**transaction) for transaction in transactions
            ],
            "loans": [Loan(**loan) for loan in loans],
            "liens": [Lien(**lien) for lien in liens],
            "mortgages": [Mortgage(**mortgage) for mortgage in mortgages],
            "foreclosures": [
                Foreclosure(**foreclosure) for foreclosure in foreclosures
            ],
        }
        return property_data

    def _extract_owners(self, json_array):
        owners = [
            {
                "first_name": json_array.get("owner1FirstName"),
                "middle_name": json_array.get("owner1MiddleName", [None])[0],
                "last_name": json_array.get("owner1LastName"),
            },
            {
                "first_name": json_array.get("owner2FirstName"),
                "middle_name": json_array.get("owner2MiddleName", [None])[0],
                "last_name": json_array.get("owner2LastName"),
            },
        ]
        return [owner for owner in owners if any(owner.values())]

    def get_zillow_output(self, address):
        try:
            url = f"{self.zillow_base_url}?address={address}"
            headers = self._get_headers("zillow")
            response = requests.get(url, headers=headers)
            data = response.json()
            if not data:
                return None

            status = data.get("homeStatus")
            if status:
                if status == "OTHER":
                    status = "OFF_MARKET"

            broker = (
                data.get("brokerageName").upper() if data.get("brokerageName") else None
            )
            price = data.get("price") if data.get("price") else 0
            zestimate = data.get("zestimate") if data.get("zestimate") else 0
            zestimate = max(price, zestimate)

            zestimateLowPercent = (
                data.get("zestimateLowPercent", 0)
                if data.get("zestimateLowPercent", 0)
                else 0
            )
            if not zestimate:
                zestimate = 0

            url = data.get("url")

            if broker == "AUCTION.COM":
                status = "AUCTION"

            return {
                "zestimate": zestimate,
                "zestimate_low": zestimate * (100 - int(zestimateLowPercent)) / 100,
                "beds": data.get("bedrooms", 0),
                "baths": data.get("bathrooms", 0),
                "status": status,
                "square_footage": data.get("livingAreaValue", 0),
                "year_built": data.get("yearBuilt", 0),
                "zillow_link": f"https://www.zillow.com{url}" if url else None,
            }
        except:
            return None

    def get_propstream_output(self, address):
        try:
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                "Referer": "https://login.propstream.com/",
            }

            session = requests.session()
            session.headers.update(headers)

            login_result = session.post(
                self.propstream_login_url,
                data={
                    "username": self.propstream_username,
                    "password": self.propstream_password,
                },
            )

            auth_token = (
                session.get(
                    f"{self.propstream_base_url}eqbackend/resource/auth?t={login_result.url.split('=')[1]}"
                )
                .json()
                .get("authToken")
            )
            session.headers["X-Auth-Token"] = auth_token
            suggestion = session.get(
                f"{self.propstream_base_url}eqbackend/resource/auth/ps4/property/suggestionsnew?q={address}"
            ).json()
            property_id = suggestion[0].get("id")
            address_type = suggestion[0].get("type")

            result = session.get(
                f"{self.propstream_base_url}eqbackend/resource/auth/ps4/property?id={property_id}&addressType={address_type}"
            ).json()
            session.get(f"{self.propstream_base_url}/logout")

            return self._parse_propstream_result(result)
        except:
            return None

    def get_tracer_output(
        self, first_name, middle_name, last_name, address, city, state, zip
    ):
        try:
            payload = {
                "firstName": first_name or "",
                "middleName": middle_name or "",
                "lastName": last_name or "",
                "Addresses": [
                    {"AddressLine1": address, "AddressLine2": f"{state} {zip}"}
                ],
            }
            data = self._person_search(payload).get("persons", [])
            latitude = self.DATA.latitude
            longitude = self.DATA.longitude

            def get_person_info(
                person, person_type, relation_type, latitude, longitude
            ):
                return Person(
                    **{
                        "tahoeId": person["tahoeId"],
                        "first_name": person["name"]["firstName"],
                        "middle_name": person["name"]["middleName"],
                        "last_name": person["name"]["lastName"],
                        "date_of_birth": person.get("dob", None),
                        "age": person.get("age", None),
                        "person_type": person_type,
                        "relationship_to_owner": relation_type,
                        "is_decedent": person.get("deathRecords", {}).get(
                            "isDeceased", None
                        ),
                        "date_of_death": person.get("dod", None),
                        "emails": get_emails_info(person.get("emailAddresses")),
                        "phone_numbers": get_phones_info(person.get("phoneNumbers")),
                        "addresses": get_addresses_info(
                            person.get("addresses"), person_type, latitude, longitude
                        ),
                    }
                )

            def process_individuals(entities, role):
                results = [
                    result
                    for entity in entities
                    if (
                        result := get_person_info(
                            entity, role, None, latitude, longitude
                        )
                    )
                    and (role != "Neighbor" or result.model_dump().get("addresses"))
                ]
                return results

            persons = []
            for person in data:
                persons.extend(process_individuals([person], "Owner"))
                persons.extend(
                    process_individuals(person.get("relatives", []), "Relative")
                )
                persons.extend(
                    process_individuals(person.get("associates", []), "Associate")
                )
                for address in person.get("addresses", []):
                    persons.extend(
                        process_individuals(address.get("neighbors", []), "Neighbor")
                    )

            return persons
        except:
            return None
