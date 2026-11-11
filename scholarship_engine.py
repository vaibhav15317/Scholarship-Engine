"""
Smart Scholarship Engine — cinematic desktop UI
Python 3.10+ | PySide6
Run: python smart_scholarship_engine.py
Install: pip install PySide6
Note: Scholarship catalogue is a starter list. Verify eligibility and deadlines on official portals.
"""
import sys, json, os, webbrowser
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QFont, QColor, QPainter, QLinearGradient, QBrush
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton, QLineEdit,
    QComboBox, QSpinBox, QDoubleSpinBox, QCheckBox, QTextEdit, QVBoxLayout,
    QHBoxLayout, QGridLayout, QScrollArea, QStackedWidget, QFormLayout,
    QMessageBox, QProgressBar, QButtonGroup, QSplitter
)

APP_NAME = "Smart Scholarship Engine"
PORTALS = {
    "Karnataka SSP": "https://ssp.karnataka.gov.in/",
    "National Scholarship Portal": "https://scholarships.gov.in/Students",
    "All NSP Scholarships": "https://scholarships.gov.in/All-Scholarships",
}

# Starter catalogue only; verify current-year availability and rules on official portals.
SCHOLARSHIPS = [
    dict(name="Karnataka State Scholarship Portal (SSP)", provider="Government of Karnataka",
         category="Karnataka State", levels="SSLC / PUC / Diploma / Degree / PG",
         amount="Varies by scheme", categories=["SC", "ST", "OBC", "Minority", "General"],
         docs=["Identity proof", "Marks card", "Bank passbook"], url=PORTALS["Karnataka SSP"],
         desc="Entry point for multiple Karnataka pre-matric and post-matric schemes. Exact eligibility depends on the scheme."),
    dict(name="Post-Matric Scholarship for SC Students", provider="Government scheme",
         category="SC/ST", levels="PUC / Diploma / Degree / PG",
         amount="As per scheme rules", categories=["SC"],
         docs=["Caste/category certificate", "Income certificate", "Marks card", "Bank passbook"],
         url=PORTALS["Karnataka SSP"], desc="For eligible students studying beyond matriculation. Check income, course and renewal conditions."),
    dict(name="Post-Matric Scholarship for ST Students", provider="Government scheme",
         category="SC/ST", levels="PUC / Diploma / Degree / PG",
         amount="As per scheme rules", categories=["ST"],
         docs=["Caste/category certificate", "Income certificate", "Marks card", "Bank passbook"],
         url=PORTALS["Karnataka SSP"], desc="For eligible ST students in post-matric education. Verify current rules on the official portal."),
    dict(name="BC / OBC Fee Concession or Reimbursement", provider="Karnataka Backward Classes Welfare",
         category="Karnataka State", levels="PUC / Diploma / Degree / PG",
         amount="Depends on approved fees and scheme", categories=["OBC", "2A", "2B", "3A", "3B"],
         docs=["Caste/category certificate", "Income certificate", "Marks card", "Admission / bonafide proof"],
         url=PORTALS["Karnataka SSP"], desc="Potential fee support for eligible backward-class students; conditions vary by scheme and course."),
    dict(name="Vidyasiri Food & Accommodation Assistance", provider="Karnataka Backward Classes Welfare",
         category="Karnataka State", levels="PUC / Diploma / Degree / PG",
         amount="As specified by current notification", categories=["OBC", "2A", "2B", "3A", "3B"],
         docs=["Caste/category certificate", "Income certificate", "Admission / bonafide proof", "Hostel / accommodation proof"],
         url=PORTALS["Karnataka SSP"], desc="Accommodation/food assistance may be available for eligible students who meet the current conditions."),
    dict(name="Chief Minister Raitha Vidya Nidhi", provider="Government of Karnataka",
         category="Karnataka State", levels="PUC / Diploma / Degree / PG",
         amount="As specified by current notification", categories=["Farmer family"],
         docs=["Farmer-family / land record", "Marks card", "Admission / bonafide proof"],
         url=PORTALS["Karnataka SSP"], desc="Student support associated with eligible farmer families. Confirm current scope and eligibility."),
    dict(name="AICTE Pragati Scholarship", provider="AICTE",
         category="Merit / Special", levels="Diploma / Degree",
         amount="As specified by AICTE", categories=["Girls"],
         docs=["Marks card", "Income certificate", "Admission / bonafide proof", "Bank passbook"],
         url="https://www.aicte-india.org/", desc="Scholarship for eligible girl students in approved technical education; check the current AICTE notification."),
    dict(name="AICTE Saksham Scholarship", provider="AICTE",
         category="Merit / Special", levels="Diploma / Degree",
         amount="As specified by AICTE", categories=["Disability"],
         docs=["Disability / UDID proof", "Marks card", "Admission / bonafide proof", "Bank passbook"],
         url="https://www.aicte-india.org/", desc="Support for eligible students with disabilities in approved technical courses; verify current criteria."),
    dict(name="National Means-cum-Merit Scholarship (NMMS)", provider="Government of India",
         category="Central Government", levels="Class 8 / School",
         amount="As specified by current notification", categories=["Merit"],
         docs=["Marks card", "Income certificate", "Bank passbook"],
         url=PORTALS["National Scholarship Portal"], desc="School-level merit-cum-means scheme; eligibility and continuation rules apply."),
    dict(name="Central Sector Scheme of Scholarship (CSSS)", provider="Government of India",
         category="Central Government", levels="PUC / Degree / PG",
         amount="As specified by current notification", categories=["Merit"],
         docs=["Marks card", "Income certificate", "Admission / bonafide proof", "Bank passbook"],
         url=PORTALS["National Scholarship Portal"], desc="Merit-based support for eligible college students; check the current selection and renewal rules."),
    dict(name="Minority Welfare Student Support", provider="Karnataka Minority Welfare Department",
         category="Minority", levels="PUC / Diploma / Degree / PG",
         amount="Depends on active scheme", categories=["Minority"],
         docs=["Minority community proof", "Income certificate", "Marks card", "Bank passbook"],
         url=PORTALS["Karnataka SSP"], desc="Potential support under active minority welfare schemes. Availability and eligibility change by notification."),
    dict(name="Arivu Education Loan Scheme", provider="Karnataka Minority Welfare Department",
         category="Loan (not scholarship)", levels="Diploma / Degree / PG",
         amount="Loan; repayment conditions apply", categories=["Minority"],
         docs=["Minority community proof", "Income certificate", "Admission / bonafide proof"],
         url=PORTALS["Karnataka SSP"], desc="Education-loan option, not a scholarship or free grant. Read repayment terms before applying."),
]

