from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from database import get_session
from models import (OrderCreate, OrderItemCreate, CustomerCreate, ProductCreate, CashierCreate, OrderUpdate)
from requests import (
    # функции просмотра
    get_all_customers, get_all_cashiers, get_all_suppliers,
    get_all_products, get_all_orders, get_all_order_items,
    get_all_returns, get_products_by_category, get_orders_by_status,
    get_cashiers_by_shift, get_order_items_by_order_id,
    get_customer_by_id, get_product_by_id, get_order_by_id, get_cashier_by_id,
    # функции для операций
    create_order, create_order_item, create_customer, create_product, create_cashier,
    update_order_status, cancel_order, complete_order, delete_order,
    delete_customer, delete_product, delete_cashier, delete_order_item,
    recalculate_order_total
)

app = FastAPI(
    title="Store Management API. Демьяненко Елена",
    version="1.0.0",
    description="Система управления магазином с автоматическим расчётом сумм заказов"
)

@app.get("/")
def read_root():
    return {
        "message": "store management api работает",
        "student": "Демьяненко Елена", 
        "lab": "Минимаркет",
        "feature": "Автоматический расчёт сумм заказов"
    }

# ==================== БЛОК "ПОКУПАТЕЛИ" ====================
@app.get("/customers")
def read_customers(session: Session = Depends(get_session)):
    customers = get_all_customers(session)
    return {"customers": customers, "count": len(customers)}

