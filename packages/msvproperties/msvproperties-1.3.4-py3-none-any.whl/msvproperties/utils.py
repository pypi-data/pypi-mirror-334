import usaddress
import re
from datetime import datetime
from duckduckgo_search import DDGS
from geopy.distance import geodesic
from .data_models import Phone, Email

def get_phones_info(phones):
    if not phones:
        return []

    extracted_info = []
    for phone in phones:
        extracted_phone = extract_phone_info(phone)
        if extracted_phone not in extracted_info:
            extracted_info.append(extracted_phone)
    return extracted_info


def extract_phone_info(phone):
    return Phone(
        phone_number=phone.get("phoneNumber"),
        phone_type=phone.get("phoneType"),
        is_connected=phone.get("isConnected"),
    )


def get_emails_info(emails):
    if not emails:
        return []

    extracted_info = []
    for email in emails:
        extracted_email = extract_email_info(email)
        if extracted_email not in extracted_info:
            extracted_info.append(extracted_email)
    return extracted_info


def extract_email_info(email):
    return Email(email_address=email.get("emailAddress"))


def extract_address_info(address):
    return {
        "address_line": address.get("fullAddress"),
        "city": address.get("city"),
        "state": address.get("state"),
        "zip_code": address.get("zip"),
        "first_reported_date": fix_date_fields(address.get("firstReportedDate")),
        "last_reported_date": fix_date_fields(address.get("lastReportedDate")),
        "public_first_seen_date": fix_date_fields(address.get("publicFirstSeenDate")),
        "total_first_seen_date": fix_date_fields(address.get("totalFirstSeenDate")),
        "latitude": address.get("latitude"),
        "longitude": address.get("longitude"),
    }

def convert_types(address, abbreviations):
    pattern = re.compile(r'\b(' + '|'.join(map(re.escape, abbreviations.keys())) + r')\b', re.IGNORECASE)
    
    def replace_match(match):
        full_name = match.group(0)
        return abbreviations.get(full_name.title(), full_name)

    return pattern.sub(replace_match, address)

def get_addresses_info(addresses, person_type, latitude, longitude):
    if not addresses:
        return []

    processed_coordinates = set()
    extracted_info = []

    for address in addresses:
        addr_latitude = address.get("latitude")
        addr_longitude = address.get("longitude")

        if (addr_latitude, addr_longitude) in processed_coordinates:
            continue

        processed_coordinates.add((addr_latitude, addr_longitude))
        extracted_address = extract_address_info(address)

        if person_type in ["Neighbor", "Owner"]:
            if (
                is_property_too_close(
                    latitude, longitude, addr_latitude, addr_longitude, 150
                )
                and extracted_address not in extracted_info
            ):
                extracted_info.append(extracted_address)
        else:
            extracted_info.append(extracted_address)

    return extracted_info


def camel_to_snake(name: str) -> str:
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def fix_date_fields(date_input):
    if not date_input:
        return None

    if isinstance(date_input, datetime):
        return date_input.strftime("%Y-%m-%d")

    if isinstance(date_input, (int, float)):
        try:
            return datetime.fromtimestamp(date_input / 1000).strftime("%Y-%m-%d")
        except (ValueError, OSError):
            return None

    date_input = date_input = re.sub(r"(\d+)(st|nd|rd|th)", r"\1", date_input)
    if isinstance(date_input, str):
        date_formats = [
            "%A, %b %d, %Y",
            "%Y-%m-%d",
            "%d-%m-%Y",
            "%m-%d-%Y",
            "%d/%m/%Y",
            "%m/%d/%Y",
            "%Y/%m/%d",
            "%b %d, %Y",
            "%B %d, %Y",
            "%d %b %Y",
            "%d %B %Y",
            "%Y.%m.%d",
            "%d.%m.%Y",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
            "%d-%m-%Y %H:%M:%S",
            "%m-%d-%Y %H:%M:%S",
            "%d/%m/%Y %H:%M:%S",
            "%m/%d/%Y %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%m/%d/%Y %H:%M",
            "%A, %B %d, %Y at %I:%M %p",
        ]
        for fmt in date_formats:
            try:
                return datetime.strptime(date_input, fmt).strftime("%Y-%m-%d")
            except ValueError:
                continue

    return None


def search_in_web(text):
    results = DDGS().text(text, max_results=5)
    return results


def smart_reformat_address(address):
    try:
        prompt = f"""
        you are an expert in cleaning and converting us addresses and you must only return the final address ,
        this is extra information about this address in web : {search_in_web(address)} ,
        convert all ordinal numbers to numbers and convert all numbers to digits and convert all formal format to street abbreviations,
        reformat this us address and use extra information if address is incomplete: {address} 
        to us formal format like :
        street address #(unit or apt number only number), city, state zipcode .
        attention to the spaces in the sample format.
        """
        result = DDGS().chat(prompt, model="gpt-4o-mini")
        return result
    except:
        return reformat_address(address)


def reformat_address(address):
    try:
        parsed_address = usaddress.tag(address)[0]
        occupancy_identifier = ""
        street_name_post_type = parsed_address.get("StreetNamePostType", "")
        if parsed_address.get("OccupancyIdentifier"):
            occupancy_identifier = (
                f"{parsed_address.get('OccupancyIdentifier','').strip()},"
            )
            if not occupancy_identifier.startswith("#"):
                occupancy_identifier = "#" + occupancy_identifier
            else:
                occupancy_identifier = occupancy_identifier.replace("# ", "#")
        else:
            street_name_post_type += ","

        formatted_address = " ".join(
            [
                parsed_address.get("AddressNumber", ""),
                parsed_address.get("StreetName", ""),
                street_name_post_type,
                occupancy_identifier,
                parsed_address.get("PlaceName", "") + ",",
                parsed_address.get("StateName", ""),
                parsed_address.get("ZipCode", ""),
            ]
        )
        formatted_address = " ".join(formatted_address.split())
        return ", ".join(i.strip() for i in formatted_address.split(","))

    except:
        return None


def convert_camel_to_snake(obj):
    if isinstance(obj, list):
        return [convert_camel_to_snake(item) for item in obj]
    elif isinstance(obj, dict):
        return {
            camel_to_snake(key): convert_camel_to_snake(value)
            for key, value in obj.items()
        }
    else:
        return obj


def is_property_too_close(
    target_lat, target_lon, property_lat, property_lon, max_distance_m
):
    target = (target_lat, target_lon)
    property = (property_lat, property_lon)
    distance = geodesic(target, property).m
    if distance > max_distance_m:
        return False
    return True


def extract_number(s):
    if not s:
        return None
    if isinstance(s, (int, float)):
        return s
    match = re.search(r"[\d,]+(?:\.\d+)?", s)
    if match:
        return float(match.group(0).replace(",", ""))
    return None
