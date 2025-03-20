import json
from typing import Any, Dict

import shopify

# general GraphQL navigation utilities
from arklex.env.tools.shopify.utils_slots import ShopifySlots, ShopifyOutputs
from arklex.env.tools.shopify.utils import authorify_admin
from arklex.env.tools.shopify.utils_nav import *

from arklex.env.tools.tools import register_tool

description = "Get the details of the collection."
slots = [
    ShopifySlots.COLLECTION_ID,
    *PAGEINFO_SLOTS
]
outputs = [
    ShopifyOutputs.COLLECTIONS_DETAILS,
    *PAGEINFO_OUTPUTS
]
COLLECTION_NOT_FOUND = "error: collection not found"
errors = [COLLECTION_NOT_FOUND]

@register_tool(description, slots, outputs, lambda x: x not in errors)
def get_collection(collection_id: list, **kwargs) -> str:
    nav = cursorify(kwargs)
    if not nav[1]:
        return nav[0]
    auth = authorify_admin(kwargs)
    if auth["error"]:
        return auth["error"]
    
    try:
        with shopify.Session.temp(**auth["value"]):
            response = shopify.GraphQL().execute(f"""
            {{
                collection (id: "{collection_id}") {{
                    title
                    description
                    productsCount {{
                        count
                    }}
                    products ({nav[0]}) {{
                        nodes {{
                            id
                        }}
                        pageInfo {{
                            endCursor
                            hasNextPage
                            hasPreviousPage
                            startCursor
                        }}
                    }}
                }}
            }}
            """)
            results = json.loads(response)["data"]["collection"]
            return results
    except Exception as e:
        return {"content": COLLECTION_NOT_FOUND}