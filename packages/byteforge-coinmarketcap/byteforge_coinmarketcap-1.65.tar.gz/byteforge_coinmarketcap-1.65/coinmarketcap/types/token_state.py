from dataclasses import dataclass, field
from typing import List, Optional, Dict
import time
import datetime
import json

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import datetime
from dateutil import parser

from dataclasses import dataclass
from typing import Optional
import datetime

@dataclass
class Quote:
    base_currency: str
    price: float
    volume_24h: float
    percent_change_1h: float
    percent_change_24h: float
    percent_change_7d: float
    percent_change_30d: float
    market_cap: float
    last_updated: datetime.datetime

    # Now all optional/default parameters follow
    volume_change_24h: float = 0.0
    percent_change_60d: float = 0.0
    percent_change_90d: float = 0.0
    market_cap_dominance: float = 0.0
    fully_diluted_market_cap: float = 0.0
    tvl: Optional[float] = None
    volume_30d: Optional[float] = None
    volume_30d_reported: Optional[float] = None
    volume_24h_reported: Optional[float] = None
    volume_7d_reported: Optional[float] = None
    market_cap_by_total_supply: Optional[float] = None
    volume_7d: Optional[float] = None
    total_supply: Optional[float] = None
    circulating_supply: Optional[float] = None

    @staticmethod
    def from_dict(currency: str, dct_quote_data: Dict) -> 'Quote':


        if 'price' not in dct_quote_data:
            print(f"Payload: {json.dumps(dct_quote_data, indent=4)}")
            raise ValueError("Payload must contain 'price' field.")

        # insure integers are handled as floats (so 1 becomes 1.0)
        dct_quote_data['price'] = float(dct_quote_data['price'])
        dct_quote_data['market_cap'] = float(dct_quote_data['market_cap'])


        # Handle both 'last_updated' and 'timestamp' for the last_updated field
        if 'last_updated' in dct_quote_data:
            last_updated_str = dct_quote_data['last_updated']
        elif 'timestamp' in dct_quote_data:
            last_updated_str = dct_quote_data['timestamp']
        else:
            raise ValueError("Payload must contain either 'last_updated' or 'timestamp' field.")

        # Remove both possible keys to avoid errors in the constructor
        dct_quote_data.pop('last_updated', None)
        dct_quote_data.pop('timestamp', None)

        last_updated = parser.parse(last_updated_str)
        
        return Quote(base_currency=currency, last_updated=last_updated, **dct_quote_data)


@dataclass
class TokenState:
    id: int
    name: str
    symbol: str
    last_updated: datetime.datetime
    quote_map: Dict[str, Quote]

    timestamp: int = int(time.time())
    infinite_supply: bool = None
    slug: Optional[str] = None
    num_market_pairs: Optional[int] = None
    date_added: Optional[datetime.datetime] = None
    tags: Optional[List[str]] = None
    max_supply: Optional[int] = None
    circulating_supply: Optional[int] = None
    total_supply: Optional[float] = None
    platform: Optional[str] = None
    cmc_rank: Optional[int] = None
    self_reported_circulating_supply: Optional[int] = None
    self_reported_market_cap: Optional[float] = None
    tvl_ratio: Optional[float] = None
    is_market_cap_included_in_calc: Optional[bool] = None
    is_active: Optional[bool] = None
    is_fiat: Optional[bool] = None


    @staticmethod
    def from_dict(data: Dict) -> 'TokenState':
        data = data.copy()

        # Convert 'is_market_cap_included_in_calc' from 0/1 to False/True
        if 'is_market_cap_included_in_calc' in data:
            data['is_market_cap_included_in_calc'] = bool(data['is_market_cap_included_in_calc'])

        quote_map = {}
        dct_quote_data = data.pop('quote')
        for currency, dct_quote_data in dct_quote_data.items():
            quote_map[currency] = Quote.from_dict(currency, dct_quote_data)
        data['quote_map'] = quote_map

        # Set optional attributes to None if not present in the data
        optional_fields = [
            'num_market_pairs', 'date_added', 'tags', 'max_supply', 'circulating_supply',
            'total_supply', 'platform', 'cmc_rank', 'self_reported_circulating_supply',
            'self_reported_market_cap', 'tvl_ratio'
        ]

        for attr_name in optional_fields:
            if attr_name not in data:
                data[attr_name] = None

        return TokenState(**data)

