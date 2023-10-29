import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time, os, platform


current_os = platform.system()

ATENDIMENTOS = pd.read_csv("Controle de Atendimentos 2023.xlsx - Página3.csv")
URL_RFB = "https://www.gov.br/receitafederal/pt-br/assuntos/educacao-fiscal/educacao-fiscal/naf/naf-questionarios/questionario-servico-prestado"


def makeDir(name):
    if not os.path.exists(f"./{name}"):
        os.mkdir(name)

    return os.path.join(".", name)


def getGeckodriverPath():
    if current_os == "Linux":
        geckodriver_path = os.path.join("geckodriver", "geckodriver")
    elif current_os == "Windows":
        geckodriver_path = os.path.join("geckodriver", "geckodriver.exe")
    else:
        raise Exception(f"Unsupported operating system: {current_os}")

    return geckodriver_path


def atendimentoValido(atendimento):
    is_conclusivo = atendimento[7]
    alread_sended = atendimento[8]

    return (is_conclusivo == "Conclusivo" and alread_sended == "NÃO")


def preencher_formulario(driver, atendimento):
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


def tirar_print(driver, save_path):
    driver.execute_script("document.querySelector('header#site-header').remove()")
    driver.execute_script("document.querySelector('nav.govbr-skip-menu').remove()")
    driver.execute_script("document.querySelector('footer#portal-footer').remove()")
    time.sleep(5)

    driver.save_full_page_screenshot(
        os.path.join(save_path, f"screenshot-{int(time.time())}.png")
    )


def main():
    prints_path = makeDir("prints")
    
    geckodriver_path = getGeckodriverPath()

    service = Service(geckodriver_path)

    driver = webdriver.Firefox(service=service)

    driver.get(URL_RFB)

    # Remove overlay de login
    driver.execute_script(
        "document.getElementById('govbr-login-overlay-wrapper').click()"
    )
    driver.execute_script("document.querySelector('button.reject-all').click()")

    time.sleep(5)

    # Loop sobre todos os atendimentos para lançamento
    for row in ATENDIMENTOS.head().iterrows():
        atendimento = row[1]
        historico = atendimento[5]

        if atendimentoValido(atendimento):
            preencher_formulario(driver, atendimento)

            time.sleep(5)
            
            # Tira screenshot da página de confirmação
            tirar_print(driver, prints_path)    
        else:
            print(f"Não conclusivo ou já enviado - {historico}")
            continue

        driver.get(URL_RFB)

    driver.close()


if __name__ == "__main__":
    main()
