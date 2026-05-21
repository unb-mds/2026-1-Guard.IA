-- ============================================================
-- Sistema de Monitoramento Legislativo
-- Módulo: Armazenamento
-- Arquivo: schema.sql
-- Descrição: Criação do banco de dados e tabela principal
-- ============================================================

-- Cria o banco (rodar separado se necessário)
-- CREATE DATABASE monitoramento_legislativo;

-- Conectar ao banco antes de rodar o restante:
-- \c monitoramento_legislativo

-- Remove a tabela se já existir (útil durante desenvolvimento)
DROP TABLE IF EXISTS proposicoes;

-- Criação da tabela principal
CREATE TABLE proposicoes (
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

-- Índices para acelerar as consultas do Dashboard
CREATE INDEX idx_categoria       ON proposicoes (categoria);
CREATE INDEX idx_casa            ON proposicoes (casa);
CREATE INDEX idx_data            ON proposicoes (data_apresentacao);
CREATE INDEX idx_confianca       ON proposicoes (confianca);