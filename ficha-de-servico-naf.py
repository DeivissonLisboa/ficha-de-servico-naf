import os
import platform
import time
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


URL_RFB = "https://www.gov.br/receitafederal/pt-br/assuntos/educacao-fiscal/educacao-fiscal/naf/naf-questionarios/questionario-servico-prestado"


def makeDir(path):
    if not os.path.exists(path):
        os.mkdir(path)
    return path


def getCsvFile():
    csv_files = [file for file in os.listdir(os.getcwd()) if file.endswith(".csv")]

    for i, filename in enumerate(csv_files):
        print(f"{i}: {filename}")

    more = len(csv_files) + 1
    print(f"{more}: Outro...")

    selection = int(input("Digite o número do arquivo de atendimentos: "))

    if selection == more:
        return input("Caminho para o arquivo .csv: ")
    else:
        return csv_files[selection]


def getGeckodriverPath():
    current_os = platform.system()
    print(f"Firefox geckodriver for {current_os}")

    if current_os == "Linux":
        geckodriver_path = os.path.join("geckodrivers", "geckodriver")
    elif current_os == "Windows":
        geckodriver_path = os.path.join("geckodrivers", "geckodriver.exe")
    else:
        raise Exception(f"Unsupported operating system: {current_os}")

    return geckodriver_path


def isValidAtendimento(atendimento):
    is_conclusivo, already_sent = atendimento[7], atendimento[8]
    return is_conclusivo == "Conclusivo" and already_sent == "NÃO"


def fillForm(driver, atendimento):
    data, cpf, servico_atendimento, historico_atendimento, modalidade = (
        atendimento[0],
        atendimento[4],
        atendimento[2],
        atendimento[5],
        atendimento[9],
    )
    day, month, year = map(int, data.split("/"))

    # Seleciona BA - UFBA - SALVADOR como instituição de ensino
    driver.execute_script(
        "document.getElementById('instituicao-responsavel-pelo-atendimento').selectedIndex = 37"
    )

    # Seleciona dia, mês e ano
    driver.execute_script(
        f"document.getElementById('edit_form_data-de-atendimento_0_year').selectedIndex = document.getElementById('edit_form_data-de-atendimento_0_year').childElementCount - 1"
    )
    driver.execute_script(
        f"document.getElementById('edit_form_data-de-atendimento_0_month').selectedIndex = {month}"
    )
    driver.execute_script(
        f"document.getElementById('edit_form_data-de-atendimento_0_day').selectedIndex = {day}"
    )

    # Seleciona a modalidade do atendimento
    driver.execute_script(
        f"document.getElementById('modalidade-de-atendimento_{1 if (modalidade == 'PRESENCIAL' or modalidade == '') else 2}').checked = true"
    )

    # Verifica tipo de usuário
    is_cnpj = len(cpf) == 18
    driver.execute_script(
        f"document.getElementById('tipo-de-usuario').selectedIndex = {2 if is_cnpj else 1}"
    )

    # Seleciona "sim" para atendimento conclusivo
    driver.execute_script(
        "document.getElementById('o-atendimento-prestado-foi-conclusivo').selectedIndex = 1"
    )

    # Seleciona tipo de atendimento
    container_tipos_de_servico = driver.find_element(By.ID, "tipo-de-atendimento")
    tipos_de_servico_rfb = container_tipos_de_servico.find_elements(
        By.TAG_NAME, "label"
    )

    for tipo_de_servico_rfb in tipos_de_servico_rfb:
        texto_servico = tipo_de_servico_rfb.text
        if servico_atendimento == texto_servico:
            tipo_de_servico_rfb.click()

    # Seleciona o tipo de atendimento "Outros"
    driver.execute_script(
        "document.getElementById('tipo-de-atendimento_23').checked = true"
    )

    # Escreve a especificação do atendimento
    driver.execute_script(
        f"document.getElementById('se-respondeu-outro-especifique-aqui').value = '{historico_atendimento}'"
    )

    # Clica no botão de enviar
    # driver.execute_script("document.querySelector('.formControls > input.context').click()")


def takeScreenshot(driver):
    prints_folder_path = makeDir(f"prints")

    today = datetime.today().strftime("%d-%m-%Y")

    today_prints_path = makeDir(os.path.join(prints_folder_path, today))

    print_path = os.path.join(today_prints_path, f"screenshot-{int(time.time())}.png")

    elements_to_remove = [
        "header#site-header",
        "nav.govbr-skip-menu",
        "footer#portal-footer",
    ]

    for element in elements_to_remove:
        driver.execute_script(f"document.querySelector('{element}').remove()")

    driver.save_full_page_screenshot(print_path)


def main():
    atendimentos_path = getCsvFile()

    atendimentos = pd.read_csv(atendimentos_path)

    geckodriver_path = getGeckodriverPath()

    service = Service(geckodriver_path)

    print("Iniciando o navegador...")
    driver = webdriver.Firefox(service=service)

    driver.get(URL_RFB)

    # Remove overlay de login
    driver.execute_script(
        "document.getElementById('govbr-login-overlay-wrapper').click()"
    )
    driver.execute_script("document.querySelector('button.reject-all').click()")

    time.sleep(5)

    # Loop sobre todos os atendimentos para lançamento
    for i, atendimento in atendimentos.iterrows():
        if isValidAtendimento(atendimento):
            fillForm(driver, atendimento)

            # Marca o atendimento como enviado
            # (NÃO TEM RELAÇÃO COM A PLANILHA NO GOOGLE DRIVE)
            atendimentos.at[i, "Lançado no site RFB"] = "SIM"
            atendimentos.to_csv(atendimentos_path, index=False)

            time.sleep(5)

            # Tira screenshot da página de confirmação
            takeScreenshot(driver)
        else:
            # Não conclusivo ou já enviado
            continue

        driver.get(URL_RFB)

    # Substitui o arquivo utilizado com lançamentos já lançados
    # para evitar que ele seja reutilizado.

    print("Fechando navegador...")
    driver.close()


if __name__ == "__main__":
    main()
