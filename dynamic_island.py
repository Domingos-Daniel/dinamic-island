"""Dynamic Island – iPhone-style launcher for Windows.

A sleek, animated, frameless PyQt6 widget inspired by Apple's Dynamic Island.
Features smooth spring-like animations, glassmorphism effects, real SVG icons,
and subtle visual feedback on hover/press.

Requirements:
    - PyQt6
    - Python 3.10+
"""
from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import webbrowser
from pathlib import Path
from typing import Callable

from PyQt6.QtCore import (
    QEasingCurve,
    QParallelAnimationGroup,
    QPoint,
    QPointF,
    QPropertyAnimation,
    QRect,
    QRectF,
    QSequentialAnimationGroup,
    QSize,
    Qt,
    QTimer,
    QVariantAnimation,
    pyqtProperty,
    pyqtSignal,
)
from PyQt6.QtGui import (
    QBrush,
    QColor,
    QCursor,
    QFont,
    QFontDatabase,
    QGuiApplication,
    QLinearGradient,
    QMouseEvent,
    QPainter,
    QPainterPath,
    QPen,
    QRadialGradient,
)
from PyQt6.QtSvg import QSvgRenderer
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QColorDialog,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QFormLayout,
    QGraphicsDropShadowEffect,
    QGraphicsOpacityEffect,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)

# For global hotkey support
try:
    import keyboard
    KEYBOARD_AVAILABLE = True
except ImportError:
    KEYBOARD_AVAILABLE = False


# ──────────────────────────────────────────────────────────────────────────────
# SVG Icons (Base64-like inline strings for portability)
# ──────────────────────────────────────────────────────────────────────────────

ICON_WHATSAPP = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347z" fill="#25D366"/>
  <path d="M12 2C6.477 2 2 6.477 2 12c0 1.89.525 3.66 1.438 5.168L2 22l4.932-1.41A9.953 9.953 0 0012 22c5.523 0 10-4.477 10-10S17.523 2 12 2zm0 18c-1.66 0-3.203-.506-4.483-1.371l-.32-.192-2.933.84.877-2.858-.21-.334A7.948 7.948 0 014 12c0-4.411 3.589-8 8-8s8 3.589 8 8-3.589 8-8 8z" fill="#25D366"/>
</svg>
"""

ICON_FACEBOOK = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M24 12c0-6.627-5.373-12-12-12S0 5.373 0 12c0 5.99 4.388 10.954 10.125 11.854V15.47H7.078V12h3.047V9.356c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874V12h3.328l-.532 3.469h-2.796v8.385C19.612 22.954 24 17.99 24 12z" fill="#1877F2"/>
</svg>
"""

ICON_LINKEDIN = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z" fill="#0A66C2"/>
</svg>
"""

ICON_VSCODE = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M23.15 2.587L18.21.21a1.494 1.494 0 00-1.705.29l-9.46 8.63-4.12-3.128a.999.999 0 00-1.276.057L.327 7.261A1 1 0 00.326 8.74L3.899 12 .326 15.26a1 1 0 00.001 1.479L1.65 17.94a.999.999 0 001.276.057l4.12-3.128 9.46 8.63a1.492 1.492 0 001.704.29l4.942-2.377A1.5 1.5 0 0024 20.06V3.939a1.5 1.5 0 00-.85-1.352zm-5.146 14.861L10.826 12l7.178-5.448v10.896z" fill="#007ACC"/>
</svg>
"""

ICON_BRAVE = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M12 0L8.934.002l.002.002L7.548 1.9H5.2l.678 2.006-.946 1.08.946 1.45-.4.68 1.144 1.932-.478.968 1.3 2.39-.18.37 1.702 4.254.034.152 1.2 3.398.8 1.64L12 24l.9-1.78.8-1.64 1.2-3.398.034-.152 1.702-4.254-.18-.37 1.3-2.39-.478-.968 1.144-1.932-.4-.68.946-1.45-.946-1.08.678-2.006h-2.348L13.066.004l.002-.002L12 0z" fill="#FB542B"/>
</svg>
"""

ICON_NOTES = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="3" y="3" width="18" height="18" rx="3" fill="#FFE066"/>
  <path d="M7 8h10M7 12h10M7 16h6" stroke="#333" stroke-width="1.5" stroke-linecap="round"/>
</svg>
"""

ICON_MUSIC = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <circle cx="12" cy="12" r="10" fill="url(#musicGrad)"/>
  <path d="M9.5 8.5L14.5 12L9.5 15.5V8.5z" fill="#fff"/>
  <defs>
    <linearGradient id="musicGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#FF6B9D;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#C239B3;stop-opacity:1" />
    </linearGradient>
  </defs>
</svg>
"""

ICON_PREV = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 6h2v12H6V6zm3.5 6l8.5 6V6l-8.5 6z" fill="#E0E0E0"/>
</svg>
"""

ICON_PLAY = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M8 5v14l11-7z" fill="#E0E0E0"/>
</svg>
"""

ICON_PAUSE = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 4h4v16H6V4zm8 0h4v16h-4V4z" fill="#E0E0E0"/>
</svg>
"""

ICON_NEXT = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z" fill="#E0E0E0"/>
</svg>
"""

ICON_CLOSE = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" fill="#FF4444"/>
</svg>
"""

