--
-- PostgreSQL database dump
--

-- Dumped from database version 15.13 (Debian 15.13-1.pgdg120+1)
-- Dumped by pg_dump version 15.12

-- Started on 2025-05-18 00:10:49 UTC

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 227 (class 1259 OID 16522)
-- Name: aramdura; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.aramdura (
    "idItem" integer NOT NULL,
    "dadoDefesa" character varying(3) NOT NULL,
    "defesaPassiva" integer NOT NULL,
    "criticoDefensivo" integer NOT NULL,
    "bonusDefesa" integer NOT NULL,
    "tipoArmadura" character varying(15) NOT NULL
);


ALTER TABLE public.aramdura OWNER TO moonlighter;

--
-- TOC entry 226 (class 1259 OID 16514)
-- Name: arma; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.arma (
    "idItem" integer NOT NULL,
    "dadoAtaque" character varying(3) NOT NULL,
    "chanceCritico" real NOT NULL,
    multiplicador integer NOT NULL,
    "multiplicadorCritico" integer NOT NULL,
    alcance integer NOT NULL,
    "tipoArma" character varying(15) NOT NULL
);


ALTER TABLE public.arma OWNER TO moonlighter;

--
-- TOC entry 229 (class 1259 OID 16553)
-- Name: inst_item; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.inst_item (
    "idItem" integer NOT NULL,
    quantidade integer NOT NULL,
    "idMonstro" integer,
    "idInventario" integer,
    "idLojaNPC" integer,
    "seedSala" character varying(10),
    "nickName" integer
);


ALTER TABLE public.inst_item OWNER TO moonlighter;

--
-- TOC entry 215 (class 1259 OID 16428)
-- Name: inst_masmorra; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.inst_masmorra (
    "nomeMasmorra" character varying(30) NOT NULL,
    "seedMasmorra" character varying(10) NOT NULL,
    "posicaoX_Jogador" integer NOT NULL,
    "posicaoY_Jogador" integer NOT NULL
);


ALTER TABLE public.inst_masmorra OWNER TO moonlighter;

--
-- TOC entry 223 (class 1259 OID 16493)
-- Name: inst_monstro; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.inst_monstro (
    "idMonstro" integer NOT NULL,
    "vidaAtual" integer NOT NULL,
    status boolean NOT NULL,
    "seedSala" character varying(10)
);


ALTER TABLE public.inst_monstro OWNER TO moonlighter;

--
-- TOC entry 225 (class 1259 OID 16509)
-- Name: item; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.item (
    "idItem" integer NOT NULL,
    nome character varying(30) NOT NULL,
    descricao character varying(60) NOT NULL,
    tipo character varying(15) NOT NULL,
    "precoBase" integer NOT NULL,
    raridade integer NOT NULL,
    "stackMaximo" integer NOT NULL,
    "idEfeito" integer
);


ALTER TABLE public.item OWNER TO moonlighter;

--
-- TOC entry 224 (class 1259 OID 16508)
-- Name: item_idItem_seq; Type: SEQUENCE; Schema: public; Owner: moonlighter
--

ALTER TABLE public.item ALTER COLUMN "idItem" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."item_idItem_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 219 (class 1259 OID 16464)
-- Name: mapa; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.mapa (
    "idMapa" integer NOT NULL,
    periodo character varying(8) NOT NULL,
    dia integer NOT NULL
);


ALTER TABLE public.mapa OWNER TO moonlighter;

--
-- TOC entry 218 (class 1259 OID 16463)
-- Name: mapa_idMapa_seq; Type: SEQUENCE; Schema: public; Owner: moonlighter
--

ALTER TABLE public.mapa ALTER COLUMN "idMapa" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."mapa_idMapa_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 214 (class 1259 OID 16423)
-- Name: masmorra; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.masmorra (
    "nomeMasmorra" character varying(30) NOT NULL,
    descricao character varying(100) NOT NULL,
    nivel integer NOT NULL,
    "qtdAndar" integer NOT NULL
);


ALTER TABLE public.masmorra OWNER TO moonlighter;

--
-- TOC entry 220 (class 1259 OID 16469)
-- Name: masmorra_mapa; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.masmorra_mapa (
    "nomeMasmorra" character varying(30) NOT NULL,
    "idMapa" integer NOT NULL,
    desbloqueado boolean NOT NULL
);


ALTER TABLE public.masmorra_mapa OWNER TO moonlighter;

