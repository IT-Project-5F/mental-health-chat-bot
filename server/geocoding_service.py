import re
import requests
import time
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class AddressGeocoder:
    """Service for extracting addresses and converting them to coordinates"""

    def __init__(self):
        self.nominatim_base_url = "https://nominatim.openstreetmap.org/search"
        self.rate_limit_delay = 1.0  # Nominatim requires 1 request per second

    def extract_addresses_from_response(self, rag_response: str) -> List[Dict[str, str]]:
        """
        Extract address information from RAG response text
        Returns list of address dictionaries with parsed components
        """
        addresses = []

        # Pattern to match "Address: [address], [suburb] [state] [postcode]"
        address_pattern = r'Address:\s*([^,\n]+)(?:,\s*([^,\n]+?))?(?:\s+([A-Z]{2,3}))?\s*(\d{4})?'

        matches = re.finditer(address_pattern, rag_response, re.MULTILINE)

        for match in matches:
            address_dict = {
                'street': match.group(1).strip() if match.group(1) else '',
                'suburb': match.group(2).strip() if match.group(2) else '',
                'state': match.group(3).strip() if match.group(3) else '',
                'postcode': match.group(4).strip() if match.group(4) else '',
                'full_address': match.group(0).replace('Address:', '').strip()
            }
            addresses.append(address_dict)

        return addresses

    def extract_addresses_from_service_data(self, service_data: List[Dict]) -> List[Dict[str, str]]:
        """
        Extract address information from structured service data
        """
        addresses = []

        logger.info(f"Extracting addresses from {len(service_data)} services")

        for service in service_data:
            logger.info(f"Service data: {service}")
            if service.get('address'):
                address_dict = {
                    'street': service.get('address', ''),
                    'suburb': service.get('suburb', ''),
                    'state': service.get('state', ''),
                    'postcode': service.get('postcode', ''),
                    'organisation': service.get('organisation_name', ''),
                    'service_name': service.get('service_name', ''),
                    'full_address': self._build_full_address(service)
                }
                logger.info(f"Created address: {address_dict}")
                addresses.append(address_dict)

        logger.info(f"Extracted {len(addresses)} addresses")
        return addresses

    def _build_full_address(self, service: Dict) -> str:
        """Build a complete address string from service components"""
        parts = []

        if service.get('address'):
            # Clean up address (remove trailing commas)
            address = str(service['address']).strip().rstrip(',')
            parts.append(address)
        if service.get('suburb'):
            parts.append(str(service['suburb']).strip())
        if service.get('state'):
            parts.append(str(service['state']).strip())
        if service.get('postcode'):
            # Convert to string and remove .0 suffix if present
            postcode = str(service['postcode']).strip()
            if postcode.endswith('.0'):
                postcode = postcode[:-2]
            parts.append(postcode)

        return ', '.join(parts)

    async def geocode_address(self, address: str, country_code: str = 'AU') -> Optional[Tuple[float, float]]:
        """
        Convert address to latitude/longitude coordinates using Nominatim
        Returns (latitude, longitude) tuple or None if not found
        """
        try:
            params = {
                'q': address,
                'format': 'json',
                'countrycodes': country_code,
                'limit': 1,
                'addressdetails': 1
            }

            headers = {
                'User-Agent': 'MentalHealthChatBot/1.0 (mental.health.app@example.com)'
            }

            response = requests.get(
                self.nominatim_base_url,
                params=params,
                headers=headers,
                timeout=10
            )

            # Rate limiting for Nominatim
            time.sleep(self.rate_limit_delay)

            if response.status_code == 200:
                data = response.json()
                if data:
                    lat = float(data[0]['lat'])
                    lon = float(data[0]['lon'])
                    logger.info(f"Geocoded '{address}' to ({lat}, {lon})")
                    return (lat, lon)

            logger.warning(f"Could not geocode address: {address}")
            return None

        except Exception as e:
            logger.error(f"Error geocoding address '{address}': {str(e)}")
            return None

    async def process_addresses_to_coordinates(self, addresses: List[Dict[str, str]]) -> List[Dict]:
        """
        Convert list of addresses to coordinates and return map markers
        """
        markers = []

        for i, addr in enumerate(addresses):
            coordinates = await self.geocode_address(addr['full_address'])

            if coordinates:
                marker = {
                    'id': i + 1,
                    'position': [coordinates[0], coordinates[1]],  # [lat, lng]
                    'title': f"{addr.get('organisation', 'Unknown')} - {addr.get('service_name', 'Service')}",
                    'address': addr['full_address'],
                    'details': {
                        'organisation': addr.get('organisation', ''),
                        'service_name': addr.get('service_name', ''),
                        'street': addr.get('street', ''),
                        'suburb': addr.get('suburb', ''),
                        'state': addr.get('state', ''),
                        'postcode': addr.get('postcode', '')
                    }
                }
                markers.append(marker)

        return markers

# Global instance
geocoder = AddressGeocoder()

async def extract_and_geocode_from_response(rag_response: str) -> List[Dict]:
    """
    Async function to extract addresses from RAG response and convert to map markers
    """
    addresses = geocoder.extract_addresses_from_response(rag_response)
    markers = await geocoder.process_addresses_to_coordinates(addresses)
    return markers

async def extract_and_geocode_from_service_data(service_data: List[Dict]) -> List[Dict]:
    """
    Async function to extract addresses from service data and convert to map markers
    """
    addresses = geocoder.extract_addresses_from_service_data(service_data)
    markers = await geocoder.process_addresses_to_coordinates(addresses)
    return markers