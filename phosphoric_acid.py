import tkinter as tk
from tkinter import ttk, messagebox, filedialog

try:
    from odf.opendocument import OpenDocumentText
    from odf.text import P
except ImportError:
    OpenDocumentText = None  # ODT export disabled; install with: pip install odfpy

# --- Molar Masses (g/mol) ---
M = {"P2O5": 141.94, "H2SO4": 98.08, "H3PO4": 97.99, "CaSO4_2H2O": 172.17, "HF": 20.01}

UNIT_FACTORS = {"kg": 1, "g": 1000, "t": 0.001}

# --- Translations ---
LANGUAGES = {
    "en": {
        "title": "Phosphoric Acid Calculator",
        "ore_kg": "Ore Mass",
        "p2o5_frac": "P2O5 Content (%)",
        "acid_excess": "Acid Excess (%)",
        "recovery": "Recovery Rate (%)",
        "phos_type": "Phosphate Form",
        "fluoride": "With Fluoride (Fluorapatite)",
        "no_fluoride": "Without Fluoride (Tricalcium Phosphate)",
        "calc_btn": "Calculate",
        "export_btn": "Export to .odt",
        "unit": "Output Unit",
        "results": "Results",
        "error": "Error",
        "error_msg": "Please enter valid numbers.",
        "error_range": "Values out of range:\n"
                       "- Ore mass must be > 0\n"
                       "- P2O5 content must be in (0, 100] %\n"
                       "- Acid excess must be >= 0\n"
                       "- Recovery must be in (0, 100] %",
        "calc_first": "Please calculate first.",
        "no_odfpy": "The 'odfpy' package is required for export.\nInstall it with: pip install odfpy",
        "saved_title": "Export",
        "saved": "File saved successfully!",
        "language": "Language",
        "p2o5": "P2O5",
        "h2so4_feed": "H2SO4 feed",
        "h3po4_theo": "H3PO4 theoretical",
        "h3po4_act": "H3PO4 actual",
        "gypsum": "Gypsum",
        "hf": "HF (Fluoride)",
    },
    "fr": {
        "title": "Calculateur d'Acide Phosphorique",
        "ore_kg": "Masse du Minerai",
        "p2o5_frac": "Teneur en P2O5 (%)",
        "acid_excess": "Excès d'Acide (%)",
        "recovery": "Taux de Récupération (%)",
        "phos_type": "Forme de Phosphate",
        "fluoride": "Avec Fluorure (Fluorapatite)",
        "no_fluoride": "Sans Fluorure (Phosphate Tricalcique)",
        "calc_btn": "Calculer",
        "export_btn": "Exporter en .odt",
        "unit": "Unité de Sortie",
        "results": "Résultats",
        "error": "Erreur",
        "error_msg": "Veuillez entrer des nombres valides.",
        "error_range": "Valeurs hors limites :\n"
                       "- La masse du minerai doit être > 0\n"
                       "- La teneur en P2O5 doit être dans ]0, 100] %\n"
                       "- L'excès d'acide doit être >= 0\n"
                       "- Le taux de récupération doit être dans ]0, 100] %",
        "calc_first": "Veuillez d'abord calculer.",
        "no_odfpy": "Le paquet 'odfpy' est requis pour l'export.\nInstallez-le avec : pip install odfpy",
        "saved_title": "Export",
        "saved": "Fichier enregistré avec succès!",
        "language": "Langue",
        "p2o5": "P2O5",
        "h2so4_feed": "Alimentation H2SO4",
        "h3po4_theo": "H3PO4 théorique",
        "h3po4_act": "H3PO4 réel",
        "gypsum": "Gypse",
        "hf": "HF (Fluorure)",
    },
    "de": {
        "title": "Phosphorsäure-Rechner",
        "ore_kg": "Erzmasse",
        "p2o5_frac": "P2O5-Anteil (%)",
        "acid_excess": "Säureüberschuss (%)",
        "recovery": "Rückgewinnungsrate (%)",
        "phos_type": "Phosphat-Form",
        "fluoride": "Mit Fluorid (Fluorapatit)",
        "no_fluoride": "Ohne Fluorid (Tricalciumphosphat)",
        "calc_btn": "Berechnen",
        "export_btn": "Als .odt exportieren",
        "unit": "Ausgabeeinheit",
        "results": "Ergebnisse",
        "error": "Fehler",
        "error_msg": "Bitte geben Sie gültige Zahlen ein.",
        "error_range": "Werte außerhalb des Bereichs:\n"
                       "- Erzmasse muss > 0 sein\n"
                       "- P2O5-Anteil muss in (0, 100] % liegen\n"
                       "- Säureüberschuss muss >= 0 sein\n"
                       "- Rückgewinnung muss in (0, 100] % liegen",
        "calc_first": "Bitte zuerst berechnen.",
        "no_odfpy": "Das Paket 'odfpy' wird für den Export benötigt.\nInstallation: pip install odfpy",
        "saved_title": "Export",
        "saved": "Datei erfolgreich gespeichert!",
        "language": "Sprache",
        "p2o5": "P2O5",
        "h2so4_feed": "H2SO4-Zufuhr",
        "h3po4_theo": "H3PO4 theoretisch",
        "h3po4_act": "H3PO4 tatsächlich",
        "gypsum": "Gips",
        "hf": "HF (Fluorid)",
    },
}


