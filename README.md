<div align="center">
 
  ![Bote (1)](https://user-images.githubusercontent.com/98557500/207730448-b865fa5d-c884-4c5b-a800-b694ab4038c2.png)

</div>
<h1 align="center"> Bote </h1>
          
![GitHub top language](https://img.shields.io/github/languages/top/fga-eps-mds/2022-2-Bote?style=flat)
![GitHub contributors](https://img.shields.io/github/contributors/fga-eps-mds/2022-2-Bote?style=flat)
![GitHub issues](https://img.shields.io/github/issues-raw/fga-eps-mds/2022-2-Bote?style=flat)
![GitHub last commit](https://img.shields.io/github/last-commit/fga-eps-mds/2022-2-Bote?style=flat)
![GitHub closed issues](https://img.shields.io/github/issues-closed-raw/fga-eps-mds/2022-2-Bote?style=flat)
[![GitHub Status Badge](https://dev.azure.com/Squad05-Bote/Bote/_apis/build/status/fga-eps-mds.2022-2-Bote%20(2)?branchName=main)](https://dev.azure.com/Squad05-Bote/Bote/_build/latest?definitionId=3&branchName=main&style=for-the-badge)
[![codecov](https://codecov.io/github/fga-eps-mds/2022-2-Bote/branch/main/graph/badge.svg?token=Q3JLLAIH9Q)](https://codecov.io/github/fga-eps-mds/2022-2-Bote)


# 🛶 Descrição do Projeto
Projeto em desenvolvimento para a disciplina de Métodos de Desenvolvimento de Software, ministrada na Universidade de Brasília (UnB) - Faculdade do Gama (FGA), no segundo semestre letivo de 2022. 
O Bote é um bot para Telegram que visa facilitar o compartilhamento de materiais de um curso ao enviá-los de forma automática para os alunos matriculados.
          
O Bote permitirá que professores façam upload de materiais e estabeleçam uma ordem para que sejam enviados automaticamente aos alunos. O critério para compartilhamento de um novo bloco de materiais é que o aluno tenha confirmado que já estudou o material anterior.

O projeto é composto de 2 bots, o bot de criação dos cursos ([bot_cursos.py](bot_cursos.py)), e o bot de interação com os alunos ([bot_alunos.py](bot_alunos.py)). Para rodar sua instância de cada um deles, basta colocar os Tokens do seus bots nas variáveis BOT_TOKEN no topo dos arquivos de cada bot.

Conheça mais sobre o projeto em nossa [GitPage](https://fga-eps-mds.github.io/2022-2-Bote/#/?id).
          
# 📈 Status do Projeto

- Release 2 entregue
- ~~Release 1 entregue~~

<!--
# :hammer: Funcionalidades do projeto
 
<h4 align="center"> 
    :construction:  em construção  :construction:
</h4>

- `Funcionalidade 1`: descrição da funcionalidade 1
- `Funcionalidade 2`: descrição da funcionalidade 2
- `Funcionalidade 2a`: descrição da funcionalidade 2a relacionada à funcionalidade 2
- `Funcionalidade 3`: descrição da funcionalidade 3
-->     
                  
# 📁 Acesso ao projeto

- Para acessar o bot hospedado para esse trabalho, é necessário acessar pelo link ou pesquisando no telegram [@GerenciadorDeCursosBot](t.me/GerenciadorDeCursosBot) para acessar o bot do professor responsável pelo envio dos conteúdos, e [@cursos_sender_bot](t.me/cursos_sender_bot) para acessar o bot dos alunos que recebem o conteúdo no Telegram.

# 🛠️ Abrir e rodar o projeto
>Para rodar uma instância do bot, é necessário modificar os campos de texto correspondentes aos Bot Tokens e colocar os tokens correspondentes a sua conta e bot, pois os tokens atuais se conectam a conta e ao bot hospedados pelo projeto. 
- ### Windows
Baixe o pacote Python3 do [site official](https://www.python.org/downloads/), e no momento da instalação, marque a opção "Add Python to PATH" para no próximo passo instalar as dependências via terminal.

- ### Linux
Execute no terminal do Linux a atualização dos pacotes e instalação do python3

```bash
sudo apt update
sudo apt install python3
sudo apt install python3-pip
```
- ### Ambos os sistemas
Abra um terminal na pasta raiz onde foram salvos os arquivos do projeto e execute o comando:

```bash
pip install -r requirements.txt
```
- ### Execução
```
python3 ./app.py
```
ou 
```
python ./app.py
```

>Caso tenha problemas para importar os pacotes para rodar o projeto, rode os comandos em terminal elevado (de administrador), e caso ainda tenha problemas, recomendamos acessar o FAQ do [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-Asked-Questions#why-am-i-getting-importerror-cannot-import-name-xy-from-telegram).
                  
# ✔️ Técnicas e tecnologias utilizadas

- Python
- API do Telegram
- SQLite
- Azure Pipelines
- Codecov
- Metodologias Ágeis
              
# ✒️ Autores
                  
<div align="center">

|  [<img src="https://avatars.githubusercontent.com/u/82895172?v=4" width=115><br><sub>Otávio</sub>](https://github.com/knz13) | [<img src="https://avatars.githubusercontent.com/u/56135971?v=4" width=115><br><sub>Ana Letíca</sub>](https://github.com/analeticiaa) |  [<img src="https://avatars.githubusercontent.com/u/59586312?v=4" width=115><br><sub>Arthur</sub>](https://github.com/arthur-augusto) |  [<img src="https://avatars.githubusercontent.com/u/98557500?v=4" width=115><br><sub>Brunna</sub>](https://github.com/brunna-martins) |  [<img src="https://avatars.githubusercontent.com/u/22137470?v=4" width=115><br><sub>Caetano</sub>](https://github.com/caeslucio) |  [<img src="https://avatars.githubusercontent.com/u/97994511?v=4" width=115><br><sub>Larissa</sub>](https://github.com/larigs) |
| :---: | :---: | :---: | :---: | :---: | :---: |

</div>

É possível ver a lista de todos os [colaboradores](https://github.com/fga-eps-mds/2022-2-Squad05/colaboradores) que participaram deste projeto.

# 📄 Licença

Este projeto está sob a licença [MIT](https://opensource.org/licenses/MIT)

# 🎁 Expressões de gratidão

- Conte a outras pessoas sobre este projeto! 📢 <br>
A sua divulgação é valiosa para nós. ❤️
<br>
<br>
- Convide alguém da equipe para um café! ☕ <br>Nós não mordemos! 😅 
