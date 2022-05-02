# API-modelos-IA

API REST em Python para modelos de IA utilizando o framework Flask.

## Especificações:
1. Ao fazer uma requisição GET para /modelo/, deverá ser retornado todos os modelos e suas descrições
em um JSON unificado.

2. Ao fazer uma requisição GET para /modelo/<nome-do-modelo>, onde <nome-do-modelo> é o
parâmetro, deverá ser retornado um JSON contendo somente o nome e a descrição do modelo
requisitado.
  
3. Ao fazer uma requisição POST para /modelo/, essa rota deverá receber um JSON de entrada e
armazenar as informações do novo modelo no banco de dados.
 
## Exemplo de JSON enviado para a aplicação
```
{
  "nome": "AlexNet",
  "descricao": "Modelo de CNN para classificação de imagens. Possui uma
  estrutura complexa com milhões de parâmetros."
}
```
## Bônus implementado:
1. Ao fazer uma requisição GET para /modelo/<id-do-modelo>, onde <id-do-modelo> é o
parâmetro, deverá ser retornado um JSON contendo somente o nome e a descrição do modelo
requisitado.

2. Ao fazer uma requisição PUT para /modelo/<id-do-modelo>, essa rota deverá receber um JSON de entrada e
atualizar as informações do modelo passado no parâmetro <id-do-modelo>.
  
3. Ao fazer uma requisiç/delete/<id-do-modelo>, o modelo informado em pelo parâmetro <id-do-modelo> deverá ser deletado da base de dados.
  
4. Deploy utilizando o Heroku.

5. Aplicação Web Cliente que acessa a API.
