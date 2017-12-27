# Leia-me

Esse protótipo foi desenvolvido para atender aos requisitos do T1 da disciplina Sistemas Multiagentes,  Profa. Célia Ghedini Ralha.A licença é de livre utilização e cópia sem necessidade de citar o autor. 

Está hospedado em https://unb-multiagents.firebaseapp.com/. 

Código fonte e relatório em markdown disponível em https://github.com/lucasosouza/unb-multiagents.

# Relatório

> O aluno deve enviar um relatório descrevendo o modelo escolhido com o respectivo ambiente e
suas propriedades, descrição do(s) agente(s) com PAGE (Percepts, Actions, Goals, Environment),
linguagem/ferramenta utilizada, programa fonte, o executável, uma pequena explicação de como
executar o programa (readme file). Todos estes arquivos devem ser compactados (zipados) em um
único arquivo.

## Ambiente e suas propriedades

O ambiente é a simulação de uma sala com sujeira, com 16 peças de cerâmica, ou quadrados. Cada quadrado tem dois estados possíveis, sujo e não-sujo. De acordo com a classificação de Russel e Norvig, o ambiente é:

- Parcialmente observável: o agente não tem conhecimento do estado dos quadrados adjacentes, apenas do quadrado onde está no momento. O agente tem conhecimento da sua posição na sala. 
- Agente único: há apenas um agente em ação no ambiente.
- Determinístico: O próximo estado é totalmente determinável a partir do estado atual e da ação escolhida pelo agente.
- Sequencial: o estado atual do ambiente é afetado pelas ações anteriores tomadas pelo agente.
- Estático: o estado atual do ambiente não é alterado enquanto o agente delibera suas ações. Foi implementado também uma versão dinâmica (ou semi-estatíca), onde o estado atual do ambiente pode alterar enquanto o agente delibera e executa a ação. 
- Discreto: o ambiente tem um número finito de estados.
- Conhecido: o agente tem conhecimento do impacto das suas ações no ambiente.

## Descrição do agente com PAGE

- Performance Measure: a performance é avaliada pelo número de ações necessárias para limpar cada quadrado, denominado Actions/CleanedTiles Ratio e exibida na interface. O agente reativo baseado em modelo apresenta uma média de 3 ações por quadrado limpado, enquanto o agente reativo simples tem uma performance média de 6 ações por quadrado.

- Actuators: o agente age sobre o ambiente se movendo, em quatro direções (esquerda, direita, acima, abaixo), e limpando o quadrado quando sujo. Essas cinco ações são as únicas disponíveis ao agente.

- Sensors: o agente é capaz de perceber o estado atual do quadrado (se sujo ou limpo) e as movimentações possíveis a partir do quadrado em que está (por exemplo no canto superior direito, as únicas movimentações possíveis são esquerda e abaixo). O agente não consegue perceber sujeira além do quadrado em que está localizado. 

- Environment: o ambiente é uma sala, com 16 quadrados, que podem estar sujos ou não. O agente se locomove no ambiente entre quadrados adjacentes na linha horizontal ou vertical, um quadrado por vez. 

## Linguagem/ferramenta utilizada

O projeto foi desenvolvido em Javascript, com elementos do Javascript versão ES6, como a utilização de classes. Para comunicação com a interface foi utilizado o framework Angular, da Google. 

Javascript não é uma linguagem puramente orientada a objeto, o que dificulta a programação em modelo orientado a objeto. A escolha da tecnologia foi motivada pela interface simpels, utilizando HTML e CSS, e a facilidade de reprodução via navegador.

## Programa Fonte

Código fonte em https://github.com/lucasosouza/unb-multiagents e anexo a este relatório.

## Executável

Está hospedado em https://unb-multiagents.firebaseapp.com/. 

Outra opção é rodar em máquina local, utilizando qualquer servidor web. Se OSX, acessar a pasta public e rodar o comando `python -m SimpleHTTPServer`. Após inicializar o servidor, acessar localhost:8000 no navegador.
