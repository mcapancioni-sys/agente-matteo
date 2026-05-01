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
    """Analisi dettagliata prezzi metalli ed energetici"""
    
    commodities = {
        '🪙 Oro': 'GC=F',
        '🥈 Argento': 'SI=F',
        '🔴 Rame': 'HG=F',
        '🛢️ Petrolio WTI': 'CL=F',
        '🔥 Petrolio Brent': 'BZ=F',
        '⛽ Gas Naturale': 'NG=F'
    }
    
    report = "📊 <b>RAPPORTO MATERIE PRIME - ANALISI COMPLETA</b>\n"
    report += f"📅 {datetime.now().strftime('%A %d %B %Y')}\n"
    report += "━" * 25 + "\n\n"
    
    soglie = {
        '🪙 Oro': {'min': 2300, 'max': 2450},
        '🔴 Rame': {'min': 4.20, 'max': 4.80},
        '🛢️ Petrolio WTI': {'min': 75, 'max': 90}
    }
    
    alert_messages = []
    
    for nome, simbolo in commodities.items():
        try:
            ticker = yf.Ticker(simbolo)
            
            # Scarichiamo diversi periodi
            hist_1gg = ticker.history(period='1d')
            hist_5gg = ticker.history(period='5d')
            hist_1m = ticker.history(period='1mo')
            hist_1y = ticker.history(period='1y')
            
            if len(hist_5gg) >= 2 and len(hist_1m) >= 2 and len(hist_1y) >= 2:
                prezzo = hist_5gg['Close'].iloc[-1]
                
                # Calcoli variazioni
                prezzo_ieri = hist_5gg['Close'].iloc[-2]
                var_giorno = ((prezzo - prezzo_ieri) / prezzo_ieri) * 100
                
                prezzo_settimana_fa = hist_5gg['Close'].iloc[0] if len(hist_5gg) >= 5 else prezzo
                var_settimana = ((prezzo - prezzo_settimana_fa) / prezzo_settimana_fa) * 100
                
                prezzo_mese_fa = hist_1m['Close'].iloc[0] if len(hist_1m) >= 20 else prezzo
                var_mese = ((prezzo - prezzo_mese_fa) / prezzo_mese_fa) * 100
                
                # Statistiche annuali
                max_annuale = hist_1y['High'].max()
                min_annuale = hist_1y['Low'].min()
                posizione_annuale = ((prezzo - min_annuale) / (max_annuale - min_annuale)) * 100
                
                # Volume
                volume_medio = hist_5gg['Volume'].mean()
                volume_oggi = hist_5gg['Volume'].iloc[-1]
                volume_ratio = (volume_oggi / volume_medio) * 100
                
                # Trend
                media_20gg = hist_1m['Close'].mean() if len(hist_1m) >= 20 else prezzo
                trend = "🟢 RIALZISTA" if prezzo > media_20gg else "🔴 RIBASSISTA"
                
                # Costruzione report per singola commodity
                report += f"<b>{nome}</b>\n"
                report += f"  💰 Prezzo: <b>${prezzo:.2f}</b>\n"
                report += f"\n  📈 <u>Variazioni:</u>\n"
                report += f"     Oggi: {f'🟢 +{var_giorno:+.2f}%' if var_giorno > 0 else f'🔴 {var_giorno:+.2f}%'}\n"
                report += f"     Settimana: {f'🟢 +{var_settimana:+.2f}%' if var_settimana > 0 else f'🔴 {var_settimana:+.2f}%'}\n"
                report += f"     Mese: {f'🟢 +{var_mese:+.2f}%' if var_mese > 0 else f'🔴 {var_mese:+.2f}%'}\n"
                report += f"\n  📊 <u>Range annuale:</u>\n"
                report += f"     Min: ${min_annuale:.2f}\n"
                report += f"     Max: ${max_annuale:.2f}\n"
                report += f"     Posizione: {posizione_annuale:.0f}% del range\n"
                report += f"\n  📊 <u>Volume scambi:</u>\n"
                report += f"     Oggi: {volume_oggi:,.0f}\n"
                report += f"     vs media: {f'🟢 +{volume_ratio:.0f}%' if volume_ratio > 100 else f'🔴 {volume_ratio:.0f}%'}\n"
                report += f"\n  📈 Trend 20gg: {trend}\n"
                report += "\n"
                
                # Alert personalizzati
                if nome in soglie:
                    if prezzo > soglie[nome]['max']:
                        alert_messages.append(f"⚠️ {nome} sopra soglia max: ${prezzo:.2f} > ${soglie[nome]['max']}")
                    elif prezzo < soglie[nome]['min']:
                        alert_messages.append(f"⚠️ {nome} sotto soglia min: ${prezzo:.2f} < ${soglie[nome]['min']}")
                        
        except Exception as e:
            report += f"<b>{nome}</b>\n  ❌ Dati non disponibili al momento\n\n"
    
    # Sezione alert
    if alert_messages:
        report += "━" * 25 + "\n"
        report += "🚨 <b>ALERT DI MERCATO</b>\n"
        for alert in alert_messages:
            report += f"  {alert}\n"
        report += "\n"
    
    report += "━" * 25 + "\n"
    report += "<i>📌 Analisi automatica. Soglie personalizzabili nel codice.</i>"
    
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
