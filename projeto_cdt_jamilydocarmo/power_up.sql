CREATE TABLE IF NOT EXISTS exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    grupo_muscular TEXT NOT NULL,
    musculos TEXT NOT NULL,
    execucao TEXT NOT NULL
);

INSERT INTO exercicios (nome, grupo_muscular, musculos, execucao) VALUES

('Elevação de quadril', 'gluteos', 'Glúteos',
'Deite-se de costas, dobre os joelhos e mantenha os pés firmes no chão. Contraia o abdômen e eleve o quadril de forma controlada, apertando os glúteos no ponto mais alto. Depois, abaixe lentamente sem deixar o movimento descontrolado.'),

('Abdução de quadril', 'gluteos', 'Glúteos',
'Mantenha o tronco firme e faça o movimento de afastar a perna para o lado de maneira controlada. Evite inclinar o corpo para compensar o movimento. Retorne lentamente à posição inicial.'),

('Extensão de quadril', 'gluteos', 'Glúteos',
'Mantenha o tronco estável e leve uma perna para trás, realizando a extensão do quadril. Faça o movimento sem balançar o corpo e retorne lentamente à posição inicial.'),

('Agachamento', 'gluteos', 'Glúteos e quadríceps',
'Fique em pé com os pés aproximadamente na largura dos ombros. Flexione os joelhos e leve o quadril para trás, mantendo o tronco estável. Desça de maneira confortável e depois volte à posição inicial controlando o movimento.'),

('Stiff', 'gluteos', 'Glúteos e posteriores',
'Fique em pé com os pés firmes no chão e mantenha as costas em posição neutra. Leve o quadril para trás enquanto inclina o tronco, mantendo as pernas levemente flexionadas. Depois, volte à posição inicial usando o movimento do quadril.'),

('Agachamento', 'quadriceps', 'Quadríceps e glúteos',
'Posicione os pés de forma confortável, mantenha o peito aberto e flexione os joelhos enquanto leva o quadril para trás. Desça de maneira controlada e retorne à posição inicial sem realizar movimentos bruscos.'),

('Leg press', 'quadriceps', 'Quadríceps e glúteos',
'Sente-se no equipamento e mantenha as costas apoiadas. Posicione os pés na plataforma e empurre controladamente, sem travar os joelhos. Depois, flexione novamente as pernas de forma lenta e controlada.'),

('Cadeira extensora', 'quadriceps', 'Quadríceps',
'Sente-se com as costas apoiadas e ajuste o equipamento de acordo com sua posição. Estenda os joelhos de forma controlada, aproximando as pernas da posição reta. Depois, retorne lentamente.'),

('Mesa flexora', 'posteriores', 'Posteriores da coxa',
'Deite-se no equipamento com o corpo bem apoiado. Posicione as pernas corretamente e flexione os joelhos, aproximando os pés do corpo. Retorne lentamente à posição inicial.'),

('Stiff', 'posteriores', 'Posteriores e glúteos',
'Mantenha os pés firmes e os joelhos levemente flexionados. Leve o quadril para trás enquanto inclina o tronco, mantendo as costas em posição neutra. Retorne controladamente à posição inicial.'),

('Flexão nórdica', 'posteriores', 'Posteriores da coxa',
'Mantenha as pernas estabilizadas e o tronco alinhado. Incline o corpo lentamente para frente, controlando o movimento, e retorne à posição inicial de maneira segura.'),

('Elevação de panturrilha', 'panturrilhas', 'Panturrilhas',
'Fique em uma posição estável e eleve os calcanhares, apoiando o movimento na ponta dos pés. Faça uma pequena pausa no alto e depois abaixe lentamente.'),

('Panturrilha no leg press', 'panturrilhas', 'Panturrilhas',
'Posicione os pés na parte adequada da plataforma, mantendo apenas a região da frente dos pés apoiada. Empurre a plataforma com o movimento dos tornozelos, elevando os calcanhares e retornando de forma controlada.'),

('Puxada frontal', 'costas', 'Costas e bíceps',
'Sente-se com o corpo estabilizado e segure a barra com as mãos afastadas. Puxe a barra em direção à parte superior do peito, mantendo os ombros controlados. Depois, retorne lentamente.'),

