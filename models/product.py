from datetime import datetime
from typing import List

import ulid
from pydantic import BaseModel, EmailStr, Field


class Product(BaseModel):
    id: str = Field(default_factory=lambda: str(ulid.new()), description="Product ulid")
    name: str = Field(description="Product name")
    description: str = Field(description="Product description")
    price: float = Field(gt=0, description="The price must be greater than zero")
    quantity: int = Field(description="Product quantity")
    active: bool = Field(default=True, description="Product active status")
    created_at: datetime = Field(
        default_factory=datetime.now, description="Create product timestamp"
    )
    updated_at: datetime | None = Field(
        default=None, description="Update product timestamp"
    )


class Customer(BaseModel):
    id: str = Field(
        default_factory=lambda: str(ulid.new()),
        description="Identificador único do cliente no formato ULID.",
    )
    name: str = Field(..., description="Nome do cliente.")
    email: EmailStr = Field(..., description="Endereço de email válido do cliente.")
    active: bool = Field(
        default=True, description="Status do cliente (ativo ou inativo)."
    )
    created_at: datetime = Field(
        default_factory=datetime.now, description="Data de criação do cliente."
    )
    updated_at: datetime | None = Field(
        default=None, description="Data de atualização do cliente."
    )


class ProductAndCustomer(BaseModel):
    products: List[Product]
    customers: List[Customer]
