import datetime
import tkinter as tk
import zipfile
from tkinter import ttk, filedialog, messagebox

global zip_file_path  # Globální proměnná přístupná i pro jiné funkce


def choose_zip_file():
    global zip_file_path
    # Zvolení ZIP souboru k prohlížení
    zip_file_path = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip")])
    print(f"Selected ZIP file: {zip_file_path}")  # kontrolní print do terminálu
    return zip_file_path


def get_structure(zip_file_path):
    # Získání struktury adresáře pomocí slovniku a vnořených slovníků
    result_dict = {}

    with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
        for file_info in zip_ref.infolist():
            path_parts = file_info.filename.split('/')
            current_dict = result_dict

            for part in path_parts[:-1]:  # Ignorovat poslední část (soubor)
                if part not in current_dict:
                    current_dict[part] = {}
                current_dict = current_dict[part]

            if file_info.is_dir():  # Je to složka
                current_dict[path_parts[-1]] = {}
            else:  # Je to soubor
                current_dict[path_parts[-1]] = None
    print(f"Structure of dict: {result_dict}")  # Kontrolní print obsahu slovníku se strukturou
    return result_dict


def update_treeview(tree, data, parent=""):
    # Aktualizuje strukturu treeview
    for key, value in data.items():
        item = tree.insert(parent, "end", text=key)
        if isinstance(value, dict):
            update_treeview(tree, value, parent=item)


def browse_zip():
    # Prochází ZIP souboru a zobrazí jeho obsah
    zip_file_path = choose_zip_file()
    structure_dict = get_structure(zip_file_path)

    tree.delete(*tree.get_children())  # Vyčištění stromu před aktualizací
    update_treeview(tree, structure_dict)


def on_treeview_click(event):
    # Získává text položky, o které uživatel chce zobrazit info
    item = tree.selection()[0]  # Získání vybrané položky ve stromu
    item_text = tree.item(item, "text")  # Získání textu vybrané položky
    show_file_info(item_text)


def show_file_info(item_text):
    # Zobrazuje informace o souboru, který si uživatel vybral
    with zipfile.ZipFile(zip_file_path, 'r') as zipFile:  # otevírá zip pro čtení
        files_in_zip_list = zipFile.namelist()  # získá seznam položek v zipu
        for file_path in files_in_zip_list:
            if file_path.endswith(item_text):
                file_info = zipFile.getinfo(file_path)  # získává informace o souboru v archivu
                filename = file_path.split("/")[-1]
                formatted_date_time = datetime.datetime(*file_info.date_time).strftime('%Y-%m-%d %H:%M:%S')
                break
    print(zipFile.getinfo(file_path))
    tk.messagebox.showinfo("Informace o souboru",
                           f"Jméno souboru: {filename}\n"
                           f"Velikost: {file_info.file_size} bajtů\n"
                           f"Datum a čas:  {formatted_date_time}\n")


# Vytvoření úvodního okna
intro_window = tk.Tk()
intro_window.title("Vítejte v Basic Zip browseru")
intro_window.geometry("900x500")  # Nastavení šířky a výšky okna
icon = intro_window.iconbitmap("zipico.ico")

# Nastavení velikosti textu a fontu pro úvodní okno
welcome_label = tk.Label(intro_window, text="Vítejte v Basic Zip browseru:", font=("Arial", 14, "bold"))
welcome_label.pack(pady=20)

# Nastavení textu před tlačítkem Select Zip File
label_before_button = tk.Label(intro_window, text="Vyberte ZIP soubor:")
label_before_button.pack(pady=5)

# Tlačítko pro výběr cesty k ZIP souboru
select_button = tk.Button(intro_window, text="Select ZIP", command=browse_zip)
select_button.pack(pady=10)

# Treeview pro zobrazení stromové struktury
tree = ttk.Treeview(intro_window)
tree.heading("#0", text="ZIP File Contents", anchor=tk.W)
tree.pack(expand=True, fill="both")
tree.bind("<Double-1>", on_treeview_click)

# Spuštění hlavní smyčky Tkinter
intro_window.mainloop()