('Remada baixa', 'costas', 'Costas e bíceps',
'Sente-se no equipamento e mantenha o tronco firme. Puxe o apoio em direção ao corpo, aproximando os cotovelos do tronco. Retorne lentamente, mantendo o controle durante todo o movimento.'),

('Remada unilateral', 'costas', 'Costas',
'Apoie o corpo de maneira estável e mantenha a coluna em posição confortável. Puxe o peso em direção ao tronco, levando o cotovelo para trás. Depois, abaixe lentamente.'),

('Pulldown', 'costas', 'Costas',
'Mantenha o corpo estável e segure o equipamento. Puxe o cabo para baixo utilizando principalmente o movimento dos braços e das costas. Retorne lentamente à posição inicial.'),

('Supino', 'peito', 'Peitoral, ombros e tríceps',
'Deite-se com as costas apoiadas e mantenha os pés firmes. Segure o peso com as mãos e desça de forma controlada em direção ao peito. Depois, empurre o peso para cima sem realizar movimentos bruscos.'),

('Crucifixo', 'peito', 'Peitoral',
'Mantenha as costas apoiadas e os braços posicionados de maneira confortável. Abra os braços de forma controlada e depois aproxime-os novamente, mantendo o movimento lento e estável.'),

('Flexão de braços', 'peito', 'Peitoral, ombros e tríceps',
'Posicione as mãos no chão e mantenha o corpo alinhado. Flexione os cotovelos para aproximar o corpo do chão e depois empurre o chão para retornar à posição inicial.'),

('Elevação lateral', 'ombros', 'Ombros',
'Fique em pé com os braços ao lado do corpo. Eleve os braços para os lados de maneira controlada, sem balançar o tronco. Depois, abaixe lentamente.'),

('Desenvolvimento de ombros', 'ombros', 'Ombros e tríceps',
'Mantenha o corpo estabilizado e segure os pesos na altura dos ombros. Empurre os pesos para cima de maneira controlada e depois retorne lentamente à posição inicial.'),

('Elevação frontal', 'ombros', 'Ombros',
'Fique em pé e mantenha os braços próximos ao corpo. Eleve os braços para a frente até uma altura confortável e depois abaixe lentamente, mantendo o tronco estável.'),

('Rosca direta', 'biceps', 'Bíceps',
'Fique em pé com os braços próximos ao corpo. Flexione os cotovelos para aproximar as mãos dos ombros, sem balançar o tronco. Depois, estenda os braços lentamente.'),

('Rosca martelo', 'biceps', 'Bíceps e antebraços',
'Segure os pesos com as palmas das mãos voltadas uma para a outra. Flexione os cotovelos mantendo os braços próximos ao corpo. Depois, retorne lentamente.'),

('Rosca alternada', 'biceps', 'Bíceps',
'Segure um peso em cada mão. Flexione um braço de cada vez, mantendo o cotovelo próximo ao corpo. Abaixe lentamente e repita com o outro braço.'),

('Tríceps na polia', 'triceps', 'Tríceps',
'Fique de frente para a polia e mantenha os cotovelos próximos ao corpo. Empurre o cabo para baixo até estender os braços e depois retorne lentamente à posição inicial.'),

('Tríceps francês', 'triceps', 'Tríceps',
'Segure o peso acima da cabeça e mantenha os cotovelos apontados para frente. Flexione os cotovelos levando o peso para trás da cabeça e depois estenda os braços de maneira controlada.'),

('Abdominal tradicional', 'abdomen', 'Abdômen',
'Deite-se com os joelhos flexionados e os pés apoiados. Contraia o abdômen e eleve o tronco de forma controlada, sem puxar o pescoço. Depois, retorne lentamente.'),

('Prancha', 'abdomen', 'Abdômen e core',
'Apoie os antebraços e mantenha o corpo alinhado. Contraia o abdômen e evite deixar o quadril cair ou subir excessivamente. Mantenha a posição de forma confortável e controlada.'),

('Abdominal bicicleta', 'abdomen', 'Abdômen',
'Deite-se de costas e mantenha os joelhos flexionados. Faça o movimento alternado das pernas enquanto realiza a rotação controlada do tronco. Evite puxar o pescoço durante o exercício.');