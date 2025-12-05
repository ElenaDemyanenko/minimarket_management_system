from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# Модели таблиц (остаются без изменений)
class Customer(SQLModel, table=True):
    __tablename__ = "customers"
    __table_args__ = {'schema': 'Demyanenko'}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    phone: Optional[str] = Field(max_length=20)
    email: Optional[str] = Field(max_length=100)

class Cashier(SQLModel, table=True):
    __tablename__ = "cashiers"
    __table_args__ = {'schema': 'Demyanenko'}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    full_name: str = Field(max_length=100)
    shift: str = Field(max_length=50)
    username: str = Field(max_length=50)
    password: str = Field(max_length=50)

class Supplier(SQLModel, table=True):
    __tablename__ = "suppliers"
    __table_args__ = {'schema': 'Demyanenko'}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    company_name: str = Field(max_length=100)
    contact_info: Optional[str] = None

class Product(SQLModel, table=True):
    __tablename__ = "products"
    __table_args__ = {'schema': 'Demyanenko'}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(max_length=100)
    category: Optional[str] = Field(max_length=50)
    price: float = Field()
    quantity: int = Field()
    expiration_date: Optional[datetime] = None
    supplier_id: Optional[int] = Field(foreign_key="Demyanenko.suppliers.id")

class Order(SQLModel, table=True):
    __tablename__ = "orders"
    __table_args__ = {'schema': 'Demyanenko'}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="Demyanenko.customers.id")
    cashier_id: int = Field(foreign_key="Demyanenko.cashiers.id")
    total_amount: float = Field()
    status: str = Field(max_length=50)

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"
    __table_args__ = {'schema': 'Demyanenko'}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="Demyanenko.orders.id")
    product_id: int = Field(foreign_key="Demyanenko.products.id")
    quantity: int = Field()
    unit_price: float = Field()

class Return(SQLModel, table=True):
    __tablename__ = "returns"
    __table_args__ = {'schema': 'Demyanenko'}
    
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="Demyanenko.orders.id")
    product_id: int = Field(foreign_key="Demyanenko.products.id")
    amount_refunded: float = Field()

# Модели для создания - ОБНОВЛЕНО!
class OrderCreate(SQLModel):
    customer_id: int
    cashier_id: int
    status: str = "new"
    # total_amount удалён - теперь рассчитывается автоматически

class OrderItemCreate(SQLModel):
    order_id: int
    product_id: int
    quantity: int
    unit_price: float

class OrderUpdate(SQLModel):
    status: Optional[str] = None
    total_amount: Optional[float] = None

class CustomerCreate(SQLModel):
    first_name: str
    last_name: str
    phone: Optional[str] = None
    email: Optional[str] = None

class ProductCreate(SQLModel):
    name: str
    category: Optional[str] = None
    price: float
    quantity: int
    expiration_date: Optional[datetime] = None
    supplier_id: Optional[int] = None

class CashierCreate(SQLModel):
    full_name: str
    shift: str
    username: str
    password: str