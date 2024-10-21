# Cloud Functions

Para o upload de imagens, foi pensado em criar uma cloud function (a AWS Lambda da GCP), isso porque a criação de imagens além de salvar no bucket, poderia salvar elas no banco, recebendo um produto. São diferentes formas de fazer, mas vou deixar aqui a forma de testar localmente e um esboço da function pra salvar no bucket.

## Formas para rodar local

### Primeira Forma
- Instalar o functions-framework no ambiente virtual da function em que esteja desenvolvendo, mas não por nos requirements.txt
  `pip install functions-framework`

- Adicionar import e decorator no código a ser testado
```python
import functions_framework

@functions_framework.http
def hello(request):
    return "Hello world!"
```
- Executar no terminal

```bash
functions-framework --target hello --debug
```

### Segunda Forma
- Para testar as functions localmente, utilizar o [pacote](https://www.npmjs.com/package/@google-cloud/functions-framework) @google-cloud/functions-framework, rodando o comando no diretório correspondente ao da function a ser testada. Exemplo:
```bash
npx @google-cloud/functions-framework --target=<entrypoint>	
```

## Observações
- Outros exemplos são encontrados [aqui](https://github.com/GoogleCloudPlatform/functions-framework-python)

