from sqlmodel import select, Session
from models import (
    Customer, Cashier, Supplier, Product, Order, OrderItem, Return,
    OrderCreate, OrderItemCreate, OrderUpdate, CustomerCreate, ProductCreate, CashierCreate
)

# ==================== ФУНКЦИИ АВТОМАТИЧЕСКОГО ПЕРЕСЧЁТА ====================

def recalculate_order_total(session: Session, order_id: int):
    """Автоматический пересчёт суммы заказа на основе товаров"""
    order_items = get_order_items_by_order_id(session, order_id)
    total = 0.0
    
    for item in order_items:
        total += item.quantity * item.unit_price
    
    # Обновляем сумму заказа
    order = get_order_by_id(session, order_id)
    if order:
        order.total_amount = total
        session.add(order)
        session.commit()
        session.refresh(order)
    
    return total

# ==================== ФУНКЦИИ ЧТЕНИЯ ====================

def get_all_customers(session: Session):
    return session.exec(select(Customer)).all()

def get_all_cashiers(session: Session):
    return session.exec(select(Cashier)).all()

def get_all_suppliers(session: Session):
    return session.exec(select(Supplier)).all()

def get_all_products(session: Session):
    return session.exec(select(Product)).all()

def get_all_orders(session: Session):
    return session.exec(select(Order)).all()

def get_all_order_items(session: Session):
    return session.exec(select(OrderItem)).all()

def get_all_returns(session: Session):
    return session.exec(select(Return)).all()

def get_products_by_category(session: Session, category: str):
    return session.exec(select(Product).where(Product.category == category)).all()

def get_orders_by_status(session: Session, status: str):
    return session.exec(select(Order).where(Order.status == status)).all()

def get_cashiers_by_shift(session: Session, shift: str):
    return session.exec(select(Cashier).where(Cashier.shift == shift)).all()

def get_order_items_by_order_id(session: Session, order_id: int):
    return session.exec(select(OrderItem).where(OrderItem.order_id == order_id)).all()

def get_customer_by_id(session: Session, customer_id: int):
    return session.exec(select(Customer).where(Customer.id == customer_id)).first()

def get_product_by_id(session: Session, product_id: int):
    return session.exec(select(Product).where(Product.id == product_id)).first()

def get_order_by_id(session: Session, order_id: int):
    return session.exec(select(Order).where(Order.id == order_id)).first()

def get_cashier_by_id(session: Session, cashier_id: int):
    return session.exec(select(Cashier).where(Cashier.id == cashier_id)).first()

# ==================== ФУНКЦИИ СОЗДАНИЯ, ОБНОВЛЕНИЯ, УДАЛЕНИЯ ====================

def create_order(session: Session, order_data: OrderCreate):
    """Создание заказа с автоматической установкой суммы = 0"""
    db_order = Order(**order_data.dict(), total_amount=0.0)
    session.add(db_order)
    session.commit()
    session.refresh(db_order)
    return db_order

def create_order_item(session: Session, order_item_data: OrderItemCreate):
    """Добавление товара в заказ с автоматическим пересчётом суммы"""
    db_order_item = OrderItem(**order_item_data.dict())
    session.add(db_order_item)
    session.commit()
    session.refresh(db_order_item)
    
    # Автоматически пересчитываем сумму заказа
    recalculate_order_total(session, order_item_data.order_id)
    
    return db_order_item

def delete_order_item(session: Session, order_item_id: int):
    """Удаление товара из заказа с пересчётом суммы"""
    order_item = session.exec(select(OrderItem).where(OrderItem.id == order_item_id)).first()
    if order_item:
        order_id = order_item.order_id
        session.delete(order_item)
        session.commit()
        # Пересчитываем сумму после удаления
        recalculate_order_total(session, order_id)
        return True
    return False

def create_customer(session: Session, customer_data: CustomerCreate):
    db_customer = Customer(**customer_data.dict())
    session.add(db_customer)
    session.commit()
    session.refresh(db_customer)
    return db_customer

def create_product(session: Session, product_data: ProductCreate):
    db_product = Product(**product_data.dict())
    session.add(db_product)
    session.commit()
    session.refresh(db_product)
    return db_product

def create_cashier(session: Session, cashier_data: CashierCreate):
    db_cashier = Cashier(**cashier_data.dict())
    session.add(db_cashier)
    session.commit()
    session.refresh(db_cashier)
    return db_cashier

def update_order_status(session: Session, order_id: int, new_status: str):
    db_order = get_order_by_id(session, order_id)
    if db_order:
        db_order.status = new_status
        session.add(db_order)
        session.commit()
        session.refresh(db_order)
    return db_order

def cancel_order(session: Session, order_id: int):
    return update_order_status(session, order_id, "cancelled")

def complete_order(session: Session, order_id: int):
    return update_order_status(session, order_id, "completed")

def delete_order(session: Session, order_id: int):
    db_order = get_order_by_id(session, order_id)
    if db_order:
        session.delete(db_order)
        session.commit()
        return True
    return False

def delete_customer(session: Session, customer_id: int):
    customer = get_customer_by_id(session, customer_id)
    if customer:
        session.delete(customer)
        session.commit()
        return True
    return False

def delete_product(session: Session, product_id: int):
    product = get_product_by_id(session, product_id)
    if product:
        session.delete(product)
        session.commit()
        return True
    return False

def delete_cashier(session: Session, cashier_id: int):
    cashier = get_cashier_by_id(session, cashier_id)
    if cashier:
        session.delete(cashier)
        session.commit()
        return True
    return False