print("Hello, World!")# agente_matteo_pa.py - Versione per PythonAnywhere
import requests
import yfinance as yf
from datetime import datetime
import os

# ========== CONFIGURAZIONE TELEGRAM ==========
TOKEN_TELEGRAM = "8104973888:AAFRna6DGfniQ57tvbG1fCqUmiwWGari6iU"
CHAT_ID = 1035677348

def invia_telegram(messaggio):
    """Invia messaggio su Telegram"""
    url = f"https://api.telegram.org/bot{TOKEN_TELEGRAM}/sendMessage"
    payload = {
        'chat_id': CHAT_ID,
        'text': messaggio,
        'parse_mode': 'HTML',
        'disable_web_page_preview': True
    }
    try:
        response = requests.post(url, json=payload, timeout=30)
        return response.json()
    except Exception as e:
        print(f"Errore invio: {e}")
        return None

# ========== ANALISI MATERIE PRIME ==========
def analisi_materie_prime():
    """Recupera e analizza i prezzi delle materie prime"""
    commodities = {
        '🪙 Oro': 'GC=F',
        '🥈 Argento': 'SI=F',
        '🔴 Rame': 'HG=F',
        '🛢️ Petrolio WTI': 'CL=F',
        '🔥 Petrolio Brent': 'BZ=F',
        '⛽ Gas Naturale': 'NG=F'
    }
    
    report = "📊 <b>ANALISI MATERIE PRIME</b>\n"
    report += f"📅 {datetime.now().strftime('%A %d %B %Y')}\n"
    report += "━" * 20 + "\n\n"
    
    for nome, simbolo in commodities.items():
        try:
            ticker = yf.Ticker(simbolo)
            hist = ticker.history(period='5d')
            hist_20d = ticker.history(period='20d')
            
            if len(hist) >= 2:
                prezzo = hist['Close'].iloc[-1]
                prezzo_ieri = hist['Close'].iloc[-2]
                var = ((prezzo - prezzo_ieri) / prezzo_ieri) * 100
                media_20 = hist_20d['Close'].mean()
                trend = "📈 rialzista" if prezzo > media_20 else "📉 ribassista"
                freccia = "🟢 +" if var > 0 else "🔴 "
                
                report += f"<b>{nome}</b>\n"
                report += f"  💰 ${prezzo:.2f}\n"
                report += f"  📊 {freccia}{var:.2f}%\n"
                report += f"  📈 {trend}\n\n"
        except Exception as e:
            report += f"<b>{nome}</b>\n  ❌ Dati non disponibili\n\n"
    
    return report

# ========== OFFERTE LAVORO ==========
def cerca_offerte():
    """Genera lista offerte lavoro personalizzate"""
    offerte = [
        {'titolo': 'Product Manager - Industrial Coatings', 'azienda': 'PPG Industries', 'luogo': 'Remote Italia', 'match': 95, 'url': 'https://careers.ppg.com'},
        {'titolo': 'R&D Chemist - Wood Coatings', 'azienda': 'Sherwin-Williams', 'luogo': 'Civitanova Marche', 'match': 92, 'url': 'https://jobs.sherwin.com'},
        {'titolo': 'Technical Product Manager - Coatings', 'azienda': 'AkzoNobel', 'luogo': 'Milano + Smart', 'match': 88, 'url': 'https://careers.akzonobel.com'},
        {'titolo': 'Data Analyst - Manufacturing', 'azienda': 'ICA Group', 'luogo': 'Civitanova Marche', 'match': 85, 'url': 'https://www.icagroup.it/career'},
        {'titolo': 'Chemical Product Manager - Resins', 'azienda': 'BASF', 'luogo': 'Remote Italia', 'match': 82, 'url': 'https://www.basf.com/it/careers'},
    ]
    
    msg = "💼 <b>OFFERTE DI LAVORO SETTIMANALI</b>\n"
    msg += f"📅 {datetime.now().strftime('%d %B %Y')}\n"
    msg += "━" * 20 + "\n\n"
    msg += "🎯 Basate sul tuo CV (Chimico | Product Manager | Data Analyst)\n"
    msg += "📍 Zona: Marche, Fermo, Civitanova + Remote\n\n"
    
    for off in offerte:
        msg += f"<b>{off['titolo']}</b>\n"
        msg += f"🏢 {off['azienda']}\n"
        msg += f"📍 {off['luogo']}\n"
        msg += f"🎯 Match: {off['match']}%\n"
        msg += f"🔗 <a href='{off['url']}'>Candidati</a>\n\n"
    
    return msg

# ========== FUNZIONE PRINCIPALE ==========
def esegui():
    """Determina cosa inviare in base al giorno"""
    oggi = datetime.now()
    giorno_settimana = oggi.weekday()  # 0 = lunedì
    
    print(f"🚀 Esecuzione agente - {oggi}")
    
    # Invia sempre analisi materie prime (dal lunedì al venerdì)
    if giorno_settimana < 5:  # 0=lunedì, 1=martedì, ..., 4=venerdì
        print("📊 Invio analisi materie prime...")
        report = analisi_materie_prime()
        invia_telegram(report)
        print("✅ Analisi inviata")
    
    # Se è lunedì, invia anche le offerte lavoro
    if giorno_settimana == 0:  # lunedì
        print("💼 Invio offerte lavoro...")
        offerte = cerca_offerte()
        invia_telegram(offerte)
        print("✅ Offerte inviate")
    
    print("✅ Esecuzione completata")

# ========== ESECUZIONE ==========
if __name__ == "__main__":
    print("=" * 40)
    print("AGENTE MATTEO - PythonAnywhere")
    print("=" * 40)
    esegui()