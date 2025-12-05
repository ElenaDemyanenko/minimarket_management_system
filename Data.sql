SET search_path TO "Demyanenko";

-- Покупатели
INSERT INTO customers (first_name, last_name, phone, email) VALUES
('Елена', 'Демьяненко', '+79110001122', 'eledem@example.com'),
('Анна', 'Мышкина', '+79875553322', 'anna@example.com'),
('Дмитрий', 'Кузнецов', '+79297773355', 'dim@example.com');

-- Кассиры
INSERT INTO cashiers (full_name, shift, username, password) VALUES
('Мария Петрова', 'Утренняя', 'mpetrova', 'pass123'),
('Дмитрий Орлов', 'Вечерняя', 'dorlov', 'qwerty');

-- Поставщики
INSERT INTO suppliers (company_name, contact_info) VALUES
('ООО Продукт№1', 'Москва, ул. Ленина, 22'),
('ЗАО Фрукт', 'Москва, ул. Садовая, 14');

-- Товары
INSERT INTO products (name, category, price, quantity, expiration_date, supplier_id) VALUES
('Хлеб белый', 'Выпечка', 45.00, 100, '2025-12-31', 1),
('Молоко 2.5%', 'Молочные продукты', 70.00, 50, '2025-12-16', 1),
('Яблоки', 'Фрукты', 120.00, 200, '2025-09-30', 2),
('Чай черный', 'Напитки', 90.00, 50, '2026-03-15', 1),
('Сыр Российский', 'Молочные продукты', 280.00, 30, '2025-12-20', 1),
('Батон нарезной', 'Выпечка', 35.00, 80, '2025-10-05', 1),
('Апельсины', 'Фрукты', 150.00, 60, '2025-12-31', 2);

-- Заказы
INSERT INTO orders (customer_id, cashier_id, total_amount, status) VALUES
(1, 1, 115.00, 'paid'),
(2, 2, 120.00, 'new');

-- Позиции заказов
INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 45.00),
(1, 2, 1, 70.00),
(2, 3, 1, 120.00);

-- Возвраты
INSERT INTO returns (order_id, product_id, amount_refunded) VALUES
(1, 2, 70.00);