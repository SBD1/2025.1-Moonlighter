<span style="background-color:#1ec68e; color:white; font-size:0.8em; font-weight: bold; padding:2px 6px; border-radius:4px;">Versão 1.0</span>

# Triggers 

Triggers são blocos de código executados automaticamente pelo banco de dados em resposta a determinados eventos, como inserções, atualizações ou remoções de dados em tabelas. Eles são utilizados para garantir regras de negócio, integridade dos dados e automatizar processos que devem ocorrer de forma transparente para o usuário.

No contexto do projeto Moonlighter, triggers são fundamentais para garantir a integridade das especializações de itens e locais, além de realizar remoções em cascata e outras validações automáticas.

---

## Triggers implementadas no Projeto Moonlighter

A seguir, estão descritas as principais triggers implementadas no banco de dados do projeto, com seus objetivos e funcionamento:

### 1. Validação de Especialização Única de Itens

- **Triggers:**
    - `trigger_validar_armadura_unica` (para armaduras)
    - `trigger_validar_pocao_unica` (para poções)
    - `trigger_validar_arma_unica` (para armas)
- **Função:** Garante que um item só possa pertencer a uma especialização (Arma, Armadura ou Poção) por vez, evitando inconsistências.
- **Evento:** `BEFORE INSERT` nas tabelas especializadas.
- **Resumo:** Impede que um mesmo item seja cadastrado em mais de uma especialização, mantendo a integridade do modelo relacional.

### 2. Validação de Especialização Única de Locais

- **Triggers:**
    - `trigger_validar_estabelecimento_unico` (para estabelecimentos)
    - `trigger_validar_masmorra_unica` (para masmorras)
- **Função:** Garante que um local só possa ser classificado como Estabelecimento ou Masmorra, nunca ambos.
- **Evento:** `BEFORE INSERT` nas tabelas especializadas.
- **Resumo:** Mantém a consistência das especializações de locais no banco de dados.

### 3. Remoção em Cascata de Especializações

- **Triggers:**
    - `trigger_remover_especializacoes_item` (quando um item é removido)
    - `trigger_remover_especializacoes_local` (quando um local é removido)
- **Função:** Remove automaticamente todas as especializações associadas a um item ou local quando o registro principal é excluído.
- **Evento:** `BEFORE DELETE` nas tabelas generalizadas.
- **Resumo:** Evita registros órfãos e mantém a integridade referencial.

### 4. Atualização de Tipo após Remoção de Especialização

- **Triggers:**
    - `trigger_atualizar_tipo_apos_remover_arma`
    - `trigger_atualizar_tipo_apos_remover_armadura`
    - `trigger_atualizar_tipo_apos_remover_pocao`
    - `trigger_atualizar_tipo_apos_remover_estabelecimento`
    - `trigger_atualizar_tipo_apos_remover_masmorra`
- **Função:** Atualiza o tipo do item ou local na tabela generalizada caso todas as suas especializações sejam removidas.
- **Evento:** `AFTER DELETE` nas tabelas especializadas.
- **Resumo:** Garante que o tipo do registro principal reflita corretamente sua situação após remoções.

---

## Exemplo de Trigger: Remoção em Cascata no Inventário

Ao remover um item do inventário, é importante garantir que todas as especializações relacionadas a esse item (arma, armadura, poção) também sejam removidas automaticamente. Isso evita inconsistências e registros órfãos no banco de dados.

```sql
CREATE OR REPLACE FUNCTION remover_especializacoes_item()
RETURNS TRIGGER AS $$
BEGIN
    -- Remove o item de todas as tabelas especializadas
    DELETE FROM "arma" WHERE "idItem" = OLD."idItem";
    DELETE FROM "armadura" WHERE "idItem" = OLD."idItem";
    DELETE FROM "pocao" WHERE "idItem" = OLD."idItem";
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_remover_especializacoes_item
    BEFORE DELETE ON "item"
    FOR EACH ROW
    EXECUTE FUNCTION remover_especializacoes_item();
```

**Resumo:**
- Sempre que um item for removido da tabela principal de itens, todas as suas especializações também serão excluídas automaticamente.
- Isso garante a integridade do sistema de inventário, evitando que especializações fiquem sem referência ao item principal.

---

| Data       | Versão | Autor(es)        | Mudanças                                               |
| ---------- | ------ | ---------------- | ------------------------------------------------------ |
| 06/07/2025 | `1.0`  | Todos da Equipe  | Criação da Página e Inserção Triggers                 |
