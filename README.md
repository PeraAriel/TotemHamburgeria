# Totem Hamburgeria - Sistema Completo

Sistema integrato per una hamburgeria con totem cliente Flutter, pannello staff Angular e backend Flask.

## 📋 Struttura del Progetto

```
TotemHamburgeria/
├── api/                    # Backend Flask (API REST)
├── backend/               # Frontend Angular (Pannello Staff)
└── totem/                # App Flutter (Totem Cliente)
```

## 🏗️ Componenti

### 1. **API Backend (Flask)** - `/api`
REST API che gestisce:
- 📁 Categorie di prodotti
- 🍔 Prodotti del menù
- 📦 Ordini e loro stato

**Stack**: Python, Flask, PyMySQL, MySQL Aiven

**Features**:
- DatabaseWrapper per gestire tutte le query
- CORS abilitato
- Gestione errori robusta
- Dati di esempio

### 2. **Pannello Staff (Angular SPA)** - `/backend`
Interfaccia web per lo staff della hamburgeria.

**Stack**: Angular 19, TypeScript, Standalone Components, RxJS

**Features**:
- 📋 Dashboard con tab Ordini e Menù
- 🔄 Aggiornamento ordini in tempo reale (ogni 5 secondi)
- 👀 Gestione visuale dello stato degli ordini
- 🍔 Gestione completa del menù

### 3. **Totem Cliente (Flutter)** - `/totem`
Applicazione mobile/web per i clienti

**Stack**: Flutter, Dart, Provider

**Features**:
- 🏠 Home con visualizzazione prodotti
- 🔍 Filtro per categoria
- 🛒 Carrello persistente
- ✅ Invio ordini all'API
- 💰 Calcolo automatico del totale

## 🚀 Setup Rapido

### Prerequisiti
- Python 3.8+
- Node.js 18+
- Flutter 3.11+
- MySQL database (MySQL Aiven consigliato)

### 1. Backend Flask (Porta 5000)

```bash
cd api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Modificare i parametri di connessione
python app.py
```

### 2. Pannello Staff Angular (Porta 4200)

```bash
cd backend
npm install
npm start
```

### 3. Totem Flutter

```bash
cd totem
flutter pub get
flutter run
```

## 📝 Configurazione

### URL API
Aggiornare gli URL nelle vostre applicazioni:

**Flutter** (`totem/lib/services/api_service.dart`):
```dart
static const String baseUrl = 'http://localhost:5000/api';
```

**Angular** (`backend/src/app/services/api.service.ts`):
```typescript
private baseUrl = 'http://localhost:5000/api';
```

## 📚 Documentazione Dettagliata

- [Backend Flask](./api/README.md) - API REST e Database
- [Pannello Staff Angular](./backend/README.md) - Gestione menù e ordini
- [Totem Flutter](./totem/README.md) - App cliente

## 🔄 Flusso di Comunicazione

```
Cliente (Flutter) → API Flask → Database MySQL
                      ↓
                 Staff (Angular)
```

## 📄 Licenza

Progetto per uso interno hamburgeria.

---

**Creato**: Febbraio 2026
**Componenti**: Flask, Angular, Flutter
**Database**: MySQL Aiven