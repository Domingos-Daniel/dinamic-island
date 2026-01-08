# Dynamic Island - Design Guide

## Filosofia de Design

O Dynamic Island segue os princípios do **Fluent Design System** da Microsoft, combinado com inspirações do **iOS Dynamic Island**.

### Princípios Centrais

1. **Glassmorphism/Acrylic**: Transparência sofisticada com efeito de vidro fosco
2. **Microinterações**: Animações sutis que fornecem feedback tátil
3. **Hierarquia Visual**: Bordas arredondadas, sombras suaves e gradientes refinados
4. **Paleta Neutra**: Preto, branco, cinza como base, com acentos vibrantes

---

## Paleta de Cores

### Neutros (Base)
- **Preto**: `#000000`
- **Cinza Escuro**: `#1A1A1A` (backgrounds)
- **Cinza Médio**: `#2D2D30` (borders, texto secundário)
- **Cinza Claro**: `#CCCCCC` (texto secundário)
- **Branco**: `#FFFFFF` (highlights, ícones)

### Acentos Vibrantes
- **Azul**: `#0078D4` (principal)
- **Azul Brilhante**: `#50E6FF` (highlights)
- **Verde**: `#107C10`
- **Verde Brilhante**: `#13A538`
- **Roxo**: `#8764B8`
- **Rosa/Vermelho**: `#E81B23`
- **Ciano**: `#00B4EF`

---

## Tipografia

### Family
- **Primária**: `Segoe UI`
- **Fallback**: `-apple-system, BlinkMacSystemFont, SF Pro Display`

### Tamanhos
- **Pequeno**: 11px (tooltips)
- **Médio**: 12px (labels)
- **Grande**: 14px (headings)
- **Extra Large**: 16px (títulos principais)

### Características
- **Weight**: 400 (regular), 500 (semibold), 600 (bold)
- **Line Height**: 1.5
- **Letter Spacing**: normal (legibilidade máxima)

---

## Efeitos Visuais

### Bordas Arredondadas
- **Raio Padrão**: 14px (elementos principais)
- **Raio Pequeno**: 6px (botões secundários)
- **Raio Grande**: 20px (modais)

### Sombras

#### Sombra Principal
```
Blur: 24px
Color: #00000033 (preto com 20% opacidade)
```

#### Sombra Suave (Hover)
```
Blur: 12px
Color: #00000026 (preto com 15% opacidade)
```

### Vidro Acrílico
- **Opacidade**: 80% (backgrounds)
- **Blur Effect**: Simulado com gradientes
- **Border**: 1.2px, 50% de opacidade

---

## Animações

### Durações
- **Rápida**: 150ms (feedback imediato)
- **Normal**: 300ms (transições padrão)
- **Lenta**: 500ms (entrada/saída)

### Easing Curves
- **Default**: `OutCubic` (saídas naturais)
- **Smooth**: `InOutSine` (transições suaves)
- **Spring**: `OutBack` (bounce effect)

### Tipos de Animação

#### 1. Expand/Collapse
- Duração: 500ms
- Easing: `OutCubic`
- Inclui: geometria, sombra, border glow

#### 2. Hover (Botão)
- Duração: 200ms
- Easing: `OutCubic`
- Efeito: scale 1.0 → 1.15, glow fade-in

#### 3. Press (Botão)
- Duração: 150ms
- Easing: `OutBack`
- Efeito: rotation (-8° → 0°), scale 1.0 → 0.85

#### 4. Pulse (Notificação)
- Duração: 1200ms
- Easing: `InOutSine`
- Efeito: rings expandindo com fade-out

#### 5. Collapse Indicator
- Multi-phase sine wave
- Frequências diferentes para cada ring
- Cria movimento orgânico e atrativo

---

## Componentes

### 1. GlowButton
**Uso**: Ícones de aplicativos no Dynamic Island

**Características**:
- Tamanho fixo: 54x54px
- Ícone SVG: 28x28px
- Glassmorphic com gradiente radial
- Hover: 1.15x scale + glow
- Press: 0.85x scale + tilt (-8°)
- Bounce on release: 1.25x scale (overshoot)

