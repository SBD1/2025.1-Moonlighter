-- Criação parcial do jogador e suas instâncias de inventário

-- Criação de um novo jogador
INSERT INTO "jogador"
    ("nickName", "maxHP", "atualHP", "ouro", "idEfeito")
VALUES
    ('NovoJogador', 100, 100, 0, NULL);

-- Criação da loja do jogador
INSERT INTO "lojaJogador"
    ("nickName", "nivel", "exposicaoMaxima", "exposicaoUsada", "idMapa")
VALUES
    ('NovoJogador', 1, 10, 0, 1);

-- Criação das instâncias de inventário para o jogador
INSERT INTO "inst_inventario"
    ("idInventario", "nickname", "slotOcupado")
VALUES
    (1, 'NovoJogador', 0),  -- Mochila
    (2, 'NovoJogador', 0),  -- Bolsos
    (3, 'NovoJogador', 0),  -- Equipamento - Armadura
    (4, 'NovoJogador', 0),  -- Equipamento - Arma 1
    (5, 'NovoJogador', 0),  -- Equipamento - Arma 2
    (6, 'NovoJogador', 0),  -- Equipamento - Acessório
    (7, 'NovoJogador', 0);  -- Familiar Mimic 