--
-- TOC entry 222 (class 1259 OID 16483)
-- Name: monstro; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.monstro (
    "idMonsto" integer NOT NULL,
    nome character varying(30) NOT NULL,
    descricao character varying(100) NOT NULL,
    nivel integer NOT NULL,
    "vidaMaxima" integer NOT NULL,
    "ouroDropado" integer NOT NULL,
    "dadoAtaque" character varying(3) NOT NULL,
    "chanceCritico" real NOT NULL,
    multiplicador integer NOT NULL,
    "multiplicadorCritico" integer NOT NULL,
    chefe boolean NOT NULL,
    "nomeMasmorra" character varying(60) NOT NULL,
    "idEfeito" integer
);


ALTER TABLE public.monstro OWNER TO moonlighter;

--
-- TOC entry 221 (class 1259 OID 16482)
-- Name: monstro_idMonsto_seq; Type: SEQUENCE; Schema: public; Owner: moonlighter
--

ALTER TABLE public.monstro ALTER COLUMN "idMonsto" ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public."monstro_idMonsto_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- TOC entry 230 (class 1259 OID 16573)
-- Name: monstro_item; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.monstro_item (
    "idMonstro" integer NOT NULL,
    "idItem" integer NOT NULL,
    "chanceDrop" real NOT NULL,
    "qtdMinima" integer NOT NULL,
    "qtdMaxima" integer NOT NULL
);


ALTER TABLE public.monstro_item OWNER TO moonlighter;

--
-- TOC entry 228 (class 1259 OID 16530)
-- Name: pocao; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.pocao (
    "idItem" integer NOT NULL,
    "duracaoTurnos" integer NOT NULL
);


ALTER TABLE public.pocao OWNER TO moonlighter;

--
-- TOC entry 216 (class 1259 OID 16440)
-- Name: sala; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.sala (
    "seedSala" character varying(10) NOT NULL,
    "posicaoX" integer NOT NULL,
    "posicaoY" integer NOT NULL,
    categoria character varying(60) NOT NULL,
    explorada boolean NOT NULL,
    "nomeMasmorra" character varying(30) NOT NULL
);


ALTER TABLE public.sala OWNER TO moonlighter;

--
-- TOC entry 217 (class 1259 OID 16450)
-- Name: sala_inst_masmorra; Type: TABLE; Schema: public; Owner: moonlighter
--

CREATE TABLE public.sala_inst_masmorra (
    "seedSala" character varying(10) NOT NULL,
    "nomeMasmorra" character varying(30) NOT NULL
);


ALTER TABLE public.sala_inst_masmorra OWNER TO moonlighter;

--
-- TOC entry 3443 (class 0 OID 16522)
-- Dependencies: 227
-- Data for Name: aramdura; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.aramdura ("idItem", "dadoDefesa", "defesaPassiva", "criticoDefensivo", "bonusDefesa", "tipoArmadura") FROM stdin;
\.


--
-- TOC entry 3442 (class 0 OID 16514)
-- Dependencies: 226
-- Data for Name: arma; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.arma ("idItem", "dadoAtaque", "chanceCritico", multiplicador, "multiplicadorCritico", alcance, "tipoArma") FROM stdin;
\.


--
-- TOC entry 3445 (class 0 OID 16553)
-- Dependencies: 229
-- Data for Name: inst_item; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.inst_item ("idItem", quantidade, "idMonstro", "idInventario", "idLojaNPC", "seedSala", "nickName") FROM stdin;
\.


--
-- TOC entry 3431 (class 0 OID 16428)
-- Dependencies: 215
-- Data for Name: inst_masmorra; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.inst_masmorra ("nomeMasmorra", "seedMasmorra", "posicaoX_Jogador", "posicaoY_Jogador") FROM stdin;
\.


--
-- TOC entry 3439 (class 0 OID 16493)
-- Dependencies: 223
-- Data for Name: inst_monstro; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.inst_monstro ("idMonstro", "vidaAtual", status, "seedSala") FROM stdin;
\.


--
-- TOC entry 3441 (class 0 OID 16509)
-- Dependencies: 225
-- Data for Name: item; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.item ("idItem", nome, descricao, tipo, "precoBase", raridade, "stackMaximo", "idEfeito") FROM stdin;
\.


--
-- TOC entry 3435 (class 0 OID 16464)
-- Dependencies: 219
-- Data for Name: mapa; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.mapa ("idMapa", periodo, dia) FROM stdin;
\.


