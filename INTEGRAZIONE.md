# 🚀 Guida di Integrazione e Deploy - Totem Hamburgeria

Guida completa per integrare, testare e avviare il sistema completo.

## ⚙️ Prerequisiti Globali

- Python 3.8+
- Node.js 18+
- Flutter 3.11+
- MySQL 5.7+ (MySQL Aiven consigliato)
- 4 terminali aperti (uno per ogni componente)

## 📋 Checklist Setup

### 1️⃣ Database MySQL

#### Su MySQL Aiven o locale:

```bash
# Connettersi a MySQL
mysql -h HOST -u USER -p

# Eseguire lo script di inizializzazione
source /path/to/api/init_db.sql

# Verificare le tabelle create
SHOW TABLES IN hamburgeria;
```

#### Tabelle create:
- `categories` (4 categorie di esempio)
- `products` (10 prodotti di esempio)
- `orders` (vuota, pronta per ordini)
- `order_items` (vuota, articoli ordini)

---

## 🏗️ COMPONENTE 1: Backend Flask (Porta 5000)

### Setup

```bash
cd api

# Creare ambiente virtuale
python3 -m venv venv

# Attivare ambiente
source venv/bin/activate
# Windows: venv\Scripts\activate

# Installare dipendenze
pip install -r requirements.txt

# Configurare .env
cp .env.example .env
```

### Configurare `.env`

Modificare `/api/.env`:
```env
# MySQL Aiven
DB_HOST=pg-XXXXX-XXXXX.aivencloud.com
DB_USER=avnadmin
DB_PASSWORD=your-password
DB_NAME=hamburgeria
DB_PORT=3306

# Flask
SECRET_KEY=your-secret-key
DEBUG=False
```

### Avviare

```bash
python app.py
```

### ✅ Verificare

```bash
curl http://localhost:5000/api/health
# Risposta: {"status":"ok"}

curl http://localhost:5000/api/categories
# Risposta: [categorie...]
```

---

## 🌐 COMPONENTE 2: Pannello Staff Angular (Porta 4200)

### Setup

```bash
cd backend

# Installare dipendenze globali (se non presente)
npm install -g @angular/cli

# Installare dipendenze locali
npm install
```

### Configurare URL API

Modificare `/backend/src/app/services/api.service.ts`:
```typescript
private baseUrl = 'http://localhost:5000/api';
```

### Avviare

```bash
npm start
# o
ng serve
```

### ✅ Verificare

- Aprire browser su http://localhost:4200
- Dovrebbe visualizzare dashboard rossa
- Tab "Ordini" dovrebbe essere vuoto (nessun ordine)
- Tab "Menù" dovrebbe mostrare 10 prodotti di esempio

---

## 📱 COMPONENTE 3: Totem Flutter

### Setup Android/iOS Emulator

```bash
cd totem

# Installare dipendenze
flutter pub get

# Verificare setup
flutter doctor
```

### Configurare URL API

Modificare `/totem/lib/services/api_service.dart`:

**Per emulatore locale**:
```dart
static const String baseUrl = 'http://localhost:5000/api';
```

**Per dispositivo Android fisico**:
```dart
// Trovare IP locale della macchina
static const String baseUrl = 'http://192.168.1.100:5000/api';
```

### Avviare

```bash
# Su emulatore Android
flutter run

# Su Chrome
flutter run -d chrome

# Su dispositivo fisico
flutter run
```

### ✅ Verificare

- Dovrebbe caricare il menù
- Visualizzare 10 prodotti in griglia
- Mostrare categorie come filtri
- Carrello dovrebbe essere vuoto (counter = 0)

---

## 🔄 TEST DI INTEGRAZIONE COMPLETA

### Flusso Cliente → Backend → Staff

#### Passo 1: Cliente aggiunge prodotto al carrello
- Aprire app Flutter
- Cliccare su un prodotto (es. "Hamburger Classico")
- Verificare: Counter carrello passa da 0 a 1

#### Passo 2: Cliente completa il carrello
- Aggiungere 2-3 prodotti diversi
- Counter dovrebbe mostrare 3+

