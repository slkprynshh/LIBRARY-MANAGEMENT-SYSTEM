import os

COVERS_DIR = r"c:\Users\Priyanshu\Desktop\library-frontend\assets\images\covers"
AVATARS_DIR = r"c:\Users\Priyanshu\Desktop\library-frontend\assets\images\avatars"

GENRE_COLORS = {
    "Fiction":     ("#1E3A5F", "#60A5FA", "#BFDBFE"),
    "Science":     ("#064E3B", "#34D399", "#A7F3D0"),
    "Technology":  ("#1E1B4B", "#818CF8", "#C7D2FE"),
    "History":     ("#451A03", "#F59E0B", "#FDE68A"),
    "Mathematics": ("#1F2937", "#A78BFA", "#EDE9FE"),
    "Literature":  ("#4A044E", "#E879F9", "#F5D0FE"),
    "Self-Help":   ("#052E16", "#4ADE80", "#BBF7D0"),
    "Productivity":("#0C4A6E", "#38BDF8", "#BAE6FD"),
    "Psychology":  ("#3B0764", "#C084FC", "#E9D5FF"),
    "default":     ("#0F172A", "#0EA5E9", "#BAE6FD"),
}

BOOKS = [
    # (filename_slug, short_title, author_initials, genre)
    ("the-alchemist",           "The\nAlchemist",           "PC",  "Fiction"),
    ("to-kill-mockingbird",     "To Kill a\nMockingbird",   "HL",  "Fiction"),
    ("1984",                    "1984",                     "GO",  "Fiction"),
    ("the-great-gatsby",        "The Great\nGatsby",        "FSF", "Fiction"),
    ("brave-new-world",         "Brave New\nWorld",         "AH",  "Fiction"),
    ("brief-history-time",      "A Brief\nHistory\nof Time","SH",  "Science"),
    ("selfish-gene",            "The Selfish\nGene",        "RD",  "Science"),
    ("cosmos",                  "Cosmos",                   "CS",  "Science"),
    ("origin-of-species",       "Origin of\nSpecies",       "CD",  "Science"),
    ("astrophysics-hurry",      "Astrophysics\nfor People", "NDT", "Science"),
    ("clean-code",              "Clean\nCode",              "RM",  "Technology"),
    ("pragmatic-programmer",    "Pragmatic\nProgrammer",    "AH",  "Technology"),
    ("intro-algorithms",        "Introduction\nto Algorithms","TC","Technology"),
    ("ai-modern-approach",      "AI: A Modern\nApproach",   "SR",  "Technology"),
    ("deep-learning",           "Deep\nLearning",           "IG",  "Technology"),
    ("sapiens",                 "Sapiens",                  "YNH", "History"),
    ("guns-germs-steel",        "Guns Germs\n& Steel",      "JD",  "History"),
    ("silk-roads",              "The Silk\nRoads",          "PF",  "History"),
    ("peoples-history-us",      "A People's\nHistory",      "HZ",  "History"),
    ("diary-young-girl",        "Diary of a\nYoung Girl",   "AF",  "History"),
    ("fermats-last-theorem",    "Fermat's Last\nTheorem",   "SS",  "Mathematics"),
    ("man-knew-infinity",       "The Man Who\nKnew Infinity","RK", "Mathematics"),
    ("how-to-solve-it",         "How to\nSolve It",         "GP",  "Mathematics"),
    ("godel-escher-bach",       "Gödel Escher\nBach",       "DH",  "Mathematics"),
    ("joy-of-x",                "The Joy\nof x",            "SS2", "Mathematics"),
    ("pride-prejudice",         "Pride &\nPrejudice",       "JA",  "Literature"),
    ("crime-punishment",        "Crime &\nPunishment",      "FD",  "Literature"),
    ("hundred-years-solitude",  "100 Years\nof Solitude",   "GGM", "Literature"),
    ("brothers-karamazov",      "The Brothers\nKaramazov",  "FD2", "Literature"),
    ("don-quixote",             "Don\nQuixote",             "MC",  "Literature"),
    # Extra books referenced in mock-data
    ("design-patterns",         "Design\nPatterns",         "GOF", "Technology"),
    ("atomic-habits",           "Atomic\nHabits",           "JC",  "Self-Help"),
    ("deep-work",               "Deep\nWork",               "CN",  "Productivity"),
    ("thinking-fast-slow",      "Thinking\nFast & Slow",    "DK",  "Psychology"),
    ("python-crash-course",     "Python\nCrash Course",     "EM",  "Technology"),
    ("lean-startup",            "The Lean\nStartup",        "ER",  "Technology"),
    ("zero-to-one",             "Zero\nto One",             "PT",  "Technology"),
    ("thinking-in-systems",     "Thinking\nin Systems",     "DM",  "Science"),
    ("refactoring",             "Refactoring",              "MF",  "Technology"),
    ("code-complete",           "Code\nComplete",           "SM",  "Technology"),
    ("art-of-war",              "The Art\nof War",          "ST",  "History"),
    ("harry-potter",            "Harry\nPotter",            "JKR", "Fiction"),
]