@app.get("/customers/{customer_id}")
def read_customer(customer_id: int, session: Session = Depends(get_session)):
    customer = get_customer_by_id(session, customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Покупатель не найден")
    return customer

@app.post("/customers")
def create_new_customer(customer: CustomerCreate, session: Session = Depends(get_session)):
    """Создание нового клиента"""
    return create_customer(session, customer)

@app.delete("/customers/{customer_id}")
def delete_customer_endpoint(customer_id: int, session: Session = Depends(get_session)):
    """Удаление покупателя"""
    success = delete_customer(session, customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Покупатель не найден")
    return {"message": f"Покупатель {customer_id} удален"}

# ==================== БЛОК "ТОВАРЫ" ====================
@app.get("/products")
def read_products(session: Session = Depends(get_session)):
    products = get_all_products(session)
    return {"products": products, "count": len(products)}

@app.get("/products/{product_id}")
def read_product(product_id: int, session: Session = Depends(get_session)):
    product = get_product_by_id(session, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return product

@app.post("/products")
def create_new_product(product: ProductCreate, session: Session = Depends(get_session)):
    """Создание нового продукта"""
    return create_product(session, product)

@app.delete("/products/{product_id}")
def delete_product_endpoint(product_id: int, session: Session = Depends(get_session)):
    """Удаление товара"""
    success = delete_product(session, product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Товар не найден")
    return {"message": f"Товар {product_id} удален"}

# ==================== БЛОК "ЗАКАЗЫ" ====================
@app.get("/orders")
def read_orders(session: Session = Depends(get_session)):
    orders = get_all_orders(session)
    return {"orders": orders, "count": len(orders)}

@app.get("/orders/{order_id}")
def read_order(order_id: int, session: Session = Depends(get_session)):
    order = get_order_by_id(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return order

@app.post("/orders")
def create_new_order(order: OrderCreate, session: Session = Depends(get_session)):
    """Создание нового заказа (сумма рассчитывается автоматически)"""
    return create_order(session, order)

@app.put("/orders/{order_id}/status")
def update_order_status_endpoint(order_id: int, new_status: str, session: Session = Depends(get_session)):
    """Обновление статуса заказа"""
    order = update_order_status(session, order_id, new_status)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {"message": f"Статус заказа {order_id} изменен на '{new_status}'", "order": order}

@app.put("/orders/{order_id}/cancel")
def cancel_order_endpoint(order_id: int, session: Session = Depends(get_session)):
    """Отмена заказа"""
    order = cancel_order(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {"message": f"Заказ {order_id} отменен", "order": order}

@app.put("/orders/{order_id}/complete")
def complete_order_endpoint(order_id: int, session: Session = Depends(get_session)):
    """Завершение заказа"""
    order = complete_order(session, order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {"message": f"Заказ {order_id} завершен", "order": order}

@app.delete("/orders/{order_id}")
def delete_order_endpoint(order_id: int, session: Session = Depends(get_session)):
    """Удаление заказа"""
    success = delete_order(session, order_id)
    if not success:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return {"message": f"Заказ {order_id} удален"}

# ==================== БЛОК "ПОЗИЦИИ ЗАКАЗА" ====================
@app.get("/order-items")
def read_order_items(session: Session = Depends(get_session)):
    order_items = get_all_order_items(session)
    return {"order_items": order_items, "count": len(order_items)}

@app.post("/order-items")
def create_new_order_item(order_item: OrderItemCreate, session: Session = Depends(get_session)):
    """Добавление товара в заказ (сумма пересчитывается автоматически)"""
    return create_order_item(session, order_item)

@app.delete("/order-items/{order_item_id}")
def delete_order_item_endpoint(order_item_id: int, session: Session = Depends(get_session)):
    """Удаление товара из заказа (сумма пересчитывается автоматически)"""
    success = delete_order_item(session, order_item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Позиция заказа не найдена")
    return {"message": f"Товар {order_item_id} удален из заказа"}

# ==================== БЛОК "КАССИРЫ" ====================
@app.get("/cashiers")
def read_cashiers(session: Session = Depends(get_session)):
    cashiers = get_all_cashiers(session)
    return {"cashiers": cashiers, "count": len(cashiers)}

@app.get("/cashiers/{cashier_id}")
def read_cashier(cashier_id: int, session: Session = Depends(get_session)):
    cashier = get_cashier_by_id(session, cashier_id)
    if not cashier:
        raise HTTPException(status_code=404, detail="Кассир не найден")
    return cashier

@app.post("/cashiers")
def create_new_cashier(cashier: CashierCreate, session: Session = Depends(get_session)):
    """Создание нового кассира"""
    return create_cashier(session, cashier)

@app.delete("/cashiers/{cashier_id}")
def delete_cashier_endpoint(cashier_id: int, session: Session = Depends(get_session)):
    """Удаление кассира"""
    success = delete_cashier(session, cashier_id)
    if not success:
        raise HTTPException(status_code=404, detail="Кассир не найден")
    return {"message": f"Кассир {cashier_id} удален"}

# ==================== ФИЛЬТРЫ И СПЕЦИАЛЬНЫЕ ЗАПРОСЫ ====================
@app.get("/products/category/{category}")
def read_products_by_category(category: str, session: Session = Depends(get_session)):
    products = get_products_by_category(session, category)
    return {"products": products, "category": category, "count": len(products)}

@app.get("/orders/status/{status}")
def read_orders_by_status(status: str, session: Session = Depends(get_session)):
    orders = get_orders_by_status(session, status)
    return {"orders": orders, "status": status, "count": len(orders)}

@app.get("/cashiers/shift/{shift}")
def read_cashiers_by_shift(shift: str, session: Session = Depends(get_session)):
    cashiers = get_cashiers_by_shift(session, shift)
    return {"cashiers": cashiers, "shift": shift, "count": len(cashiers)}

@app.get("/orders/{order_id}/items")
def read_order_items_by_order(order_id: int, session: Session = Depends(get_session)):
    order_items = get_order_items_by_order_id(session, order_id)
    return {"order_id": order_id, "items": order_items, "count": len(order_items)}

# ==================== ДОПОЛНИТЕЛЬНЫЕ СУЩНОСТИ ====================
@app.get("/suppliers")
def read_suppliers(session: Session = Depends(get_session)):
    suppliers = get_all_suppliers(session)
    return {"suppliers": suppliers, "count": len(suppliers)}

@app.get("/returns")
def read_returns(session: Session = Depends(get_session)):
    returns = get_all_returns(session)
    return {"returns": returns, "count": len(returns)}

@app.get("/info")
def project_info():
    return {
        "project": "Минимаркет",
        "student": "Демьяненко Елена",
        "description": "Полнофункциональная система управления магазином с автоматическим расчётом сумм",
        "status": "API работает с реальными данными",
        "key_feature": "Автоматический расчёт суммы заказа при добавлении/удалении товаров",
        "endpoints_available": [
            "Блок 'Покупатели': GET/POST/DELETE /customers",
            "Блок 'Товары': GET/POST/DELETE /products, фильтры по категориям",
            "Блок 'Заказы': GET/POST/PUT/DELETE /orders, управление статусами",
            "Блок 'Позиции заказа': GET/POST/DELETE /order-items"
        ]
    }