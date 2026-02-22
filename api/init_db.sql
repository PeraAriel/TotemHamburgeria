-- Creazione database
CREATE DATABASE IF NOT EXISTS hamburgeria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE hamburgeria;

-- Tabella Categorie
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabella Prodotti
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(255),
    category_id INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    UNIQUE KEY unique_product_per_category (name, category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabella Ordini
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number INT UNIQUE NOT NULL,
    status ENUM('pending', 'preparing', 'ready', 'completed', 'cancelled') DEFAULT 'pending',
    total_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabella Articoli Ordine
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    unit_price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dati di esempio
INSERT INTO categories (name, description) VALUES
('Panini', 'Panini freschi e gustosi'),
('Bevande', 'Bevande fredde e calde'),
('Menu', 'Menu completi'),
('Dolci', 'Dolci e dessert');

INSERT INTO products (name, description, price, category_id) VALUES
('Hamburger Classico', 'Pane, carne, pomodoro, lattuga, cipolla', 7.50, 1),
('Cheeseburger', 'Con formaggio cheddar premium', 8.50, 1),
('Veggie Burger', 'Panino vegetariano con verdure grigliate', 7.00, 1),
('Coca Cola', 'Lattina 33cl', 2.50, 2),
('Acqua Naturale', 'Bottiglia 50cl', 1.50, 2),
('Birra', 'Birra artigianale 33cl', 4.00, 2),
('Menu Combo', 'Hamburger + Patatine + Bevanda', 12.00, 3),
('Menu Deluxe', 'Cheeseburger + Patatine + Bevanda + Dolce', 15.00, 3),
('Tiramisù', 'Dolce tradizionale italiano', 4.50, 4),
('Gelato', 'Gelato assortito', 3.50, 4);

-- Creazione indici aggiuntivi per performance
CREATE INDEX idx_product_category ON products(category_id);
