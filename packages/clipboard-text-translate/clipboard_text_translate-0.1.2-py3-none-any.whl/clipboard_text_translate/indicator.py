import sys
import json
import signal
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QLabel, QScrollArea, QPushButton, QTextEdit, QDialog, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QDesktopServices
from PyQt5.QtCore import QStandardPaths, Qt,QUrl
import platform
import os


import clipboard_text_translate.modules.lib_files as lib_files
import clipboard_text_translate.modules.lib_translate as lib_translate
import clipboard_text_translate.about as about


CONFIG_FILE = "~/.config/clipboard_text_translate/config.json"
config_file_path = os.path.expanduser(CONFIG_FILE)
config_data = {
    "GoogleTranslateLauncher": {
        "To english": "en",
        "To spanish": "es",
        "To portuguese": "pt"
    },
    "RawTranslateLauncher": {
        "To english": "en",
        "To spanish": "es",
        "To portuguese": "pt"
    }
    
}


try:
    if not os.path.exists(config_file_path):
        os.makedirs(os.path.dirname(config_file_path), exist_ok=True)
        
        with open(config_file_path, "w", encoding="utf-8") as arquivo:
            json.dump(config_data, arquivo, indent=4)
        print(f"Arquivo criado em: {config_file_path}")
        
    with open(config_file_path, "r") as arquivo:
        config_data = json.load(arquivo)
    
except FileNotFoundError:
    print(f"Erro: O arquivo '{config_file_path}' não foi encontrado.")
    sys.exit()
    
except json.JSONDecodeError:
    print(f"Erro: O arquivo '{config_file_path}' não contém um JSON válido.")
    sys.exit()

################################################################################
################################################################################
################################################################################


def show_notification_message(title, message):
    """Show a system notification"""
    if platform.system() == "Linux":
        os.system(f'notify-send "⚠️ {title} ⚠️" "{message}"')
    else:
        app = QApplication.instance()
        tray_icon = app.property("tray_icon")
        if tray_icon:
            tray_icon.showMessage("⚠️ " + title + " ⚠️", message, QSystemTrayIcon.Information, 3000)

class AboutWindow(QDialog):
    """About dialog window"""
    def __init__(self, data, logo_path, parent=None):
        super().__init__(parent)
        self.setWindowTitle("About")
        self.setMinimumSize(500, 300)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(logo_path)
        pixmap = pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(logo_label)
        
        # Description
        description_label = QLabel(f"<b>{data['description']}</b>")
        description_label.setWordWrap(True)
        description_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        layout.addWidget(description_label)
        
        # Add separator
        separator = QLabel()
        separator.setFrameShape(QLabel.HLine)
        separator.setFrameShadow(QLabel.Sunken)
        layout.addWidget(separator)
        
        # Package info
        package_label = QLabel(f"Package: {data['package']}")
        package_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        package_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(package_label)
        
        # Program info
        program_label = QLabel(f"Program: {data['linux_indicator']}")
        program_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        program_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(program_label)
        
        # Version info
        version_label = QLabel(f"Version: {data['version']}")
        version_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        version_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(version_label)
        
        # Author info
        author_label = QLabel(f"Author: {data['author']}")
        author_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        author_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(author_label)
        
        # Email info
        email_label = QLabel(f"Email: <a href=\"mailto:{data['email']}\">{data['email']}</a>")
        email_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        email_label.setOpenExternalLinks(True)
        email_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(email_label)
        
        # Add another separator
        separator2 = QLabel()
        separator2.setFrameShape(QLabel.HLine)
        separator2.setFrameShadow(QLabel.Sunken)
        layout.addWidget(separator2)
        
        # Source URL
        source_label = QLabel(f"Source: <a href=\"{data['url_source']}\">{data['url_source']}</a>")
        source_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        source_label.setOpenExternalLinks(True)
        source_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(source_label)
        
        # Funding URL
        funding_label = QLabel(f"Funding: <a href=\"{data['url_funding']}\">{data['url_funding']}</a>")
        funding_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        funding_label.setOpenExternalLinks(True)
        funding_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(funding_label)
        
        # Bugs URL
        bugs_label = QLabel(f"Bugs: <a href=\"{data['url_bugs']}\">{data['url_bugs']}</a>")
        bugs_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        bugs_label.setOpenExternalLinks(True)
        bugs_label.setAlignment(Qt.AlignLeft)
        layout.addWidget(bugs_label)
        
        # OK Button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

def show_about_window(data, logo_path):
    dialog = AboutWindow(data, logo_path)
    dialog.exec_()