#### Passo 3: Cliente invia ordine
- Cliccare carrello (icona shopping_cart)
- Cliccare "Invia Ordine"
- Dovrebbe apparire numero ordine (#1 o successivo)

#### Passo 4: Staff visualizza ordine
- Aprire Angular Dashboard (http://localhost:4200)
- Andare a tab "Ordini"
- Dovrebbe visualizzare il nuovo ordine
- Mostrare articoli, prezzo totale, stato "pending"

#### Passo 5: Staff aggiorna stato
- Nel dashboard, trovare ordine
- Cambiare stato da "In Attesa" a "In Preparazione"
- Verificare cambio colore bordo ordine (allo stato corrispondente)

#### Passo 6: Cliente verifica (opzionale)
- Tornare a Flutter
- Dovrebbe ancora mostrare carrello vuoto (ordine inviato)

---

## 📊 TEST DEL MENÙ

### Aggiungere Categoria

1. Aprire Angular Dashboard
2. Tab "Menù"
3. Cliccare "+ Nuova Categoria"
4. Compilare form:
   - Nome: "Snack"
   - Descrizione: "Snack rapidi"
5. Cliccare "Salva"
6. **Verificare**: Categoria appare in lista

### Aggiungere Prodotto

1. In Menu Component, selezionare categoria
2. Cliccare "+ Nuovo Prodotto"
3. Compilare:
   - Nome: "Patatine Piccole"
   - Prezzo: 3.50
   - Categoria: Snack
   - Descrizione: "Porzione piccola"
4. Salva
5. **Verificare**: 
   - Prodotto appare in Angular
   - Ricare Flutter (hot reload)
   - Nuo prodotto visibile nel totem

### Modificare Prezzo

1. Nel menù, trovare un prodotto
2. Cliccare "Modifica"
3. Cambiare prezzo
4. Salvare
5. **Verificare**: Flutter aggiorna prezzo al reload

### Eliminare Prodotto

1. Cliccare "Elimina" su un prodotto
2. Confermare dialogo
3. **Verificare**: Producto scompare da entrambe le app

---

## 🔧 Troubleshooting

### Errore: "Connection refused" su Flutter

**Problema**: Flutter non raggiunge API

**Soluzione**:
```bash
# Controllare che Flask sia avviato
# Terminale 1: python app.py

# Controllare URL base URL in api_service.dart
# Usare http://localhost:5000/api per emulatore
# Usare http://IP_LOCALE:5000/api per dispositivo fisico
```

### Errore: CORS Error su Angular

**Problema**: Angular non riesce a raggiungere API

**Soluzione**:
```python
# Verificare che flask_cors sia caricato in app.py
from flask_cors import CORS
CORS(app)
```

### Database: Nessun dato

**Problema**: Tabelle vuote o non create

**Soluzione**:
```bash
# Eseguire di nuovo init_db.sql
mysql -h HOST -u USER -p < api/init_db.sql

# Verificare
mysql -h HOST -u USER -p -e "SELECT COUNT(*) FROM hamburgeria.products;"
```

### Hot Reload Flutter non funziona

**Problema**: Modifiche non applicate

**Soluzione**:
```bash
# Premere 'r' in terminale per hot reload
# Premere 'R' per full restart
# O riavviare flutter run
```

### Angular non carica componenti

**Problema**: Blank page

**Soluzione**:
```bash
# Controllare console browser (F12)
# Verificare che tutti i componenti siano importati
# Eseguire: npm install
# Riavviare: npm start
```

---

## 📝 URLs di Riferimento

| Componente | URL | Note |
|-----------|-----|------|
| Backend Flask | http://localhost:5000 | API REST su /api/* |
| Angular Dashboard | http://localhost:4200 | Staff panel |
| Flutter Emulator | - | Connesso a localhost:5000 |
| Flutter Web | http://localhost:3000 | Se avviato con flutter run -d chrome |
| MySQL | DB_HOST:3306 | Configurare in .env |

---

## 🚀 Deploy su Produzione

### Backend Flask

```bash
# Build
cd api
pip install gunicorn

# Avviare con Gunicorn (8 worker)
gunicorn -w 8 -b 0.0.0.0:5000 app:app

# Opzionale: usare supervisor/systemd per auto-restart
```

### Angular SPA

```bash
# Build ottimizzato
cd backend
npm run build

# Output in: dist/backend/
# Servire con Nginx/Apache
```

### Flutter

```bash
# Build APK
cd totem
flutter build apk --release

# Build iOS
flutter build ios --release

# Build Web
flutter build web
```

---

## 📊 Monitoraggio

### Log Flask

```bash
# Durante esecuzione, dovrebbe mostrare:
# GET /api/products
# GET /api/orders
# PUT /api/orders/1/status
# POST /api/orders (con dettagli nuovo ordine)
```

### Console Angular

Aprire DevTools (F12) per vedere:
- Richieste HTTP (Network tab)
- Errori console
- State dell'applicazione

### Log Flutter

```bash
flutter logs

# Dovrebbe mostrare:
# Connected API: true
# Loaded products: 10
# Order submitted: #1
```

---

## 🎯 Segnali di Successo

✅ Setup completato quando:

1. **Flask**: `curl http://localhost:5000/api/health` → {"status":"ok"}
2. **Angular**: Carica dashboard senza errori sul browser
3. **Flutter**: Mostra menù con prodotti dal database
4. **Integrazione**: Cliente invía ordine → Staff lo visualizza
5. **Menù**: Aggiunta prodotto su Angular → Visibile in Flutter dopo reload

---

## 📞 Prossimi Passi

1. **Test esteso**: Provare scenari di errore
2. **Performance**: Monitorare con load test
3. **UI Refinement**: Feedback da utenti
4. **Deployment**: Preparare ambiente di produzione
5. **Monitoring**: Setup logging centralizzato

---

**Data di Creazione**: Febbraio 2026
**Durata Total Setup**: ~30-45 minuti
**Team**: Dev, DBA, QA
