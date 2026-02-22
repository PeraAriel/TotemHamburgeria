# Backend Flask - Hamburgeria API

API REST per gestire categorie di prodotti, prodotti e ordini della hamburgeria.

## Setup

### Prerequisiti
- Python 3.8+
- MySQL 5.7+

### Installazione

1. Creare un ambiente virtuale:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows
```

2. Installare le dipendenze:
```bash
pip install -r requirements.txt
```

3. Configurare il database:
- Creare un database MySQL
- Eseguire lo script: `init_db.sql`

4. Configurare le variabili d'ambiente:
```bash
cp .env.example .env
# Modificare .env con i vostri parametri
```

### Avvio

```bash
python app.py
```

L'API sarà disponibile su `http://localhost:5000`

## Endpoints API

### Categorie
- `GET /api/categories` - Recupera tutte le categorie
- `GET /api/categories/<id>` - Recupera una categoria
- `POST /api/categories` - Crea una nuova categoria
- `PUT /api/categories/<id>` - Aggiorna una categoria
- `DELETE /api/categories/<id>` - Elimina una categoria

### Prodotti
- `GET /api/products` - Recupera tutti i prodotti
- `GET /api/products/<id>` - Recupera un prodotto
- `GET /api/products/category/<category_id>` - Prodotti di una categoria
- `POST /api/products` - Crea un nuovo prodotto
- `PUT /api/products/<id>` - Aggiorna un prodotto
- `DELETE /api/products/<id>` - Elimina un prodotto

### Ordini
- `GET /api/orders` - Recupera tutti gli ordini
- `GET /api/orders/<id>` - Recupera un ordine
- `POST /api/orders` - Crea un nuovo ordine
- `PUT /api/orders/<id>/status` - Aggiorna lo stato di un ordine
- `DELETE /api/orders/<id>` - Elimina un ordine

## Struttura del Progetto

```
api/
├── app.py                 # Applicazione Flask principale
├── database_wrapper.py    # Wrapper per operazioni database
├── config.py             # Configurazione
├── init_db.sql           # Script di inizializzazione database
├── requirements.txt      # Dipendenze Python
├── .env.example          # Esempio file .env
└── routes/               # Cartella per future route modulari
```
