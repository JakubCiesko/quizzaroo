import tkinter as tk
import asyncio
from tkinter import filedialog
from tkinter import ttk, filedialog
from textsnippet import TextSnippet
from snippetcollection import SnippetCollection
from quizmaker import QuizMaker
from text import Text

class HighlighterApp:
    text = None
    snippets = SnippetCollection()


    def __init__(self, master):
        self.master = master
        self.master.title("Quizzaroo")

        # Create tabs
        self.tabs = ttk.Notebook(self.master)
        self.tabs.pack(fill="both", expand=True)

        # Tab 1: Text Highlighting
        self.create_highlight_tab()

        # Tab 2: Generate Test Settings
        self.create_settings_tab()

        # Tab 3: Audio Upload/Record
        self.create_audio_tab()

    def create_highlight_tab(self):
        highlight_tab = tk.Frame(self.tabs)
        self.tabs.add(highlight_tab, text="Input")
        
        text_frame = tk.Frame(highlight_tab)
        text_frame.pack(expand=True, fill="both")

        # Text Entry
        self.text_widget = CustomText(text_frame, wrap="word", height=15, width=80)
        self.text_widget.pack(expand=True, fill="both", side="left")
        scrollbar = tk.Scrollbar(text_frame, command=self.text_widget.yview)
        scrollbar.pack(side="right", fill="y")
        self.text_widget.config(yscrollcommand=scrollbar.set)

        # Buttons
        open_button = tk.Button(highlight_tab, text="Upload text file", command=self.open_file)
        open_button.pack(side="left")

        highlight_button = tk.Button(highlight_tab, text="Highlight", command=self.highlight_text)
        highlight_button.pack(side="left")

        
        remove_button = tk.Button(highlight_tab, text="Remove Highlight", command=self.remove_highlight)
        remove_button.pack(side="left")


        generate_test_button = tk.Button(highlight_tab, text="Generate Test", command=self.create_test)
        generate_test_button.pack(side="bottom")


        # Listbox for highlighted parts
        self.highlighted_listbox = tk.Listbox(highlight_tab)
        self.highlighted_listbox.pack(side="bottom", fill="both", expand=True)
        
    def highlight_text(self):
        selected_text = self.text_widget.get("sel.first", "sel.last").replace("\n", " ")
        if selected_text:
            self.text_widget.tag_add("highlight", "sel.first", "sel.last")
            location = (self.text_widget.index(tk.SEL_FIRST), self.text_widget.index(tk.SEL_LAST))
            self.highlighted_listbox.insert("end", selected_text)
            self.create_snippet(selected_text, location=location)

    def remove_highlight(self):
        selected_index = self.highlighted_listbox.curselection()
        if selected_index:
            self.highlighted_listbox.delete(selected_index)
            snippet = self.snippets[selected_index[0]]
            snippet_location = snippet.get_location()
            self.text_widget.tag_remove("highlight", snippet_location[0], snippet_location[1])
            self.remove_snippet(snippet)
        
    def remove_snippet(self, snippet):
        self.snippets.pop_snippet(snippet)
        
    def create_snippet(self, text, location=None):
        text_snippet = TextSnippet(text)
        if location: 
            text_snippet.set_location(location)
        self.snippets.add_snippet(text_snippet)
        return text_snippet

    def get_test_settings(self):
        return self.test_type_var, self.test_level_var

    def create_test(self):
        test_type, test_level = self.get_test_settings()
        quiz_maker = QuizMaker()
        quiz_maker.set_api_key("YOUR_API_KEY")
        quiz_maker.set_model("gpt-4")
        quiz_maker.set_topic_snippets(self.snippets)
        text = Text(self.text_widget.get("1.0", tk.END))
        quiz_maker.set_topic(text)
        quiz = quiz_maker.create_quiz(test_type)
        self.create_test_tab(quiz)
        return quiz 
        

    def create_test_tab(self, quiz_obj):
        test_tab = tk.Frame(self.tabs)
        self.tabs.add(test_tab, text="Test Tab")
        label = tk.Label(test_tab, text="Test:")
        label.grid(row=0, column=0)
        label.pack()
        quiz_str = quiz_obj.parse_questions_to_str()
        text_widget = tk.Text(test_tab, wrap=tk.WORD, height=100, width=100)
        text_widget.pack(pady=10)
        text_widget.config(state=tk.NORMAL)  # Set the state to normal for editing
        text_widget.delete("1.0", tk.END)  # Clear existing content
        text_widget.insert(tk.END, quiz_str)  # Set new content
        text_widget.config(state=tk.DISABLED)

        


    def create_settings_tab(self):
        settings_tab = ttk.Frame(self.tabs)
        self.tabs.add(settings_tab, text="Test Settings")

        # Settings Widgets
        type_label = tk.Label(settings_tab, text="What to use to create test:")
        type_label.grid(row=0, column=0, sticky="w", padx=10, pady=5)

        # Variable for test_type
        self.test_type_var = tk.StringVar(value="snippets")

        # Combobox for test_type
        #test_type_combobox = ttk.Combobox(settings_tab, textvariable=self.test_type_var, values=["whole_text", "snippets"])
        #test_type_combobox.grid(row=0, column=1, padx=10, pady=5, sticky="w")

        
        snippets_radio = ttk.Radiobutton(settings_tab, text="Snippets", variable=self.test_type_var, value="snippets")
        snippets_radio.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        text_radio = ttk.Radiobutton(settings_tab, text="Whole Text", variable=self.test_type_var, value="text")
        text_radio.grid(row=1, column=2, padx=10, pady=5, sticky="w")


      
        level_label = tk.Label(settings_tab, text="Test Level:")
        level_label.grid(row=2, column=0, sticky="w", padx=10, pady=5)

        # Radiobuttons for test_level

        # Variable for test_level
        self.test_level_var = tk.StringVar(value="easy")

        # Radiobuttons for test_level
        easy_radio = ttk.Radiobutton(settings_tab, text="Easy", variable=self.test_level_var, value="easy")
        easy_radio.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        medium_radio = ttk.Radiobutton(settings_tab, text="Medium", variable=self.test_level_var, value="medium")
        medium_radio.grid(row=3, column=2, padx=10, pady=5, sticky="w")

        hard_radio = ttk.Radiobutton(settings_tab, text="Hard", variable=self.test_level_var, value="hard")
        hard_radio.grid(row=3, column=3, padx=10, pady=5, sticky="w")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                content = file.read()
                self.text_widget.set_text(content)

    #TODO:This needs to be coded
    def create_audio_tab(self):
        pass

    def upload_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.mp3;*.wav")])
        if file_path:
            # TO-DO: transcritpion
            result_text = f"Simulated transcription from {file_path}"
            self.audio_textbox.insert("end", result_text + "\n")

    def record_audio(self):
        # Simulate recording audio
        result_text = "Simulated audio recording"
        self.audio_textbox.insert("end", result_text + "\n")

    def check_summary(self):
        # Simulate checking summary using Hugging Face "whisper" model
        result_text = "Simulated summary from Hugging Face model"
        self.audio_textbox.insert("end", result_text + "\n")
            

class CustomText(tk.Text):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.tag_configure("highlight", background="yellow")

    def set_text(self, content):
        self.delete("1.0", tk.END)
        self.insert(tk.END, content)

def main():
    root = tk.Tk()
    app = HighlighterApp(root)
    root.geometry("800x600")
    root.mainloop()


class EReaderApp:
    def __init__(self):
        self.app = HighlighterApp
    
    def mainloop(self, geometry="800x600"):
        root = tk.Tk()
        app = self.app(root)
        root.geometry(geometry)
        root.mainloop()
    
    

if __name__ == "__main__":
    app = EReaderApp()
    app.mainloop()
