#!/usr/bin/python3
#!/usr/bin/python

import signal
import sys
import os
import json
import traceback
import platform
from PyQt5.QtWidgets import (QApplication, QMainWindow, QMenu, QSystemTrayIcon, QAction, 
                            QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
                            QTextEdit, QScrollArea, QFileDialog, QMessageBox)
from PyQt5.QtGui import QIcon, QPixmap, QTextCursor, QDesktopServices
from PyQt5.QtCore import Qt, QUrl

from clipboard_text_correction.about import __version__

import clipboard_text_correction.lib_funcs as lib_funcs
import clipboard_text_correction.lib_files as lib_files
import clipboard_text_correction.lib_stats as lib_stats
import clipboard_text_correction.lib_latex as lib_latex

import clipboard_text_correction.about as about

CONFIG_FILE = "~/.config/clipboard_text_correction/config_data.json"

config_data = lib_funcs.SYSTEM_DATA
config_file_path = os.path.expanduser(CONFIG_FILE)

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


try:
    article_format_data = {}
    base_dir_path = os.path.dirname(os.path.abspath(__file__))
    article_format_path = os.path.join(base_dir_path, 'data', 'article_format.json')
    with open(article_format_path, "r") as arquivo:
        article_format_data = json.load(arquivo)
    
except FileNotFoundError:
    print(f"Erro: O arquivo '{base_dir_path}' não foi encontrado.")
    sys.exit()
    
except json.JSONDecodeError:
    print(f"Erro: O arquivo '{base_dir_path}' não contém um JSON válido.")
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


class MessageDialog(QDialog):
    """Display a message with copyable text and an OK button"""
    def __init__(self, message, width=600, height=300, parent=None, read_only=False):
        super().__init__(parent)
        self.setWindowTitle("Message")
        self.resize(width, height)
        
        # Create layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create text view for displaying the message
        self.text_edit = QTextEdit()
        self.text_edit.setPlainText(message)
        self.text_edit.setReadOnly(read_only)
        self.text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        
        # Add text view to a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidget(self.text_edit)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)
        
        # Copy to clipboard Button
        copy_button = QPushButton("Copy to clipboard")
        copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(copy_button)
        
        # OK Button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

    def copy_to_clipboard(self):
        """Copy the text from the text edit to clipboard"""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.text_edit.toPlainText())

def show_message(message, width=600, height=300, read_only=False):
    dialog = MessageDialog(message, width, height, read_only=read_only)
    dialog.exec_()
    res = dialog.text_edit.toPlainText()
    return res

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

