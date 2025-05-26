-- INSERÇÕES DE TUPLAS NAS TABELAS

-- INSERÇÃO NA TABELA ITENS:
INSERT INTO "item"
    ("nome", "descricao", "tipo", "precoBase", "cultura", "stackMaximo", "idEfeito")
    VALUES
    -- ITENS SEM CATEGORIA:
    ('Espada Quebrada', 'Bastante inútil na sua forma atual, mas eu poderia ser facilmente derretido para criar algo novo!', NULL, 150, 'Golem', 5, NULL),
    ('Tecido', 'Robusto, mas áspero ao tato. Imagino que alguns queiram utilizá-lo na criação de decorações.', NULL, 250, 'Golem', 5, NULL),
    ('Restos de Fundição', 'Creio que isto são os restos de uma antiga fundição. Se os Golems foram criados, o que é que os criou?', NULL, 150, 'Golem', 5, NULL),
    ('Cinzel de Golem', 'Esse é definitivamente um cinzel usado para esculpir e moldar um Golem. Por sua estrutura, imagino que os arquitetos não eram muito diferentes de nós.', NULL, 500, 'Golem', 5, NULL),
    ('Aço Endurecido', 'O aço mais forte que já encontrei. Perfeito para( a criação de novos equipamentos.', NULL, 300, 'Golem', 5, NULL),
    ('Barra de Ferro', 'Ferro. Bastante básico, mas a pedra fundamental de qualquer equipamento de nível médio que se queira fabricar.', NULL, 25, 'Golem', 10, NULL),
    ('Geléia Rica', 'Substância gelatinosa com muitas propriedades curativas. Pode ser extraída de vários Slimes. Essencial na preparação de poções.', NULL, 5, 'Mercador', 10, NULL),
    ('Raíz', 'Uma raiz de uma planta gigante. Muito útil para a criação de novos arcos.', NULL, 5, 'Golem', 10, NULL),
    ('Ferramenta Rúnica', 'Parece ter sido uma ferramenta usada para inscrever texto em metal e pedra. Talvez possa ser usada para inscrever runas em meu equipamento.', NULL, 1500, 'Golem', 5, NULL),
    ('Pedra de Dente', 'Pedra muito afiada, comumente encontrada nos corpos de Golems antigos.', NULL, 5, 'Golem', 10, NULL),
    ('Cipó', 'Um material forte, porém flexível, usado pelas criaturas Tangle para se protegerem.', NULL, 2, 'Golem', 10, NULL),
    ('Esfera de Água', 'Uma esfera branca leitosa ou algum material desconhecido contendo água emitindo uma luz estranha, quase sinistra.', NULL, 100, 'Golem', 10, NULL),
    ('Pedra de Amolar', 'Pedra básica usada por ferreiros para amolar e afiar armas. Nunca é demais ter uma pedra dessas.', NULL, 15, 'Golem', 10, NULL),
    ('Madeira Antiga', 'Madeira petrificada devido a anos de permanência em ambientes com elementos específicos.', NULL, 1000, 'Floresta', 5, NULL),
    ('Madeira Mágica', 'Madeira embebida em resíduos mágicos durante anos. Emite pequenas faíscas azuis. Material potencialmente útil para resistir a outras magias elementares.', NULL, 100, 'Floresta', 10, NULL),
    ('Bulbo Antigo', 'Um bulbo bastante grande que pertenceu a uma planta já morta... Não está vivo... mas também não está realmente morto...', NULL, 2000, 'Floresta', 5, NULL),
    ('Raíz Preservada', 'Uma raiz muito antiga e muito bem preservada.', NULL, 600, 'Floresta', 5, NULL),
    ('Ácido Puro', 'Puro ácido. Não sei o que me levou a tentar colecionar esse material. Derrete em quase tudo.', NULL, 400, 'Floresta', 10, NULL),
    ('Palha', 'Uma simples pilha de palha. Nada surpreendente. No entanto, parece estar coberto por alguns líquidos corrosivos. Talvez tenha sido usado como isolamento para alguma coisa?', NULL, 500, 'Floresta', 5, NULL),
    ('Folhas Fortes', 'Folhas endurecidas que são flexíveis o suficiente para ricochetear nas paredes em vez de se estilhaçar. Essa foi uma lição duramente aprendida...', NULL, 400, 'Floresta', 10, NULL),
    ('Geléia de Veneno', 'Uma variante de geleia venenosa encontrada em slimes da floresta. Extraia com cuidado.', NULL, 20, 'Floresta', 10, NULL),
    ('Corda do Deserto', 'Uma corda... que não pega fogo... Quem quer que tenha residido na Masmorra do Deserto deve ter sido um povo incrivelmente inventivo.', NULL, 450, 'Deserto', 5, NULL),
    ('Lingote De Aço do Deserto', 'Aço bruto encontrado na Masmorra do Deserto. Anos de ventos arenosos parecem tê-lo endurecido mais do que a maioria dos metais.', NULL, 7500, 'Deserto', 5, NULL),
    ('Joia de Fogo', 'Faísca instantânea ao entrar em contato com uma pedra ou até mesmo com um pano grosso. Um iniciador de fogo perfeito.', NULL, 1700, 'Deserto', 10, NULL),
    ('Geléia de Fogo', 'Uma variante de gelatina que parece estar sempre pegando fogo... Encontrada nos Slimes do Deserto. Não posso beber nada feito com isso... posso?', NULL, 100, 'Mercador', 10, NULL),
    ('Tecido à Prova de Fogo', 'Um tecido que se recusa a queimar. Frequentemente encontrado enrolado em pilhas de areia. Possivelmente usado para proteger a areia durante um processo de aquecimento extremo?', NULL, 1150, 'Deserto', 10, NULL),
    ('Pó Inflamável', 'Pó altamente inflamável. Ótimo para reacender o fogo. Preciso ter alguns em estoque perto do fogão.', NULL, 400, 'Deserto', 10, NULL),
    ('Pó de Insolação', 'Pó usado para isolar conduítes do calor.', NULL, 2050, 'Deserto', 10, NULL),
    ('Magnetita', 'Um mineral usado para magnetizar outros materiais.', NULL, 800, 'Deserto', 10, NULL),
    ('Motor Termomagnético', 'Com tantas peças giratórias, ele parece mágico. Um dispositivo que transforma a energia térmica em ondas magnéticas.', NULL, 9200, 'Deserto', 5, NULL),
    ('Metal Condutor', 'Sucata de metal encontrada em torno da Masmorra da Tecnologia. Pode ser usado como condutor durante a fabricação.', NULL, 600, 'Tecnologia', 10, NULL),
    ('Bobina de Cobre', 'O cobre condutor é fiado em fios e depois enrolado nessa bobina. Fácil de acessar. Design criativo.', NULL, 7500, 'Tecnologia', 5, NULL),
    ('Geléia Elétrica', 'Essa geleia é elétrica, e não estou falando de movimentos de dança... Extraído de Slimes da Tecnologia. Eu poderia criar algumas armas inéditas com isso.', NULL, 400, 'Mercador', 10, NULL),
    ('Fios de Ouro', 'Fios de ouro reais entrelaçados em fios usados por muitas das máquinas das masmorras da Tecnologia. A manutenção deve ser cara.', NULL, 2100, 'Tecnologia', 10, NULL),
    ('Madeira Tratada', 'Madeira tratada para resistir a líquidos corrosivos.', NULL, 5150, 'Tenologia', 5 , NULL),
    ('Bateria de Célula Tripla', 'Uma variante muito maior do Capacitor. Aparentemente, ele pode armazenar grandes quantidades de energia não mágica.', NULL, 10000, 'Tecnologia', 5, NULL),
    ('Pistola de Solda', 'Com o uso de vários outros recursos, esse dispositivo pode unir firmemente determinados metais.', NULL, 11650, 'Tecnologia', 5, NULL),
    ('Fios', 'Pequenos fios de metal usados para conduzir eletricidade.', NULL, 2550, 'Tecnologia', 10, NULL),
    ('Pedra de Wolfram', 'Uma versão bruta do metal tungstênio. Não processado, mas certamente valioso para quem precisa do material.', NULL, 6350, 'Tecnologia', 5, NULL);

    -- ITENS DO TIPO ARMA:

    -- ITENS DO TIPO ARMADURA:

    -- ITENS DO TIPO PORÇÃO:

