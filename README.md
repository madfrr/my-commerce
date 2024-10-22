# My-Commerce

## Descrição

My-Commerce é um sistema que suporta operações básicas de e-commerce, como gerenciamento de usuários, produtos, anúncios e transações. O sistema utiliza PostgreSQL como banco de dados, integra-se com a Google Cloud Platform (GCP) para armazenamento de imagens e está configurado para deploy automático via Cloud Run e CI/CD do GitHub Actions.
Esse projeto também serve para ser utilizado como boilerplate.

## Instruções para Compilar e Executar o Projeto
### Como Usar

O primeiro passo é fazer uma cópia do arquivo `.env_sample` e o renomear para `.env`. Após isso, é possível seguir com a execução do projeto utilizando ou não Docker.

#### Docker
Caso não houver docker instalado, é necessário fazer a instalação seguindos os passos em: [link docker](https://www.docker.com/products/docker-desktop), [link docker compose](https://docs.docker.com/compose/install/);

Para executar, basta digitar o comando abaixo no terminal
```bash
docker compose up --build
```

Para facilitar, os comandos acima foram adicionados em um Makefile. Então, caso tenha o make instalado no computador, basta executar:

```bash
make develop-docker
```

Com isso, tanto uma instancia do Postgres quanto a API serão levantadas. Para testar o funcionamento da API, acessar a rota de health-check, pois ela não necessita de autenticação.

```bash
curl --location 'localhost:5000/api/my-commerce/health-check'
```
Ou acessando a documentação via swagger pelo link `localhost:5000/api/my-commerce/docs`

#### Sem Docker
Caso deseje executar a aplicação em ambiente de desenvolvimento, para execução de testes, deve-se primeiro verificar se a versão instalada do Pythom em seu sistema operacional é maior ou igual a 3.10.12, por motivos de compatibilidade. Caso afirmativo, executar os seguintes comandos no terminal:
```bash
python3 -m venv venv 
source venv/bin/activate 
pip install -r requirements.txt
uvicorn --app-dir=./src server:api --reload --port 5000
```

Ou, executando com make:
```bash
make setup-local-dev-environment
make develop
```

Obs

### Testes e lint
Basta executar os comandos make abaixo ou verificar o comando por extenso dentro do Makefile.
```bash
make test
make lint
make format
```

## Decisões Técnicas e Arquiteturais
### Arquitetura dos Sistemas
    
![Arquitetura do Sistema](system_design.png)

- Existe um servidor hospedando a API do MyCommerce. Essa API executa operações de CRUD sobre o banco de dados Postgres.
- Foi escolhido um banco de dados relacional pois para transações e compras, é necessário ter consistência e respeitar as propriedades ACID.
- Ao realizar qualquer operação de escrita em uma entidade, uma mensagem pode ser enviada a um sistema de mensageria, como o Kafka ou o próprio Google Cloud Pub/Sub. Caso a ferramenta de mensageria escolhida seja o Pub/Sub, é possível plugar a saída de um tópico em uma tabela no Google Cloud BigQuery (uma ferramenta de Datalake e Analytics).
- Como dentro da parte de análise transacional entra análise de riscos e fraudes, foi pensado em conectar um worker na fila do pub/sub para popular um banco de grafos. O banco de grafos é comumente utilizado no mercado com esse intuito dado a facilidade de encontrar relações entre entidades (em outras palavras, caminhos dentro de um grafo). Esse mesmo serviço pode ter um processo responsável pela ingestão dos dados e outro processo para avaliar risco das últimas transações e, em caso de possível fraude, alertar um canal como Slack.

### Estrutura do Banco de Dados
Como Modelo Entidade Relacionamento (MER), as seguintes entidades foram elaboradas: Usuário(Cliente, Vendedor), Anuncio, Produto, Ordem (como uma ordem de serviço) e Transação. Como o código está padronizado em inglês, os nomes das entidades são respectivamente: User, Advertising, Product, Order e Transaction

#### Entidades:
- User: Usuário do sistema. Pode ser tanto um comprador quanto um vendedor;
- Advertising: É o anúncio de um determinado usuário. Um usuário pode ter vários anúnios mas um anúncio pertence somente a um usuário;
- Product: É o produto que está sendo "anunciado pelo anuncio";
- Order: Em um e-commerce, geralmente um cliente consegue executar apenas uma transação para comprar vários produtos, assim como um produto poderia também ser pago com transações diferentes (exemplo, transação de cashback + crédito);
- Transaction: É a transação feita entre dois usuários. 

#### Algumas regras ao elaborar o MER:
- Uma Transaction é ou uma compra ou uma venda;
- Um Advertising é de um Product em específico, porém pode ter N quantidade deste mesmo Product;
- Advertising tem data de expiração;
- Um Advertising pode ter no mínimo 0 produtos. Quando chega a esse valor, ele é desativado;
- Quando a data de expiração de um Advertising é alcançada, ele é desativado;

![MER](mer.png)

#### Observações: 
- Entidade "Order" foi criada pois a relação de transaction e Advertising estava N..N
- No MeLi, o cliente consegue fazer apenas um pagamento e esse pagamento pode ser a compra de vários produtos de anúncios de vendedores diferentes. Mas para simplificar o diagrama, vamos considerar que o cliente consegue comprar/pagar 1 produto por vez;
- No MER, produto aparece como entidade fraca de advertising, porém considerei com chave própria pois como o modelo está em estágio inicial, senti que seria uma melhoria prematura. Sem contar que essa modelagem pode evoluir para projetos como deduplicação de anúncios (onde existem vários anúncios com as mesmas características e produtos "iguais"), por exemplo.
    

### Arquitetura da API

A arquitetura da API pode ser entendida observando a estrutura de pastas abaixo. Resumidamente, todas as classes responsaveis pela interação com a camada HTTP se encontra na pasta `controllers`. Essas classes, chamam as responsáveis pela regra de negócio na camada de domínio (ou `domain`) que por sua vez interage com bancos de dados e serviços externos pela camada de repositório (ou `repositories`).

Na pasta `data`, além de encontrar os repositórios, também são encontrados as classes de conexão com banco de dados e um dump do próprio banco.

Em `error_handler` e `exceptions`, são encontradas todas as lógicas para lidar com qualquer erro da aplicação.

Em `models` são encontrados os DTOs e as classes de definição/serialização de objetos. Também são uteis para documentação. 

Algumas funcionalidades devem ser executadas como `middlewares`, ou seja, códigos que devem ser executados antes das requisições, como por exemplo validação de CORs e autenticação.

Lógicas que são comuns em vários lugares, são encontradas dentro de `utils`.

Para finalizar, foi utilizado o design pattern de *factory* com o objeto da API (objeto FastAPI). Basicamente, quando o app passa por algum método com prefixo "setup_", o app é modificado para receber esse novo conjunto de funcionalidades. Dessa forma fica fácil acoplar, desacoplar tanto as funcionalidades que já existem quanto novas. Sem contar que é possível reaproveitar essas funcionalidades em outras APIs. 
Tudo isso é possível ser observado a partir do método `create_api` no arquivo `build.py`. Exemplo: caso o desenvolvedor deseja remover os middlewares, basta remover a linha `setup_middlewares(app)`.

```
src
├── controllers
├── data
│   ├── dump.sql
│   ├── gevent_pgsql.py
│   ├── __init__.py
│   └── repositories
├── domain
├── error_handler
├── exceptions
├── middlewares
├── models
├── utils
├── server.py
├── lifespan.py
├── build.py
└── config.py
```

### Justificativa para Frameworks ou Bibliotecas

- FastAPI: Dentre as frameworks de desenvolvimento web em python, é uma das mais rápidas, permitindo processamento assíncrono de requisições. Possui integração nativa com OpenAPI, facilitando a criação de documentações, também possui tipagem forte na camada de HTTP, é bem adotado pela comunidade, tem atualizações frequentes e documentação bem escrita e com exemplos. Também foi cogitado utilizar Flask com SQLAlchemy, porém acredito que FastAPI seja mais prático.

- Pytest, pytest-cov, pytest-mock, pytest-env e pytest-docker: Usado para testes unitários e funcionais. São bibliotecas simples e eficazes o suficiente para garantir cobertura, detectar bugs e fazer mock de funções e métodos sem a necessidade de criar classes específicas de mock. Com o pytest-mock, também é possível investigar a quantidade de vezes que uma função é chamada e se os argumentos de entrada e retorno estão corretos. Com pytest-docker é possível levantar serviços e bancos no momento de execução de testes.

- ruff: É o linter que prefiro. Útil para manter um padrão de código, identificação de variáveis e importações não utilizadas, facilitando a leitura e manutenção do código.

- google-cloud-storage: Client da GCP para manipulação de arquivos no bucket da google, que eles chamam de cloud storage.

- psycopg2: Driver de conexão com PostgreSQL.

## Cloud

O projeto também foi deployado na GCP. Foi criado um container registry para subir as imagens do docker. As imagens são deployadas em uma solução serveless chamada Cloud Run. O Google Cloud Run está no meio termo da "escala de serveless" entre uma Máquina Virtual e uma AWS Lambda. Pesquisando pela internet, ela se assemelha ao AWS Fargate ou AWS AppRunner.
O Cloud Run cria um ou mais containers a partir do registry e também acessa o Cloud SQL, que é a versão gerenciada do PostgresSQL as a service da Google.

## Trabalhos Futuros
### Regras de negócio:
- No endpoint de atualização de Advertising, adicionar regra de quando zerar a quantidade (quantity), atualizar o status para inativo;
- Ao criar uma order, atualizar Advertising com a regra acima, ou seja, toda order criada atualiza a quantity e status de uma Advertising;

### Arquitetura:
- Criar fila no Google Cloud Pub/Sub;
- Publicar toda operação de escrita de transições no Pub/Sub;
- Criar worker responsável por analisar e alertar sobre fraudes, além de popular o GraphQL.
- Adicionar monitoramento como Requests por minuto (RPM), tempo médio das requisições, tempo médio em 80, 90 e 95 percentil, quantidade de erros por requisição por dia e erros 500 não mapeados. Tudo isso é possível ser feito pelo Datadog.

### Código:
- Melhorar a cobertura de testes;
- Adicionar mais testes funcionais;
- Adicionar novas funcionalidades para files. Talvez transformar ele em uma entidade com próprio controller e domain.

## Observações
- Dentro da pasta `postman` é possível importar as requisições e ambiente para usar o Postman;
- Dentro da pasta `lambda_functions` tem um exemplo de como criar uma lambda em ambiente de desenvolvimento

## Links Úteis
[Diagrama](https://drive.google.com/file/d/1KiddnHSylonrtCbz23Yjnux5R27XsBxb/view?usp=drive_link)
[Documentação](https://my-commerce-api-1001377699753.southamerica-east1.run.app/api/my-commerce/docs)
[Versão Deployada](https://docs.docker.com/compose/install/)
