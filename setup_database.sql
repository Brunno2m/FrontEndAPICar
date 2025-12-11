-- Script SQL para configurar o banco de dados MySQL
-- Execute este script antes de iniciar a aplicação

-- Criar banco de dados
CREATE DATABASE IF NOT EXISTS carros
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

-- Usar o banco de dados
USE carros;

-- Criar tabela de carros
CREATE TABLE IF NOT EXISTS carros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    modelo VARCHAR(255) NOT NULL UNIQUE,
    preco DECIMAL(12, 2) NOT NULL,
    image VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_modelo (modelo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Inserir dados de exemplo (opcional)
INSERT IGNORE INTO carros (modelo, preco) VALUES
('Toyota Corolla', 125000.00),
('Honda Civic', 135000.00),
('Volkswagen Golf', 115000.00),
('Ford Focus', 95000.00),
('Chevrolet Onix', 75000.00);

-- Exibir carros cadastrados
SELECT * FROM carros;

-- Mostrar informações da tabela
SHOW TABLE STATUS LIKE 'carros';