BG = "#070B14"
PANEL = "#0E1625"
PANEL2 = "#121E32"
BORDER = "#24344C"
TEXT = "#F2F6FF"
MUTED = "#9AAAC4"
BLUE = "#5C7CFA"
PURPLE = "#8B5CF6"
CYAN = "#39C6E6"
GREEN = "#27D6A0"
GOLD = "#FFC857"

def card(parent=None, extra=""):
    f = QFrame(parent)
    f.setObjectName("panel")
    if extra:
        f.setProperty("class", extra)
    return f

def heading(text, size=18, color=TEXT, weight=700):
    label = QLabel(text)
    label.setFont(QFont("Segoe UI", size, weight))
    label.setStyleSheet(f"color:{color};")
    return label

class ScholarshipCard(QFrame):
    def __init__(self, item, match, saved, on_save):
        super().__init__()
        self.item = item
        self.setObjectName("scholarshipCard")
        self.setMinimumWidth(250)
        self.setMaximumWidth(340)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(10)
        row = QHBoxLayout()
        tag = QLabel(item["category"].upper())
        tag.setStyleSheet(f"background:#202E50;color:{CYAN};padding:5px 8px;border-radius:7px;font-size:10px;font-weight:700;")
        row.addWidget(tag)
        row.addStretch()
        score = QLabel(f"{match}% MATCH")
        score.setStyleSheet(f"background:#123C36;color:{GREEN};padding:5px 8px;border-radius:7px;font-size:10px;font-weight:700;")
        row.addWidget(score)
        layout.addLayout(row)
        title = QLabel(item["name"])
        title.setWordWrap(True)
        title.setMinimumHeight(48)
        title.setFont(QFont("Segoe UI", 14, 700))
        title.setStyleSheet(f"color:{TEXT};")
        layout.addWidget(title)
        provider = QLabel(item["provider"])
        provider.setStyleSheet(f"color:{MUTED};font-size:11px;")
        layout.addWidget(provider)
        amount = QLabel("◈  " + item["amount"])
        amount.setStyleSheet(f"color:{GOLD};font-size:12px;font-weight:600;")
        layout.addWidget(amount)
        desc = QLabel(item["desc"])
        desc.setWordWrap(True)
        desc.setMinimumHeight(65)
        desc.setStyleSheet(f"color:{MUTED};font-size:11px;")
        layout.addWidget(desc)
        layout.addStretch()
        buttons = QHBoxLayout()
        save_btn = QPushButton("♥  Saved" if item["name"] in saved else "♡  Shortlist")
        save_btn.setObjectName("secondaryButton")
        save_btn.clicked.connect(lambda: on_save(item["name"]))
        buttons.addWidget(save_btn)
        open_btn = QPushButton("View details  ↗")
        open_btn.setObjectName("primaryButton")
        open_btn.clicked.connect(lambda: webbrowser.open(item["url"]))
        buttons.addWidget(open_btn)
        layout.addLayout(buttons)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(APP_NAME)
        self.resize(1440, 900)
        self.setMinimumSize(1100, 720)
        self.saved = set()
        self.profile = {}
        root = QWidget()
        root.setObjectName("root")
        self.setCentralWidget(root)
        outer = QVBoxLayout(root)
        outer.setContentsMargins(0, 0, 0, 0)
        outer.setSpacing(0)

        top = QFrame()
        top.setObjectName("topbar")
        top_layout = QHBoxLayout(top)
        top_layout.setContentsMargins(28, 14, 28, 14)
        logo = QLabel("✦")
        logo.setStyleSheet(f"color:{CYAN};font-size:30px;font-weight:900;")
        top_layout.addWidget(logo)
        brand_box = QVBoxLayout()
        brand_box.addWidget(heading("SMART SCHOLARSHIP", 15))
        brand_box.addWidget(QLabel("ENGINE  /  YOUR FUTURE, UNLOCKED"))
        brand_box.itemAt(1).widget().setStyleSheet(f"color:{MUTED};font-size:9px;letter-spacing:2px;")
        top_layout.addLayout(brand_box)
        top_layout.addSpacing(28)
        self.search = QLineEdit()
        self.search.setPlaceholderText("⌕   Search scholarships, schemes or keywords...")
        self.search.setMinimumWidth(300)
        self.search.textChanged.connect(self.refresh_cards)
        top_layout.addWidget(self.search, 1)
        self.profile_chip = QLabel("  STUDENT PROFILE  ●")
        self.profile_chip.setStyleSheet(f"color:{GREEN};background:#112A2B;padding:10px 14px;border-radius:12px;font-size:11px;font-weight:700;")
        top_layout.addWidget(self.profile_chip)
        outer.addWidget(top)

        body = QHBoxLayout()
        body.setContentsMargins(0, 0, 0, 0)
        body.setSpacing(0)
        outer.addLayout(body, 1)

        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(210)
        side = QVBoxLayout(sidebar)
        side.setContentsMargins(16, 24, 16, 18)
        side.setSpacing(9)
        side.addWidget(QLabel("WORKSPACE"))
        side.itemAt(0).widget().setStyleSheet(f"color:{MUTED};font-size:10px;font-weight:700;letter-spacing:2px;padding:0 8px 8px;")
        self.nav_group = QButtonGroup(self)
        self.nav_group.setExclusive(True)
        for i, (label, page) in enumerate([("⌂   Overview", 0), ("◎   Student profile", 1), ("▦   Scholarship explorer", 2), ("♡   My shortlist", 3)]):
            btn = QPushButton(label)
            btn.setCheckable(True)
            btn.setObjectName("navButton")
            self.nav_group.addButton(btn, page)
            side.addWidget(btn)
            btn.clicked.connect(lambda checked=False, p=page: self.show_page(p))
            if i == 0: btn.setChecked(True)
        side.addStretch()
        quote = QLabel("“Education is the most powerful tool you can use to change the world.”\n\n— Nelson Mandela")
        quote.setWordWrap(True)
        quote.setStyleSheet(f"color:{MUTED};font-style:italic;font-size:11px;padding:12px;")
        side.addWidget(quote)
        body.addWidget(sidebar)

        self.pages = QStackedWidget()
        body.addWidget(self.pages, 1)
        self.home_page = self.make_home()
        self.profile_page = self.make_profile()
        self.explorer_page = self.make_explorer()
        self.shortlist_page = self.make_shortlist()
        for p in [self.home_page, self.profile_page, self.explorer_page, self.shortlist_page]:
            self.pages.addWidget(p)
        self.show_page(0)
        self.refresh_cards()
        self.apply_style()

    def scroll_page(self, child):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setWidget(child)
        return scroll

    def make_home(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 26, 28, 30)
        lay.setSpacing(22)
        hero = QFrame()
        hero.setObjectName("hero")
        hl = QHBoxLayout(hero)
        hl.setContentsMargins(30, 28, 30, 28)
        copy = QVBoxLayout()
        eyebrow = QLabel("PERSONALISED FUNDING DISCOVERY")
        eyebrow.setStyleSheet(f"color:{CYAN};font-size:10px;font-weight:800;letter-spacing:3px;")
        copy.addWidget(eyebrow)
        title = QLabel("Your dreams deserve\nfinancial support.")
        title.setFont(QFont("Segoe UI", 29, 800))
        title.setStyleSheet("color:#FFFFFF;")
        copy.addWidget(title)
        sub = QLabel("Find scholarships that fit your education, profile and achievements.")
        sub.setWordWrap(True)
        sub.setStyleSheet(f"color:#C1CDE1;font-size:13px;")
        copy.addWidget(sub)
        btn = QPushButton("Find my scholarships   →")
        btn.setObjectName("primaryButton")
        btn.setMaximumWidth(230)
        btn.clicked.connect(lambda: self.show_page(2))
        copy.addSpacing(8)
        copy.addWidget(btn)
        copy.addStretch()
        hl.addLayout(copy, 2)
        visual = QFrame()
        visual.setMinimumWidth(180)
        visual.setStyleSheet("background: qradialgradient(cx:0.5,cy:0.5,radius:0.8,stop:0 #344C86,stop:0.55 #18294A,stop:1 #10192B);border-radius:18px;")
        vl = QVBoxLayout(visual)
        vl.addWidget(heading("FUND YOUR NEXT CHAPTER", 11, "#C9D7FF"))
        vl.addStretch()
        vl.addWidget(heading("01  DISCOVER", 15))
        vl.addWidget(heading("02  MATCH", 15, CYAN))
        vl.addWidget(heading("03  APPLY", 15, GREEN))
        vl.addStretch()
        hl.addWidget(visual, 1)
        lay.addWidget(hero)

        stats = QHBoxLayout()
        for label, value, color in [
            ("CATALOGUE STARTER SET", str(len(SCHOLARSHIPS)), CYAN),
            ("OFFICIAL PORTALS", "03", PURPLE),
            ("YOUR SHORTLIST", "0", GREEN),
        ]:
            panel = card()
            pl = QVBoxLayout(panel)
            pl.setContentsMargins(18, 16, 18, 16)
            pl.addWidget(QLabel(label))
            pl.itemAt(0).widget().setStyleSheet(f"color:{MUTED};font-size:10px;font-weight:700;letter-spacing:1px;")
            pl.addWidget(heading(value, 25, color))
            stats.addWidget(panel)
        lay.addLayout(stats)
        row = QHBoxLayout()
        row.addWidget(heading("Picked for your profile", 20))
        row.addStretch()
        view = QPushButton("Explore all  →")
        view.setObjectName("textButton")
        view.clicked.connect(lambda: self.show_page(2))
        row.addWidget(view)
        lay.addLayout(row)
        self.home_cards = QHBoxLayout()
        self.home_cards.setSpacing(14)
        lay.addLayout(self.home_cards)
        note = QLabel("Note: matches are indicative, not a guarantee of eligibility. Confirm deadlines and requirements on official scheme portals.")
        note.setWordWrap(True)
        note.setStyleSheet(f"color:{MUTED};font-size:10px;padding:8px;")
        lay.addWidget(note)
        lay.addStretch()
        return self.scroll_page(page)

    def make_profile(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 26, 28, 30)
        lay.setSpacing(18)
        lay.addWidget(heading("Student profile", 26))
        lay.addWidget(QLabel("Fill in the details you are comfortable providing to improve scholarship filtering."))
        form_panel = card()
        grid = QGridLayout(form_panel)
        grid.setContentsMargins(24, 24, 24, 24)
        grid.setHorizontalSpacing(20)
        grid.setVerticalSpacing(15)
        self.name = QLineEdit(); self.name.setPlaceholderText("Student name")
        self.gender = QComboBox(); self.gender.addItems(["Prefer not to say", "Female", "Male", "Other"])
        self.category = QComboBox(); self.category.addItems(["Prefer not to say", "General", "SC", "ST", "OBC", "2A", "2B", "3A", "3B", "Minority", "Farmer family", "Disability"])
        self.level = QComboBox(); self.level.addItems(["Class 8 / School", "SSLC / Class 10", "PUC / Class 12", "Diploma", "Degree", "Engineering", "PG"])
        self.state = QComboBox(); self.state.addItems(["Karnataka", "Other Indian state"])
        self.age = QSpinBox(); self.age.setRange(0, 100); self.age.setSpecialValueText("Not entered")
        self.income = QComboBox(); self.income.addItems(["Not specified", "Below ₹1 lakh", "₹1–2.5 lakh", "₹2.5–5 lakh", "₹5–8 lakh", "Above ₹8 lakh"])
        self.marks = QDoubleSpinBox(); self.marks.setRange(0, 100); self.marks.setDecimals(2); self.marks.setSuffix(" %")
        self.marks.setSpecialValueText("Not entered")
        self.certifications = QTextEdit(); self.certifications.setPlaceholderText("e.g. coding certificate, sports achievement, NCC, Olympiad, disability certificate…")
        self.certifications.setMaximumHeight(90)
        fields = [
            ("Full name", self.name), ("Gender", self.gender),
            ("Category", self.category), ("Education level", self.level),
            ("State / region", self.state), ("Age", self.age),
            ("Annual family income", self.income), ("Latest marks (%)", self.marks),
        ]
        for idx, (label, widget) in enumerate(fields):
            r, c = divmod(idx, 2)
            box = QVBoxLayout()
            box.addWidget(QLabel(label))
            box.addWidget(widget)
            grid.addLayout(box, r, c)
        grid.addWidget(QLabel("Certifications and achievements"), 4, 0, 1, 2)
        grid.addWidget(self.certifications, 5, 0, 1, 2)
        docs_label = QLabel("Documents available (tick what you have)")
        grid.addWidget(docs_label, 6, 0, 1, 2)
        self.doc_checks = {}
        docs = ["Caste/category certificate", "Income certificate", "Identity proof", "Marks card",
                "Admission / bonafide proof", "Bank passbook", "Disability / UDID proof",
                "Farmer-family / land record", "Minority community proof", "Hostel / accommodation proof"]
        doc_grid = QGridLayout()
        for i, doc in enumerate(docs):
            cb = QCheckBox(doc)
            self.doc_checks[doc] = cb
            doc_grid.addWidget(cb, i // 2, i % 2)
        grid.addLayout(doc_grid, 7, 0, 1, 2)
        save = QPushButton("Save profile & refresh matches  ✓")
        save.setObjectName("primaryButton")
        save.clicked.connect(self.save_profile)
        grid.addWidget(save, 8, 0, 1, 2)
        lay.addWidget(form_panel)
        lay.addStretch()
        return self.scroll_page(page)

    def make_explorer(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 26, 28, 30)
        lay.setSpacing(18)
        lay.addWidget(heading("Scholarship explorer", 26))
        lay.addWidget(QLabel("Search the starter catalogue, compare potential matches, then verify scheme details at the official source."))
        filters = QHBoxLayout()
        self.category_filter = QComboBox()
        self.category_filter.addItems(["All categories", "Karnataka State", "SC/ST", "Central Government", "Minority", "Merit / Special", "Loan (not scholarship)"])
        self.category_filter.currentTextChanged.connect(self.refresh_cards)
        self.level_filter = QComboBox()
        self.level_filter.addItems(["All education levels", "School", "SSLC", "PUC", "Diploma", "Degree", "Engineering", "PG"])
        self.level_filter.currentTextChanged.connect(self.refresh_cards)
        filters.addWidget(self.category_filter)
        filters.addWidget(self.level_filter)
        filters.addStretch()
        lay.addLayout(filters)
        self.explorer_count = QLabel()
        self.explorer_count.setStyleSheet(f"color:{MUTED};font-size:11px;")
        lay.addWidget(self.explorer_count)
        self.explorer_cards = QGridLayout()
        self.explorer_cards.setSpacing(14)
        lay.addLayout(self.explorer_cards)
        lay.addStretch()
        return self.scroll_page(page)

    def make_shortlist(self):
        page = QWidget()
        lay = QVBoxLayout(page)
        lay.setContentsMargins(28, 26, 28, 30)
        lay.setSpacing(18)
        lay.addWidget(heading("My shortlist", 26))
        lay.addWidget(QLabel("Keep promising options in one place while you verify eligibility and application dates."))
        self.shortlist_cards = QGridLayout()
        self.shortlist_cards.setSpacing(14)
        lay.addLayout(self.shortlist_cards)
        lay.addStretch()
        return self.scroll_page(page)

    def show_page(self, page):
        self.pages.setCurrentIndex(page)
        for b in self.nav_group.buttons():
            b.setChecked(self.nav_group.id(b) == page)
        if page == 3: self.refresh_shortlist()

    def save_profile(self):
        self.profile = {
            "name": self.name.text().strip(),
            "gender": self.gender.currentText(),
            "category": self.category.currentText(),
            "level": self.level.currentText(),
            "state": self.state.currentText(),
            "age": self.age.value(),
            "income": self.income.currentText(),
            "marks": self.marks.value(),
            "certifications": self.certifications.toPlainText().strip(),
            "documents": [d for d, cb in self.doc_checks.items() if cb.isChecked()],
        }
        self.profile_chip.setText("  PROFILE SAVED  ✓")
        self.refresh_cards()
        QMessageBox.information(self, "Profile saved", "Your profile has been applied to the on-screen matching rules. This prototype saves the profile for this session only.")

    def match_score(self, item):
        score = 48
        p = self.profile
        cat = p.get("category", "")
        if cat and cat != "Prefer not to say":
            if cat in item["categories"] or (cat in ("2A", "2B", "3A", "3B") and "OBC" in item["categories"]):
                score += 25
            elif cat not in ("General",):
                score -= 8
        level = p.get("level", "")
        if level:
            if level.lower().split(" /")[0] in item["levels"].lower() or level in item["levels"]:
                score += 12
            elif level in ("Degree", "Engineering") and any(x in item["levels"] for x in ("Degree", "Diploma", "PG")):
                score += 5
        if p.get("state") == "Karnataka" and "Karnataka" in item["category"]:
            score += 8
        docs = set(p.get("documents", []))
        if item["docs"]:
            score += min(7, round(7 * len(docs.intersection(item["docs"])) / len(item["docs"])))
        return max(10, min(96, score))

    def filtered(self):
        query = self.search.text().strip().lower()
        cat = self.category_filter.currentText() if hasattr(self, "category_filter") else "All categories"
        level = self.level_filter.currentText() if hasattr(self, "level_filter") else "All education levels"
        out = []
        for item in SCHOLARSHIPS:
            blob = " ".join([item["name"], item["provider"], item["category"], item["desc"], item["levels"]]).lower()
            if query and query not in blob: continue
            if cat != "All categories" and item["category"] != cat: continue
            if level != "All education levels" and level.lower() not in item["levels"].lower(): continue
            out.append(item)
        return sorted(out, key=self.match_score, reverse=True)

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget(): child.widget().deleteLater()
            elif child.layout(): self.clear_layout(child.layout())

    def toggle_save(self, name):
        if name in self.saved: self.saved.remove(name)
        else: self.saved.add(name)
        self.refresh_cards()
        self.refresh_shortlist()

    def refresh_cards(self, *args):
        if not hasattr(self, "home_cards") or not hasattr(self, "explorer_cards"): return
        items = self.filtered()
        self.clear_layout(self.home_cards)
        for item in items[:3]:
            self.home_cards.addWidget(ScholarshipCard(item, self.match_score(item), self.saved, self.toggle_save))
        self.home_cards.addStretch()
        self.clear_layout(self.explorer_cards)
        for i, item in enumerate(items):
            self.explorer_cards.addWidget(ScholarshipCard(item, self.match_score(item), self.saved, self.toggle_save), i // 3, i % 3)
        self.explorer_count.setText(f"{len(items)} schemes in this starter catalogue · sorted by indicative profile match")
        self.refresh_shortlist()

    def refresh_shortlist(self):
        if not hasattr(self, "shortlist_cards"): return
        self.clear_layout(self.shortlist_cards)
        saved_items = [x for x in SCHOLARSHIPS if x["name"] in self.saved]
        if not saved_items:
            empty = QLabel("Your shortlist is empty. Browse scholarships and choose ♡ Shortlist on any card.")
            empty.setStyleSheet(f"color:{MUTED};padding:20px;")
            self.shortlist_cards.addWidget(empty, 0, 0, 1, 3)
        for i, item in enumerate(saved_items):
            self.shortlist_cards.addWidget(ScholarshipCard(item, self.match_score(item), self.saved, self.toggle_save), i // 3, i % 3)

    def apply_style(self):
        self.setStyleSheet(f"""
        QWidget {{ background:{BG}; color:{TEXT}; font-family:'Segoe UI'; font-size:12px; }}
        QMainWindow {{ background:{BG}; }}
        #topbar {{ background:#0A101D; border-bottom:1px solid {BORDER}; }}
        #sidebar {{ background:#0A101D; border-right:1px solid {BORDER}; }}
        #panel {{ background:{PANEL}; border:1px solid {BORDER}; border-radius:16px; }}
        #hero {{ background:qlineargradient(x1:0,y1:0,x2:1,y2:1,stop:0 #182C50,stop:0.52 #17213C,stop:1 #281C45); border:1px solid #34496D; border-radius:22px; }}
        #scholarshipCard {{ background:qlineargradient(x1:0,y1:0,x2:0,y2:1,stop:0 #121F34,stop:1 #0D1524); border:1px solid #263B58; border-radius:16px; }}
        #scholarshipCard:hover {{ border:1px solid {BLUE}; background:#15243C; }}
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {{ background:#0A1220; color:{TEXT}; border:1px solid #2A3B56; border-radius:9px; padding:10px; selection-background-color:{BLUE}; }}
        QComboBox QAbstractItemView {{ background:#111B2D; selection-background-color:{BLUE}; }}
        QCheckBox {{ spacing:8px; color:#D8E2F2; }}
        QCheckBox::indicator {{ width:16px; height:16px; }}
        QPushButton {{ border:0; border-radius:9px; padding:10px 13px; font-weight:650; }}
        QPushButton#primaryButton {{ color:white; background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 {BLUE},stop:1 {PURPLE}); }}
        QPushButton#primaryButton:hover {{ background:#718BFF; }}
        QPushButton#secondaryButton {{ color:#DCE6FF; background:#202E48; border:1px solid #344967; }}
        QPushButton#secondaryButton:hover {{ background:#2B3E60; }}
        QPushButton#textButton {{ color:{CYAN}; background:transparent; }}
        QPushButton#navButton {{ color:#AAB8CF; background:transparent; text-align:left; padding:13px 12px; }}
        QPushButton#navButton:hover {{ color:white; background:#142039; }}
        QPushButton#navButton:checked {{ color:white; background:qlineargradient(x1:0,y1:0,x2:1,y2:0,stop:0 #283E80,stop:1 #34245E); border-left:3px solid {CYAN}; }}
        QScrollArea {{ border:0; background:transparent; }}
        QScrollBar:vertical {{ background:#0A101D; width:10px; margin:2px; }}
        QScrollBar::handle:vertical {{ background:#2D405E; min-height:25px; border-radius:5px; }}
        QScrollBar::add-line:vertical,QScrollBar::sub-line:vertical {{ height:0; }}
        """)
        # Keep top-level containers transparent where appropriate
        for w in self.findChildren(QLabel):
            if w.parent() and w.parent().objectName() not in ("panel", "hero", "scholarshipCard"):
                pass

def main():
    app = QApplication(sys.argv)
    app.setApplicationName(APP_NAME)
    app.setFont(QFont("Segoe UI", 10))
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
