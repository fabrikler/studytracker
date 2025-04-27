# 🐍 Study Tracker App

Ein persönlicher Tracker für meine Python-Lerneinheiten, gebaut mit Streamlit.
Mit dieser kleinen Web-App kann ich meine Lernzeiten erfassen, Themenbereiche dokumentieren und meinen Fortschritt visuell nachverfolgen.
Geplant ist, den Tracker in einem weiteren Update um zusätzliche Funktionen wie Auswertungen, Statistik und unterschiedliche Datenformate zu erweitern.

## Features
- 📅 Kalender-Heatmap der Lerneinheiten
- ➕ Sessions hinzufügen (mit Kategorie und Kommentar)
- 🔒 Passwortschutz für das Eintragen und Löschen
- 📊 Zusammenfassung der Lernzeit nach Kategorie

## Benutzung
- Sessions eintragen mit Passwort
- Sessions löschen mit Passwort
- Übersicht der bisherigen Sessions und Lernzeit

## Deployment
Diese App läuft auf [Streamlit Cloud](https://streamlit.io/cloud) und nutzt [Streamlit Secrets](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management) für sichere Passwörter.

## Lokales Setup

Um die App lokal zu nutzen musst du folgendes beachten:

1. `pip install -r requirements.txt`
2. `.streamlit/secrets.toml` Datei erstellen für lokale Tests
3. `streamlit run app.py`

## 🔒 Passwort / Secrets Management

Die App verwendet ein Passwortschutz-System für das Speichern und Löschen von Sessions.

Damit die App funktioniert, muss ein Secret `tracker_password` gesetzt werden.

### Deployment auf Streamlit Cloud

- Gehe in die **App Settings → Secrets**.
- Trage folgendes ein:

```toml
[general]
tracker_password = "dein_passwort"
```

Mehr Informationen findest du in der offiziellen [Streamlit Secrets Dokumentation](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/secrets-management)

Viel Spass beim lernen 🤖

---

© 2025 Carlos Meyer 
