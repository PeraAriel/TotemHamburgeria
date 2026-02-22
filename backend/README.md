# Pannello Staff - Hamburgeria Angular SPA

Interfaccia web moderna e intuitiva per la gestione della hamburgeria in tempo reale.

## 🎯 Features

### 📋 Gestione Ordini
- **Visualizzazione in Tempo Reale**: Auto-refresh ordini ogni 5 secondi
- **Filtri per Stato**: pending, preparing, ready, completed, cancelled
- **Gestione Stato**: Dropdown per cambiare lo stato dell'ordine
- **Design Visivo**: Codice colore per ogni stato
- **Dettagli Ordine**: Numero, totale, articoli, orario creazione

### 🍔 Gestione Menù
- **Categorie**: Crea, modifica, elimina categorie di prodotti
- **Prodotti**: CRUD completo con validazione
- **Filtri**: Seleziona prodotti per categoria
- **Form Modali**: UI intuitiva per aggiunta/modifica

## 🛠️ Stack Tecnologico

- **Angular 19**: Framework principale
- **TypeScript**: Tipizzazione forte
- **Standalone Components**: Moderno e leggero
- **RxJS**: Gestione asincrona

## 🚀 Setup

```bash
# Installare dipendenze
npm install

# Avviare il server di sviluppo
npm start

# Build per produzione
npm run build

# Avviare i test
npm test
```

L'applicazione sarà disponibile su `http://localhost:4200`

## 📚 Documentazione Completa

Vedi [api/README.md](../api/README.md) per informazioni sul backend Flask e database.

```bash
ng e2e
```

Angular CLI does not come with an end-to-end testing framework by default. You can choose one that suits your needs.

## Additional Resources

For more information on using the Angular CLI, including detailed command references, visit the [Angular CLI Overview and Command Reference](https://angular.dev/tools/cli) page.
