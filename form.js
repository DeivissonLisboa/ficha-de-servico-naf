let instituicao = document.getElementById("instituicao-responsavel-pelo-atendimento")

// Seleciona: BA - UFBA - Salvador
instituicao.selectedIndex = 37

// Data
let year = document.getElementById("edit_form_data-de-atendimento_0_year")
let month = document.getElementById("edit_form_data-de-atendimento_0_month")
let day = document.getElementById("edit_form_data-de-atendimento_0_day")

// Sempre seleciona o ultimo ano disponivel
year.selectedIndex = year.childElementCount - 1 

month.selectedIndex = 1

// Modalidade do atendimento
let modalidade = "Presencial"
let radio_modalidade

switch (modalidade) {
    case "Presencial":
        radio_modalidade = document.getElementById("modalidade-de-atendimento_1")
        break
    case "Remoto":
        radio_modalidade = document.getElementById("modalidade-de-atendimento_2")
        break
}

radio_modalidade.checked = true

// Seleciona o tipo de usuatio
let cpf = "000.000.000-00"
// let cpf = "00.000.000/0001-00"
let is_CPNJ = false
let tipo_de_usuario = document.getElementById("tipo-de-usuario")

// CPF ou CNPJ?
if (cpf.length == 14) {
    is_CPNJ = true
}

if (is_CPNJ) {
    tipo_de_usuario.selectedIndex = 2
} else {
    tipo_de_usuario.selectedIndex = 1
}

// Sempre seleciona "sim" para atendimento conclusivo
let atendimento_conclusivo = document.getElementById("o-atendimento-prestado-foi-conclusivo")

atendimento_conclusivo.selectedIndex = 1

// Tipo de atendimento: "outro"
let outro_checkbox = document.getElementById("tipo-de-atendimento_23")

outro_checkbox.checked = true

// especificação
let descricao = "texto sobre o atendimento aqui!"
let input_descricao = document.getElementById("se-respondeu-outro-especifique-aqui")

input_descricao.value = descricao

// enviar
let submit_btn = document.querySelector(".formControls > input.context")

// submit_btn.click()