ICON_SETTINGS = """
<svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
  <path d="M19.14,12.94c0.04-0.3,0.06-0.61,0.06-0.94c0-0.32-0.02-0.64-0.07-0.94l2.03-1.58c0.18-0.14,0.23-0.41,0.12-0.61 l-1.92-3.32c-0.12-0.22-0.37-0.29-0.59-0.22l-2.39,0.96c-0.5-0.38-1.03-0.7-1.62-0.94L14.4,2.81c-0.04-0.24-0.24-0.41-0.48-0.41 h-3.84c-0.24,0-0.43,0.17-0.47,0.41L9.25,5.35C8.66,5.59,8.12,5.92,7.63,6.29L5.24,5.33c-0.22-0.08-0.47,0-0.59,0.22L2.74,8.87 C2.62,9.08,2.66,9.34,2.86,9.48l2.03,1.58C4.84,11.36,4.8,11.69,4.8,12s0.02,0.64,0.07,0.94l-2.03,1.58 c-0.18,0.14-0.23,0.41-0.12,0.61l1.92,3.32c0.12,0.22,0.37,0.29,0.59,0.22l2.39-0.96c0.5,0.38,1.03,0.7,1.62,0.94l0.36,2.54 c0.05,0.24,0.24,0.41,0.48,0.41h3.84c0.24,0,0.44-0.17,0.47-0.41l0.36-2.54c0.59-0.24,1.13-0.56,1.62-0.94l2.39,0.96 c0.22,0.08,0.47,0,0.59-0.22l1.92-3.32c0.12-0.22,0.07-0.47-0.12-0.61L19.14,12.94z M12,15.6c-1.98,0-3.6-1.62-3.6-3.6 s1.62-3.6,3.6-3.6s3.6,1.62,3.6,3.6S13.98,15.6,12,15.6z" fill="#888888"/>
</svg>
"""


# ──────────────────────────────────────────────────────────────────────────────
# Custom Animated Button
# ──────────────────────────────────────────────────────────────────────────────


class GlowButton(QWidget):
    """A sleek animated button with SVG icon, glow effect and scale animation."""

    SIZE = 54
    ICON_SIZE = 28

    def __init__(
        self,
        svg_data: str,
        tooltip: str,
        callback: Callable[[], None],
        accent_color: str = "#ffffff",
    ) -> None:
        super().__init__()
        self.svg_data = svg_data
        self.tooltip_text = tooltip
        self.callback = callback
        self.accent = QColor(accent_color)
        self._scale = 1.0
        self._glow = 0.0
        self._pressed = False

        self.setFixedSize(self.SIZE, self.SIZE)
        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.setToolTip(tooltip)

        # Animations
        self._scale_anim = QPropertyAnimation(self, b"scale")
        self._scale_anim.setDuration(150)
        self._scale_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        self._glow_anim = QPropertyAnimation(self, b"glow")
        self._glow_anim.setDuration(200)
        self._glow_anim.setEasingCurve(QEasingCurve.Type.InOutQuad)

        self.renderer = QSvgRenderer(self.svg_data.encode())

    # ─── Qt properties for animation ──────────────────────────────────────────
    @pyqtProperty(float)
    def scale(self) -> float:
        return self._scale

    @scale.setter
    def scale(self, value: float) -> None:
        self._scale = value
        self.update()

    @pyqtProperty(float)
    def glow(self) -> float:
        return self._glow

    @glow.setter
    def glow(self, value: float) -> None:
        self._glow = value
        self.update()

    # ─── Events ───────────────────────────────────────────────────────────────
    def enterEvent(self, _event) -> None:
        self._animate_scale(1.15)
        self._animate_glow(1.0)

    def leaveEvent(self, _event) -> None:
        self._animate_scale(1.0)
        self._animate_glow(0.0)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._pressed = True
            self._animate_scale(0.92)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if self._pressed and event.button() == Qt.MouseButton.LeftButton:
            self._pressed = False
            self._animate_scale(1.15 if self.underMouse() else 1.0)
            if self.rect().contains(event.pos()):
                self.callback()

    def _animate_scale(self, target: float) -> None:
        self._scale_anim.stop()
        self._scale_anim.setStartValue(self._scale)
        self._scale_anim.setEndValue(target)
        self._scale_anim.start()

    def _animate_glow(self, target: float) -> None:
        self._glow_anim.stop()
        self._glow_anim.setStartValue(self._glow)
        self._glow_anim.setEndValue(target)
        self._glow_anim.start()

    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        center = QPointF(self.width() / 2, self.height() / 2)
        radius = (self.SIZE / 2 - 4) * self._scale

        # Glow
        if self._glow > 0.01:
            glow_color = QColor(self.accent)
            glow_color.setAlphaF(0.35 * self._glow)
            gradient = QRadialGradient(center, radius * 1.6)
            gradient.setColorAt(0, glow_color)
            gradient.setColorAt(1, QColor(0, 0, 0, 0))
            painter.setBrush(gradient)
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(center, radius * 1.6, radius * 1.6)

        # Background circle
        bg = QColor(40, 40, 42) if self._glow < 0.5 else QColor(55, 55, 58)
        painter.setBrush(bg)
        painter.setPen(QPen(QColor(80, 80, 85), 1.2))
        painter.drawEllipse(center, radius, radius)

        # Icon
        icon_size = self.ICON_SIZE * self._scale
        icon_rect = QRectF(
            center.x() - icon_size / 2,
            center.y() - icon_size / 2,
            icon_size,
            icon_size,
        )
        self.renderer.render(painter, icon_rect)


# ──────────────────────────────────────────────────────────────────────────────
# Settings Dialog
# ──────────────────────────────────────────────────────────────────────────────


