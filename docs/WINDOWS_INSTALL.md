# Instalação Windows — ECU Pro Tune

## Requisitos

- Windows 10 ou Windows 11.
- Python 3.11 de 64 bits.
- Python Launcher (py) instalado e disponível no PATH.
- Acesso à Internet durante a instalação das dependências.

Verifica o Python:

    py -3.11 --version

O projeto está validado em Python 3.11 pelo pipeline Windows do GitHub Actions. Não uses um ambiente virtual criado com outra versão.

## Instalação

1. Descarrega ou clona o repositório.
2. Abre a pasta raiz do ECU Pro Tune.
3. Executa install_ecu_pro_tune.bat.
4. O instalador cria .venv, instala requirements.txt, executa pip check e valida os imports centrais.
5. Se o instalador encontrar uma .venv de outra versão Python, não a apaga. Renomeia-a manualmente e volta a executar.

Para iniciar:

    .venv\Scripts\python.exe -m src.app.main

## FFmpeg é opcional

A aplicação GUI não depende de FFmpeg. Os sons WAV de fallback funcionam sem ele.

FFmpeg só é necessário para fluxos opcionais de conversão ou geração MP3. Se não estiver instalado, o instalador pergunta antes de tentar usar winget. Responder N não bloqueia a instalação da aplicação.

Depois de instalar FFmpeg, abre uma nova consola para atualizar o PATH.

## Testes

Executa ecu_test.bat para validar a versão Python, dependências, compilação e testes automatizados.

Alternativamente:

    .venv\Scripts\python.exe -m pip check
    .venv\Scripts\python.exe -m compileall -q src tests
    .venv\Scripts\python.exe -m pytest -q tests

## Criar o executável

Executa build_exe.bat.

O resultado é:

    dist\ECUProTune\ECUProTune.exe

É um pacote PyInstaller onedir. O script de release cria um ZIP versionado em release, acompanhado por BUILD-MANIFEST.json e SHA256SUMS.txt. O manifesto regista a versão, plataforma, Python, tamanho e SHA-256. Mantém a pasta completa, incluindo _internal; não distribuas apenas o EXE.

## Problemas comuns

- py não encontrado: instala Python 3.11 com a opção Python Launcher.
- Python 3.11 não encontrado: instala a versão 3.11 de 64 bits e confirma py -0p.
- .venv incompatível: fecha a aplicação, renomeia a pasta .venv existente e executa novamente o instalador.
- pip check falha: copia o erro completo; não ignores conflitos de dependências.
- FFmpeg ausente: podes ignorar o aviso; a GUI e os WAV fallback continuam disponíveis.
- EXE não arranca: executa ecu_test.bat e volta a criar o pacote com build_exe.bat.

## Segurança operacional

Esta versão é exclusivamente para gestão, visualização e simulação. Não escreve em ECUs, não contém driver de flash e não programa hardware físico.
