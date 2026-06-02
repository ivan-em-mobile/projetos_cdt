from app import app, db, Conteudo

def povoar_banco():
    with app.app_context():
        db.create_all()        
        if Conteudo.query.first():
            print("Banco de dados já está povoado.")
            return

        dados = [
            Conteudo(categoria_id=1, opcao_id=1, titulo="O que é o Credo?", 
                     texto="Tendo recebido do Senhor a ordem de irem como Seus embaixadores, pelo mundo inteiro, a pregar o Evangelho a toda criatura, os Apóstolos acharam que se devia compor uma fórmula de fé cristã. Serviria esta para que todos tivessem a mesma crença e a mesma linguagem, e não houvesse separações entre os que foram chamados à unidade da mesma fé, mas fossem todos perfeitamente conforme no mesmo modo de pensar e de sentir. A esta profissão de fé e esperança cristã, que acabavam de redigir, os Apóstolos chamaram-lhe 'Símbolo', ou porque se forma das várias proposições que cada um deles apresentou, ou porque devia servir de senha para identificar os desertores, os irmãos falsos e intrusos que adulteravam o Evangelho, e assim distingui-los daqueles que verdadeiramente tomavam um santo compromisso na milícia de Cristo. O Símbolo divide-se em três partes, como já diziam os antigos cristãos, quando se punham a explicá-lo com amor e cuidado. A primeira parte trata da Primeira Pessoa da natureza divina, e da prodigiosa obra da Criação. A segunda trata da Segunda Pessoa e do mistério da Redenção dos homens. A terceira afinal descreve, em várias fórmulas adequadas, a Terceira Pessoa, autor e princípio de nossa santificação."),
            
            Conteudo(categoria_id=1, opcao_id=2, titulo="1° Artigo - Creio em Deus Pai Todo-Poderoso, Criador do céu e da terra", 
                     texto="Estas palavras querem dizer: Creio com toda a certeza, e sem nenhuma hesitação confesso a Deus Pai, a primeira Pessoa da Santíssima Trindade, que pela virtude de Sua onipotência criou do nada o próprio céu, a terra, e tudo que se contém em suas dimensões; que sustenta e governa todas as coisas criadas. E não só de coração o creio, e de boca o confesso, mas com o maior afeto e filial piedade a Ele me entrego, por ser o bem sumo e perfeito."),
            
            Conteudo(categoria_id=1, opcao_id=3, titulo="2° Artigo - E em Jesus Cristo, seu único Filho, Nosso Senhor", 
                     texto="Em crer e professar o presente Artigo, encontra o gênero humano imensas e admiráveis vantagens, consoante o testemunho de São João: 'Quem confessa que Jesus Cristo é o Filho de Deus, Deus permanece nele, e ele permanece em Deus'(1Jo 4,15) Prova-o também a palavra de Cristo Nosso Senhor, quando proclamava a bem-aventurança do Príncipe dos Apóstolos: 'Bem-aventurado és tu, Simão, filho de Jonas, pois não foi a carne nem o sangue que te revelou isto, mas antes Meu Pai que está nos céus'.(Mt 16,17) Realmente, esta fé e esta profissão constituem a base mais sólida para nosso resgate e salvação."),
            
            Conteudo(categoria_id=1, opcao_id=4, titulo="3° Artigo - O qual foi concebido do Espírito Santo, nasceu da Virgem Maria", 
                     texto="A Sagrada Escritura no-lo propõe, frequentes vezes, como fator fundamental de nossa salvação. Ensinará como seu sentido se resume em crermos e confessarmos que o mesmo Jesus Cristo, nosso único Senhor e Filho de Deus, assumindo carne humana no seio da Virgem pela nossa salvação, não foi concebido por meio de varão, como os outros homens, mas por obra do Espírito Santo, acima de todas as leis da natureza, de sorte que a mesma Pessoa permaneceu Deus, qual era desde toda a eternidade, e tornou-Se então Homem, o que antes nunca tinha sido. Desde aquele instante, começou realmente a cumprir-se a grandiosa promessa de Deus a Abraão, quando lhe dissera que, um dia, 'todos os povos seriam abençoados em sua descendência'. Maria, a quem proclamamos e veneramos como verdadeira Mãe de Deus, por ter dado à luz aquela Pessoa que era ao mesmo tempo Deus e Homem, [Maria] descendia da estirpe real de Davi"),
            
            Conteudo(categoria_id=1, opcao_id=5, titulo="4° Artigo - Padeceu sob o poder de Pôncio Pilatos, foi cuzificado, morto e sepultado", 
                     texto="Este Artigo nos propõe a crer que Cristo Nosso Senhor foi crucificado, quando Pôncio Pilatos governava, em nome de Tibério César, a província da Judeia. Fora encarcerado, escarnecido, coberto de toda a sorte de opróbrios e tormentos, e finalmente arvorado no madeiro da Cruz. Por esta razão, em primeiro lugar, a Paixão do Senhor livrou-nos do pecado, conforme o declara São João: 'Amou-nos, e no Seu Sangue nos lavou de nossos pecados'(Ap 1,5) E o Apóstolo diz também: '[Deus] vos fez reviver com Ele, per-doou-vos todos os pecados, cancelando e pregando na cruz o título de condenação, que contra nós fora lavrado'(Cl 2,13-14) Em segundo lugar, livrou-nos da tirania do demônio. O Senhor mesmo disse: 'Eis chegado o julgamento do mundo. O príncipe deste mundo será expulso agora. E Eu atrairei tudo a mim, quando for elevado da terra'.(Jo 12,31-32..) Em terceiro lugar, satisfez a pena devida pelos nossos pecados (Rm 5,10;2 Cor 5,19). Em quarto lugar, como não se podia oferecer outro sacrificio mais agradável e mais bem aceito aos olhos de Deus, reconciliou-nos com o Pai, a quem aplacou e tornou propício para conosco. Finalmente, destruindo o pecado, franqueou-nos a entrada para o céu, à qual punha embargo a culpa comum do gênero humano. É o que o Apóstolo nos dá a entender com as palavras: 'Em virtude do Sangue de Cristo, temos a confiança de entrar no Santo dos Santos'(Hb 9,11 ss)."),
            
            Conteudo(categoria_id=1, opcao_id=6, titulo="5° Artigo - Desceu aos infernos, ao terceiro dia ressurgiu dos mortos", 
                     texto="A primeira cláusula deste Artigo propõe-nos a crer que, após a morte de Cristo, Sua Alma desceu aos infernos, e lá ficou todo o tempo que Seu Corpo esteve no sepulcro. Com estas palavras, confessamos igualmente que a mesma Pessoa de Cristo esteve nos infernos, ao mesmo tempo em que jazia num túmulo. Este fato não deve estranhar a ninguém. Conforme já dissemos várias vezes, a Divindade nunca se apartou da alma nem do corpo, não obstante a separação que houve entre alma e corpo. Vem agora a segunda cláusula do presente Artigo. Conforme insinua o Apóstolo: 'Lembra-te de que Nosso Senhor Jesus Cristo ressuscitou dentre os mortos!'(2 Tm 2,8) Não há dúvida, esta ordem dada a Timóteo se estende também a todos os mais que tenham encargo de almas. Vejamos, pois, o significado deste Artigo. Depois que Cristo Nosso Senhor rendeu o espírito na Cruz, na sexta-feira à hora nona (Pelas três horas da tarde), foi sepultado na tarde do mesmo dia, pelos Seus Discípulos. Com a permissão do procurador Pilatos, haviam descido da Cruz o Corpo do Senhor, e depositado num sepulcro, que ficava num jardim das imediações. No terceiro dia depois da morte, que era um domingo, pela madrugada, Sua Alma se uniu novamente ao Corpo. Deste modo, Aquele que por três dias estivera morto, tornou à vida que, com a morte, havia deixado, e ressuscitou."),
            
            Conteudo(categoria_id=1, opcao_id=7, titulo="6° Artigo - Subiu aos céus, está sentado à direita de Deus Pai Todo-Poderoso", 
                     texto="Os fiéis devem crer, sem a menor dúvida, que Jesus Cristo, depois de consumar o mistério de nossa Redenção, subiu aos céus enquanto Homem, com corpo e alma; enquanto Deus, nunca de lá se ausentou, pois que enche todos os lugares com Sua Divindade. Todavia, subiu por virtude própria. Não foi arrebatado por uma força estranha, como Elias que fora levado ao céu num carro de fogo (2 Rs 2,11-12), nem como Habacuc (Dn 14,35) ou o diácono Filipe (At 8,39) que, transportados através dos ares por uma virtude divina, venceram as distâncias de terras longinquas. Entretanto, não subiu aos céus só pela virtude de Sua Onipotência, mas também em Sua condição de homem. Isto não podia acontecer por força da natureza; mas, pela virtude de que estava munida, podia a gloriosa Alma de Cristo mover o corpo a seu grado. Tendo já a posse da glória, o corpo obedecia, sem dificuldade, a direção que a alma lhe dava, em seus movimentos. Desta maneira é que acreditamos ter Cristo subido. Na segunda parte do Artigo estão as palavras: 'Está sentado à direita de [Deus] Pai'. Esta figura de expressão encerra uma figura de linguagem, muito usada nas Escrituras. Para maior facilidade de compreensão, atribuímos a Deus afetos e membros humanos, apesar de não podermos imagine nada de corpóreo em Deus, porque é [puro] espírito. Mas, como nas relações sociais julgamos dar maior honra a quem colocamos à nossa direita, assim aplicamos também o mesmo princípio às coisas do céu. Confessamos que Cristo está à direita do Pai, para exprimir a glória que, como Homem, alcançou acima de todas as criaturas."),
            
            Conteudo(categoria_id=1, opcao_id=8, titulo="7° Artigo - Donde há de vir julgar os vivos e os mortos", 
                     texto="As Sagradas Escrituras atestam que são duas as vindas do Filho de Deus. A primeira foi quando assumiu carne, para nos salvar, e Se fez homem no seio da Virgem; a segunda será, quando vier para julgar todos os homens, na consumação dos séculos. Nas Escrituras, esta segunda vinda se chama 'Dia do Senhor' (1 Pd 3,10; Ap 3,26), do qual diz o Apóstolo: 'O dia do Senhor há de vir como o ladrão de noite' (1 Ts 5,2). 'Aquele dia, porém, e aquela hora, ninguém os conhece', declara o próprio Salvador (Mt 24,36). Em prova do Juízo Final, basta citar esta passagem do Apóstolo: 'Todos nós teremos de comparecer perante o tribunal de Cristo, para que cada um receba retribuição do bem ou do mal, que tiver praticado em sua vida terrena' (2 Cor 5,10; Rm 14,10). Se desde o início do mundo, todos ansiavam por aquele primeiro dia em que o Senhor Se revestiu de nossa carne, porquanto nesse mistério havia a esperança de seu resgate, também agora devemos depois da Morte e Ascensão do Filho de Deus - suspirar ardentemente pelo segundo Dia do Senhor, 'aguardando a ditosa esperança e o aparecimento da glória do grande Deus'(Tt 2,13)."),
            
            Conteudo(categoria_id=1, opcao_id=9, titulo="8° Artigo - Creio no Espírito Santo", 
                     texto="Professamos que o Espírito Santo é a Terceira Pessoa da Santíssima Trindade, Deus igual ao Pai e ao Filho, procedendo de ambos como de um único princípio de amor. Conforme o Catecismo Romano, Ele é o sopro divino vivificante que governa, santifica e vivifica a Igreja, sendo o Consolador prometido por Cristo para guiar os apóstolos em toda a verdade."),
            
            Conteudo(categoria_id=1, opcao_id=10, titulo="9° Artigo - Creio na Santa Igreja Católica, na comunhão dos santos", 
                     texto="A Igreja é o Corpo Místico de Cristo, a sociedade visível dos fiéis convocados pela Palavra de Deus sob uma só cabeça na terra: o Papa. A 'Comunhão dos Santos' significa que todos os membros da Igreja — na terra (militante), no purgatório (padecente) e no céu (triunfante) — partilham dos mesmos bens espirituais, méritos, orações e sacramentos."),
            
            Conteudo(categoria_id=1, opcao_id=11, titulo="10° Artigo - A remissão dos pecados", 
                     texto="O Catecismo de Trento ensina que Cristo confiou à Igreja o poder de perdoar os pecados através dos sacramentos do Batismo e da Penitência. Este poder é absoluto e estende-se a qualquer pecado, por mais grave que seja, desde que haja verdadeiro arrependimento e contrição por parte do penitente."),
            
            Conteudo(categoria_id=1, opcao_id=12, titulo="11° Artigo - A ressurreição da carne", 
                     texto="Cremos que no último dia, por virtude de Deus, os corpos de todos os homens defuntos serão novamente unidos às suas respectivas almas. Os corpos dos justos ressuscitarão gloriosos e imortais, à semelhança do corpo de Cristo ressuscitado, para desfrutarem da eterna bem-aventurança."),
            
            Conteudo(categoria_id=1, opcao_id=13, titulo="12° Artigo - A vida eterna", 
                     texto="É o fim último do homem: a felicidade imperecível na visão beatífica de Deus. Para os eleitos, será a posse total e eterna de Deus no Céu; para os ímpios e condenados, infelizmente, significará a separação eterna de Deus e o castigo eterno no inferno, conforme a justiça divina."),

            Conteudo(categoria_id=2, opcao_id=1, titulo="O que é Sacramento?", 
                     texto="Conforme o Concílio de Trento, Sacramento é um sinal visível da graça invisível, instituído por Jesus Cristo para nossa santificação. São sete canais eficazes que não apenas simbolizam, mas realizam e conferem o que significam (ex opere operato) aos que não lhes opõem obstáculos."),
            
            Conteudo(categoria_id=2, opcao_id=2, titulo="Batismo", 
                     texto="O Sacramento da regeneração pela água na Palavra. Apaga o pecado original, todos os pecados atuais (se houver), infunde a graça santificante e imprime na alma o caráter indelével de filho de Deus e membro da Igreja. É a porta de entrada para os demais sacramentos."),
            
            Conteudo(categoria_id=2, opcao_id=3, titulo="Confirmação (Crisma)", 
                     texto="Sacramento que robustece e aperfeiçoa a graça batismal. Por meio da unção com o santo crisma e a imposição das mãos do Bispo, o fiel recebe a efusão plenária do Espírito Santo e seus sete dons, tornando-se soldado de Cristo para defender e propagar a fé."),
            
            Conteudo(categoria_id=2, opcao_id=4, titulo="Eucaristia", 
                     texto="O maior de todos os Sacramentos. Sob as espécies de pão e vinho, após a consagração sacerdotal, Cristo está contido verdadeira, real e substancialmente em Seu Corpo, Sangue, Alma e Divindade pela Transubstanciação. É o sacrifício incruento do Calvário renovado no altar (Santo Sacrifício da Missa)."),
            
            Conteudo(categoria_id=2, opcao_id=5, titulo="Penitência (Confissão)", 
                     texto="Instituído por Cristo para perdoar os pecados cometidos após o Batismo. Exige do penitente: exame de consciência, contrição (dor do pecado), propósito de não mais pecar, confissão íntegra dos pecados graves ao sacerdote e o cumprimento da satisfação (penitência)."),
            
            Conteudo(categoria_id=2, opcao_id=6, titulo="Unção dos Enfermos", 
                     texto="Sacramento instituído para aliviar espiritual e corporalmente os fiéis gravemente enfermos ou em perigo de morte. Alivia a alma, perdoa os pecados veniais (e até mortais não confessados por impossibilidade, desde que haja contrição), e concede forças contra as tentações da agonia."),
            
            Conteudo(categoria_id=2, opcao_id=7, titulo="Ordem", 
                     texto="Sacramento pelo qual homens são constituídos ministros sagrados na Igreja, recebendo o poder espiritual e a graça para exercer as funções divinas (oferecer o Sacrifício da Missa, perdoar pecados e governar o povo de Deus). Divide-se em Episcopado, Presbiterado e Diaconato."),
            
            Conteudo(categoria_id=2, opcao_id=8, titulo="Matrimônio", 
                     texto="A união indissolúvel e legítima entre um homem e uma mulher cristãos, elevada por Cristo à dignidade de Sacramento. Concede aos esposos a graça de se amarem santamente, de guardarem fidelidade mútua e de educarem os filhos na fé e no temor de Deus."),

            Conteudo(categoria_id=3, opcao_id=1, titulo="O que é o Decálogo?", 
                     texto="São os Dez Mandamentos da Lei de Deus, gravados no coração do homem pelo Criador (Lei Natural) e promulgados no Monte Sinai. O Catecismo Romano ensina que sua observância é obrigatória para todos os homens e resume-se em dois preceitos: Amar a Deus sobre todas as coisas e ao próximo como a si mesmo."),
            
            Conteudo(categoria_id=3, opcao_id=2, titulo="1° Mandamento - Eu sou o Senhor teu Deus, que te tirei da terra do Egito, da mansão do cativeiro", 
                     texto="Ordena-nos adorar o único Deus verdadeiro com fé, esperança e caridade. Proíbe a idolatria, a superstição, o sacrilégio, o ateísmo e o culto a falsos deuses. A veneração das imagens dos santos e da Virgem Maria é legítima, pois honra o protótipo e não o objeto em si."),
            
            Conteudo(categoria_id=3, opcao_id=3, titulo="2° Mandamento - Não tomarás em vão o nome do Senhor teu Deus", 
                     texto="Prescreve o respeito devido ao Nome Santíssimo de Deus e das coisas sagradas. Proíbe a blasfêmia, os juramentos falsos ou desnecessários (perjúrio) e a violação de votos feitos a Deus."),
            
            Conteudo(categoria_id=3, opcao_id=4, titulo="3° Mandamento - Lembra-te de santificar o dia do sábado", 
                     texto="Na Lei Antiga, guardava-se o sábado; na Nova Lei, a Igreja transferiu essa obrigação para o Domingo, dia da Ressurreição do Senhor. Exige a participação na Santa Missa e o repouso de trabalhos servis para a dedicação ao culto divino e obras de caridade."),
            
            Conteudo(categoria_id=3, opcao_id=5, titulo="4° Mandamento - Honra teu pai e tua mãe, para teres longa vida na terra, que o Senhor teu Deus te há de dar", 
                     texto="Ordena o respeito, amor, obediência e assistência material e espiritual aos pais. Estende-se também aos legítimos pastores da Igreja, governantes e superiores naquilo que não for contrário à lei de Deus."),
            
            Conteudo(categoria_id=3, opcao_id=6, titulo="5° Mandamento - Não matarás!", 
                     texto="Proíbe o homicídio voluntário, o aborto, a eutanásia, o suicídio, a automutilação e a violência injusta. Proíbe também o escândalo, que é o ato de induzir outrem ao pecado, matando a vida da graça na alma do próximo."),
            
            Conteudo(categoria_id=3, opcao_id=7, titulo="6° Mandamento - Não cometerás adultério", 
                     texto="Ordena a pureza e a castidade nos atos, palavras e comportamentos, segundo o estado de vida de cada um. Proíbe o adultério, a fornicação, a pornografia e qualquer ato sexual fora da legitimidade do matrimônio."),
            
            Conteudo(categoria_id=3, opcao_id=8, titulo="7° Mandamento - Não furtarás", 
                     texto="Proíbe o roubo, o furto, a retenção injusta dos bens alheios, a fraude nos negócios, a usura e qualquer dano causado à propriedade do próximo. Exige a realização integral do que foi roubado ou fraudado."),
            
            Conteudo(categoria_id=3, opcao_id=9, titulo="8° Mandamento - Não dirás falso testemunho contra o teu próximo", 
                     texto="Proíbe a mentira, o falso testemunho em juízo, a calúnia, a difamação, os juízos temerários e a violação do segredo (especialmente o segredo de confissão). Exige a reparação da honra lesada do próximo."),
            
            Conteudo(categoria_id=3, opcao_id=10, titulo="9° e 10° Mandamentos - Não cobiçarás os bens alheios", 
                     texto="O 9° proíbe os desejos impuros e pensamentos consentidos contra a castidade. O 10° proíbe a cobiça desordenada dos bens alheios e a inveja do progresso material do próximo. Ambos atacam a raiz interna dos pecados (o coração)."),

            Conteudo(categoria_id=4, opcao_id=1, titulo="O que é oração?", 
                     texto="A oração é a elevação da alma a Deus para louvá-Lo, dar-Lhe graças e pedir-Lhe os bens necessários para a nossa salvação. O Catecismo de Trento ensina que ela é um dever de piedade e uma necessidade absoluta para obtermos a graça do auxílio divino."),
            
            Conteudo(categoria_id=4, opcao_id=2, titulo="Introdução à Oração Dominical - Pai-Nosso, que estais nos céus", 
                     texto="Chamamos Deus de 'Pai' para reconhecer Sua infinita bondade e misericórdia, inflamando em nós o amor filial e a confiança. 'Que estais nos céus' não indica limitação de espaço, mas a excelsa majestade de Deus e a pátria para a qual caminhamos."),
            
            Conteudo(categoria_id=4, opcao_id=3, titulo="1ª Petição - Santificado seja o Vosso Nome", 
                     texto="Pedimos que o Nome de Deus seja glorificado, conhecido e honrado por toda a humanidade através de nossas vidas, palavras e ações santas, evitando que Seu Nome seja blasfemado por culpa dos nossos pecados."),
            
            Conteudo(categoria_id=4, opcao_id=4, titulo="2ª Petição - Venha a nós o Vosso Reino", 
                     texto="Pedimos o Reino da Graça em nossas almas nesta vida, o triunfo da Igreja no mundo e, finalmente, a consumação do Reino da Glória no Céu, onde reinaremos eternamente com Deus."),
            
            Conteudo(categoria_id=4, opcao_id=5, titulo="3ª Petição - Seja feita a Vossa vontade, assim na terra como no Céu", 
                     texto="Suplicamos a graça de obedecer perfeitamente aos mandamentos de Deus na terra com a mesma prontidão, amor e fidelidade com que os anjos e santos O obedecem no Céu."),
            
            Conteudo(categoria_id=4, opcao_id=6, titulo="4ª Petição - O pão nosso de cada dia nos dai hoje", 
                     texto="Pedimos o sustento material necessário para o corpo (alimento, vestuário, saúde) sem ganância, e principalmente o sustento espiritual da alma: a Palavra de Deus e a Santíssima Eucaristia."),
            
            Conteudo(categoria_id=4, opcao_id=7, titulo="5ª Petição - Perdoai-nos as nossas dívidas, assim como nós perdoamos aos nossos devedores", 
                     texto="Imploramos a misericórdia de Deus para o perdão dos nossos pecados. No entanto, o próprio Cristo estabelece uma condição solene: Deus só nos perdoará se perdoarmos de coração as ofensas recebidas do nosso próximo."),
            
            Conteudo(categoria_id=4, opcao_id=8, titulo="6ª Petição - E não nos deixeis cair em tentação", 
                     texto="Não pedimos para não sermos tentados (pois a tentação prova a virtude), mas sim para que Deus nos conceda a força espiritual e as graças atuais para resistirmos e não consentirmos nas seduções do demônio, do mundo e da carne."),
            
            Conteudo(categoria_id=4, opcao_id=9, titulo="7ª Petição - Mas livrai-nos do mal", 
                     texto="Pedimos que Deus nos livre de todos os males presentes, passados e futuros, tanto da alma (o pecado, a condenação) quanto do corpo, transformando as tribulações temporais em méritos para a eternidade."),
            
            Conteudo(categoria_id=4, opcao_id=10, titulo="Última palavra da oração dominical - Amém", 
                     texto="É a assinatura da fé. Significa 'Assim seja', expressando o nosso firme assentimento, o desejo ardente e a esperança confiante de obtermos tudo o que pedimos nas petições anteriores."),
            
            Conteudo(categoria_id=4, opcao_id=11, titulo="Outras orações", 
                     texto="A Igreja recomenda as orações litúrgicas, o Santo Rosário, as jaculatórias, a Ave-Maria e a invocação constante aos santos anjos e padroeiros como canais de oração e intercessão diante do trono divino."),

            Conteudo(categoria_id=5, opcao_id=1, titulo="O que é Dogma?", 
                     texto="Dogma é uma verdade de fé contida explicitamente na Revelação Divina (Escritura ou Tradição) e que o Magistério da Igreja propõe de forma infalível como obrigatória para a crença dos fiéis. Negar um dogma constitui heresia."),
            
            Conteudo(categoria_id=5, opcao_id=2, titulo="Dogma da Santíssima Trindade", 
                     texto="O mistério central da fé cristã. Há um só Deus verdadeiro em três Pessoas distintas e consubstanciais: o Pai, o Filho e o Espírito Santo. Não são três deuses, mas uma só natureza divina em três Pessoas."),
            
            Conteudo(categoria_id=5, opcao_id=3, titulo="Dogma da Divindade de Jesus Cristo", 
                     texto="Jesus Cristo é o Filho Unigênito de Deus, a Segunda Pessoa da Trindade, verdadeiro Deus e verdadeiro Homem. Possui duas naturezas (divina e humana) unidas hipostaticamente em uma única Pessoa divina."),
            
            Conteudo(categoria_id=5, opcao_id=4, titulo="Dogma da Imaculada Conceição", 
                     texto="Proclamado pelo Papa Pio IX (Ineffabilis Deus). A Bem-Aventurada Virgem Maria, por uma graça e privilégio singular de Deus, em previsão dos méritos de Cristo, foi preservada imune de toda mancha do pecado original desde o primeiro instante de sua concepção."),
            
            Conteudo(categoria_id=5, opcao_id=5, titulo="Dogma da Virgindade Perpétua de Maria", 
                     texto="Definido em vários concílios (como o de Latrão). Maria Santíssima permaneceu Virgem antes, durante e perpetuamente depois do parto de Jesus Cristo, operado por obra do Espírito Santo."),

            Conteudo(categoria_id=6, opcao_id=1, titulo="O que é Tradição?", 
                     texto="É a Palavra de Deus que não foi totalmente registrada por escrito na Bíblia, mas confiada por Cristo e pelo Espírito Santo aos Apóstolos e transmitida oralmente de geração em geração, mantida viva pela Igreja sem alteração na sua essência."),
            
            Conteudo(categoria_id=6, opcao_id=2, titulo="O que são as Escrituras?", 
                     texto="A Bíblia Sagrada é a coleção de livros escritos por homens sob a inspiração direta do Espírito Santo. Tem Deus por autor e contém a verdade salvífica sem erro. O Cânon católico foi fixado infalivelmente no Concílio de Trento."),
            
            Conteudo(categoria_id=6, opcao_id=3, titulo="O que é Magistério?", 
                     texto="É o encargo e o poder de ensinar em nome de Jesus Cristo, confiado exclusivamente ao Papa e aos Bispos em comunhão com ele. O Magistério não está acima da Palavra de Deus, mas a serve, interpretando-a de forma autêntica e infalível."),
            
            Conteudo(categoria_id=6, opcao_id=4, titulo="Quais suas importâncias?", 
                     texto="Formam o tripé da fé católica (Constituição Dei Verbum). Eles estão de tal forma interligados que um não subsiste sem os outros. A Escritura e a Tradição são o depósito da fé, e o Magistério garante a sua interpretação correta contra heresias."),

            Conteudo(categoria_id=7, opcao_id=1, titulo="O que é a Igreja Católica?", 
                     texto="É a única e verdadeira Igreja fundada por Jesus Cristo sobre o apóstolo Pedro (Mt 16,18). Conforme o Catecismo de Trento e a encíclica Mystici Corporis Christi de Pio XII, ela é visível e invisível, una na fé e sacramentos, santa em sua doutrina, católica (universal) e apostólica. Fora dela não há salvação (Extra Ecclesiam nulla salus), entendida como a necessidade de pertença à arca da salvação que é Cristo através de Seu Corpo Místico."),
                        
            Conteudo(categoria_id=7, opcao_id=2, titulo="Notas da Igreja",
                     texto="As notas da Igreja são as propriedades que a identificam como a única e verdadeira Igreja de Cristo: Ela é Uma, Santa, Católica e Apostólica."),
            
            Conteudo(categoria_id=7, opcao_id=3, titulo="Membros da Igreja",
                     texto="São membros da Igreja Católica todos os batizados que professam a fé católica, participam dos sacramentos e estão em união com o Papa e a hierarquia da Igreja.")
        ]
        
        db.session.bulk_save_objects(dados)
        db.session.commit()
        print("Banco de dados inicializado com sucesso!")

if __name__ == '__main__':
    povoar_banco()