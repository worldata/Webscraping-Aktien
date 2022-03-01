import requests
from bs4 import BeautifulSoup as bs
from datetime import datetime
import pickle

ID_Liste = []
Aktienname_Liste = []
aktueller_Preis_Liste = []
WKN_Liste = []
ISIN_Liste = []


pickle_in = open(r"C:\Users\Max\Desktop\Aktien\aktien_db", "rb")
maindf = pickle.load(pickle_in)

datum_now = datetime.now().strftime("%d.%m.%Y")

aktien_liste = [
    "merck-aktie",
    "bayer-aktie",
    "allianz-aktie",
    "basf-aktie",
    "apple-aktie",
    "microsoft-aktie",
    "cloudflare-aktie",
    "crowdstrike-aktie",
    "sayona_mining-aktie",
    "amazon-aktie",
    "deutsche_telekom-aktie",
    "the_madison_square_garden-aktie",
    "volkswagen_vz-aktie",
    "taiwan_semiconductor_manufacturing-aktie",
    "coinbase-aktie",
    "canopy_growth-aktie",
    "amd-aktie",
    "air_canada_voting_and_variable_voting-aktie",
    "Alibaba-Aktie",
    "Boeing-Aktie",
    "munich_re-aktie",
    "mutares-aktie",
    "nio-aktie",
    "Palantir-Aktie",
    "Paypal-Aktie",
    "Visa-Aktie",
    "Xiaomi-Aktie",
    "nel-aktie",
    "SAP-Aktie",
]
etfs = [
    "https://www.onvista.de/etf/iShares-Global-Clean-Energy-ETF-IE00B1XNHC34",
    "https://www.onvista.de/etf/XTRACKERS-MSCI-AC-WORLD-UCITS-ETF-1C-EUR-ACC-ETF-IE00BGHQ0G80",
    "https://www.onvista.de/etf/ISHARES-DIGITAL-SECURITY-UCITS-ETF-USD-ACC-ETF-IE00BG0J4C88",
]


def getdata_etf(url):
    url = url
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    preis = soup.find("data", {"class": "text-nowrap"}).text
    name = soup.find(
        "h1",
        {"class": "headline"},
    ).text

    WKN_und_ISIN = soup.findAll("div", {"class": "text-size--small"})[2].text.split("·")
    WKN = WKN_und_ISIN[0].split("xa0")[0].split("xa0")[0]
    WKN_final = WKN.split("WKN:\xa0")[1]
    ISIN_final = WKN_und_ISIN[1].split("ISIN:")[1]

    WKN_Liste.append(WKN_final)
    ISIN_Liste.append(ISIN_final)

    return name + ": " + preis[0:-3]


def getdata(tag):
    url = f"https://www.finanzen.net/aktien/{tag}"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    preis = soup.find(
        "div", {"class": "col-xs-5 col-sm-4 text-sm-right text-nowrap"}
    ).text
    name = soup.find("h1", {"class": "line-height-fix"}).text
    preisf = [x for x in preis[0:-3] if x]
    preisf.append(datum_now)

    wkn_isin = soup.find("span", {"class": "instrument-id"}).text.split("/")
    WKN = wkn_isin[0].split(" ")[1]
    ISIN = wkn_isin[1].split(" ")[2]

    WKN_Liste.append(WKN)
    ISIN_Liste.append(ISIN)

    return name + ": " + preis[0:-3]


def get_wkn_isin(tag):
    url = f"https://www.finanzen.net/aktien/{tag}"
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    wkn_isin = soup.find("span", {"class": "instrument-id"}).text.split("/")
    WKN = wkn_isin[0].split(" ")[1]
    ISIN = wkn_isin[1].split(" ")[2]
    return WKN, ISIN


def Listen_befüllen():
    for e in etfs:
        string = getdata_etf(e)
        Aktienname1 = str(string).split(":")[0]
        Aktienpreis = str(string).split(":")[1]
        Aktienpreis1 = Aktienpreis.replace(".", "")
        Aktienpreis2 = Aktienpreis1.replace(",", ".")
        Aktienpreis3 = float(Aktienpreis2)
        Aktienname_Liste.append(Aktienname1)
        aktueller_Preis_Liste.append(Aktienpreis3)

    for e in aktien_liste:
        print(e)
        string = getdata(e)
        Aktienname1 = str(string).split(":")[0]
        Aktienpreis = str(string).split(":")[1]
        Aktienpreis1 = Aktienpreis.replace(".", "")
        Aktienpreis2 = Aktienpreis1.replace(",", ".")
        Aktienpreis3 = float(Aktienpreis2)

        Aktienname_Liste.append(Aktienname1)
        aktueller_Preis_Liste.append(Aktienpreis3)


def Spalte_mit_Nummerbefüllen():
    for i in aktueller_Preis_Liste:
        counter = len(aktueller_Preis_Liste) + 1

    for i in range(1, counter):
        ID_Liste.append(i)


Listen_befüllen()
Spalte_mit_Nummerbefüllen()

maindf[str(datum_now)] = aktueller_Preis_Liste


pickle_out = open(r"C:\Users\Max\Desktop\Aktien\aktien_db", "wb")
pickle.dump(maindf, pickle_out)
pickle_out.close
