from typing import Tuple
from pymonad.tools import curry
from pyfuncify import fn

"""
+ UBS wants primary listing venue for jurisdiction
"""

class FinancialProduct:

    @staticmethod
    @curry(2)
    def has_listing_at_jur(jur, listing):
        return listing.at_jurisdiction(jur)

    def __init__(self,
                 id,
                 asset_class,
                 cfi_code,
                 gics_class,
                 sedol,
                 isin,
                 permid,
                 openfigi_id,
                 listings):
        self.id = id
        self.asset_class = asset_class
        self.cfi_code = cfi_code
        self.gics_class = gics_class
        self.sedol = sedol
        self.isin = isin
        self.permid = permid
        self.openfigi_id = openfigi_id
        self.listings = listings

    def for_listed_jurisdiction(self, jur):
        listing = fn.find(self.__class__.has_listing_at_jur(jur), self.listings)
        return (self, listing)


class TradingVenue:
    def __init__(self, name, iso20222_op_mic, iso20222_mic, trading_jurisdiction):
        self.name = name
        self.iso20222_op_mic = iso20222_op_mic
        self.iso20222_mic = iso20222_mic
        self.trading_jurisdiction = trading_jurisdiction

    def at_geo_jurisdiction(self):
        return self.trading_jurisdiction.iso3166_country_code

class TradingJurisdiction:

    def __init__(self, handle):
        self.handle = handle


class Instrument:

    def __init__(self, symbol):
        self.symbol = symbol

class Listing(Instrument):
    def __init__(self, id, listing_identity, symbol):
        super().__init__(symbol)
        self.id = id
        self.listing_identity = listing_identity

class VenueListing(Listing):

    def __init__(self, id, listing_identity, symbol, listed_at: TradingVenue):
        super().__init__(id, listing_identity, symbol)
        self.listed_at = listed_at

    def at_jurisdiction(self, jur):
        # TODO: jurisdiction is defined as a 3166 str, it needs to be an object with type
        return jur == self.listed_at.at_geo_jurisdiction()
        # return jur in list(map(lambda listing: listing.at_geo_jurisdiction(), self.listed_at))

    def sane_price(self, price) -> Tuple[str, str]:
        outcome = self.to_outcome((float(price['price']) <= self.current_price() + 0.1) and (float(price['price']) >= self.current_price() - 0.1))
        return outcome, ""

    def valid_expiry(self, expiry) -> Tuple[str, str]:
        return 'success', ""

    def valid_price_tick(self, price) -> Tuple[str, str]:
        return 'success', ""


    def current_price(self):
        return 10.2

    def to_outcome(self, test: bool) -> str:
        return 'success' if test else "failure"

class ChannelListing(Listing):
    pass



class Market(TradingVenue):

    def __init__(self, name, iso20222_op_mic, iso20222_mic, trading_jurisdiction):
        super().__init__(name, iso20222_op_mic, iso20222_mic, trading_jurisdiction)


class GeographicJurisdiction(TradingJurisdiction):

    def __init__(self, handle, iso3166_country_code):
        super().__init__(handle)
        self.iso3166_country_code = iso3166_country_code


class JurisdictionBroker:
    pass

class TradingChannel:
    pass

