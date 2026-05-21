-- ============================================================
-- Sistema de Monitoramento Legislativo
-- Módulo: Armazenamento
-- Arquivo: schema.sql
-- Descrição: Criação do banco de dados e tabelas
-- ============================================================

-- Criação da tabela de proposições
CREATE TABLE IF NOT EXISTS proposicoes (
    id                 SERIAL PRIMARY KEY,
    id_externo         VARCHAR(50)  NOT NULL UNIQUE,
    ementa             TEXT         NOT NULL,
    autor              VARCHAR(255),
    partido            VARCHAR(50),
    estado             VARCHAR(2),
    casa               VARCHAR(20)  CHECK (casa IN ('Câmara', 'Senado')),
    data_apresentacao  DATE,
    categoria          VARCHAR(100),
    confianca          FLOAT        CHECK (confianca >= 0 AND confianca <= 1),
    coletado_em        TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Criação da tabela de usuários
CREATE TABLE IF NOT EXISTS usuarios (
    id                SERIAL PRIMARY KEY,
    nome              VARCHAR(100) NOT NULL,
    email             VARCHAR(150) UNIQUE NOT NULL,
    senha_hash        VARCHAR(255) NOT NULL,
    criado_em         TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Índices para acelerar as consultas do Dashboard
CREATE INDEX IF NOT EXISTS idx_categoria       ON proposicoes (categoria);
CREATE INDEX IF NOT EXISTS idx_casa            ON proposicoes (casa);
CREATE INDEX IF NOT EXISTS idx_data            ON proposicoes (data_apresentacao);
CREATE INDEX IF NOT EXISTS idx_confianca       ON proposicoes (confianca);
CREATE INDEX IF NOT EXISTS idx_email_usuario   ON usuarios (email);