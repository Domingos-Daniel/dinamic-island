# Dynamic Island - Guia de Instalação

## 🚀 Quick Start (Executável Pré-compilado)

### Windows (Mais Fácil)
1. **Baixe o executável** da aba [Releases](https://github.com/Domingos-Daniel/dinamic-island/releases)
2. **Extraia o arquivo** `DynamicIsland.exe`
3. **Execute o arquivo** (clique duplo)
4. **Pronto!** O Dynamic Island está rodando

### Iniciar com Windows
Para que o app inicie automaticamente ao ligar o PC:

1. Crie um atalho para `DynamicIsland.exe`
2. Copie para: `C:\Users\<SeuUsuario>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`

---

## 🔧 Instalação a partir do Código-Fonte

### Requisitos
- Python 3.10+
- Git (opcional)

### Passos

1. **Clone o repositório**
```bash
git clone https://github.com/Domingos-Daniel/dinamic-island.git
cd dinamic-island
```

2. **Instale as dependências**
```bash
pip install PyQt6 keyboard
```

3. **Execute o app**
```bash
python dynamic_island.py
```

---

## 📦 Gerar seu próprio Executável

Se quiser criar um `.exe` personalizado:

1. **Instale PyInstaller**
```bash
pip install pyinstaller
```

2. **Compile o projeto**
```bash
pyinstaller --noconsole --onefile --name dynamic-island dynamic_island.py
```

3. **Seu executável estará em**: `dist\dynamic-island.exe`

---

## ⌨️ Atalhos de Teclado

| Atalho | Ação |
|--------|------|
| `Ctrl+1` | Mostrar/Ocultar |
| `Ctrl+3` | Teste de Notificação |
| `Ctrl+4` | Histórico de Notificações |

---

## ⚙️ Configuração

Edite `config.json` para personalizar:

```json
{
  "apps": [
    {
      "name": "Seu App",
      "type": "local",
      "enabled": true,
      "icon_name": "ICON_CUSTOM",
      "color": "#0078D4"
    }
  ],
  "music_controls_enabled": true,
  "auto_collapse_delay": 3000,
  "expanded_width": 650,
  "collapsed_width": 50
}
```

---

## 🐛 Troubleshooting

### Notificações não aparecem
- Certifique-se de que tem permissões de administrador
- Teste com `Ctrl+3`
- Verifique se o banco de dados de notificações existe

### Música não detecta
- Certifique-se de que a música está tocando em um app suportado
- Apps suportados: Spotify, YouTube, VLC, iTunes, Groove, etc

### Atalhos globais não funcionam
- Execute como Administrador
- O módulo `keyboard` requer privilégios elevados

---

## 📖 Documentação Completa

Veja [DESIGN_GUIDE.md](DESIGN_GUIDE.md) para detalhes sobre o sistema de design.

---

## 💬 Suporte

- Abra uma [Issue](https://github.com/Domingos-Daniel/dinamic-island/issues)
- Consulte o [README.md](README.md) para mais informações