**Estados**:
- Normal: muted glow
- Hover: bright glow
- Press: dark + tilt
- Notification (Pulsing): rings expandindo

### 2. Dynamic Island Container
**Uso**: Widget principal

**Características**:
- Forma de pílula (pill shape)
- Bordas arredondadas: 14px
- Glassmorphic com múltiplas camadas de sombra
- Collapse width: 50px
- Expanded width: 650px (configurável)
- Altura: 90px (expandido), 28px (colapsado)

**Animações**:
- Expand: 500ms suave
- Collapse: 150ms fade + 350ms shrink
- Border glow ao expandir
- Shadow intensity ao expandir

### 3. Collapsed Indicator
**Uso**: Widget visual do estado colapsado

**Características**:
- Pulsing center dot
- Multi-ring animation
- Atmospheric glow
- Glass-like reflection highlight

**Animações**:
- 3 rings com diferentes fases
- Pulsação: 0-1 ciclo contínuo
- Efeito de profundidade com camadas

---

## Padrões de Interação

### 1. Hover → Expand
```
User hovers over collapsed island
↓
Smooth expand animation (500ms)
↓
Content fade-in (350ms, delayed 80ms)
↓
Border glow appears
```

### 2. Click Application
```
User hovers over button
↓
Scale 1.15x + glow fade-in (200ms)
↓
User clica
↓
Scale 0.85x + tilt -8° (150ms)
↓
Release: bounce 1.25x (overshoot)
↓
Launch application
```

### 3. Auto-Collapse
```
User expands island
↓
Interação time-out (3000ms padrão)
↓
Border glow fade-out
↓
Smooth collapse (150ms fade + 350ms shrink)
↓
Back to collapsed indicator
```

### 4. Notification Pulse
```
Notificação recebida
↓
Button inicia pulsing animation
↓
Rings expandindo com fade-out
↓
Usuário clica
↓
Pulsing para
↓
Aplicação é ativada
```

---

## Guia de Acessibilidade

### Cores
- Razão de contraste mínimo: 4.5:1 (WCAG AA)
- Neutros com acentos mantêm legibilidade

### Animações
- Duração máxima: 500ms (evita desorientação)
- Easing curves suaves (evita efeitos jarring)
- Respeita preferências do sistema (`prefers-reduced-motion`)

### Tipografia
- Tamanho mínimo: 11px
- Family: system default (melhor legibilidade)

---

## Implementação

### Colors
Usar QColor com valores RGB ou hex:
```python
QColor(45, 45, 50, 235)  # Cinza médio com transparência
QColor("#0078D4")  # Azul acento
```

### Gradients
```python
# Linear
gradient = QLinearGradient(x1, y1, x2, y2)
gradient.setColorAt(0.0, QColor(...))
gradient.setColorAt(1.0, QColor(...))

# Radial (para sombras e glows)
gradient = QRadialGradient(cx, cy, radius)
```

### Animations
```python
anim = QPropertyAnimation(widget, b"property")
anim.setDuration(300)  # milliseconds
anim.setEasingCurve(QEasingCurve.Type.OutCubic)
anim.setStartValue(start)
anim.setEndValue(end)
anim.start()
```

---

## Notas de Referência

- **Fluent Design**: https://fluent2.microsoft.design/
- **iOS Human Interface**: https://developer.apple.com/design/human-interface-guidelines/
- **Glassmorphism**: Modern UI trend com glass-like surfaces
- **Microinteractions**: Subtle feedback que melhora UX

---

## Changelog

### v2.0 - UI Modernization
- ✅ Implementado Glassmorphism/Acrylic effects
- ✅ Melhorados bordas arredondadas e sombras
- ✅ Adicionadas animações contextuais fluidas
- ✅ Implementada paleta de cores moderna
- ✅ Adicionadas microinterações (pulsing)
- ✅ Otimizada tipografia e ícones
