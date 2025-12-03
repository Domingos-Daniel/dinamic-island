# Dynamic Island Launcher

Pequeno utilitário PyQt6 inspirado no Dynamic Island do iPhone. Cria uma janela arredondada, preta, sem moldura e sempre no topo, com botões animados para abrir apps e páginas comuns.

## Funcionalidades
- 🔔 **Sistema de Notificações** – Mostra notificações de TODOS os apps do Windows (WhatsApp, Email, etc.)
- 🎵 **Controles de música** – Play/pause, anterior, próxima (funciona com Spotify, YouTube, etc.)
- 🚀 **Apps rápidos** – WhatsApp, Facebook, LinkedIn, VS Code, Brave, Sticky Notes
- ⚙️ **Totalmente configurável** – Adicione seus próprios apps, URLs e ícones personalizados
- 🎨 **UI estilo iPhone** – Animações suaves, ícones SVG coloridos, efeitos glassmorphism
- 🖱️ **Arrastável** – Clique e arraste para mover para qualquer posição
- ⌨️ **Atalhos globais** – 
  - `Ctrl+1` para ocultar/mostrar o Dynamic Island
  - `Ctrl+3` para testar o sistema de notificações

## Como funcionam as notificações
O Dynamic Island monitora automaticamente as notificações do Windows em tempo real:
- Detecta notificações de WhatsApp, Gmail, Spotify, Discord, Teams e qualquer outro app
- Expande automaticamente quando uma notificação chega
- Mostra o nome do app e a mensagem de forma discreta
- Desaparece após 4 segundos

**Para testar:**
1. Execute o Dynamic Island
2. Pressione `Ctrl+3` para ver uma notificação de teste
3. Ou receba uma mensagem real no WhatsApp/Email/etc

## Requisitos
- Python 3.10 ou superior
- [PyQt6](https://pypi.org/project/PyQt6/)
- [keyboard](https://pypi.org/project/keyboard/) (para atalho global Ctrl+1)

Instale as dependências:
```powershell
pip install PyQt6 keyboard
```

## Executar em modo desenvolvimento
```powershell
python dynamic_island.py
```

## Gerar executável com PyInstaller
1. Instale o PyInstaller (uma única vez):
   ```powershell
   pip install pyinstaller
   ```
2. Gere o `.exe` sem console:
   ```powershell
   pyinstaller --noconsole --onefile --name dynamic-island dynamic_island.py
   ```
   O executável ficará em `dist\dynamic-island.exe`.

## Iniciar automaticamente com o Windows
1. Crie um atalho (`.lnk`) para `dist\dynamic-island.exe`.
2. Copie o atalho para a pasta de inicialização do Windows:
   ```
   C:\Users\<Usuario>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup
   ```
3. Substitua `<Usuario>` pelo seu nome de usuário. Ao reiniciar, o Dynamic Island abrirá automaticamente.
