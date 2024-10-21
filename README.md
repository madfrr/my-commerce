# My-Commerce

## Descrição

My-Commerce é um sistema que suporta operações básicas de e-commerce, como gerenciamento de usuários, produtos, anúncios e transações. O sistema utiliza PostgreSQL como banco de dados, integra-se com a Google Cloud Platform (GCP) para armazenamento de imagens e está configurado para deploy automático via Cloud Run e CI/CD do GitHub Actions.
Esse projeto também serve para ser utilizado como boilerplate.

## Instruções para Compilar e Executar o Projeto
## Como Usar

O primeiro passo é fazer uma cópia do arquivo `.env_sample` e o renomear para `.env`. Após isso, é possível seguir com a execução do projeto utilizando ou não Docker.

### Docker
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

### Sem Docker
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

![MER](image.png)

#### Observações: 
	- Entidade "Order" foi criada pois a relação de transaction e Advertising estava N..N
	- No MeLi, o cliente consegue fazer apenas um pagamento e esse pagamento pode ser a compra de vários produtos de anúncios de vendedores diferentes. Mas para simplificar o diagrama, vamos considerar que o cliente consegue comprar/pagar 1 produto por vez;
	- No MER, produto aparece como entidade fraca de advertising, porém considerei com chave própria pois como o modelo está em estágio inicial, senti que seria uma melhoria prematura. Sem contar que essa modelagem pode evoluir para projetos como deduplicação de anúncios (onde existem vários anúncios com as mesmas características e produtos "iguais"), por exemplo.
    

### Arquitetura da API
Algumas regras de negócio são:
- 
### Estrutura de Pastas
### Justificativa para Frameworks ou Bibliotecas

## Trabalhos Futuros
### Regras de negócio:
- No endpoint de atualização de Advertising, adicionar regra de quando zerar a quantidade (quantity), atualizar o status para inativo;
- Ao criar uma order, atualizar Advertising com a regra acima, ou seja, toda order criada atualiza a quantity e status de uma Advertising;

### Arquitetura

## Observações
## Links Úteis
    - Link do diagrama
    - Link do vídeo


- CRUD simples de todas as entidades (create, read, read_list, update, delete) -> foi
- Adicionar Error handler -> foi
- Middleware para autenticação -> foi
- Subir postgres local -> foi
- Transaction buyer_id e seller_id tem que ser diferente  -> foi
- Deixar user.email unique -> foi
- Criar a freeaccount na GCP pro gsferreira.dev@gmail.com -> foi
- Criar Banco postgres sql -> foi
- Criar o bucket -> foi
- Criar código da function de produto -> foi
- Criar a Function -> foi
- CREATE, UPDATE, DELETE de produto bate na function, alterar na API -> foi
- Dockerfile -> foi
- Criar Cloud Run. -> foi
- Liberar acesso do ip publico para meu ip -> foi
- CI/CD GithubActions -> foi


Amanhã:
- Documentação
    - Fazer um readme detalhado, com os diagramas, tomadas de decisão, o que foi feito em cloud, o que falta fazer
    - Puxar o PDF ou JPG do draw.io para jogar aqui. Também puxar o arquivo do próprio draw.io

Vídeo:
    - Passar pelo diagrama ER
    - Falar o que foi feito em relação de serviço
    - Mostrar o que está deployado
    - Mostrar o banco de dados vazio
    - Rodar os Selects
    - Dizer o que falta fazer.

O que faltaria fazer
- Datadog
- Criar a fila do pub/sub
- Criar topico e sub da transaction
- Criar transaction publica na fila, modificar na API
- Conectar a fila no big query no pubsub
- Worker pro graphql
- graphql


- Vídeo explicativo

