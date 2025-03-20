from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ShipStationBaseModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)


class ShipStationOrderCreate(BaseModel):
    pass


class ShipStationAddressBase(ShipStationBaseModel):
    name: str = Field(..., description="Name of person.")
    company: str = Field(..., description="Name of company.")
    street1: str = Field(..., description="First line of address.")
    street2: str = Field(..., description="Second line of address.")
    street3: str = Field(..., description="Third line of address.")
    city: str = Field(..., description="City.")
    state: str = Field(..., description="State.")
    postal_code: str = Field(..., description="Postal Code.", alias="postalCode")
    country: str = Field(
        ..., min_length=2, max_length=2, description="Two-letter ISO country code."
    )
    phone: str = Field(..., description="Telephone number.")
    residential: bool = Field(
        ..., description="Specifies whether the given address is residential."
    )


class ShipStationAddressCreate(ShipStationAddressBase):
    pass


class ShipStationAddressRead(ShipStationAddressBase):
    address_verified: str = Field(
        ...,
        description="ShipStation address verification status.",
        alias="addressVerified",
    )


class ShipStationClient:
    def __init__(
        self,
        api_key,
    ):
        self.api_key = api_key

    def create_order(self, order: ShipStationOrderCreate):
        """
        https://www.shipstation.com/docs/api/orders/create-update-order/
        """
        pass
