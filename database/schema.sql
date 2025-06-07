-- database/schema.sql

-- Tabela de Usuários (para simular login local)
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE
);

-- Tabela de Ativos (metadados dos ativos)
CREATE TABLE IF NOT EXISTS assets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL UNIQUE, -- Ex: 'PETR4.SA'
    name TEXT NOT NULL,          -- Ex: 'PETROBRAS PN N2'
    sector TEXT,                 -- Ex: 'Petróleo, Gás e Biocombustíveis'
    sub_sector TEXT,             -- Ex: 'Exploração e Produção'
    is_fii BOOLEAN DEFAULT 0     -- 0 para Ação, 1 para FII (se for expandir)
);

-- Tabela de Preços Diários e Métricas
CREATE TABLE IF NOT EXISTS daily_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER NOT NULL,
    date TEXT NOT NULL, -- Formato YYYY-MM-DD
    open_price REAL,
    close_price REAL,
    high_price REAL,
    low_price REAL,
    volume INTEGER,
    pl REAL,             -- Preço/Lucro
    pvp REAL,            -- Preço/Valor Patrimonial
    dividend_yield REAL, -- Dividend Yield anualizado
    FOREIGN KEY (asset_id) REFERENCES assets(id),
    UNIQUE(asset_id, date) -- Garante que um ativo tenha apenas um registro por dia
);

-- Tabela de Carteira do Usuário
CREATE TABLE IF NOT EXISTS user_portfolios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    asset_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    purchase_price REAL NOT NULL,
    purchase_date TEXT NOT NULL, -- Formato YYYY-MM-DD HH:MM:SS
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (asset_id) REFERENCES assets(id),
    UNIQUE(user_id, asset_id) -- Um usuário só pode ter uma entrada para o mesmo ativo na carteira
);