--
-- TOC entry 3430 (class 0 OID 16423)
-- Dependencies: 214
-- Data for Name: masmorra; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.masmorra ("nomeMasmorra", descricao, nivel, "qtdAndar") FROM stdin;
\.


--
-- TOC entry 3436 (class 0 OID 16469)
-- Dependencies: 220
-- Data for Name: masmorra_mapa; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.masmorra_mapa ("nomeMasmorra", "idMapa", desbloqueado) FROM stdin;
\.


--
-- TOC entry 3438 (class 0 OID 16483)
-- Dependencies: 222
-- Data for Name: monstro; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.monstro ("idMonsto", nome, descricao, nivel, "vidaMaxima", "ouroDropado", "dadoAtaque", "chanceCritico", multiplicador, "multiplicadorCritico", chefe, "nomeMasmorra", "idEfeito") FROM stdin;
\.


--
-- TOC entry 3446 (class 0 OID 16573)
-- Dependencies: 230
-- Data for Name: monstro_item; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.monstro_item ("idMonstro", "idItem", "chanceDrop", "qtdMinima", "qtdMaxima") FROM stdin;
\.


--
-- TOC entry 3444 (class 0 OID 16530)
-- Dependencies: 228
-- Data for Name: pocao; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.pocao ("idItem", "duracaoTurnos") FROM stdin;
\.


--
-- TOC entry 3432 (class 0 OID 16440)
-- Dependencies: 216
-- Data for Name: sala; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.sala ("seedSala", "posicaoX", "posicaoY", categoria, explorada, "nomeMasmorra") FROM stdin;
\.


--
-- TOC entry 3433 (class 0 OID 16450)
-- Dependencies: 217
-- Data for Name: sala_inst_masmorra; Type: TABLE DATA; Schema: public; Owner: moonlighter
--

COPY public.sala_inst_masmorra ("seedSala", "nomeMasmorra") FROM stdin;
\.


--
-- TOC entry 3452 (class 0 OID 0)
-- Dependencies: 224
-- Name: item_idItem_seq; Type: SEQUENCE SET; Schema: public; Owner: moonlighter
--

SELECT pg_catalog.setval('public."item_idItem_seq"', 1, false);


--
-- TOC entry 3453 (class 0 OID 0)
-- Dependencies: 218
-- Name: mapa_idMapa_seq; Type: SEQUENCE SET; Schema: public; Owner: moonlighter
--

SELECT pg_catalog.setval('public."mapa_idMapa_seq"', 1, false);


--
-- TOC entry 3454 (class 0 OID 0)
-- Dependencies: 221
-- Name: monstro_idMonsto_seq; Type: SEQUENCE SET; Schema: public; Owner: moonlighter
--

SELECT pg_catalog.setval('public."monstro_idMonsto_seq"', 1, false);


--
-- TOC entry 3256 (class 2606 OID 16434)
-- Name: inst_masmorra INST_MASMORRA_SeedMasmorra_key; Type: CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.inst_masmorra
    ADD CONSTRAINT "INST_MASMORRA_SeedMasmorra_key" UNIQUE ("seedMasmorra");


--
-- TOC entry 3258 (class 2606 OID 16432)
-- Name: inst_masmorra INST_MASMORRA_pkey; Type: CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.inst_masmorra
    ADD CONSTRAINT "INST_MASMORRA_pkey" PRIMARY KEY ("nomeMasmorra");


--
-- TOC entry 3254 (class 2606 OID 16427)
-- Name: masmorra MASMORRA_pkey; Type: CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.masmorra
    ADD CONSTRAINT "MASMORRA_pkey" PRIMARY KEY ("nomeMasmorra");


--
-- TOC entry 3260 (class 2606 OID 16444)
-- Name: sala SALA_pkey; Type: CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.sala
    ADD CONSTRAINT "SALA_pkey" PRIMARY KEY ("seedSala");


--
-- TOC entry 3270 (class 2606 OID 16557)
-- Name: inst_item inst_item_pkey; Type: CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.inst_item
    ADD CONSTRAINT inst_item_pkey PRIMARY KEY ("idItem");


--
-- TOC entry 3266 (class 2606 OID 16497)
-- Name: inst_monstro inst_monstro_pkey; Type: CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.inst_monstro
    ADD CONSTRAINT inst_monstro_pkey PRIMARY KEY ("idMonstro");


--
-- TOC entry 3268 (class 2606 OID 16513)
-- Name: item item_pkey; Type: CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.item
    ADD CONSTRAINT item_pkey PRIMARY KEY ("idItem");


