import asyncio

from addrx.core.addrx_core import AddrXCore

class AddrX:

    @classmethod
    def single_parser(cls, url: str, address: str, exclude_address_type: list[str] = None):
        """Parse a address using the AddrX service.

        Args:
            url: URL of the Libpostal service.
            address: address to parse.
            exclude_address_type: List of address types to exclude from the output.

        Returns:
            parsed address.
        """
        addrx = AddrXCore(url=url, exclude_address_types=exclude_address_type)
        results = addrx.parse(address)

        return results

    @classmethod
    def parser(cls,url: str, address_list: list[str], exclude_address_type: list[str] = None):
        """Parse a list of addresses using the AddrX service.

        Args:
            url: URL of the Libpostal service.
            address_list: List of addresses to parse.
            exclude_address_type: List of address types to exclude from the output.

        Returns:
            List of parsed addresses.
        """
        addrx = AddrXCore(url=url, exclude_address_types=exclude_address_type)
        results = []

        
        results = list(map(addrx.parse, address_list))


        return results
    
    @classmethod
    def async_parser(cls, url: str, address_list: list[str], exclude_address_type: list[str] = None):
        """Parse a list of addresses asynchronously using the AddrX service.

        Args:
            url: URL of the Libpostal service.
            address_list: List of addresses to parse.
            exclude_address_type: List of address types to exclude from the output.

        Returns:
            List of parsed addresses.
        """

        async def addrx_call(url: str, address_list: list):
            addrx = AddrXCore(url, exclude_address_types=exclude_address_type)
            result = await addrx.async_parse(address_list)

            return result

        result = asyncio.run(addrx_call(url, address_list))

        return result