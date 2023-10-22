import pandas as pd
from selenium import webdriver
import time, os


ATENDIMENTOS = pd.read_csv("Controle de Atendimentos 2023.xlsx - Página3.csv")
URL = "https://www.gov.br/receitafederal/pt-br/assuntos/educacao-fiscal/educacao-fiscal/naf/naf-questionarios/questionario-servico-prestado"


def main():
    if not os.path.exists("./prints"):
        os.mkdir("prints")

    driver = webdriver.Firefox()

    driver.get(URL)

    # Remove overlay de login
    driver.execute_script(
        "document.getElementById('govbr-login-overlay-wrapper').click()"
    )
    driver.execute_script("document.querySelector('button.reject-all').click()")
    # driver.execute_script("document.querySelector('header#site-header').remove()")

    time.sleep(30)

    # Loop sobre todos os atendimentos para lançamento
    for row in ATENDIMENTOS.head().iterrows():
        atendimento = row[1]

        data = atendimento[0]
        dia, mes, ano = data.split("/")
        cpf = atendimento[4]
        historico = atendimento[5]
        modalidade = atendimento[9]

        # Seleciona BA - UFBA - SALVADOR como instituição de ensino
        driver.execute_script(
            """
                let instituicao = document.getElementById("instituicao-responsavel-pelo-atendimento")
                                
                instituicao.selectedIndex = 37
            """
        )

        # Seleciona dia, mês e ano
        driver.execute_script(
            f"""
                let year = document.getElementById("edit_form_data-de-atendimento_0_year")
                                
                year.selectedIndex = year.childElementCount - 1 

                let month = document.getElementById("edit_form_data-de-atendimento_0_month")

                month.selectedIndex = {int(mes)}

                let day = document.getElementById("edit_form_data-de-atendimento_0_day")
                                
                day.selectedIndex = {int(dia)}
            """
        )

        # Seleciona a modalidade do atendimento
        radio_modalidade = ""
        if modalidade == "PRESENCIAL":
            radio_modalidade = "document.getElementById('modalidade-de-atendimento_1')"
        else:
            radio_modalidade = "document.getElementById('modalidade-de-atendimento_2')"

        driver.execute_script(
            f"""
                {radio_modalidade}.checked = true
            """
        )

        # Verifica tipo de usuário
        is_cnpj = len(cpf) == 18

        if is_cnpj:
            driver.execute_script(
                "document.getElementById('tipo-de-usuario').selectedIndex = 2"
            )
        else:
            driver.execute_script(
                "document.getElementById('tipo-de-usuario').selectedIndex = 1"
            )

        # Seleciona "sim" para atendimento conclusivo
        driver.execute_script(
            """
                let atendimento_conclusivo = document.getElementById('o-atendimento-prestado-foi-conclusivo')
                                    
                atendimento_conclusivo.selectedIndex = 1
            """
        )

        # Seleciona tipo de atendimento: "outro"
        driver.execute_script(
            """
                let outro_checkbox = document.getElementById('tipo-de-atendimento_23')

                outro_checkbox.checked = true
            """
        )

        # Escreve a especificação do atendimeto
        driver.execute_script(
            f"""
                let input_descricao = document.getElementById('se-respondeu-outro-especifique-aqui')

                input_descricao.value = '{historico}'
            """
        )

        # Clica no butão de enviar
        # driver.execute_script("document.querySelector('.formControls > input.context').click()")

        # Tira screenshot da página de confirmação
        driver.execute_script("document.querySelector('header#site-header').remove()")
        driver.execute_script("document.querySelector('nav.govbr-skip-menu').remove()")
        driver.execute_script("document.querySelector('footer#portal-footer').remove()")
        time.sleep(5)

        driver.save_full_page_screenshot(
            os.path.join("./prints", f"screenshot-{int(time.time())}.png")
        )

        driver.get(URL)

    driver.close()


if __name__ == "__main__":
    main()