--
-- TOC entry 3262 (class 2606 OID 16468)
-- Name: mapa mapa_pkey; Type: CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.mapa
    ADD CONSTRAINT mapa_pkey PRIMARY KEY ("idMapa");


--
-- TOC entry 3264 (class 2606 OID 16487)
-- Name: monstro monstro_pkey; Type: CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.monstro
    ADD CONSTRAINT monstro_pkey PRIMARY KEY ("idMonsto");


--
-- TOC entry 3271 (class 2606 OID 16435)
-- Name: inst_masmorra INST_MASMORRA_NomeMasmorra_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.inst_masmorra
    ADD CONSTRAINT "INST_MASMORRA_NomeMasmorra_fkey" FOREIGN KEY ("nomeMasmorra") REFERENCES public.masmorra("nomeMasmorra");


--
-- TOC entry 3272 (class 2606 OID 16445)
-- Name: sala SALA_NomeMasmorra_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.sala
    ADD CONSTRAINT "SALA_NomeMasmorra_fkey" FOREIGN KEY ("nomeMasmorra") REFERENCES public.inst_masmorra("nomeMasmorra");


--
-- TOC entry 3281 (class 2606 OID 16525)
-- Name: aramdura aramdura_idItem_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.aramdura
    ADD CONSTRAINT "aramdura_idItem_fkey" FOREIGN KEY ("idItem") REFERENCES public.item("idItem");


--
-- TOC entry 3280 (class 2606 OID 16517)
-- Name: arma arma_idItem_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.arma
    ADD CONSTRAINT "arma_idItem_fkey" FOREIGN KEY ("idItem") REFERENCES public.item("idItem");


--
-- TOC entry 3283 (class 2606 OID 16558)
-- Name: inst_item inst_item_idItem_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.inst_item
    ADD CONSTRAINT "inst_item_idItem_fkey" FOREIGN KEY ("idItem") REFERENCES public.item("idItem");


--
-- TOC entry 3284 (class 2606 OID 16563)
-- Name: inst_item inst_item_idMonstro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.inst_item
    ADD CONSTRAINT "inst_item_idMonstro_fkey" FOREIGN KEY ("idMonstro") REFERENCES public.inst_monstro("idMonstro");


--
-- TOC entry 3285 (class 2606 OID 16568)
-- Name: inst_item inst_item_seedSala_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.inst_item
    ADD CONSTRAINT "inst_item_seedSala_fkey" FOREIGN KEY ("seedSala") REFERENCES public.sala("seedSala");


--
-- TOC entry 3278 (class 2606 OID 16498)
-- Name: inst_monstro inst_monstro_idMonstro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.inst_monstro
    ADD CONSTRAINT "inst_monstro_idMonstro_fkey" FOREIGN KEY ("idMonstro") REFERENCES public.monstro("idMonsto");


--
-- TOC entry 3279 (class 2606 OID 16503)
-- Name: inst_monstro inst_monstro_seedSala_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.inst_monstro
    ADD CONSTRAINT "inst_monstro_seedSala_fkey" FOREIGN KEY ("seedSala") REFERENCES public.sala("seedSala");


--
-- TOC entry 3275 (class 2606 OID 16477)
-- Name: masmorra_mapa masmorra_mapa_idMapa_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.masmorra_mapa
    ADD CONSTRAINT "masmorra_mapa_idMapa_fkey" FOREIGN KEY ("idMapa") REFERENCES public.mapa("idMapa");


--
-- TOC entry 3276 (class 2606 OID 16472)
-- Name: masmorra_mapa masmorra_mapa_nomeMasmorra_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.masmorra_mapa
    ADD CONSTRAINT "masmorra_mapa_nomeMasmorra_fkey" FOREIGN KEY ("nomeMasmorra") REFERENCES public.masmorra("nomeMasmorra");


--
-- TOC entry 3286 (class 2606 OID 16581)
-- Name: monstro_item monstro_item_idItem_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.monstro_item
    ADD CONSTRAINT "monstro_item_idItem_fkey" FOREIGN KEY ("idItem") REFERENCES public.item("idItem");


--
-- TOC entry 3287 (class 2606 OID 16576)
-- Name: monstro_item monstro_item_idMonstro_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.monstro_item
    ADD CONSTRAINT "monstro_item_idMonstro_fkey" FOREIGN KEY ("idMonstro") REFERENCES public.monstro("idMonsto");


