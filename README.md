# django-biblioteca
Modelo de sistema de gerenciamento de biblioteca com django

## Configuração do Ambiente

1. **Crie o ambiente virtual**:
    ```bash
    python -m venv .venv
    ```

2. **Ative o ambiente virtual**:
    - No Bash:
        ```bash
        source .venv/Scripts/activate
        ```
    - No PowerShell:
        ```powershell
        .\.venv\Scripts\Activate.ps1
        ```

3. **Instale as dependências**:
    ```bash
    pip install -r requirements.txt
    ```

## Executando os Testes

1. **Defina a variável de ambiente**:
    ```bash
    export DJANGO_SETTINGS_MODULE=biblioteca.settings
    ```

2. **Execute os testes**:
    ```bash
    pytest
    ```