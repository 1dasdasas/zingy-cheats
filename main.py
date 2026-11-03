import customtkinter as ctk

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


# ---------- Описание настроек для каждой функции ----------
# Каждая настройка: (тип, имя, значение_по_умолчанию, доп_параметры)
# type: "slider" -> (min, max), "checkbox" -> bool, "entry" -> str, "option" -> list
FEATURE_SETTINGS = {
    "Reach": [
        ("slider", "Distance", 4.5, (3.0, 6.0)),
        ("checkbox", "Only while sprinting", False, None),
    ],
    "Killaura": [
        ("slider", "Range", 4.0, (2.0, 8.0)),
        ("slider", "CPS", 12, (1, 20)),
        ("option", "Target", "Closest", ["Closest", "Lowest HP", "Angle"]),
    ],
    "Hitbox": [
        ("slider", "Expand X", 0.2, (0.0, 1.0)),
        ("slider", "Expand Y", 0.2, (0.0, 1.0)),
    ],
    "Fly": [
        ("slider", "Speed", 1.0, (0.1, 5.0)),
        ("checkbox", "Anti-kick", True, None),
    ],
    "Speed": [
        ("slider", "Multiplier", 1.5, (1.0, 3.0)),
    ],
    "ESP": [
        ("option", "Mode", "Box", ["Box", "Glow", "2D"]),
        ("slider", "Range", 64, (8, 256)),
        ("checkbox", "Show names", True, None),
    ],
    # Для функций без явных настроек — пустой список
}


class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, master, feature_name, settings_store):
        super().__init__(master)
        self.title(f"Настройки — {feature_name}")
        self.geometry("380x420")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.feature = feature_name
        self.store = settings_store.setdefault(feature_name, {})

        ctk.CTkLabel(self, text=feature_name, font=("Arial", 18, "bold")).pack(pady=(15, 10))

        specs = FEATURE_SETTINGS.get(feature_name, [])
        if not specs:
            ctk.CTkLabel(self, text="Для этой функции настроек нет.",
                         text_color="gray").pack(pady=20)
            return

        for spec in specs:
            self._build_control(spec)

        ctk.CTkButton(self, text="Закрыть", command=self.destroy).pack(pady=15)

    def _build_control(self, spec):
        kind, name, default, extra = spec
        current = self.store.get(name, default)

        frame = ctk.CTkFrame(self, fg_color="transparent")
        frame.pack(fill="x", padx=15, pady=6)

        if kind == "slider":
            lo, hi = extra
            ctk.CTkLabel(frame, text=name, anchor="w").pack(fill="x")
            row = ctk.CTkFrame(frame, fg_color="transparent")
            row.pack(fill="x")
            value_label = ctk.CTkLabel(row, text=str(current), width=50)
            value_label.pack(side="right")

            def on_change(v, lbl=value_label, key=name):
                # округление для красоты
                val = round(float(v), 2)
                lbl.configure(text=str(val))
                self.store[key] = val

            slider = ctk.CTkSlider(row, from_=lo, to=hi, command=on_change)
            slider.set(current)
            slider.pack(side="left", fill="x", expand=True, padx=(0, 10))

        elif kind == "checkbox":
            var = ctk.BooleanVar(value=bool(current))

            def on_toggle(key=name, v=var):
                self.store[key] = v.get()

            ctk.CTkCheckBox(frame, text=name, variable=var,
                            command=on_toggle).pack(anchor="w")

        elif kind == "entry":
            ctk.CTkLabel(frame, text=name, anchor="w").pack(fill="x")
            entry = ctk.CTkEntry(frame)
            entry.insert(0, str(current))
            entry.pack(fill="x")

            def on_key(event=None, key=name, e=entry):
                self.store[key] = e.get()

            entry.bind("<KeyRelease>", on_key)

        elif kind == "option":
            ctk.CTkLabel(frame, text=name, anchor="w").pack(fill="x")
            combo = ctk.CTkOptionMenu(frame, values=extra,
                                      command=lambda v, key=name: self.store.__setitem__(key, v))
            combo.set(current)
            combo.pack(fill="x")


class ZingyCheatsGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Zingy Cheats | 1.21.44 (Demo)")
        self.geometry("820x620")
        self.resizable(False, False)

        # Хранилище значений настроек и состояний переключателей
        self.settings_store = {}
        self.toggle_state = {}

        # Боковая панель
        self.sidebar = ctk.CTkFrame(self, width=180, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        ctk.CTkLabel(self.sidebar, text="ZINGY", font=("Arial", 24, "bold")).pack(pady=30)

        self.categories = ["Combat", "Movement", "Player", "Visuals", "Misc"]
        self.buttons = {}
        for cat in self.categories:
            btn = ctk.CTkButton(self.sidebar, text=cat, fg_color="transparent",
                                hover_color="#333", anchor="w",
                                command=lambda c=cat: self.show_category(c))
            btn.pack(pady=5, padx=10, fill="x")
            self.buttons[cat] = btn

        self.main_frame = ctk.CTkScrollableFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        self.show_category("Combat")

    def show_category(self, category):
        for w in self.main_frame.winfo_children():
            w.destroy()
        for btn in self.buttons.values():
            btn.configure(fg_color="transparent")
        self.buttons[category].configure(fg_color="#1f538d")

        ctk.CTkLabel(self.main_frame, text=category,
                     font=("Arial", 20, "bold")).pack(anchor="w", pady=(10, 20))

        features = {
            "Combat": ["Reach", "Killaura", "Hitbox", "Aim Assist", "Auto Clicker",
                       "Trigger Bot", "Elytra Target", "Удар в небо"],
            "Movement": ["Air Jump", "Airspeed", "Fly", "Speed", "Step", "Spider",
                         "Jesus", "Jetpack", "Long Jump", "Sprint", "Strafe", "No Slow Down"],
            "Player": ["Auto Totem", "Auto Firework", "Chest Aura", "Fast Eat",
                       "Fast Mine", "Scaffold", "Free Cam", "Fake Lag"],
            "Visuals": ["ESP", "Fullbright", "Freelook", "Animations"],
            "Misc": ["Anti AFK", "Anti Bot", "Disabler", "Edition Faker", "Device Spoofer"],
        }

        for name in features.get(category, []):
            self._make_feature_row(name)

    def _make_feature_row(self, name):
        row = ctk.CTkFrame(self.main_frame, fg_color="#2a2a2a", corner_radius=6)
        row.pack(fill="x", pady=3, padx=4)

        label = ctk.CTkLabel(row, text=name, anchor="w", font=("Arial", 14))
        label.pack(side="left", padx=12, pady=8, fill="x", expand=True)

        # Состояние переключателя
        var = ctk.BooleanVar(value=self.toggle_state.get(name, False))
        self.toggle_state[name] = var.get()

        def on_toggle(n=name, v=var):
            self.toggle_state[n] = v.get()

        switch = ctk.CTkSwitch(row, text="", width=50, variable=var, command=on_toggle)
        switch.pack(side="right", padx=12)

        # ---- ПКМ по строке/лейблу открывает окно настроек ----
        def open_settings(event=None, feat=name):
            # если уже открыто — поднять
            SettingsWindow(self, feat, self.settings_store)

        for widget in (row, label):
            widget.bind("<Button-3>", open_settings)   # ПКМ на Windows/Linux
            widget.bind("<Button-2>", open_settings)   # средняя (на всякий)
            # Для macOS ПКМ часто эмулируется Control+Click:
            widget.bind("<Control-Button-1>", open_settings)


if __name__ == "__main__":
    app = ZingyCheatsGUI()
    app.mainloop()
