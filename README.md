# Automação de Lançamento de Atendimentos NAF

Esse script tem como objetivo automatizar o lançamento de fichas de atendimento do Núcleo de Apoio Contábil e Fiscal (NAF) no site da Receita Federal do Brasil. Implementado em Python, utilizando a biblioteca Selenium.

## Pré-requisitos

- Python 3.x
- Bibliotecas Python: pandas, selenium
- GeckoDriver (para Firefox) - Incluído na pasta "geckodriver" no projeto

## Como Usar

1. Clone este repositório.
2. Instale as dependências usando `pip install -r requirements.txt`.
3. Execute o script: `python ficha-de-servico-naf.py`.

O script lê dados de atendimentos a partir de um arquivo CSV ("Controle de Atendimentos 2023.xlsx - Página3.csv") usando a biblioteca pandas. Certifique-se de que esse arquivo esteja no mesmo diretório que o script.

## Configuração do Ambiente

- O script utiliza o navegador Firefox para automação.
- Certifique-se de ter o GeckoDriver apropriado para o seu sistema operacional (Linux ou Windows) na pasta "geckodriver".

## Detalhes do Script

1. Abre o navegador Firefox.
2. Acessa a URL do formulário.
3. Remove overlays de login e cookies.
4. Itera sobre os atendimentos no arquivo CSV, preenchendo o formulário para cada atendimento.
5. Captura screenshots da página de confirmação para cada atendimento.

## Estrutura do Projeto

- `ficha-de-servico-naf.py`: O script principal.
- `geckodriver/`: Pasta contendo o GeckoDriver.
- `prints/`: Pasta onde as capturas de tela são salvas.

## Notas Importantes

- Certifique-se de ajustar o caminho do arquivo CSV e outros parâmetros conforme necessário.
- O script contém comentários explicativos para melhor compreensão do código.
- As capturas de tela são salvas na pasta "prints" para referência visual.
