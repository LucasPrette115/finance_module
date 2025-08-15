
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE IF NOT EXISTS accounts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE TABLE IF NOT EXISTS categories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(150) NOT NULL,
    type VARCHAR(20) NOT NULL, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    UNIQUE (name, type)
);

CREATE TABLE IF NOT EXISTS transactions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    date DATE NOT NULL,
    description TEXT,
    document VARCHAR(100),
    status VARCHAR(50),
    credit NUMERIC(14,2) DEFAULT 0 NOT NULL,
    debit  NUMERIC(14,2) DEFAULT 0 NOT NULL,
    balance  NUMERIC(14,2) DEFAULT 0 NOT NULL,
    account_id UUID NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT now(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

CREATE INDEX IF NOT EXISTS idx_transactions_date ON transactions (date);
CREATE INDEX IF NOT EXISTS idx_transactions_account ON transactions (account_id);

INSERT INTO accounts (id, name, description)
VALUES (gen_random_uuid(), 'Santander', 'Conta corrente principal')
ON CONFLICT (name) DO NOTHING;

INSERT INTO categories (id, name, type)
VALUES
 (gen_random_uuid(), 'Salário', 'income'),
 (gen_random_uuid(), 'Alimentação', 'expense'),
 (gen_random_uuid(), 'Transporte', 'expense')
ON CONFLICT (name, type) DO NOTHING;