class ErrorDialog(QDialog):
    """Error dialog with scrollable text area"""
    def __init__(self, message, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Error message")
        self.resize(400, 200)
        
        # Create layout
        layout = QVBoxLayout(self)
        
        # Error label
        label = QLabel("An error occurred:")
        layout.addWidget(label)
        
        # Text area for error message
        text_edit = QTextEdit()
        text_edit.setPlainText(message)
        text_edit.setReadOnly(True)
        text_edit.setLineWrapMode(QTextEdit.WidgetWidth)
        layout.addWidget(text_edit)
        
        # OK Button
        ok_button = QPushButton("OK")
        ok_button.clicked.connect(self.accept)
        layout.addWidget(ok_button)

def show_error_dialog(message):
    dialog = ErrorDialog(message)
    dialog.exec_()

def select_file(initial_path=None):
    """Open file dialog to select a file"""
    options = QFileDialog.Options()
    if initial_path:
        start_dir = initial_path
    else:
        start_dir = os.path.expanduser("~")
        
    filename, _ = QFileDialog.getOpenFileName(
        None, "Select a file", start_dir, "All Files (*)", options=options
    )
    
    return filename if filename else None

def get_clipboard_text():
    """Get text from clipboard"""
    app = QApplication.instance()
    clipboard = app.clipboard()
    return clipboard.text()

################################################################################

def basic_consult(type_consult, msg=None,extra_system_msg=""):
    global config_data
    
    if msg is None: 
        msg = get_clipboard_text()
        
    if len(msg) < 3:
        show_message("Too few elements on clipboard.")
        return
        
    if config_data["api_key"]=="":
        with open(config_file_path, "r") as arquivo:
            config_data = json.load(arquivo)
        
        if config_data["api_key"]=="":
            lib_files.open_from_filepath(config_file_path)
            show_notification_message("open_url_usage", config_data["usage"])
            QDesktopServices.openUrl(QUrl(config_data["usage"]))
            return
    
    try:
        fmts = lib_files.detect_formats(msg)
        fmt = max(fmts, key=fmts.get)
        ext = lib_files.EXTENSION[fmt]
        
        texts = lib_files.split_text(msg, max_size=8000, separators=["\n\n", ".", "!", "?"])
        
        all_out = ""
        is_ok = True
        
        for index, text in enumerate(texts):
            show_notification_message(type_consult, 
                                      f"{index+1}/{len(texts)} - The text was sent, please wait.")
            
            print(f"{index+1}/{len(texts)} - sent format:", fmt)
            
            res, OUT = lib_funcs.consultation_in_depth(config_data,
                                            lib_funcs.SYSTEM_QUESTION[type_consult] +
                                            f"\n- The text sent is probably written in {fmt} format."+extra_system_msg,
                                            text)
            
            if res == "<OK>":
                all_out = all_out + OUT
            elif res == "<NOERROR>":
                all_out = all_out + text
            else:
                is_ok = False
                
            show_notification_message(type_consult, f"{index+1}/{len(texts)} - Answer {res} recived! "+lib_funcs.SYSTEM_RESPONSE[res])
            
            print("recived:", res)
            
        if is_ok:
            if lib_files.program_exists('meld'):
                lib_files.compare_texts(msg, all_out, program='meld', filetype=ext)
            else:
                show_message(all_out)
        else:
            show_message("Errors in the query some answers were <ZERO>")
            
    except Exception as e:
        # Capture any exception and display the error
        error_message = f"Error: {str(e)}\n\nDetails:\n{traceback.format_exc()}"
        show_error_dialog(error_message)

def question_answer_consult(type_consult, msg=None, show=True):
    global config_data
    
    if msg is None: 
        msg = get_clipboard_text()
        
    if len(msg) < 3:
        show_message("Too few elements on clipboard.")
        return None
    
    if config_data["api_key"]=="":
        with open(config_file_path, "r") as arquivo:
            config_data = json.load(arquivo)
        
        if config_data["api_key"]=="":
            lib_files.open_from_filepath(config_file_path)
            show_notification_message("open_url_usage", config_data["usage"])
            QDesktopServices.openUrl(QUrl(config_data["usage"]))
            return None
       
    try:
        fmts = lib_files.detect_formats(msg)
        fmt = max(fmts, key=fmts.get)
        ext = lib_files.EXTENSION[fmt]
        print("format:", fmt)
    
        show_notification_message(type_consult, "The text was sent, please wait.")
        
        res = lib_funcs.question_answer_in_depth(config_data,
                                                lib_funcs.SYSTEM_QUESTION[type_consult] +
                                                f"\n- The text sent is probably written in {fmt} format.",
                                                msg)
        
        show_notification_message(type_consult, "Answer recived!")
        
        if show:
            show_message(res)
        
        return res
        
    except Exception as e:
        # Capture any exception and display the error
        error_message = f"Error: {str(e)}\n\nDetails:\n{traceback.format_exc()}"
        
        if show:
            show_error_dialog(error_message)
        
        return error_message

################################################################################
        
def improve_writing():
    basic_consult("improve_writing")

def improve_scientific_writing():
    basic_consult("improve_scientific_writing")

def improve_writing_fluency():
    basic_consult("improve_writing_fluency")

def concise_writing():
    basic_consult("concise_writing")
    
def simplified_writing():
    basic_consult("simplified_writing")

def eliminate_redundancies():
    basic_consult("eliminate_redundancies")

def paraphrase():
    basic_consult("paraphrase")

def on_action_article_template(item):
    show_notification_message("Template", "Please copy")
    res = lib_latex.generate_latex_article(item)
    show_message(res)
    
################################################################################
def improves_file_writing():
    file_path = select_file()
    
    if file_path:
        show_notification_message("Selected", file_path)
        
        if lib_files.is_binary(file_path):
            show_message("❌ 🤦‍♂️ The selected file must be a text file:\n" + file_path)
        else:
            msg = lib_files.load_file_content(file_path)
            basic_consult("improve_writing", msg=msg)

################################################################################

def summarize_text():
    question_answer_consult("summarize_text")
    
def abstract_to_title():
    question_answer_consult("abstract_to_title")
    
def text_to_computer_science_abstract():
    question_answer_consult("text_to_computer_science_abstract")
    
def logical_fallacy_detector():
    question_answer_consult("logical_fallacy_detector")

def keyword_generator():
    question_answer_consult("keyword_generator")

################################################################################

def text_to_latex_equation():
    question_answer_consult("text_to_latex_equation")
    
def text_to_latex_table():
    question_answer_consult("text_to_latex_table")
    
################################################################################

def dialog_text_to_latex_equation():
    res = show_message("")
    if len(res)>=5:
        question_answer_consult("text_to_latex_equation", msg = res)
    else:
        show_message("You need to write at least 5 characters in the description")
    
def dialog_text_to_latex_table():
    res = show_message("")
    if len(res)>=5:
        question_answer_consult("text_to_latex_table", msg = res)
    else:
        show_message("You need to write at least 5 characters in the description")
    
################################################################################    
def statistics():
    msg = get_clipboard_text()
    res = lib_stats.generate_word_token_json(msg)
    show_message(res)
    
def readability():
    msg = get_clipboard_text()
    OUT, results = lib_stats.analyze_readability(msg)
    res = question_answer_consult("readability", msg=str(results), show=False)
    
    if res is None:
        show_message(OUT)
    else:
        show_message(OUT + "\nComment:\n" + res)
    
################################################################################

def edit_config():
    lib_files.open_from_filepath(config_file_path)
    
def open_url_usage():
    show_notification_message("open_url_usage", config_data["usage"])
    QDesktopServices.openUrl(QUrl(config_data["usage"]))
    
def open_url_help():
    url = "https://github.com/trucomanx/ClipboardTextCorrection/blob/main/doc/README.md"
    show_notification_message("open_url_help", url)
    QDesktopServices.openUrl(QUrl(url))

################################################################################
def buy_me_a_coffee():
    show_notification_message("Buy me a coffee", "https://ko-fi.com/trucomanx")
    QDesktopServices.openUrl(QUrl("https://ko-fi.com/trucomanx"))

def open_about():
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

################################################################################
class ClipboardTextCorrectionApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.setQuitOnLastWindowClosed(False)
        
        # Get base directory for icons
        base_dir_path = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir_path, 'icons', 'logo.png')
        
        # Create system tray icon
        self.tray_icon = QSystemTrayIcon(QIcon(icon_path), self)
        self.tray_icon.setVisible(True)
        self.setProperty("tray_icon", self.tray_icon)
  
        
        # Create the tray menu
        self.tray_menu = QMenu()
        
        ########################################################################
        ########################################################################
        # Create improve_submenu
        self.improve_submenu = QMenu("📋 Improve texts from clipboard")
        
        # Add actions to improve_submenu
        improve_writing_action = QAction(QIcon.fromTheme("accessories-text-editor"), "Improve writing", self)
        improve_writing_action.triggered.connect(improve_writing)
        self.improve_submenu.addAction(improve_writing_action)
        
        improve_scientific_action = QAction(QIcon.fromTheme("accessories-text-editor"), "Improve scientific writing", self)
        improve_scientific_action.triggered.connect(improve_scientific_writing)
        self.improve_submenu.addAction(improve_scientific_action)

        improve_writing_fluency_action = QAction(QIcon.fromTheme("accessories-text-editor"), "Improve writing fluency", self)
        improve_writing_fluency_action.triggered.connect(improve_writing_fluency)
        self.improve_submenu.addAction(improve_writing_fluency_action)
        
        concise_writing_action = QAction(QIcon.fromTheme("accessories-text-editor"), "Concise writing", self)
        concise_writing_action.triggered.connect(concise_writing)
        self.improve_submenu.addAction(concise_writing_action)
        
        simplified_writing_action = QAction(QIcon.fromTheme("accessories-text-editor"), "Simplified writing", self)
        simplified_writing_action.triggered.connect(simplified_writing)
        self.improve_submenu.addAction(simplified_writing_action)
        
        eliminate_redundancies_action = QAction(QIcon.fromTheme("accessories-text-editor"), "Eliminate redundancies", self)
        eliminate_redundancies_action.triggered.connect(eliminate_redundancies)
        self.improve_submenu.addAction(eliminate_redundancies_action)
        
        paraphrase_action = QAction(QIcon.fromTheme("accessories-text-editor"), "Paraphrase", self)
        paraphrase_action.triggered.connect(paraphrase)
        self.improve_submenu.addAction(paraphrase_action)
        
        # Add improve_submenu to main menu
        self.tray_menu.addMenu(self.improve_submenu)
        self.tray_menu.addSeparator()
        
        
        ########################################################################
        ########################################################################
        # Create improve_file_submenu
        self.improve_file_submenu = QMenu("💻 Improve texts from files")
        
        # Add actions to improve_file_submenu
        improve_file_action = QAction(QIcon.fromTheme("edit-find-replace"), "Improves file writing", self)
        improve_file_action.triggered.connect(improves_file_writing)
        self.improve_file_submenu.addAction(improve_file_action)
        
        # Add improve_file_submenu to main menu
        self.tray_menu.addMenu(self.improve_file_submenu)
        self.tray_menu.addSeparator()
        
        
        ########################################################################
        ########################################################################
        # Create synthesize_submenu
        self.synthesize_submenu = QMenu("📋 Synthesize texts from clipboard")
        
        # Add actions to synthesize_submenu
        summarize_action = QAction(QIcon.fromTheme("document-edit"), "Summarize text", self)
        summarize_action.triggered.connect(summarize_text)
        self.synthesize_submenu.addAction(summarize_action)
        
        abstract_title_action = QAction(QIcon.fromTheme("document-edit"), "Abstract to title", self)
        abstract_title_action.triggered.connect(abstract_to_title)
        self.synthesize_submenu.addAction(abstract_title_action)
        
        cs_abstract_action = QAction(QIcon.fromTheme("document-edit"), "Text to computer science abstract", self)
        cs_abstract_action.triggered.connect(text_to_computer_science_abstract)
        self.synthesize_submenu.addAction(cs_abstract_action)
        
        fallacy_detector_action = QAction(QIcon.fromTheme("document-edit"), "Logical fallacy detector", self)
        fallacy_detector_action.triggered.connect(logical_fallacy_detector)
        self.synthesize_submenu.addAction(fallacy_detector_action)
        
        keyword_action = QAction(QIcon.fromTheme("document-edit"), "Keyword generator", self)
        keyword_action.triggered.connect(keyword_generator)
        self.synthesize_submenu.addAction(keyword_action)
        
        # Add synthesize_submenu to main menu
        self.tray_menu.addMenu(self.synthesize_submenu)
        self.tray_menu.addSeparator()
        
        
        ########################################################################
        ########################################################################

        # Create latex_submenu
        self.all_latex_submenu = QMenu("🎉 Synthesize LaTeX texts")

        #######################
        # Create latex_submenu
        self.latex_submenu = QMenu("📋 From clipboard")
        
        # Add actions to latex_submenu
        latex_equation_action = QAction(QIcon.fromTheme("font-x-generic"), "Text to latex equation", self)
        latex_equation_action.triggered.connect(text_to_latex_equation)
        self.latex_submenu.addAction(latex_equation_action)
        
        latex_table_action = QAction(QIcon.fromTheme("font-x-generic"), "Text to latex table", self)
        latex_table_action.triggered.connect(text_to_latex_table)
        self.latex_submenu.addAction(latex_table_action)
        
        # Add latex_submenu to main menu
        self.all_latex_submenu.addMenu(self.latex_submenu)
        self.all_latex_submenu.addSeparator()
        
        
        #######################
        # Create latex_submenu
        self.latex_dialog_submenu = QMenu("⌨️ From dialog")
        
        # Add actions to latex_dialog_submenu
        latex_equation_dialog_action = QAction(QIcon.fromTheme("font-x-generic"), "Text to latex equation", self)
        latex_equation_dialog_action.triggered.connect(dialog_text_to_latex_equation)
        self.latex_dialog_submenu.addAction(latex_equation_dialog_action)
        
        latex_table_dialog_action = QAction(QIcon.fromTheme("font-x-generic"), "Text to latex table", self)
        latex_table_dialog_action.triggered.connect(dialog_text_to_latex_table)
        self.latex_dialog_submenu.addAction(latex_table_dialog_action)
        
        
        # Add latex_dialog_submenu to main menu
        self.all_latex_submenu.addMenu(self.latex_dialog_submenu)
        self.all_latex_submenu.addSeparator()

        # Criar submenu para traduções
        self.article_template_menu = QMenu("🖥️ Article template")
        
        for item in article_format_data:
            label = item["title"]
            
            action = QAction(label, self)
            action.setIcon(QIcon.fromTheme("emblem-default"))
            action.triggered.connect(lambda checked, item=item: on_action_article_template(item))
            self.article_template_menu.addAction(action)
        
        self.all_latex_submenu.addMenu(self.article_template_menu)
        
        #######################
        # Add latex_submenu to main menu
        self.tray_menu.addMenu(self.all_latex_submenu)
        self.tray_menu.addSeparator()
        
        ########################################################################
        ########################################################################
        # Create analysis_submenu
        self.analysis_submenu = QMenu("📋 Text analysis from clipboard")
        
        # Add actions to analysis_submenu
        statistics_action = QAction(QIcon.fromTheme("document-page-setup"), "Text statistics", self)
        statistics_action.triggered.connect(statistics)
        self.analysis_submenu.addAction(statistics_action)
        
        readability_action = QAction(QIcon.fromTheme("document-page-setup"), "Text readability", self)
        readability_action.triggered.connect(readability)
        self.analysis_submenu.addAction(readability_action)
        
        # Add analysis_submenu to main menu
        self.tray_menu.addMenu(self.analysis_submenu)
        self.tray_menu.addSeparator()
        
        ########################################################################
        ########################################################################
        # Create program_information_submenu
        self.program_info_submenu = QMenu("🛠️ Program usage information")
        
        # Add actions to program_information_submenu
        edit_config_action = QAction(QIcon.fromTheme("applications-utilities"), "Open config file", self)
        edit_config_action.triggered.connect(edit_config)
        self.program_info_submenu.addAction(edit_config_action)
        
        url_usage_action = QAction(QIcon.fromTheme("applications-internet"), "Open url usage", self)
        url_usage_action.triggered.connect(open_url_usage)
        self.program_info_submenu.addAction(url_usage_action)
        
        url_help_action = QAction(QIcon.fromTheme("help-contents"), "Open url help", self)
        url_help_action.triggered.connect(open_url_help)
        self.program_info_submenu.addAction(url_help_action)
        
        # Add program_information_submenu to main menu
        self.tray_menu.addMenu(self.program_info_submenu)
        self.tray_menu.addSeparator()
        
        ########################################################################
        ########################################################################
        # Add direct actions to main menu
        coffee_action = QAction(QIcon.fromTheme("emblem-favorite"), "☕ Buy me a coffee: TrucomanX", self)
        coffee_action.triggered.connect(buy_me_a_coffee)
        self.tray_menu.addAction(coffee_action)
        
        about_action = QAction(QIcon.fromTheme("help-about"), "🌟 About", self)
        about_action.triggered.connect(open_about)
        self.tray_menu.addAction(about_action)
        
        self.tray_menu.addSeparator()
        
        ########################################################################
        ########################################################################
        # Add quit action
        quit_action = QAction(QIcon.fromTheme("application-exit"), "❌ Exit", self)
        quit_action.triggered.connect(self.quit)
        self.tray_menu.addAction(quit_action)
        
        # Set the menu for the tray icon
        self.tray_icon.setContextMenu(self.tray_menu)
        
        # Show the tray icon
        self.tray_icon.show()
        
def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app = ClipboardTextCorrectionApp(sys.argv)
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
