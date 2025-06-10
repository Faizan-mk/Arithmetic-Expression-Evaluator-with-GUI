import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                           QHBoxLayout, QTextEdit, QPushButton, QLabel, QTabWidget,
                           QProgressBar, QMessageBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont, QColor, QIcon, QTextCharFormat, QTextCursor
from qdarkstyle import load_stylesheet
from qtawesome import icon
from code_generator import CodeGenerator

class IntermediateCodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Interactive Intermediate Code Generator')
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize step history
        self.current_step = 0
        self.step_history = []
        
        # Apply dark theme with enhanced colors
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
            }
            
            QWidget {
                background-color: #2d2d2d;
            }
            
            QLabel {
                color: #ffffff;
                font-size: 16px;
            }
            
            QTextEdit {
                background-color: #1e1e1e;
                color: #ffffff;
                border: 2px solid #333333;
                border-radius: 10px;
                padding: 15px;
                font-size: 14px;
            }
            
            QTabWidget::pane {
                border: 2px solid #333333;
                border-radius: 10px;
                background-color: #2d2d2d;
            }
            
            QTabBar::tab {
                background-color: #333333;
                color: #ffffff;
                padding: 15px 30px;
                border: none;
                border-radius: 5px;
            }
            
            QTabBar::tab:selected {
                background-color: #4a90e2;
                color: #ffffff;
            }
            
            /* Enhanced button styles */
            QPushButton {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:1 #357abd);
                color: #ffffff;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                min-width: 120px;
            }
            
            QPushButton:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #357abd, stop:1 #296699);
            }
            
            QPushButton:pressed {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #296699, stop:1 #215280);
            }
            
            QPushButton#generate {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4CAF50, stop:1 #45a049);
            }
            
            QPushButton#generate:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #45a049, stop:1 #3c8d42);
            }
            
            QPushButton#clear {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #f44336, stop:1 #da190b);
            }
            
            QPushButton#clear:hover {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #da190b, stop:1 #c4160a);
            }
            
            QProgressBar {
                border: 2px solid #333333;
                border-radius: 5px;
                text-align: center;
                background-color: #2d2d2d;
            }
            
            QProgressBar::chunk {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #4a90e2, stop:1 #357abd);
            }
        """)
        
        # Initialize code generator
        self.code_generator = CodeGenerator()
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(25)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Create header with title and icon
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title = QLabel('Interactive Intermediate Code Generator')
        title.setFont(QFont('Arial', 28, QFont.Bold))
        title.setStyleSheet("""
            color: #4a90e2;
            padding: 10px;
        """)
        
        header_layout.addWidget(title)
        main_layout.addWidget(header)
        
        # Create input panel
        input_panel = QWidget()
        input_layout = QVBoxLayout(input_panel)
        input_layout.setSpacing(15)
        
        self.input_label = QLabel('Enter Arithmetic Expression:')
        self.input_label.setFont(QFont('Arial', 16))
        
        self.input_text = QTextEdit()
        self.input_text.setFont(QFont('Arial', 14))
        
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_text)
        
        # Create button panel
        button_panel = QWidget()
        button_layout = QHBoxLayout(button_panel)
        button_layout.setSpacing(15)
        
        self.generate_btn = QPushButton(icon('fa5s.play', color='#ffffff'), 'Generate Code')
        self.generate_btn.setFont(QFont('Arial', 14))
        self.generate_btn.clicked.connect(self.generate_code)
        self.generate_btn.setObjectName('generate')  # For special styling
        
        self.clear_btn = QPushButton(icon('fa5s.times', color='#ffffff'), 'Clear')
        self.clear_btn.setFont(QFont('Arial', 14))
        self.clear_btn.clicked.connect(self.clear_all)
        self.clear_btn.setObjectName('clear')  # For special styling
        
        button_layout.addWidget(self.generate_btn)
        button_layout.addWidget(self.clear_btn)
        
        # Create output panel with tabs
        self.output_tabs = QTabWidget()
        
        # Create styled text edits for each tab
        self.three_address_text = QTextEdit()
        self.postfix_text = QTextEdit()
        self.steps_text = QTextEdit()
        
        for text_edit in [self.three_address_text, self.postfix_text, self.steps_text]:
            text_edit.setFont(QFont('Arial', 14))
            text_edit.setReadOnly(True)
            
        self.output_tabs.addTab(self.three_address_text, 'Three-Address Code')
        self.output_tabs.addTab(self.postfix_text, 'Postfix Notation')
        self.output_tabs.addTab(self.steps_text, 'Translation Steps')
        
        # Add progress bar
        self.progress = QProgressBar()
        self.progress.setMaximum(100)
        self.progress.setTextVisible(True)
        
        # Add widgets to main layout
        main_layout.addWidget(input_panel)
        main_layout.addWidget(button_panel)
        main_layout.addWidget(self.output_tabs)
        main_layout.addWidget(self.progress)
    
    def generate_code(self):
        expression = self.input_text.toPlainText().strip()
        
        if not expression:
            QMessageBox.warning(self, 'Warning', 'Please enter an arithmetic expression')
            return
            
        try:
            # Show progress
            self.progress.setValue(0)
            self.progress.show()
            
            # Generate three-address code
            three_address_code = self.code_generator.generate_three_address_code(expression)
            self.three_address_text.setText('\n'.join(three_address_code))
            
            # Generate postfix notation
            postfix_code = self.code_generator.generate_postfix_notation(expression)
            self.postfix_text.setText('\n'.join(postfix_code))
            
            # Generate steps
            self.generate_steps(expression)
            
            # Animate progress
            self.animate_progress()
            
        except Exception as e:
            QMessageBox.critical(self, 'Error', str(e))
            self.progress.hide()
    
    def generate_steps(self, expression):
        """Generate translation steps"""
        try:
            # Step 1: Input Expression
            self.step_history.append(f"Step 1: Input Expression\n----------------------\nExpression: {expression}\n")
            
            # Step 2: Tokenization
            tokens = self.code_generator.tokenize(expression)
            self.step_history.append(f"\nStep 2: Tokenization\n-------------------\nTokens: {' '.join(tokens)}\n")
            
            # Step 3: Operator Precedence Analysis
            precedence_analysis = []
            for token in tokens:
                if token in self.code_generator.operators:
                    precedence_analysis.append(f"{token} (Precedence: {self.code_generator.precedence[token]})")
                else:
                    precedence_analysis.append(token)
            self.step_history.append(f"\nStep 3: Operator Precedence Analysis\n-----------------------------------\nAnalysis: {' '.join(precedence_analysis)}\n")
            
            # Step 4: Postfix Conversion
            postfix = self.code_generator.shunting_yard(tokens)
            self.step_history.append(f"\nStep 4: Postfix Notation\n-----------------------\nPostfix: {' '.join(postfix)}\n")
            
            # Step 5: Three-Address Code Generation
            tac = self.code_generator.generate_three_address_code(expression)
            self.step_history.append(f"\nStep 5: Three-Address Code\n-------------------------\nCode:\n{'\n'.join(tac)}")
            
            # Show all steps
            self.steps_text.setText('\n'.join(self.step_history))
            
        except Exception as e:
            self.step_history = []
            self.steps_text.setText(f"Error: {str(e)}")
    
    def animate_progress(self):
        current_value = 0
        
        def update_progress():
            nonlocal current_value
            if current_value < 100:
                current_value += 10
                self.progress.setValue(current_value)
                QTimer.singleShot(100, update_progress)
            else:
                self.progress.hide()
        
        update_progress()
    
    def highlight_syntax(self, text_edit):
        text = text_edit.toPlainText()
        
        # Clear existing formatting
        text_edit.selectAll()
        text_edit.setTextColor(QColor('#ffffff'))
        text_edit.clear()
        
        # Apply syntax highlighting
        for token in text.split():
            cursor = text_edit.textCursor()
            cursor.insertText(token + ' ')
            
            if token in ['+', '-', '*', '/']:
                text_edit.setTextColor(QColor('#ff6b6b'))  # Red for operators
            elif token in ['=', '<', '>', '==', '!=', '<=', '>=']:
                text_edit.setTextColor(QColor('#4ecdc4'))  # Teal for operators
            elif token.isnumeric():
                text_edit.setTextColor(QColor('#45b7d1'))  # Blue for numbers
            elif token.startswith('t'):  # Temporary variables
                text_edit.setTextColor(QColor('#ffd700'))  # Gold for temporaries
            else:
                text_edit.setTextColor(QColor('#ffffff'))  # White for variables
            
            text_edit.setTextCursor(cursor)
    
    def clear_all(self):
        self.input_text.clear()
        self.three_address_text.clear()
        self.postfix_text.clear()
        self.steps_text.clear()
        self.progress.hide()
        self.step_history = []
        self.current_step = 0

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(load_stylesheet())
    window = IntermediateCodeGenerator()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