class MessageDialog(QDialog):
    """Display a message with copyable text and an OK button"""
    def __init__(self, message, width=600, height=300, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Message")
        self.resize(width, height)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create text view for displaying the message
        text_edit = QTextEdit()
        text_edit.setPlainText(message)
        text_edit.setReadOnly(True)
        text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Add text view to a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(text_edit)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # OK Button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

def show_message(message, width=600, height=300):
    dialog = MessageDialog(message, width, height)
    dialog.exec_()

def get_clipboard_text():
    """Get text from clipboard"""
    app = QApplication.instance()
    clipboard = app.clipboard()
    return clipboard.text()

def edit_config():
    lib_files.open_from_filepath(config_file_path)

def open_url_help():
    url = "https://github.com/trucomanx/ClipboardTextTranslate/blob/main/doc/README.md"
    show_notification_message("open_url_help", url)
    QDesktopServices.openUrl(QUrl(url))

def on_action_googletranslate(lang_code):
    text = get_clipboard_text()
    show_notification_message("Going to Google Translate", "Open in the default web browser")
    translated_link = lib_translate.generate_google_translate_link(text, target_lang=lang_code)
    
    QDesktopServices.openUrl(QUrl(translated_link))

def on_action_rawtranslate(lang_code):
    text = get_clipboard_text()
    show_notification_message("Translating", "Please wait")
    res = lib_translate.translate_text_sync(text, target_lang=lang_code)
    show_message(res)

def open_coffee_link():
    show_notification_message("Buy me a coffee", "https://ko-fi.com/trucomanx")
    QDesktopServices.openUrl(QUrl("https://ko-fi.com/trucomanx"))

def show_about():
    data = {
        "version": about.__version__,
        "package": about.__package__,
        "linux_indicator": about.__linux_indicator__,
        "author": about.__author__,
        "email": about.__email__,
        "description": about.__description__,
        "url_source": about.__url_source__,
        "url_funding": about.__url_funding__,
        "url_bugs": about.__url_bugs__
    }
    
    base_dir_path = os.path.dirname(os.path.abspath(__file__))
    logo_path = os.path.join(base_dir_path, 'icons', 'logo.png')
    
    show_about_window(data, logo_path)

class ClipboardTextTranslate(QApplication):
    def __init__(self, argv):
        self.app = QApplication(sys.argv)
        self.setQuitOnLastWindowClosed(False)
        
        
        # Get base directory for icons
        base_dir_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir_path, 'icons', 'logo.png')
        
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path))
        self.tray_icon.setToolTip("Clipboard Text Translate")

        # Menu
        self.menu = QMenu()
                
        # Criar submenu para traduções
        self.translate_menu = QMenu("📋 Google Translate launcher", self.menu)

        translate_data = config_data.get("GoogleTranslateLauncher", {})        
        for label, lang_code in translate_data.items():
            # Translate with google
            action = QAction(label, self.menu)
            action.setIcon(QIcon.fromTheme("emblem-default"))
            action.triggered.connect(lambda checked, code=lang_code: on_action_googletranslate(code))
            self.translate_menu.addAction(action)
        
        self.menu.addMenu(self.translate_menu)

        # Separator
        self.menu.addSeparator()
        
        # Criar submenu para traduções
        self.raw_translate_menu = QMenu("📋 Translate raw text", self.menu)
        
        raw_translate_data = config_data.get("RawTranslateLauncher", {})
        for label, lang_code in raw_translate_data.items():
            # Translate with google
            action = QAction(label, self.menu)
            action.setIcon(QIcon.fromTheme("emblem-default"))
            action.triggered.connect(lambda checked, code=lang_code: on_action_rawtranslate(code))
            self.raw_translate_menu.addAction(action)
        
        self.menu.addMenu(self.raw_translate_menu)
                
        # Separator
        self.menu.addSeparator()
               
        # Create program_information_submenu
        self.program_info_submenu = QMenu("🛠️ Program usage information")
        
        # Add actions to program_information_submenu
        edit_config_action = QAction("Open config file", self.menu)
        edit_config_action.setIcon(QIcon.fromTheme("applications-utilities"))
        edit_config_action.triggered.connect(edit_config)
        self.program_info_submenu.addAction(edit_config_action)
        
        # Add heelp
        url_help_action = QAction("Open url help", self.menu)
        url_help_action.setIcon(QIcon.fromTheme("help-contents"))
        url_help_action.triggered.connect(open_url_help)
        self.program_info_submenu.addAction(url_help_action)
        
        # Add program_information_submenu to main menu
        self.menu.addMenu(self.program_info_submenu)
        
        # Separator
        self.menu.addSeparator()
        
        
        # Coffee
        coffee_action = QAction("☕ Buy me a coffee", self.menu)
        coffee_action.setIcon(QIcon.fromTheme("emblem-favorite"))
        coffee_action.triggered.connect(open_coffee_link)
        self.menu.addAction(coffee_action)
        
        # About
        about_action = QAction("🌟 About", self.menu)
        about_action.setIcon(QIcon.fromTheme("help-about"))
        about_action.triggered.connect(show_about)
        self.menu.addAction(about_action)
        
        # Separator
        self.menu.addSeparator()

        # Exit        
        exit_action = QAction("❌ Exit", self.menu)
        exit_action.setIcon(QIcon.fromTheme("application-exit"))
        exit_action.triggered.connect(self.app.quit)
        self.menu.addAction(exit_action)
        
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = ClipboardTextTranslate(sys.argv)
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