def wrap_text_svg(text, x, y, font_size, fill, line_height=None):
    if line_height is None:
        line_height = font_size + 4
    lines = text.split("\n")
    total_h = len(lines) * line_height
    start_y = y - total_h / 2 + line_height / 2
    result = []
    for i, line in enumerate(lines):
        cy = start_y + i * line_height
        result.append(
            f'<text x="{x}" y="{cy}" font-family="Georgia,serif" font-size="{font_size}" '
            f'fill="{fill}" text-anchor="middle" dominant-baseline="middle">{line}</text>'
        )
    return "\n".join(result)

def make_cover_svg(slug, title, initials, genre, w=120, h=170):
    bg, accent, light = GENRE_COLORS.get(genre, GENRE_COLORS["default"])
    lines = title.count("\n") + 1
    font_size = 13 if lines <= 2 else 11
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0%" stop-color="{bg}"/>
      <stop offset="100%" stop-color="{accent}" stop-opacity="0.3"/>
    </linearGradient>
  </defs>
  <rect width="{w}" height="{h}" fill="url(#bg)" rx="6"/>
  <rect x="6" y="6" width="{w-12}" height="{h-12}" fill="none" stroke="{accent}" stroke-width="1" rx="4" opacity="0.5"/>
  <rect x="0" y="{h-36}" width="{w}" height="36" fill="{accent}" opacity="0.85" rx="0"/>
  <rect x="0" y="{h-36}" width="{w}" height="36" fill="{accent}" opacity="0.85"/>
  <rect x="0" y="{h-6}" width="{w}" height="6" fill="{accent}" rx="0"/>
  {wrap_text_svg(title, w//2, h//2 - 14, font_size, light)}
  <text x="{w//2}" y="{h-18}" font-family="Arial,sans-serif" font-size="9" fill="{bg}" text-anchor="middle" dominant-baseline="middle" font-weight="bold">{initials}</text>
  <line x1="14" y1="{h-36}" x2="{w-14}" y2="{h-36}" stroke="{light}" stroke-width="0.5" opacity="0.4"/>
</svg>"""
    return svg

def make_avatar_svg(initials, color_pair, size=80):
    bg, fg = color_pair
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}">
  <circle cx="{size//2}" cy="{size//2}" r="{size//2}" fill="{bg}"/>
  <text x="{size//2}" y="{size//2}" font-family="Arial,sans-serif" font-size="{size//3}" fill="{fg}" text-anchor="middle" dominant-baseline="middle" font-weight="bold">{initials}</text>
</svg>"""
    return svg

# Generate book covers
for slug, title, initials, genre in BOOKS:
    svg = make_cover_svg(slug, title, initials, genre)
    path = os.path.join(COVERS_DIR, f"{slug}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)

print(f"Generated {len(BOOKS)} book covers.")

# Generate avatars
AVATARS = [
    ("admin",      "AU",  ("#1E3A5F", "#60A5FA")),
    ("librarian",  "LP",  ("#064E3B", "#34D399")),
    ("rahul",      "RS",  ("#1E1B4B", "#818CF8")),
    ("anjali",     "AS",  ("#4A044E", "#E879F9")),
    ("vikram",     "VP",  ("#451A03", "#F59E0B")),
    ("default",    "U",   ("#0F172A", "#0EA5E9")),
]
for name, initials, colors in AVATARS:
    svg = make_avatar_svg(initials, colors)
    path = os.path.join(AVATARS_DIR, f"{name}.svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(svg)

print(f"Generated {len(AVATARS)} avatars.")
print("All images generated successfully.")
