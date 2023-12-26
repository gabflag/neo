# Neo

Link oficial do respositorio: https://github.com/gabflag/neo


Repositorio destinado para elaborar as estratégias e testar as mesmas com o Python.


Principais definições do projeto:

    Programas de estratégia única:
        Ter o calculo do Valor Esperado;
        Definição de StopLoss, TakeProfit, Tranding Stop, Custos Operacionais (Spreading, Impostos);
        O programa deve receber apenas uma função para criar a estratégia;
        Layout e informações similares ao que os testes da plataforma metatrader retorna.

        Links: https://www.metatrader5.com/pt/automated-trading/strategy-tester
    
    Programa de comparação de estratégias:
        Receber os dados obtidos das estratégias e parametros e comparar com outros
        resultados obtidos.

    Mapas de Fluxo de Desenvolvimento:
        Os mapas devem ser desenvolvidos na plataforma excalidraw
        Salvar o arquivo especifico do excalidraw dentro da pasta do bot desenvolvido


Como usar o GIT:

    É necessários estar sincronizado o repositório local com o repositório remoto. Comando relevantes:
        Retorna se ouve alguma atualização no repositório remoto: git fetch
        Verifica o que foi realizado no repositório local: git status
        Para verificar os logs do Git (não é o github): git log 

        Como sincronizar:
            Inicializar o Git: git init
            Criar o branch: git branch -M main
            Adicionando repositório remoto (através do ssh): git remote add origin git@github.com:gabflag/neo.git
            Para fazer o pull (puxar as atualizações do repositório remoto): git pull origin main
        
        Para subir as atualizações do repositório local para o remoto:
            git add *
            git commit -m 'atualizei uma parte do código'
            git status
            git push origin main

        Buscar atualizações no repositório remoto:
            Para verificar se esta tudo joia: git remote -v
            Buscar atualizações: git pull origin main
        
        Caso queira desfazer o git add:
            git reset
            ou
            git reset --hard
            
        Desfazer alteração em algum arquivo em especifico:
            git restore estrategias/rsi.py

        Teste no branch Gabriel
    
        Criando um novo Branch e logando nele:
            Estar logando no branch principal:
                git checkout main
            Criando e logando no branch gabriel: 
                git branch gabriel 
            Checando os branchs:
                git branch

            
            Antes de fazer os comandos abaixo, toda vez que executar
            alguma alteração é necessário comitar no branch em que se está
            
            Para atualizar o branch primario executar os comandos:
                git checkout main
                git merge gabriel

            Para atualizar o branch secundario executar os comandos:
                git checkout gabriel
                git merge main

        Joao acabou de fazer operacao no readme


Instalações necessárias e configurações necessárias:
    pip install yfinance
    pip install python-dotenv
    pip install plotly


    Adicionar arquivo .env com as seguintes variaveis:
        CAMINHO_DIRETORIOS_DE_ESTRATEGIAS


Links relevantes:
    Esse repositório tem algum testes realizados e uma ideia da estratégia que foi utilizada
    https://github.com/geraked/metatrader5?tab=readme-ov-file