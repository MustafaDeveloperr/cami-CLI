#!/usr/bin/env python3
import sys
import requests
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

# Varsayılan şehir
DEFAULT_CITY = "Mardin"
DISPLAY_NAME = "KIZILTEPE / MARDİN"

def get_free_prayer_times(city):
    # Aladhan API üzerinden doğrudan il sorgusu atıyoruz
    url = f"https://api.aladhan.com/v1/timingsByCity?city={city}&country=Turkey&method=13"
    
    try:
        res = requests.get(url, timeout=5)
        if res.status_code == 200:
            data = res.json()["data"]["timings"]
            date_info = res.json()["data"]["date"]["readable"]
            return data, date_info
        else:
            return None, None
    except Exception:
        return None, None

def main():
    # Terminalden özel bir şehir girilirse onu al, girilmezse varsayılan Mardin
    if len(sys.argv) > 1:
        city = sys.argv[1]
        title_name = city.upper()
    else:
        city = DEFAULT_CITY
        title_name = DISPLAY_NAME

    console = Console()

    with console.status(f"[bold green]{title_name} için namaz vakitleri çekiliyor...[/bold green]"):
        timings, date_info = get_free_prayer_times(city)

    if not timings:
        console.print(f"[bold red]Hata:[/bold red] '{title_name}' için vakitler alınamadı. İnternet bağlantını veya şehir adını kontrol et.")
        return

    # Vakit isimleri ve Türkçe karşılıkları
    vakitler = {
        "Fajr": ("İmsak", timings.get("Fajr")),
        "Sunrise": ("Güneş", timings.get("Sunrise")),
        "Dhuhr": ("Öğle", timings.get("Dhuhr")),
        "Asr": ("İkindi", timings.get("Asr")),
        "Maghrib": ("Akşam", timings.get("Maghrib")),
        "Isha": ("Yatsı", timings.get("Isha"))
    }

    # Tablo Tasarımı
    table = Table(title=f"🕌 {title_name} NAMAZ VAKİTLERİ 🕌", title_style="bold cyan", show_header=True, header_style="bold magenta")
    table.add_column("Vakit", justify="center", style="bold yellow")
    table.add_column("Saat", justify="center", style="bold green")

    for key, (tr_name, time_val) in vakitler.items():
        table.add_row(tr_name, time_val)

    # Ekrana Şık Panel İçinde Basma
    console.print()
    console.print(Panel(table, subtitle=f"Tarih: {date_info}", expand=False, border_style="blue"))
    console.print()

if __name__ == "__main__":
    main()