--
-- TOC entry 3277 (class 2606 OID 16488)
-- Name: monstro monstro_nomeMasmorra_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.monstro
    ADD CONSTRAINT "monstro_nomeMasmorra_fkey" FOREIGN KEY ("nomeMasmorra") REFERENCES public.masmorra("nomeMasmorra");


--
-- TOC entry 3282 (class 2606 OID 16533)
-- Name: pocao pocao_idItem_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.pocao
    ADD CONSTRAINT "pocao_idItem_fkey" FOREIGN KEY ("idItem") REFERENCES public.item("idItem");


--
-- TOC entry 3273 (class 2606 OID 16458)
-- Name: sala_inst_masmorra sala_inst_masmorra_nomeMasmorra_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.sala_inst_masmorra
    ADD CONSTRAINT "sala_inst_masmorra_nomeMasmorra_fkey" FOREIGN KEY ("nomeMasmorra") REFERENCES public.inst_masmorra("nomeMasmorra");


--
-- TOC entry 3274 (class 2606 OID 16453)
-- Name: sala_inst_masmorra sala_inst_masmorra_seedSala_fkey; Type: FK CONSTRAINT; Schema: public; Owner: moonlighter
--

ALTER TABLE ONLY public.sala_inst_masmorra
    ADD CONSTRAINT "sala_inst_masmorra_seedSala_fkey" FOREIGN KEY ("seedSala") REFERENCES public.sala("seedSala");


-- Completed on 2025-05-18 00:10:50 UTC

--
-- PostgreSQL database dump complete
--

CREATE TABLE public.efeito (
    "idEfeito" integer NOT NULL GENERATED ALWAYS AS IDENTITY (
        SEQUENCE NAME public."efeito_idEfeito_seq"
        START WITH 1
        INCREMENT BY 1
        NO MINVALUE
        NO MAXVALUE
        CACHE 1
    ),
    "nome" character varying(30) NOT NULL,
    "descricao" character varying(100) NOT NULL,
    "tipo" character varying(15) NOT NULL,
    "valor" integer NOT NULL,
    "duracaoTurnos" integer NOT NULL,
    CONSTRAINT "PK_efeito" PRIMARY KEY ("idEfeito")
);

ALTER TABLE public.efeito OWNER TO moonlighter;

CREATE TABLE public.receita (
    "idItemFabricado" integer NOT NULL,
    "idItemFabricador" integer NOT NULL,
    "quantidade" integer NOT NULL,
    CONSTRAINT "PK_receita" PRIMARY KEY ("idItemFabricado", "idItemFabricador"),
    CONSTRAINT "FK_receita_item_fabricado" FOREIGN KEY ("idItemFabricado") REFERENCES public.item("idItem"),
    CONSTRAINT "FK_receita_item_fabricador" FOREIGN KEY ("idItemFabricador") REFERENCES public.item("idItem")
);

ALTER TABLE public.receita OWNER TO moonlighter;

CREATE TABLE public.jogador (
    "nickName" character varying(60) NOT NULL,
    "maxHP" integer NOT NULL,
    "atualHP" integer NOT NULL,
    "ouro" integer NOT NULL,
    "idEfeito" integer,
    CONSTRAINT "PK_jogador" PRIMARY KEY ("nickName"),
    CONSTRAINT "FK_jogador_efeito" FOREIGN KEY ("idEfeito") REFERENCES public.efeito("idEfeito")
);

ALTER TABLE public.jogador OWNER TO moonlighter;

CREATE TABLE public.loja_jogador (
    "nickName" character varying(60) NOT NULL,
    "nivel" integer NOT NULL,
    "exposicaoMaxima" integer NOT NULL,
    "exposicaoUsada" integer NOT NULL,
    "idMapa" integer NOT NULL,
    CONSTRAINT "PK_loja_jogador" PRIMARY KEY ("nickName"),
    CONSTRAINT "FK_loja_jogador_jogador" FOREIGN KEY ("nickName") REFERENCES public.jogador("nickName"),
    CONSTRAINT "FK_loja_jogador_mapa" FOREIGN KEY ("idMapa") REFERENCES public.mapa("idMapa")
);

ALTER TABLE public.loja_jogador OWNER TO moonlighter;

CREATE TABLE public.inst_inventario (
    "idInventario" integer NOT NULL GENERATED ALWAYS AS IDENTITY (
        SEQUENCE NAME public."inst_inventario_idInventario_seq"
        START WITH 1
        INCREMENT BY 1
        NO MINVALUE
        NO MAXVALUE
        CACHE 1
    ),
    "nome" character varying(30) NOT NULL,
    "slotMaximo" integer NOT NULL,
    CONSTRAINT "PK_inst_inventario" PRIMARY KEY ("idInventario")
);

