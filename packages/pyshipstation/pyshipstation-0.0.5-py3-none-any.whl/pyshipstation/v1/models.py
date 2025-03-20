from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ShipStationBaseModel(BaseModel):
    model_config = ConfigDict(extra="ignore", strict=True, populate_by_name=True)


class _ShipStationAddressBase(ShipStationBaseModel):
    name: str = Field(
        ...,
        description="Name of person.",
    )
    company: str = Field(..., description="Name of company.")
    street_1: str = Field(..., description="First line of address.", alias="street1")
    street_2: str = Field(..., description="Second line of address.", alias="street2")
    street_3: str = Field(..., description="Third line of address.", alias="street3")
    city: str = Field(..., description="City.")
    state: str = Field(..., description="State.")
    postal_code: str = Field(
        ...,
        description="Postal Code.",
        alias="postalCode",
    )
    country: str = Field(
        ..., min_length=2, max_length=2, description="Two-letter ISO country code."
    )
    phone: str = Field(..., description="Telephone number.")
    residential: bool | None = Field(
        ...,
        description="Specifies whether the given address is residential.",
    )


class ShipStationAddressCreate(_ShipStationAddressBase):
    pass


class ShipStationAddressRead(_ShipStationAddressBase):
    address_verified: str | None = Field(
        ...,
        description="ShipStation address verification status.",
        alias="addressVerified",
    )


class _ShipStationOrderBase(ShipStationBaseModel):
    order_number: str = Field(
        ...,
        alias="orderNumber",
    )
    order_date: str = Field(
        ...,
        alias="orderDate",
        examples=[
            "2015-06-29T08:46:27.0000000",
        ],
    )
    order_status: str = Field(..., examples=["awaiting_shipment"], alias="orderStatus")
    customer_username: Optional[str] = Field(
        None, examples=["JOEBLOGGS1"], alias="customerUsername"
    )
    customer_email: Optional[str] = Field(
        None, examples=["joe@bloggs.com"], alias="customerEmail"
    )
    bill_to: ShipStationAddressCreate = Field(..., alias="billTo")
    ship_to: ShipStationAddressCreate = Field(..., alias="shipTo")
    items: Optional[list] = Field(
        None,
    )


class ShipStationOrderCreate(_ShipStationOrderBase):
    pass


class ShipStationOrderRead(_ShipStationOrderBase):
    order_id: int = Field(..., alias="orderId", examples=[259162565])
    order_key: str = Field(
        ..., alias="orderKey", examples=["aaabc5462beb41c882cf4222fb965e97"]
    )
    create_date: str = Field(
        ..., alias="createDate", examples=["2025-03-17T08:23:24.1730000"]
    )
    modify_date: str = Field(
        ..., alias="modifyDate", examples=["2025-03-17T08:23:23.9630000"]
    )


class _ShipStationOrderItemBase(ShipStationBaseModel):
    sku: str = Field(..., examples=["GoSwag0005"])
    quantity: int = Field(..., examples=[2])
    name: str = Field(..., examples=["Waterbottle"])


class ShipStationOrderItemRead(_ShipStationOrderItemBase):
    pass


class ShipStationOrderItemCreate(_ShipStationOrderItemBase):
    pass