class SettingsDialog(QDialog):
    """Advanced settings dialog for configuring Dynamic Island."""

    def __init__(self, config_path: Path, parent=None) -> None:
        super().__init__(parent)
        self.config_path = config_path
        self.config = self._load_config()
        
        self.setWindowTitle("Dynamic Island - Configurações")
        self.setMinimumSize(700, 500)
        self.setModal(True)
        
        self._build_ui()
    
    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return self._get_default_config()
    
    def _get_default_config(self) -> dict:
        """Return default configuration."""
        return {
            "apps": [],
            "music_controls_enabled": True,
            "auto_collapse_delay": 3000,
            "expanded_width": 650,
            "collapsed_width": 220
        }
    
    def _build_ui(self) -> None:
        """Build the settings UI."""
        layout = QVBoxLayout(self)
        
        # Tabs-like sections
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)
        
        # General Settings
        general_group = QGroupBox("⚙️ Configurações Gerais")
        general_layout = QFormLayout()
        
        self.music_enabled_check = QCheckBox("Ativar controles de música")
        self.music_enabled_check.setChecked(self.config.get("music_controls_enabled", True))
        general_layout.addRow("Música:", self.music_enabled_check)
        
        self.collapse_delay_spin = QSpinBox()
        self.collapse_delay_spin.setRange(1000, 10000)
        self.collapse_delay_spin.setSingleStep(500)
        self.collapse_delay_spin.setSuffix(" ms")
        self.collapse_delay_spin.setValue(self.config.get("auto_collapse_delay", 3000))
        general_layout.addRow("Delay auto-ocultar:", self.collapse_delay_spin)
        
        self.expanded_width_spin = QSpinBox()
        self.expanded_width_spin.setRange(400, 1200)
        self.expanded_width_spin.setSingleStep(50)
        self.expanded_width_spin.setSuffix(" px")
        self.expanded_width_spin.setValue(self.config.get("expanded_width", 650))
        general_layout.addRow("Largura expandida:", self.expanded_width_spin)
        
        general_group.setLayout(general_layout)
        scroll_layout.addWidget(general_group)
        
        # Apps Management
        apps_group = QGroupBox("📱 Gerenciar Aplicativos")
        apps_layout = QVBoxLayout()
        
        # App list
        self.app_list = QListWidget()
        self._populate_app_list()
        apps_layout.addWidget(self.app_list)
        
        # App controls
        app_controls = QHBoxLayout()
        
        add_btn = QPushButton("➕ Adicionar App")
        add_btn.clicked.connect(self._add_app)
        app_controls.addWidget(add_btn)
        
        edit_btn = QPushButton("✏️ Editar")
        edit_btn.clicked.connect(self._edit_app)
        app_controls.addWidget(edit_btn)
        
        remove_btn = QPushButton("🗑️ Remover")
        remove_btn.clicked.connect(self._remove_app)
        app_controls.addWidget(remove_btn)
        
        toggle_btn = QPushButton("👁️ Ativar/Desativar")
        toggle_btn.clicked.connect(self._toggle_app)
        app_controls.addWidget(toggle_btn)
        
        apps_layout.addLayout(app_controls)
        apps_group.setLayout(apps_layout)
        scroll_layout.addWidget(apps_group)
        
        scroll_layout.addStretch()
        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)
        
        # Dialog buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self._save_and_close)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
    
    def _populate_app_list(self) -> None:
        """Populate the app list widget."""
        self.app_list.clear()
        for app in self.config.get("apps", []):
            status = "✅" if app.get("enabled", True) else "❌"
            app_type = "🌐" if app.get("type") == "url" else "💻" if app.get("type") == "local" else "⭐"
            item_text = f"{status} {app_type} {app.get('name', 'Sem nome')}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, app)
            self.app_list.addItem(item)
    
    def _add_app(self) -> None:
        """Add a new app to the list."""
        dialog = AppEditorDialog(None, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_app = dialog.get_app_data()
            self.config["apps"].append(new_app)
            self._populate_app_list()
    
    def _edit_app(self) -> None:
        """Edit the selected app."""
        current_item = self.app_list.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Aviso", "Selecione um app para editar.")
            return
        
        app_data = current_item.data(Qt.ItemDataRole.UserRole)
        dialog = AppEditorDialog(app_data, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updated_app = dialog.get_app_data()
            idx = self.app_list.currentRow()
            self.config["apps"][idx] = updated_app
            self._populate_app_list()
            self.app_list.setCurrentRow(idx)
    
    def _remove_app(self) -> None:
        """Remove the selected app."""
        current_row = self.app_list.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um app para remover.")
            return
        
        reply = QMessageBox.question(
            self, "Confirmar", "Remover este app?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            self.config["apps"].pop(current_row)
            self._populate_app_list()
    
    def _toggle_app(self) -> None:
        """Toggle app enabled/disabled state."""
        current_row = self.app_list.currentRow()
        if current_row < 0:
            return
        
        app = self.config["apps"][current_row]
        app["enabled"] = not app.get("enabled", True)
        self._populate_app_list()
        self.app_list.setCurrentRow(current_row)
    
    def _save_and_close(self) -> None:
        """Save configuration and close dialog."""
        self.config["music_controls_enabled"] = self.music_enabled_check.isChecked()
        self.config["auto_collapse_delay"] = self.collapse_delay_spin.value()
        self.config["expanded_width"] = self.expanded_width_spin.value()
        
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        
        self.accept()


class AppEditorDialog(QDialog):
    """Dialog for adding/editing individual apps."""

    def __init__(self, app_data: dict | None, parent=None) -> None:
        super().__init__(parent)
        self.app_data = app_data or {}
        
        self.setWindowTitle("Adicionar/Editar App" if app_data else "Adicionar App")
        self.setMinimumWidth(500)
        self.setModal(True)
        
        self._build_ui()
        self._load_data()
    
    def _build_ui(self) -> None:
        """Build the app editor UI."""
        layout = QFormLayout(self)
        
        # App name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Ex: Spotify, Gmail, Calculator...")
        layout.addRow("Nome do App:", self.name_edit)
        
        # App type
        self.type_combo = QComboBox()
        self.type_combo.addItems(["local", "url", "special"])
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        layout.addRow("Tipo:", self.type_combo)
        
        # URL (for web apps)
        self.url_edit = QLineEdit()
        self.url_edit.setPlaceholderText("https://...")
        layout.addRow("URL:", self.url_edit)
        
        # Local path/command
        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Ex: spotify, calc, C:\\...\\app.exe")
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_edit)
        browse_btn = QPushButton("📂 Procurar")
        browse_btn.clicked.connect(self._browse_file)
        path_layout.addWidget(browse_btn)
        scan_btn = QPushButton("🔍 Scanear Apps")
        scan_btn.clicked.connect(self._scan_installed_apps)
        path_layout.addWidget(scan_btn)
        layout.addRow("Caminho/Comando:", path_layout)
        
        # Color
        self.color_edit = QLineEdit()
        self.color_edit.setText("#888888")
        color_layout = QHBoxLayout()
        color_layout.addWidget(self.color_edit)
        color_btn = QPushButton("🎨 Escolher Cor")
        color_btn.clicked.connect(self._choose_color)
        color_layout.addWidget(color_btn)
        layout.addRow("Cor do ícone:", color_layout)
        
        # Icon (emoji or simple text)
        self.icon_edit = QLineEdit()
        self.icon_edit.setPlaceholderText("Ex: 🎵 📧 📱 ou deixe vazio para •")
        layout.addRow("Ícone (emoji):", self.icon_edit)
        
        # Enabled
        self.enabled_check = QCheckBox("Ativar este app")
        self.enabled_check.setChecked(True)
        layout.addRow("", self.enabled_check)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addRow(button_box)
    
    def _on_type_changed(self, app_type: str) -> None:
        """Update visible fields based on app type."""
        is_url = app_type == "url"
        is_local = app_type == "local"
        
        self.url_edit.setVisible(is_url)
        self.path_edit.setVisible(is_local)
    
    def _browse_file(self) -> None:
        """Browse for executable file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Selecionar Executável", "", 
            "Executáveis (*.exe);;Todos os arquivos (*.*)"
        )
        if file_path:
            self.path_edit.setText(file_path)
    
    def _choose_color(self) -> None:
        """Choose icon color."""
        color = QColorDialog.getColor()
        if color.isValid():
            self.color_edit.setText(color.name())
    
    def _scan_installed_apps(self) -> None:
        """Scan and show installed Windows apps."""
        # Get apps (optimized, should be fast)
        apps = self._find_installed_apps()
        
        if not apps:
            QMessageBox.information(self, "Apps", "Nenhum app encontrado.")
            return
        
        # Create selection dialog
        dialog = QDialog(self)
        dialog.setWindowTitle(f"Selecionar App ({len(apps)} encontrados)")
        dialog.setMinimumSize(600, 450)
        
        layout = QVBoxLayout(dialog)
        
        # Info label
        info_label = QLabel(f"✅ {len(apps)} aplicativos encontrados. Use a busca para filtrar:")
        layout.addWidget(info_label)
        
        # Search box
        search_box = QLineEdit()
        search_box.setPlaceholderText("🔍 Digite para filtrar (ex: chrome, spotify, discord)...")
        layout.addWidget(search_box)
        
        # App list
        app_list = QListWidget()
        for app_name, app_path in sorted(apps):
            # Show different icons for system vs installed apps
            icon = "🪟" if app_path in ["calc", "notepad", "mspaint", "wordpad", "cmd", "powershell", "explorer"] else "📱"
            item = QListWidgetItem(f"{icon} {app_name}")
            item.setData(Qt.ItemDataRole.UserRole, (app_name, app_path))
            item.setToolTip(app_path)  # Show path on hover
            app_list.addItem(item)
        
        # Search functionality
        def filter_apps():
            search_text = search_box.text().lower()
            visible_count = 0
            for i in range(app_list.count()):
                item = app_list.item(i)
                is_visible = search_text in item.text().lower()
                item.setHidden(not is_visible)
                if is_visible:
                    visible_count += 1
            info_label.setText(f"📱 {visible_count} de {len(apps)} apps")
        
        search_box.textChanged.connect(filter_apps)
        layout.addWidget(app_list)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        # Auto-focus search box
        search_box.setFocus()
        
        # Show dialog
        if dialog.exec() == QDialog.DialogCode.Accepted:
            current = app_list.currentItem()
            if current:
                app_name, app_path = current.data(Qt.ItemDataRole.UserRole)
                self.name_edit.setText(app_name)
                self.path_edit.setText(app_path)
    
    def _find_installed_apps(self) -> list[tuple[str, str]]:
        """Find installed Windows applications (optimized)."""
        apps = []
        max_apps = 200  # Limit to prevent slowdown
        
        # Add common Windows apps first (instant)
        common_apps = [
            ("Calculadora", "calc"),
            ("Bloco de Notas", "notepad"),
            ("Paint", "mspaint"),
            ("WordPad", "wordpad"),
            ("Prompt de Comando", "cmd"),
            ("PowerShell", "powershell"),
            ("Explorador de Arquivos", "explorer"),
            ("Ferramenta de Captura", "snippingtool"),
        ]
        apps.extend(common_apps)
        
        # Quick scan of common app locations
        quick_paths = [
            (os.environ.get("LOCALAPPDATA", ""), "Programs"),
            (os.environ.get("PROGRAMFILES", ""), ""),
        ]
        
        import glob
        scanned = 0
        
        for base, subdir in quick_paths:
            if scanned >= max_apps:
                break
                
            search_base = os.path.join(base, subdir) if subdir else base
            if not os.path.exists(search_base):
                continue
            
            # Only scan top-level directories and one level deep
            try:
                for item in os.listdir(search_base):
                    if scanned >= max_apps:
                        break
                    
                    item_path = os.path.join(search_base, item)
                    if not os.path.isdir(item_path):
                        continue
                    
                    # Look for .exe in this folder only
                    for exe_file in glob.glob(os.path.join(item_path, "*.exe")):
                        if scanned >= max_apps:
                            break
                        
                        try:
                            exe_name = os.path.basename(exe_file)
                            exe_lower = exe_name.lower()
                            
                            # Skip unwanted files
                            if any(skip in exe_lower for skip in [
                                'unins', 'update', 'install', 'setup', 
                                'crash', 'helper', 'service', 'launcher'
                            ]):
                                continue
                            
                            # Get clean app name
                            app_name = os.path.splitext(exe_name)[0]
                            app_name = app_name.replace('_', ' ').replace('-', ' ').title()
                            
                            # Avoid duplicates
                            if not any(app_name == name for name, _ in apps):
                                apps.append((app_name, exe_file))
                                scanned += 1
                        except:
                            continue
            except:
                continue
        
        return apps
    
    def _load_data(self) -> None:
        """Load existing app data into fields."""
        if not self.app_data:
            return
        
        self.name_edit.setText(self.app_data.get("name", ""))
        self.type_combo.setCurrentText(self.app_data.get("type", "local"))
        self.url_edit.setText(self.app_data.get("url", ""))
        self.path_edit.setText(self.app_data.get("path", ""))
        self.color_edit.setText(self.app_data.get("color", "#888888"))
        self.icon_edit.setText(self.app_data.get("custom_icon", ""))
        self.enabled_check.setChecked(self.app_data.get("enabled", True))
        
        self._on_type_changed(self.app_data.get("type", "local"))
    
    def get_app_data(self) -> dict:
        """Get the app data from the form."""
        return {
            "name": self.name_edit.text(),
            "type": self.type_combo.currentText(),
            "enabled": self.enabled_check.isChecked(),
            "url": self.url_edit.text() if self.type_combo.currentText() == "url" else "",
            "path": self.path_edit.text() if self.type_combo.currentText() == "local" else "",
            "color": self.color_edit.text(),
            "custom_icon": self.icon_edit.text(),
            "icon_name": f"CUSTOM_{self.name_edit.text().replace(' ', '_').upper()}"
        }


# ──────────────────────────────────────────────────────────────────────────────
# Main Dynamic Island Window
# ──────────────────────────────────────────────────────────────────────────────


class DynamicIslandWindow(QWidget):
    """The floating pill-shaped launcher widget with spring-like animations."""

    COLLAPSED_WIDTH = 220
    COLLAPSED_HEIGHT = 38
    EXPANDED_WIDTH = 650
    EXPANDED_HEIGHT = 90
    TOP_MARGIN = 12
    CORNER_RADIUS = 36

    def __init__(self) -> None:
        super().__init__()
        
        # Load configuration
        self.config_path = Path(__file__).parent / "config.json"
        self.config = self._load_config()
        
        # Apply config values
        self.EXPANDED_WIDTH = self.config.get("expanded_width", 650)
        self.COLLAPSED_WIDTH = self.config.get("collapsed_width", 220)

        # Window flags: frameless, always-on-top, tool window (no taskbar)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # Internal state
        self.expanded = False
        self._content_opacity = 0.0
        self._bg_lightness = 0.0  # 0 = pure black, 1 = slightly lighter
        self._corner_radius = float(self.CORNER_RADIUS)
        self._music_player_visible = False
        self._drag_position = None
        self._is_hidden = False

        # Geometry animation (spring-like)
        self._geom_anim = QPropertyAnimation(self, b"geometry")
        self._geom_anim.setDuration(420)
        self._geom_anim.setEasingCurve(QEasingCurve.Type.OutBack)

        # Content fade animation
        self._opacity_anim = QPropertyAnimation(self, b"contentOpacity")
        self._opacity_anim.setDuration(250)

        # Background lightness animation
        self._bg_anim = QPropertyAnimation(self, b"bgLightness")
        self._bg_anim.setDuration(300)

        # Collapse timer
        self._collapse_timer = QTimer(self)
        collapse_delay = self.config.get("auto_collapse_delay", 3000)
        self._collapse_timer.setInterval(collapse_delay)
        self._collapse_timer.setSingleShot(True)
        self._collapse_timer.timeout.connect(self.collapse)

        self._build_ui()
        self._set_geometry(self.COLLAPSED_WIDTH, self.COLLAPSED_HEIGHT)
        
        # Setup global hotkey Ctrl+1 to toggle visibility
        if KEYBOARD_AVAILABLE:
            keyboard.add_hotkey('ctrl+1', self._toggle_visibility)
    
    def _load_config(self) -> dict:
        """Load configuration from JSON file."""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {
            "apps": [],
            "music_controls_enabled": True,
            "auto_collapse_delay": 3000,
            "expanded_width": 650,
            "collapsed_width": 220
        }

    # ─── Qt custom properties ─────────────────────────────────────────────────
    @pyqtProperty(float)
    def contentOpacity(self) -> float:
        return self._content_opacity

    @contentOpacity.setter
    def contentOpacity(self, value: float) -> None:
        self._content_opacity = value
        # Update button container opacity
        if hasattr(self, "_button_container"):
            effect = self._button_container.graphicsEffect()
            if isinstance(effect, QGraphicsOpacityEffect):
                effect.setOpacity(value)

    @pyqtProperty(float)
    def bgLightness(self) -> float:
        return self._bg_lightness

    @bgLightness.setter
    def bgLightness(self, value: float) -> None:
        self._bg_lightness = value
        self.update()

    # ─── UI Setup ─────────────────────────────────────────────────────────────
    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Single container for all controls
        self._button_container = QWidget()
        self._button_container.setStyleSheet("background: transparent;")
        opacity_effect = QGraphicsOpacityEffect(self._button_container)
        opacity_effect.setOpacity(0.0)
        self._button_container.setGraphicsEffect(opacity_effect)

        btn_layout = QHBoxLayout(self._button_container)
        btn_layout.setContentsMargins(20, 0, 20, 0)
        btn_layout.setSpacing(12)
        btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add music controls first (smaller size)
        self._prev_btn = GlowButton(ICON_PREV, "Anterior", self._music_prev, "#E0E0E0")
        self._prev_btn.setFixedSize(40, 40)
        self._play_pause_btn = GlowButton(ICON_PLAY, "Play/Pause", self._music_play_pause, "#FFFFFF")
        self._play_pause_btn.setFixedSize(44, 44)
        self._next_btn = GlowButton(ICON_NEXT, "Próxima", self._music_next, "#E0E0E0")
        self._next_btn.setFixedSize(40, 40)
        
        # Music controls container (toggleable)
        self._music_controls = QWidget()
        self._music_controls.setStyleSheet("background: transparent;")
        music_layout = QHBoxLayout(self._music_controls)
        music_layout.setContentsMargins(0, 0, 12, 0)
        music_layout.setSpacing(8)
        music_layout.addWidget(self._prev_btn)
        music_layout.addWidget(self._play_pause_btn)
        music_layout.addWidget(self._next_btn)
        
        # Initially hide music controls
        self._music_controls.setVisible(False)
        btn_layout.addWidget(self._music_controls)

        # Add app launcher buttons
        for svg, tip, action, color in self._button_specs():
            btn = GlowButton(svg, tip, action, color)
            btn_layout.addWidget(btn)
        
        # Add settings button
        settings_btn = GlowButton(ICON_SETTINGS, "Configurações", self._open_settings, "#888888")
        settings_btn.setFixedSize(40, 40)
        btn_layout.addWidget(settings_btn)
        
        # Add close button at the end
        close_btn = GlowButton(ICON_CLOSE, "Fechar Dynamic Island", self._close_app, "#FF4444")
        close_btn.setFixedSize(40, 40)
        btn_layout.addWidget(close_btn)

        layout.addStretch()
        layout.addWidget(self._button_container, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

    def _button_specs(
        self,
    ) -> list[tuple[str, str, Callable[[], None], str]]:
        """Generate button specs from configuration."""
        buttons = []
        
        # Load from config
        for app in self.config.get("apps", []):
            if not app.get("enabled", True):
                continue
            
            # Map icon names to actual SVG icons
            icon_map = {
                "ICON_WHATSAPP": ICON_WHATSAPP,
                "ICON_FACEBOOK": ICON_FACEBOOK,
                "ICON_LINKEDIN": ICON_LINKEDIN,
                "ICON_VSCODE": ICON_VSCODE,
                "ICON_BRAVE": ICON_BRAVE,
                "ICON_NOTES": ICON_NOTES,
                "ICON_MUSIC": ICON_MUSIC,
            }
            
            # Get icon SVG or create custom emoji icon
            icon_svg = icon_map.get(app.get("icon_name", ""), None)
            if not icon_svg and app.get("custom_icon"):
                # Create simple SVG with emoji/text
                emoji = app.get("custom_icon", "•")
                icon_svg = f'''<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <text x="12" y="16" text-anchor="middle" font-size="14" fill="{app.get('color', '#888888')}">{emoji}</text>
                </svg>'''
            elif not icon_svg:
                # Default icon
                icon_svg = f'''<svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                    <circle cx="12" cy="12" r="8" fill="{app.get('color', '#888888')}"/>
                </svg>'''
            
            # Create action callback
            action = self._create_app_action(app)
            
            buttons.append((
                icon_svg,
                app.get("name", "App"),
                action,
                app.get("color", "#888888")
            ))
        
        return buttons
    
    def _create_app_action(self, app: dict) -> Callable[[], None]:
        """Create action callback for an app."""
        app_type = app.get("type", "local")
        app_name = app.get("name", "")
        
        if app_type == "url":
            url = app.get("url", "")
            return lambda: self._open_url(url)
        elif app_type == "local":
            # Check for predefined local apps
            if app_name == "WhatsApp":
                return self._open_whatsapp
            elif app_name == "LinkedIn":
                return self._open_linkedin
            elif app_name == "VS Code":
                return self._open_vscode
            elif app_name == "Brave":
                return self._open_brave
            elif app_name == "Sticky Notes":
                return self._open_sticky
            else:
                # Custom local app
                path = app.get("path", "")
                return lambda p=path: self._run_custom_app(p)
        elif app_type == "special":
            if app_name == "Music Player":
                return self._toggle_music_player
        
        return lambda: None
    
    def _run_custom_app(self, path: str) -> None:
        """Run a custom app from path or command."""
        try:
            if os.path.exists(path):
                subprocess.Popen([path])
            else:
                subprocess.Popen(path, shell=True)
        except Exception as exc:
            self._show_error(f"Erro ao abrir {path}: {exc}")

    # ─── Geometry helpers ─────────────────────────────────────────────────────
    def _screen_rect(self) -> QRect:
        return QGuiApplication.primaryScreen().availableGeometry()

    def _target_rect(self, w: int, h: int) -> QRect:
        screen = self._screen_rect()
        x = screen.x() + (screen.width() - w) // 2
        y = screen.y() + self.TOP_MARGIN
        return QRect(x, y, w, h)

    def _set_geometry(self, w: int, h: int) -> None:
        self.setGeometry(self._target_rect(w, h))

    def _animate_geometry(self, w: int, h: int) -> None:
        if self._geom_anim.state() == QPropertyAnimation.State.Running:
            self._geom_anim.stop()
        self._geom_anim.setStartValue(self.geometry())
        self._geom_anim.setEndValue(self._target_rect(w, h))
        self._geom_anim.start()

    # ─── Expand / Collapse ────────────────────────────────────────────────────
    def expand(self) -> None:
        if self.expanded:
            return
        self.expanded = True
        self._animate_geometry(self.EXPANDED_WIDTH, self.EXPANDED_HEIGHT)
        self._animate_opacity(1.0)
        self._animate_bg(0.12)
        self._collapse_timer.stop()

    def collapse(self) -> None:
        if not self.expanded:
            return
        self.expanded = False
        self._animate_geometry(self.COLLAPSED_WIDTH, self.COLLAPSED_HEIGHT)
        self._animate_opacity(0.0)
        self._animate_bg(0.0)

    def _animate_opacity(self, target: float) -> None:
        self._opacity_anim.stop()
        self._opacity_anim.setStartValue(self._content_opacity)
        self._opacity_anim.setEndValue(target)
        self._opacity_anim.start()

    def _animate_bg(self, target: float) -> None:
        self._bg_anim.stop()
        self._bg_anim.setStartValue(self._bg_lightness)
        self._bg_anim.setEndValue(target)
        self._bg_anim.start()

    # ─── Events ───────────────────────────────────────────────────────────────
    def enterEvent(self, _event) -> None:
        self.expand()

    def leaveEvent(self, _event) -> None:
        self._collapse_timer.start()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.MouseButton.LeftButton and self._drag_position is not None:
            self.move(event.globalPosition().toPoint() - self._drag_position)
            event.accept()

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_position = None
            event.accept()

    # ─── Painting ─────────────────────────────────────────────────────────────
    def paintEvent(self, _event) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        radius = self._corner_radius

        # Background color with subtle lightness shift
        base = int(6 + 18 * self._bg_lightness)
        bg_color = QColor(base, base, base, 245)

        # Subtle inner highlight (glassmorphism vibe)
        path = QPainterPath()
        path.addRoundedRect(QRectF(rect), radius, radius)

        # Drop shadow simulation (soft outer glow)
        shadow_color = QColor(0, 0, 0, 90)
        for i in range(4, 0, -1):
            shadow_color.setAlpha(20 + 15 * (4 - i))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(shadow_color)
            inflate = int(i * 1.5)
            painter.drawRoundedRect(rect.adjusted(-inflate, -inflate, inflate, inflate), radius + inflate, radius + inflate)

        # Main pill
        painter.setBrush(bg_color)
        painter.setPen(QPen(QColor(60, 60, 65), 0.8))
        painter.drawRoundedRect(QRectF(rect), radius, radius)

        # Top highlight line (simulates light reflection)
        highlight = QLinearGradient(rect.left(), rect.top(), rect.right(), rect.top())
        highlight.setColorAt(0, QColor(255, 255, 255, 0))
        highlight.setColorAt(0.5, QColor(255, 255, 255, int(18 + 12 * self._bg_lightness)))
        highlight.setColorAt(1, QColor(255, 255, 255, 0))
        painter.setPen(QPen(QBrush(highlight), 1))
        painter.drawLine(
            int(rect.left() + radius),
            rect.top() + 1,
            int(rect.right() - radius),
            rect.top() + 1,
        )

    # ─── Music Player ─────────────────────────────────────────────────────────
    def _toggle_music_player(self) -> None:
        """Toggle music player controls visibility."""
        self._music_player_visible = not self._music_player_visible
        
        if hasattr(self, "_music_controls"):
            self._music_controls.setVisible(self._music_player_visible)
    
    def _music_play_pause(self) -> None:
        """Send play/pause command to Windows media."""
        try:
            # VK_MEDIA_PLAY_PAUSE = 0xB3
            import ctypes
            user32 = ctypes.windll.user32
            user32.keybd_event(0xB3, 0, 0, 0)
            user32.keybd_event(0xB3, 0, 2, 0)
        except Exception as exc:
            self._show_error(f"Erro ao controlar mídia: {exc}")
    
    def _music_prev(self) -> None:
        """Send previous track command."""
        try:
            # VK_MEDIA_PREV_TRACK = 0xB1
            import ctypes
            user32 = ctypes.windll.user32
            user32.keybd_event(0xB1, 0, 0, 0)
            user32.keybd_event(0xB1, 0, 2, 0)
        except Exception as exc:
            self._show_error(f"Erro ao voltar faixa: {exc}")
    
    def _music_next(self) -> None:
        """Send next track command."""
        try:
            # VK_MEDIA_NEXT_TRACK = 0xB0
            import ctypes
            user32 = ctypes.windll.user32
            user32.keybd_event(0xB0, 0, 0, 0)
            user32.keybd_event(0xB0, 0, 2, 0)
        except Exception as exc:
            self._show_error(f"Erro ao avançar faixa: {exc}")
    
    def _toggle_visibility(self) -> None:
        """Toggle window visibility (show/hide)."""
        if self._is_hidden:
            self.show()
            self._is_hidden = False
        else:
            self.hide()
            self._is_hidden = True
    
    def _close_app(self) -> None:
        """Close the application with confirmation."""
        reply = QMessageBox.question(
            self,
            "Fechar Dynamic Island",
            "Deseja realmente encerrar o Dynamic Island?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            QApplication.quit()
    
    def _open_settings(self) -> None:
        """Open settings dialog."""
        dialog = SettingsDialog(self.config_path, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Reload configuration
            self.config = self._load_config()
            
            # Update UI parameters
            self.EXPANDED_WIDTH = self.config.get("expanded_width", 650)
            self._collapse_timer.setInterval(self.config.get("auto_collapse_delay", 3000))
            
            # Show restart message
            QMessageBox.information(
                self,
                "Configurações Salvas",
                "As configurações foram salvas!\n\nReinicie o Dynamic Island para aplicar todas as alterações.",
                QMessageBox.StandardButton.Ok
            )

    # ─── Launch helpers ───────────────────────────────────────────────────────
    def _open_url(self, url: str) -> None:
        try:
            webbrowser.open(url, new=2)
        except Exception as exc:
            self._show_error(f"Não foi possível abrir {url}: {exc}")
    
    def _open_whatsapp(self) -> None:
        """Open WhatsApp desktop app or web version."""
        try:
            # Try Windows Store app first
            try:
                os.startfile("whatsapp:")  # type: ignore[attr-defined]
                return
            except:
                pass
            
            # Try local executable paths
            import glob
            whatsapp_paths = [
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "WhatsApp", "WhatsApp.exe"),
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "WhatsApp", "WhatsApp.exe"),
            ]
            for path in whatsapp_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return
            
            # Search in WindowsApps
            windowsapps = os.path.join(os.environ.get("PROGRAMFILES", ""), "WindowsApps")
            if os.path.exists(windowsapps):
                matches = glob.glob(os.path.join(windowsapps, "*WhatsApp*", "WhatsApp.exe"))
                if matches:
                    subprocess.Popen([matches[0]])
                    return
            
            # Fallback to web
            self._open_url("https://web.whatsapp.com")
        except Exception:
            self._open_url("https://web.whatsapp.com")
    
    def _open_linkedin(self) -> None:
        """Open LinkedIn desktop app or web version."""
        try:
            # Try Windows Store app protocol
            os.startfile("linkedin:")  # type: ignore[attr-defined]
        except Exception:
            # Fallback to web
            self._open_url("https://linkedin.com")
    
    def _open_brave(self) -> None:
        """Open Brave browser."""
        try:
            # Try common Brave installation paths
            brave_paths = [
                os.path.join(os.environ.get("PROGRAMFILES", ""), "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
                os.path.join(os.environ.get("PROGRAMFILES(X86)", ""), "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "BraveSoftware", "Brave-Browser", "Application", "brave.exe"),
            ]
            for path in brave_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return
            
            # Try command line
            subprocess.Popen(["brave"], shell=True)
        except Exception as exc:
            self._show_error(f"Brave não encontrado: {exc}")
    
    def _open_vscode(self) -> None:
        """Open VS Code."""
        try:
            # Try common VS Code paths
            vscode_paths = [
                os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Microsoft VS Code", "Code.exe"),
                os.path.join(os.environ.get("PROGRAMFILES", ""), "Microsoft VS Code", "Code.exe"),
            ]
            for path in vscode_paths:
                if os.path.exists(path):
                    subprocess.Popen([path])
                    return
            
            # Try command line
            subprocess.Popen(["code"], shell=True)
        except Exception as exc:
            self._show_error(f"VS Code não encontrado: {exc}")
    
    def _run_cmd(self, cmd: str) -> None:
        """Execute a shell command."""
        try:
            subprocess.Popen(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        except FileNotFoundError:
            self._show_error(f"'{cmd}' não encontrado no PATH.")
        except Exception as exc:
            self._show_error(f"Erro ao executar '{cmd}': {exc}")

    def _open_sticky(self) -> None:
        """Open Windows Sticky Notes app."""
        try:
            # Method 1: Try protocol handler
            try:
                subprocess.Popen(["explorer.exe", "shell:appsFolder\\Microsoft.MicrosoftStickyNotes_8wekyb3d8bbwe!App"])
                return
            except:
                pass
            
            # Method 2: Try ms-stickynotes protocol
            try:
                os.startfile("ms-stickynotes:")  # type: ignore[attr-defined]
                return
            except:
                pass
            
            # Method 3: Try searching for the app in common locations
            import glob
            windowsapps = os.path.join(os.environ.get("PROGRAMFILES", ""), "WindowsApps")
            if os.path.exists(windowsapps):
                matches = glob.glob(os.path.join(windowsapps, "Microsoft.MicrosoftStickyNotes*", "*.exe"))
                if matches:
                    subprocess.Popen([matches[0]])
                    return
            
            # Method 4: Fallback
            subprocess.Popen(["cmd", "/c", "start", "ms-stickynotes:"])
        except Exception as exc:
            self._show_error(f"Sticky Notes: {exc}")

    def _show_error(self, msg: str) -> None:
        """Show error message dialog."""
        dlg = QMessageBox()
        dlg.setIcon(QMessageBox.Icon.Warning)
        dlg.setWindowTitle("Dynamic Island")
        dlg.setText(msg)
        dlg.exec()


# ──────────────────────────────────────────────────────────────────────────────
# Application Entry Point
# ──────────────────────────────────────────────────────────────────────────────


def main() -> None:
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    # Optional: dark palette for any system dialogs
    from PyQt6.QtGui import QPalette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(30, 30, 30))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
    palette.setColor(QPalette.ColorRole.Button, QColor(45, 45, 45))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(220, 220, 220))
    app.setPalette(palette)

    window = DynamicIslandWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
