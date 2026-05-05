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

def analisi_materie_prime():
    """Analisi tecnica giornaliera - confronto con ieri e medie brevi"""
    
    commodities = {
        '🪙 Oro': 'GC=F',
        '🥈 Argento': 'SI=F',
        '🔴 Rame': 'HG=F',
        '🛢️ Petrolio WTI': 'CL=F',
        '🔥 Petrolio Brent': 'BZ=F',
        '⛽ Gas Naturale': 'NG=F'
    }
    
    report = "📊 <b>RAPPORTO MATERIE PRIME - ANALISI GIORNALIERA</b>\n"
    report += f"📅 {datetime.now().strftime('%A %d %B %Y')}\n"
    report += "━" * 25 + "\n\n"
    
    for nome, simbolo in commodities.items():
        try:
            ticker = yf.Ticker(simbolo)
            hist = ticker.history(period='15d')
            
            if len(hist) >= 2:
                prezzo_oggi = hist['Close'].iloc[-1]
                prezzo_ieri = hist['Close'].iloc[-2]
                var_giorno = ((prezzo_oggi - prezzo_ieri) / prezzo_ieri) * 100
                
                # Medie mobili semplici a 5 e 10 giorni
                sma_5 = hist['Close'].tail(5).mean()
                sma_10 = hist['Close'].tail(10).mean() if len(hist) >= 10 else prezzo_oggi
                
                # Segnali tecnici
                sopra_sma5 = "✅ SOPRA" if prezzo_oggi > sma_5 else "❌ SOTTO"
                sopra_sma10 = "✅ SOPRA" if prezzo_oggi > sma_10 else "❌ SOTTO"
                
                # Trend a breve termine
                if prezzo_oggi > sma_5 > sma_10:
                    trend = "🟢 FORTEMENTE RIALZISTA"
                elif prezzo_oggi > sma_5:
                    trend = "🟡 LEGGERMENTE RIALZISTA"
                elif prezzo_oggi < sma_5 < sma_10:
                    trend = "🔴 FORTEMENTE RIBASSISTA"
                else:
                    trend = "🟠 LATERALE / INCERTO"
                
                # Massimi e minimi ultimi 5 giorni
                max_5gg = hist['High'].tail(5).max()
                min_5gg = hist['Low'].tail(5).min()
                posizione_5gg = ((prezzo_oggi - min_5gg) / (max_5gg - min_5gg)) * 100
                
                # Costruzione report
                report += f"<b>{nome}</b>\n"
                report += f"  💰 <b>${prezzo_oggi:.2f}</b>\n"
                report += f"  📉 Variazione oggi: {f'🟢 +{var_giorno:+.2f}%' if var_giorno > 0 else f'🔴 {var_giorno:+.2f}%'}\n\n"
                
                report += f"  📊 Medie mobili:\n"
                report += f"     SMA 5gg: ${sma_5:.2f} → {sopra_sma5}\n"
                report += f"     SMA 10gg: ${sma_10:.2f} → {sopra_sma10}\n\n"
                
                report += f"  📈 Range ultimi 5gg:\n"
                report += f"     Min: ${min_5gg:.2f} | Max: ${max_5gg:.2f}\n"
                report += f"     Posizione: {posizione_5gg:.0f}% del range\n\n"
                
                report += f"  🧭 Trend: {trend}\n\n"
                
        except Exception:
            report += f"<b>{nome}</b>\n  ❌ Dati non disponibili\n\n"
    
    report += "━" * 25 + "\n"
    report += "<i>📌 SMA = Media Mobile Semplice. Più il prezzo è sopra le medie, più il trend è rialzista.</i>"
    
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
    #
