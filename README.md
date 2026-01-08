# Dynamic Island Launcher

Pequeno utilitário PyQt6 inspirado no Dynamic Island do iPhone. Cria uma janela arredondada, sempre no topo, com design sofisticado e animações fluidas para acesso rápido a apps e notificações.

## ✨ Design & UI - v2.0

O Dynamic Island agora conta com um **design moderno e sofisticado** inspirado no **Fluent Design System** da Microsoft:

### Características de Design
- 🎨 **Glassmorphism/Acrílico**: Efeito de vidro fosco com transparência elegante
- ⚡ **Animações Fluidas**: Transições suaves com curvas de aceleração naturais (ease-in-out)
- 🎯 **Microinterações**: Feedback tátil sutil ao interagir (hover, press, pulse)
- 🌈 **Paleta Moderna**: Cores neutras (preto, cinza, branco) com acentos vibrantes (azul, verde, roxo)
- 📱 **Responsivo**: Expande/colapsa suavemente com animações contextuais

### Componentes Visuais
- **Bordas Arredondadas** (14px): Suaves e sofisticadas
- **Sombras Difusas**: Criam profundidade sem parecer pesadas
- **Indicador de Colapso**: Pulsing animation com múltiplos anéis
- **Ícones Monocromáticos**: Design flat com animações de escala e rotação

Veja [DESIGN_GUIDE.md](DESIGN_GUIDE.md) para detalhes completos sobre o sistema de design.

## 🎯 Funcionalidades

- 🔔 **Sistema de Notificações** – Mostra notificações de TODOS os apps do Windows (WhatsApp, Email, etc.)
- 🎵 **Controles de música** – Play/pause, anterior, próxima (funciona com Spotify, YouTube, etc.)
- 🚀 **Apps rápidos** – WhatsApp, Facebook, LinkedIn, VS Code, Brave, Sticky Notes (personalizáveis)
- ⚙️ **Totalmente configurável** – Adicione seus próprios apps, URLs e ícones SVG customizados
- 🎨 **UI moderna** – Animações suaves, ícones com acento de cor, efeitos glassmorphism
- 📌 **Pin/Unpin** – Fixe o Island expandido ou deixe-o se recolher automaticamente
- 🖱️ **Arrastável** – Clique e arraste para mover para qualquer posição
- ⌨️ **Atalhos globais** – 
  - `Ctrl+1` para ocultar/mostrar o Dynamic Island
  - `Ctrl+3` para testar o sistema de notificações
  - `Ctrl+4` para visualizar histórico de notificações

## 📖 Como funcionam as notificações

O Dynamic Island monitora automaticamente as notificações do Windows em tempo real:
- Detecta notificações de WhatsApp, Gmail, Spotify, Discord, Teams e qualquer outro app
- Expande automaticamente quando uma notificação chega com animação suave
- Mostra o nome do app e a mensagem de forma discreta
- Desaparece após 4 segundos (ou fixe com o botão de pin)

**Para testar:**
1. Execute o Dynamic Island
2. Pressione `Ctrl+3` para ver uma notificação de teste
3. Ou receba uma mensagem real no WhatsApp/Email/etc

## 📋 Requisitos

- Python 3.10 ou superior
- [PyQt6](https://pypi.org/project/PyQt6/) – Framework GUI
- [keyboard](https://pypi.org/project/keyboard/) – Para atalhos globais

Instale as dependências:
```powershell
pip install PyQt6 keyboard
```

## 🚀 Executar em modo desenvolvimento

```powershell
python dynamic_island.py
```

## 📦 Gerar executável com PyInstaller

1. Instale o PyInstaller (uma única vez):
   ```powershell
   pip install pyinstaller
   ```
2. Gere o `.exe` sem console:
   ```powershell
   pyinstaller --noconsole --onefile --name dynamic-island dynamic_island.py
   ```

O executável final estará em `dist/dynamic-island.exe`

## ⚙️ Configuração

Edite `config.json` para personalizar:

```json
{
  "apps": [
    {
      "name": "WhatsApp",
      "type": "local",
      "enabled": true,
      "icon_name": "ICON_WHATSAPP",
      "color": "#25D366"
    }
  ],
  "music_controls_enabled": true,
  "auto_collapse_delay": 3000,
  "expanded_width": 650,
  "collapsed_width": 50
}
```

### Tema UI (Novo)
A configuração inclui agora um sistema de tema completo:

```json
"ui_theme": {
  "palette": {
    "neutral": { "black", "darkGray", "mediumGray", "lightGray", "white" },
    "accents": { "blue", "brightBlue", "green", "brightGreen", "purple", "pink", "cyan" }
  },
  "typography": { "fontFamily", "sizes" },
  "effects": { "borderRadius", "shadowBlur", "glassOpacity" },
  "animations": { "durationFast", "durationNormal", "durationSlow" }
}
```

## 🎨 Personalizar Ícones

Cada app usa ícones SVG que podem ser customizados. Edite os ícones diretamente no código ou em `config.json`:

```python
ICON_CUSTOM = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="..." fill="#0078D4"/>
</svg>
"""
```

## 📱 Animações e Interações

### Hover
- Escala suavemente: 1.0x → 1.15x
- Glow fade-in (300ms)

### Press
- Escala dramaticamente: 1.0x → 0.85x
- Rotação tátil: -8°
- Bounce on release: 1.25x com overshoot

### Expand/Collapse
- Duração: 500ms
- Easing: OutCubic (suave e natural)
- Sombra e border glow animados

### Notificação (Pulsing)
- Anéis expandindo para fora
- Fade-out suave
- 1200ms de duração

## 🔧 Troubleshooting

### Notificações não funcionam
- Certifique-se de que `winrt` está instalado: `pip install windows-runtime`
- Verifique se o app está em execução com permissões de administrador
- Windows 10/11 é necessário

### Ícones não aparecem
- Verifique o caminho dos SVG no `config.json`
- Certifique-se de que o SVG é válido (use um validador online)

### Atalho global não funciona
- O package `keyboard` requer privilégios de administrador
- Tente rodar o script como Administrador

## 📄 Licença

Livre para usar e modificar conforme necessário.

## 🙏 Créditos

- Inspirado no iPhone Dynamic Island (Apple)
- Design baseado no Fluent Design System (Microsoft)
- Desenvolvido com PyQt6