def parse_number(text):
    """Parse a float, accepting both '.' and ',' as decimal separator."""
    return float(text.strip().replace(",", "."))


def fmt(value):
    """Adaptive formatting so small values don't collapse to 0."""
    if value == 0:
        return "0"
    if abs(value) >= 1:
        return f"{value:,.2f}"
    return f"{value:.4g}"


class PhosphoricAcidApp:
    def __init__(self, root):
        self.root = root
        self.current_lang = "en"
        self.last_results = {}   # computed values in kg
        self.last_form = None    # phosphate form used for last_results

        # Language selector
        self.lang_frame = tk.Frame(root)
        self.lang_frame.pack(pady=5, fill=tk.X)
        self.lang_var = tk.StringVar(value="en")
        for text, val in [("English", "en"), ("Français", "fr"), ("Deutsch", "de")]:
            tk.Radiobutton(self.lang_frame, text=text, variable=self.lang_var,
                           value=val, command=self.change_lang).pack(side=tk.LEFT, padx=5)

        # Inputs
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        self.labels = {}
        self.entries = {}

        fields = ["ore_kg", "p2o5_frac", "acid_excess", "recovery"]
        defaults = ["", "", "", ""]  # no default values

        for i, (field, default) in enumerate(zip(fields, defaults)):
            self.labels[field] = tk.Label(self.input_frame, text="", anchor="e")
            self.labels[field].grid(row=i, column=0, sticky="e", pady=2, padx=5)
            self.entries[field] = tk.Entry(self.input_frame)
            self.entries[field].insert(0, default)
            self.entries[field].grid(row=i, column=1, pady=2, padx=5)
            if field != "ore_kg":
                tk.Label(self.input_frame, text="%").grid(row=i, column=2, sticky="w")
            else:
                # Unit selector for the ore input (kg / g / t)
                self.ore_unit_var = tk.StringVar(value="kg")
                ttk.Combobox(self.input_frame, textvariable=self.ore_unit_var,
                             values=list(UNIT_FACTORS), state="readonly",
                             width=4).grid(row=i, column=2, sticky="w")

        # Phosphate form toggle
        self.labels["phos_type"] = tk.Label(self.input_frame, text="", anchor="e")
        self.labels["phos_type"].grid(row=4, column=0, sticky="e", pady=2, padx=5)

        self.phos_var = tk.StringVar(value="fluoride")
        self.phos_frame = tk.Frame(self.input_frame)
        self.phos_frame.grid(row=4, column=1, sticky="w")

        self.rb_fluoride = tk.Radiobutton(self.phos_frame, text="", variable=self.phos_var, value="fluoride")
        self.rb_no_fluoride = tk.Radiobutton(self.phos_frame, text="", variable=self.phos_var, value="no_fluoride")
        self.rb_fluoride.pack(anchor="w")
        self.rb_no_fluoride.pack(anchor="w")

        self.calc_btn = tk.Button(self.input_frame, text="", command=self.calculate)
        self.calc_btn.grid(row=5, column=0, columnspan=2, pady=15)

        # Output
        self.output_frame = tk.Frame(root)
        self.output_frame.pack(pady=10)

        self.unit_var = tk.StringVar(value="kg")
        self.unit_label = tk.Label(self.output_frame, text="")
        self.unit_label.grid(row=0, column=0, sticky="e")
        self.unit_combo = ttk.Combobox(self.output_frame, textvariable=self.unit_var,
                                       values=list(UNIT_FACTORS), state="readonly", width=5)
        self.unit_combo.grid(row=0, column=1, sticky="w", padx=5)
        self.unit_combo.bind("<<ComboboxSelected>>", self.update_display)

        self.results_text = tk.Text(self.output_frame, height=9, width=48,
                                    state="disabled", font=("Courier", 10))
        self.results_text.grid(row=1, column=0, columnspan=2, pady=5)

        self.export_btn = tk.Button(root, text="", command=self.export_odt)
        self.export_btn.pack(pady=5)

        self.change_lang()

    def t(self, key):
        return LANGUAGES[self.current_lang].get(key, key)

    def change_lang(self):
        self.current_lang = self.lang_var.get()

        self.root.title(self.t("title"))
        self.calc_btn.config(text=self.t("calc_btn"))
        self.export_btn.config(text=self.t("export_btn"))
        self.unit_label.config(text=self.t("unit"))
        self.rb_fluoride.config(text=self.t("fluoride"))
        self.rb_no_fluoride.config(text=self.t("no_fluoride"))

        for field in ["ore_kg", "p2o5_frac", "acid_excess", "recovery", "phos_type"]:
            self.labels[field].config(text=self.t(field))

        self.update_display()

    def calculate(self):
        try:
            # Convert from the selected ore unit to kg (UNIT_FACTORS maps kg -> unit)
            ore_kg = parse_number(self.entries["ore_kg"].get()) / UNIT_FACTORS[self.ore_unit_var.get()]
            # Inputs are entered in percent; convert to fractions
            p2o5_frac = parse_number(self.entries["p2o5_frac"].get()) / 100
            acid_excess = parse_number(self.entries["acid_excess"].get()) / 100
            recovery = parse_number(self.entries["recovery"].get()) / 100
        except ValueError:
            messagebox.showerror(self.t("error"), self.t("error_msg"))
            return

        if not (ore_kg > 0 and 0 < p2o5_frac <= 1 and acid_excess >= 0 and 0 < recovery <= 1):
            messagebox.showerror(self.t("error"), self.t("error_range"))
            return

        p2o5 = ore_kg * p2o5_frac
        form = self.phos_var.get()

        if form == "fluoride":
            # Ca5(PO4)3F + 5 H2SO4 + 10 H2O -> 3 H3PO4 + 5 CaSO4·2H2O + HF
            # per mol P2O5: 10/3 H2SO4, 2 H3PO4, 10/3 gypsum, 2/3 HF
            h2so4_stoich = p2o5 * (10 / 3) * M["H2SO4"] / M["P2O5"]
            gypsum = p2o5 * (10 / 3) * M["CaSO4_2H2O"] / M["P2O5"]
            hf = p2o5 * (2 / 3) * M["HF"] / M["P2O5"]
        else:
            # Ca3(PO4)2 + 3 H2SO4 + 6 H2O -> 2 H3PO4 + 3 CaSO4·2H2O
            # per mol P2O5: 3 H2SO4, 2 H3PO4, 3 gypsum
            h2so4_stoich = p2o5 * 3 * M["H2SO4"] / M["P2O5"]
            gypsum = p2o5 * 3 * M["CaSO4_2H2O"] / M["P2O5"]
            hf = None

        h3po4_theo = p2o5 * 2 * M["H3PO4"] / M["P2O5"]
        h2so4_feed = h2so4_stoich * (1 + acid_excess)
        # Note: recovery scales only the H3PO4 yield; other streams are
        # reported at 100% conversion (theoretical).
        h3po4_actual = h3po4_theo * recovery

        self.last_form = form
        self.last_results = {
            "p2o5": p2o5,
            "h2so4_feed": h2so4_feed,
            "h3po4_theo": h3po4_theo,
            "h3po4_act": h3po4_actual,
            "gypsum": gypsum,
        }
        if hf is not None:
            self.last_results["hf"] = hf
        self.update_display()

    def _result_lines(self):
        """Return (label, value_str) pairs for the current unit and language."""
        unit = self.unit_var.get()
        factor = UNIT_FACTORS[unit]
        return [(self.t(k), fmt(v * factor)) for k, v in self.last_results.items()], unit

    def update_display(self, event=None):
        self.results_text.config(state="normal")
        self.results_text.delete("1.0", tk.END)

        if self.last_results:
            lines, unit = self._result_lines()
            self.results_text.insert(tk.END, f"--- {self.t('results')} ({unit}) ---\n")
            for label, value in lines:
                self.results_text.insert(tk.END, f"{label:<24}: {value}\n")

        self.results_text.config(state="disabled")

    def export_odt(self):
        if not self.last_results:
            messagebox.showwarning(self.t("error"), self.t("calc_first"))
            return
        if OpenDocumentText is None:
            messagebox.showerror(self.t("error"), self.t("no_odfpy"))
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".odt", filetypes=[("OpenDocument Text", "*.odt")])
        if not file_path:
            return

        lines, unit = self._result_lines()

        doc = OpenDocumentText()
        doc.text.addElement(P(text=f"--- {self.t('title')} ---"))
        doc.text.addElement(P(text=f"{self.t('language')}: {self.current_lang}"))
        doc.text.addElement(P(text=f"{self.t('phos_type')}: {self.t(self.last_form)}"))
        doc.text.addElement(P(text=f"{self.t('unit')}: {unit}"))
        doc.text.addElement(P(text="---------------------------------"))
        for label, value in lines:
            doc.text.addElement(P(text=f"{label}: {value} {unit}"))

        try:
            doc.save(file_path)
        except OSError as e:
            messagebox.showerror(self.t("error"), str(e))
            return
        messagebox.showinfo(self.t("saved_title"), self.t("saved"))


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("480x600")
    app = PhosphoricAcidApp(root)
    root.mainloop()
