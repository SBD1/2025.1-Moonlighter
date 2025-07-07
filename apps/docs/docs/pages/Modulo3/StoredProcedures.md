<span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.0</span>

# Procedures 

Procedures (ou funções armazenadas) são blocos de código SQL que ficam salvos no banco de dados e podem ser executados sob demanda, encapsulando lógicas de negócio, consultas complexas ou operações recorrentes. Elas promovem reutilização, padronização e centralização de regras, além de otimizar a comunicação entre aplicação e banco de dados.

No projeto Moonlighter, procedures são utilizadas principalmente para consultas de inventário, obtenção de itens no chão, validações e operações automáticas relacionadas à integridade dos dados do jogo.

---

## Procedures implementadas no Projeto Moonlighter

A seguir, estão descritas algumas das principais procedures (funções) implementadas no banco de dados do projeto, com seus objetivos e funcionamento:

### 1. Obter Itens no Chão do Local

- **Procedure:** `obter_itens_chao_local(p_nickname VARCHAR)`
- **Função:** Retorna todos os itens que estão no chão do local onde o jogador se encontra.
- **Resumo:** Facilita a busca e exibição dos itens disponíveis para coleta no ambiente do jogador.

```sql
CREATE OR REPLACE FUNCTION obter_itens_chao_local(p_nickname VARCHAR)
RETURNS TABLE(
    "idItemChao" INTEGER,
    "idItem" INTEGER,
    "nome" VARCHAR,
    "quantidade" SMALLINT,
    "posicaoX" INTEGER,
    "posicaoY" INTEGER,
    "descricao" VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        ic."idItemChao",
        ic."idItem",
        i."nome",
        ic."quantidade",
        ic."posicaoX",
        ic."posicaoY",
        i."descricao"
    FROM "item_chao" ic
    JOIN "item" i ON ic."idItem" = i."idItem"
    JOIN "jogador" j ON j."nickname" = p_nickname
    JOIN "mundo" m ON j."nickname" = m."nickname"
    WHERE ic."seedMundo" = m."seedMundo" 
    AND ic."nomeLocal" = j."nomeLocal"
    ORDER BY ic."tempoDropado" DESC;
END;
$$ LANGUAGE plpgsql;
```

### 2. Obter Inventário Completo do Jogador

- **Procedure:** `obter_inventario_jogador(p_nickname VARCHAR)`
- **Função:** Retorna todos os itens presentes no inventário do jogador, incluindo informações detalhadas de cada item.
- **Resumo:** Permite à aplicação exibir o inventário completo do jogador de forma eficiente e organizada.

```sql
CREATE OR REPLACE FUNCTION obter_inventario_jogador(p_nickname VARCHAR)
RETURNS TABLE(
    "nickname" VARCHAR,
    "tipo_inventario" VARCHAR,
    "nome_item" VARCHAR,
    "quantidade" SMALLINT,
    "categoria_item" VARCHAR,
    "precoBase" INTEGER,
    "descricao" VARCHAR,
    "idInstItem" INTEGER
) AS $$
BEGIN
    RETURN QUERY
    SELECT * FROM view_inventario_jogador 
    WHERE "nickname" = p_nickname AND "nome_item" IS NOT NULL
    ORDER BY "tipo_inventario", "nome_item";
END;
$$ LANGUAGE plpgsql;
```

---

| Data       | Versão | Autor(es)        | Mudanças                                               |
| ---------- | ------ | ---------------- | ------------------------------------------------------ |
| 06/07/2025 | `1.0`  | Todos da Equipe  | Criação da Página e Inserção procedures                   |
