import streamlit as st
import pandas as pd
import os
import calplot
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

try:
    PASSWORD = st.secrets["tracker_password"]
except Exception:
    st.error("🚨 Passwort nicht gesetzt! Bitte in den Streamlit Secrets einrichten (Settings > Secrets).")
    st.stop()

# Datei Pfad
DATA_FILE = 'data.csv'

# Daten laden oder anlegen
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
    df['date'] = pd.to_datetime(df['date'], format='mixed')
    df['duration'] = pd.to_numeric(df['duration'], errors='coerce').fillna(0)
else:
    df = pd.DataFrame(columns=['date', 'duration', 'comment', 'category'])

st.title("🐍 Python Study Tracker")

# --------- Heatmap ---------
st.subheader("📅 Meine Sessions")

if not df.empty:
    df['date'] = pd.to_datetime(df['date'])
    session_counts = df.groupby('date')['duration'].sum()

    year = pd.to_datetime('today').year
    all_days = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31", freq='D')
    session_counts = session_counts.reindex(all_days, fill_value=0)

    session_counts.index = pd.to_datetime(session_counts.index)
    session_counts = session_counts.sort_index()

    df_calendar = pd.DataFrame({
        'date': session_counts.index,
        'dow': session_counts.index.weekday,   # Montag=0, Sonntag=6
        'week': session_counts.index.isocalendar().week,
        'month': session_counts.index.month,
        'duration': session_counts.values
    })

    df_calendar.loc[(df_calendar['date'].dt.month == 1) & (df_calendar['week'] > 50), 'week'] = 0
    df_calendar.loc[(df_calendar['date'].dt.month == 12) & (df_calendar['week'] == 1), 'week'] = df_calendar['week'].max() + 1

    # Richtig sortieren: Montag oben, Sonntag unten
    pivot = df_calendar.pivot(index='dow', columns='week', values='duration')
    pivot = pivot.reindex(index=[0,1,2,3,4,5,6])  # 0=Mo, 6=So

    fig, ax = plt.subplots(figsize=(22, 6))

    fig.patch.set_facecolor('#0e1117')
    ax.set_facecolor('#0e1117')

    colors = ['#0e1117', '#1b5e20', '#43a047', '#81c784']
    cmap = LinearSegmentedColormap.from_list("custom_green", colors)

    # Jetzt korrekt ohne origin='lower'
    c = ax.imshow(pivot, aspect='equal', cmap=cmap, vmin=0, vmax=max(1, session_counts.max()))

    # Y-Achse
    ax.set_yticks(range(7))
    ax.set_yticklabels(['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'], color='white', fontsize=12)
    ax.invert_yaxis()

    # Monatsnamen nur bei Monatsanfang
    months = df_calendar.groupby('week')['month'].first()
    last_month = None
    for week, month in months.items():
        if month != last_month:
            month_names = {1:'Jan', 2:'Feb', 3:'Mär', 4:'Apr', 5:'Mai', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Okt', 11:'Nov', 12:'Dez'}
            month_name = month_names.get(month, '')
            if month_name:
                ax.text(pivot.columns.get_loc(week), -1.5, month_name, ha='center', va='center', color='white', fontsize=13, fontweight='bold')
            last_month = month

    # Grid und Rahmen
    ax.set_xticks(np.arange(-0.5, len(pivot.columns), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, 7, 1), minor=True)
    ax.grid(which='minor', color='#444444', linestyle='-', linewidth=0.8)

    ax.plot([-0.5, len(pivot.columns)-0.5, len(pivot.columns)-0.5, -0.5, -0.5], 
            [-0.5, -0.5, 6.5, 6.5, -0.5], 
            color='#444444', linewidth=0.8)

    ax.set_xticks([])
    ax.spines[:].set_visible(False)
    ax.tick_params(which='minor', bottom=False, left=False)

    st.pyplot(fig)

else:
    st.info("Noch keine Sessions eingetragen!")


# --------- Neue Session ---------
st.subheader("➕ Neue Session eintragen")

with st.form("session_form"):
    date = st.date_input("Datum", pd.to_datetime('today'))
    duration = st.number_input("Dauer (in Minuten)", min_value=1, step=1)
    comment = st.text_input("Kommentar (optional)")
    category = st.selectbox("Kategorie", ["lesson", "homework", "project", "content"])
    password_input = st.text_input("🔒 Passwort zum Speichern", type="password")  # <-- NEU
    submitted = st.form_submit_button("Speichern")

    if submitted:
        if password_input == PASSWORD:
            new_data = pd.DataFrame({
                "date": [pd.to_datetime(date)],
                "duration": [duration],
                "comment": [comment],
                "category": [category]
            })
            df = pd.concat([df, new_data], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Session gespeichert!")
            st.rerun()
        else:
            st.error("❌ Falsches Passwort! Session wurde nicht gespeichert.")


# --------- Alle Sessions anzeigen und löschen ---------
st.subheader("📋 Meine Logs")

if not df.empty:
    # Saubere Tabelle vorbereiten
    df_display = df.copy()
    df_display['date'] = df_display['date'].dt.date
    df_display.index = range(1, len(df_display)+1)

    # Tabelle anzeigen
    st.dataframe(df_display)

    # Summary
    total_minutes = df['duration'].sum()
    st.markdown(f"**🧠 Gesamtzeit gelernt: {int(total_minutes)} Minuten**")

    # Zeit pro Kategorie berechnen
    category_summary = df.groupby('category')['duration'].sum().sort_values(ascending=False)

    # Schön anzeigen
    st.markdown("**📚 Zeit pro Kategorie:**")
    for category, minutes in category_summary.items():
        st.markdown(f"- **{category.capitalize()}**: {int(minutes)} Minuten")

    st.write("---")
    st.write("🔴 **Eintrag löschen**")


    # Dropdown-Auswahl vorbereiten
    options = [f"{i}. {row['date']} – {row['comment']} ({int(row['duration'])} min)" for i, row in df_display.iterrows()]
    selected = st.selectbox("Wähle einen Eintrag zum Löschen", options)

    password_delete = st.text_input("🔒 Passwort zum Löschen", type="password")
    
    if st.button("Löschen"):
        if password_delete == PASSWORD:
            selected_index = int(selected.split(".")[0]) - 1
            df = df.drop(df.index[selected_index])
            df.to_csv(DATA_FILE, index=False)
            st.success("✅ Eintrag gelöscht!")
            st.rerun()
        else:
            st.error("❌ Falsches Passwort! Eintrag wurde nicht gelöscht.")

            
