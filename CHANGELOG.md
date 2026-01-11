# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
e este projeto segue [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-01-11

### ✨ Adicionado

#### UI & Design (Glassmorphism)
- 🎨 Glassmorphism/Acrílico effect inspirado em Fluent Design System da Microsoft
- Bordas arredondadas suaves (14px) com sombras difusas
- Multi-layer frosted glass appearance com transparência elegante
- Indicador de colapso com pulsing animation e múltiplos anéis

#### Animações Fluidas
- ⚡ Easing curves suaves (OutCubic, InOutSine, OutBack)
- Expand/Collapse com 500ms de duração natural
- Hover animations com 200ms (1.0x → 1.15x scale)
- Press effects com tilt rotation (-8° → 5°) e bounce (1.25x overshoot)
- Pulse notifications com rings expandindo

#### Paleta de Cores Moderna
- 🌈 Cores neutras: preto, cinza, branco (base sofisticada)
- Acentos vibrantes: azul, verde, roxo, rosa, ciano
- Config.json com theme system completo
- Tipografia limpa: Segoe UI com fallback SF Pro Display

#### Microinterações
- 🎯 Feedback tátil em cada interação
- Glow effects ao hover
- Bounce effect ao clicar
- Pulsing indicator quando colapsado
- Icon animations com scale e fade

#### Música
- 🎵 Auto-detecção de aplicações tocando música
- Auto-show de controles ao expandir
- Play/Pause, Previous, Next funcional
- Suporte: Spotify, YouTube, VLC, iTunes, Groove, etc
- Timer de monitoramento a cada 500ms

#### Notificações Melhoradas
- 🔔 Sistema de notificações com logs detalhados
- Detecção de banco de dados Windows
- Fallback para título de janelas
- Emoji indicadores por app
- Histórico de notificações (últimas 50)
- Teste de notificações (Ctrl+3)

#### Pin & Do Not Disturb
- 📌 Pin button para manter expandido
- 🌙 DND mode para suprimir notificações
- Animações suaves para pin/unpin

#### Melhor Foco & Colapso
- Auto-descolapso ao perder foco (WindowDeactivate)
- Event handling robusto
- Respecta estado de pin

### 🐛 Corrigido

- ❌ Auto-collapse agora funciona corretamente ao clicar fora
- ❌ Música controls agora aparecem quando expandido
- ❌ Listener de notificações com melhor tratamento de erros
- ❌ Database lock handling com fallback
- ❌ Indentation e syntax errors corrigidos

### 📖 Documentação

- ✅ [DESIGN_GUIDE.md](DESIGN_GUIDE.md) - Sistema de design completo
- ✅ [README.md](README.md) - Features e instruções
- ✅ [INSTALL.md](INSTALL.md) - Guia de instalação
- ✅ Config.json com ui_theme section

### 🔨 Dev Tools

- PyInstaller spec file atualizado
- Config.json com tema definível
- Logs de debug para notificações
- Error handling melhorado

---

## [1.0.0] - 2024-XX-XX

### ✨ Adicionado

#### Core Features
- Dynamic Island widget (pílula animada)
- Aplicações customizáveis (config.json)
- Controles de música (play/pause, anterior, próxima)
- Sistema de notificações Windows
- Atalhos globais (Ctrl+1, Ctrl+3, Ctrl+4)

#### UI Inicial
- Design minimalista dark theme
- Ícones SVG coloridos
- Animações básicas (hover, scale)
- Settings dialog para customização

#### Configuração
- Config.json para apps, delay, dimensões
- App editor dialog
- Selecionador de ícones
- Customização de cores

### 🔧 Requisitos

- Python 3.10+
- PyQt6
- keyboard

---

## Versões Futuras

### Planejado para v2.1
- [ ] Temas light/dark customizáveis
- [ ] Suporte a ícones do Windows nativo
- [ ] Profiles de aplicativos
- [ ] Sincronização de config na nuvem
- [ ] Performance improvements

### Planejado para v3.0
- [ ] WebView para notificações ricas
- [ ] Integração com APIs (weather, calendar, etc)
- [ ] Plugins system
- [ ] Multi-monitor support
- [ ] Touch gesture support

---

## Como Reportar Issues

Abra uma [Issue no GitHub](https://github.com/Domingos-Daniel/dinamic-island/issues) com:
1. Descrição clara do problema
2. Passos para reproduzir
3. Screenshots/videos se aplicável
4. Logs (se disponível)
5. Seu ambiente (Windows version, Python version, etc)

## Como Contribuir

1. Fork o repositório
2. Crie uma branch (`git checkout -b feature/amazing`)
3. Commit suas mudanças (`git commit -m 'Add amazing feature'`)
4. Push para a branch (`git push origin feature/amazing`)
5. Abra um Pull Request

---

## Licença

Este projeto é livre para usar, modificar e distribuir.

Veja [LICENSE](LICENSE) para detalhes (se houver).

---

## Créditos

- Inspirado em [iPhone Dynamic Island](https://www.apple.com/) (Apple)
- Design: [Fluent Design System](https://fluent2.microsoft.design/) (Microsoft)
- Framework: [PyQt6](https://www.riverbankcomputing.com/software/pyqt/)
- Desenvolvido por: Domingos Daniel