ALTER TABLE public.inst_inventario OWNER TO moonlighter;

CREATE TABLE public.npc (
    "idNPC" integer NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "tipoNPC" character varying(30) NOT NULL,
    "descricao" character varying(60) NOT NULL,
    "ativo" boolean NOT NULL
);


ALTER TABLE public.npc OWNER TO moonlighter;


CREATE TABLE public.loja_npc (
    "idLojaNPC" integer NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    "nome" character varying(30) NOT NULL,
    "tipoLoja" character varying(30) NOT NULL,
    "descricao" character varying(120) NOT NULL,
    "status" boolean NOT NULL,
    "idNPC" integer NOT NULL,
    "idMapa" integer NOT NULL
);


ALTER TABLE public.loja_npc OWNER TO moonlighter;


CREATE TABLE public.forjaria (
    "idLojaNPC" integer NOT NULL
);


ALTER TABLE public.forjaria OWNER TO moonlighter;

CREATE TABLE public.varejo (
    "idLojaNPC" integer NOT NULL,
    "margemLucro" integer NOT NULL
);


ALTER TABLE public.varejo OWNER TO moonlighter;

CREATE TABLE public.banco (
    "idLojaNPC" integer NOT NULL,
    "valorEntrada" integer,
    "valorAtual" integer NOT NULL
);


ALTER TABLE public.banco OWNER TO moonlighter;

CREATE TABLE public.dialogo (
    "idDialogo" integer NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    "conteudo" character varying(300) NOT NULL,
    "ordem" integer NOT NULL,
    "tipo" character varying(60) NOT NULL,
    "idDialogo" integer
);


ALTER TABLE public.dialogo OWNER TO moonlighter;

CREATE TABLE public.dialogo_npc (
    "idDialogo" integer NOT NULL,
    "idNPC" integer NOT NULL
);

ALTER TABLE public.dialogo_npc OWNER TO moonlighter;

ALTER TABLE ONLY public.npc
    ADD CONSTRAINT npc_pkey PRIMARY KEY ("idNPC");

ALTER TABLE ONLY public.lojanpc
    ADD CONSTRAINT lojanpc_pkey PRIMARY KEY ("idLojaNPC");

ALTER TABLE ONLY public.forjaria
    ADD CONSTRAINT forjaria_pkey PRIMARY KEY ("idLojaNPC");

ALTER TABLE ONLY public.varejo
    ADD CONSTRAINT varejo_pkey PRIMARY KEY ("idLojaNPC");

ALTER TABLE ONLY public.banco
    ADD CONSTRAINT banco_pkey PRIMARY KEY ("idLojaNPC");

ALTER TABLE ONLY public.dialogo
    ADD CONSTRAINT dialogo_pkey PRIMARY KEY ("idDialogo");

ALTER TABLE ONLY public.dialogo_npc
    ADD CONSTRAINT dialogo_npc_pkey PRIMARY KEY ("idDialogo", "idNPC");

ALTER TABLE ONLY public.lojanpc
    ADD CONSTRAINT fk_lojanpc_npc FOREIGN KEY ("idNPC") REFERENCES public.npc("idNPC");

ALTER TABLE ONLY public.forjaria
    ADD CONSTRAINT fk_forjaria_lojanpc FOREIGN KEY ("idLojaNPC") REFERENCES public.lojanpc("idLojaNPC");

ALTER TABLE ONLY public.varejo
    ADD CONSTRAINT fk_varejo_lojanpc FOREIGN KEY ("idLojaNPC") REFERENCES public.lojanpc("idLojaNPC");

ALTER TABLE ONLY public.banco
    ADD CONSTRAINT fk_banco_lojanpc FOREIGN KEY ("idLojaNPC") REFERENCES public.lojanpc("idLojaNPC");

ALTER TABLE ONLY public.dialogo
    ADD CONSTRAINT fk_dialogo_pai FOREIGN KEY ("idDialogo") REFERENCES public.dialogo("idDialogo");

ALTER TABLE ONLY public.dialogo_npc
    ADD CONSTRAINT fk_dialogonpc_dialogo FOREIGN KEY ("idDialogo") REFERENCES public.dialogo("idDialogo");

ALTER TABLE ONLY public.dialogo_npc
    ADD CONSTRAINT fk_dialogonpc_npc FOREIGN KEY ("idNPC") REFERENCES public.npc("idNPC");