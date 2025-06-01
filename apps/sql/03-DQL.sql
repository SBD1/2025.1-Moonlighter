-- Consultas sobre o jogador (DQL)

-- Consultar informações básicas do jogador
SELECT nickName, maxHP, atualHP, ouro 
FROM jogador 
WHERE nickName = 'NovoJogador';

-- Consultar inventário do jogador
SELECT i.nome as nome_inventario, ii.slotOcupado
FROM inventario i
JOIN inst_inventario ii ON i.idInventario = ii.idInventario
WHERE ii.nickname = 'NovoJogador';

-- Consultar loja do jogador
SELECT j.nickName, l.nivel, l.exposicaoMaxima, l.exposicaoUsada
FROM jogador j
JOIN lojaJogador l ON j.nickName = l.nickName
WHERE j.nickName = 'NovoJogador';

-- Consultar itens no inventário do jogador (se houver)
SELECT i.nome as nome_item, inst_i.quantidade
FROM inst_item inst_i
JOIN item i ON inst_i.idItem = i.idItem
JOIN inst_inventario ii ON inst_i.idInventario = ii.idInventario
WHERE ii.nickname = 'NovoJogador';

-- Consultar status completo do jogador
SELECT 
    j.nickName,
    j.maxHP,
    j.atualHP,
    j.ouro,
    lj.nivel as nivel_loja,
    lj.exposicaoMaxima,
    e.nome as efeito_ativo,
    e.descricao as descricao_efeito
FROM jogador j
LEFT JOIN lojaJogador lj ON j.nickName = lj.nickName
LEFT JOIN efeito e ON j.idEfeito = e.idEfeito
WHERE j.nickName = 'NovoJogador'; 