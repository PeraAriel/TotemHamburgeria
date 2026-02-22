# Totem Hamburgeria - App Cliente Flutter

Applicazione Flutter per il totem digitale cliente della hamburgeria.

## 🎯 Features

### 🏠 Home Screen
- Visualizzazione griglia prodotti dinamica
- Filtri per categoria
- Immagini prodotti con fallback
- Prezzo con formattazione locale
- Aggiunta rapida al carrello

### 🛒 Carrello
- Visualizzazione articoli aggiunti
- Modifica quantità (aumenta/diminuisci)
- Eliminazione articoli
- Calcolo automatico totale
- Riepilogo ordine

### ✅ Invio Ordine
- Generazione numero ordine automatico
- Validazione carrello
- Feedback di successo/errore
- Pulizia automatica carrello dopo invio

## 🛠️ Stack Tecnologico

- **Flutter 3.11+**: Framework principale
- **Dart**: Linguaggio
- **Provider**: Gestione stato
- **HTTP**: Comunicazione API REST
- **Intl**: Formattazione valute e date
- **Material Design**: UI components

## 🚀 Setup

### Prerequisiti
- Flutter SDK 3.11+
- Dart 3.5+
- Dispositivo o emulatore
- Backend Flask in esecuzione

### Installazione

```bash
cd totem

# Ottenere dipendenze
flutter pub get

# Avviare l'app
flutter run

# Per web (Chrome)
flutter run -d chrome

# Per build APK
flutter build apk

# Per build iOS
flutter build ios
```

## 📁 Struttura Progetto

```
lib/
├── main.dart                 # Entry point
├── models/
│   ├── category.dart
│   ├── product.dart
│   └── cart_item.dart
├── services/
│   ├── api_service.dart      # Comunicazione con API
│   └── cart_provider.dart    # Gestione stato carrello
└── screens/
    ├── home_screen.dart      # Home e menù
    └── cart_screen.dart      # Carrello e checkout
```

## 🔧 Configurazione

### URL API
Modificare in `lib/services/api_service.dart`:

```dart
static const String baseUrl = 'http://localhost:5000/api';
```

Per **dispositivi fisici Android**, usare l'IP locale:
```dart
static const String baseUrl = 'http://192.168.1.X:5000/api';
```

## 📱 Schermate

### Home Screen
- Top: AppBar con logo e counter carrello
- Middle: Filtri categoria (orizzontali scrollable)
- Bottom: Griglia 2x prodotti
  - Immagine
  - Nome e descrizione
  - Prezzo
  - Pulsante aggiungi

### Cart Screen
- Lista articoli con:
  - Quantità (+/-)
  - Prezzo unitario
  - Pulsante elimina
- Footer:
  - Totale articoli
  - Prezzo totale
  - Pulsanti: Continua / Invia Ordine

### Conferma Ordine
- Dialog con numero ordine
- Messaggio di success
- Tasto OK per tornare

## 🎨 Tema e Stili

- **Tema Primario**: Deep Orange (#FF5722)
- **Accenti**: Orange (#FF7043)
- **Background**: Grigio chiaro (#F5F5F5)
- **Testo**: Gray-900 (#212121)

### Material 3
- Rounded corners
- Elevazioni moderne
- Animazioni fluide
- Responsive design

## 🔄 Gestione Stato

Utilizziamo **Provider** per:
- Gestione carrello (CartProvider)
- Aggiornamento UI reattivo
- Persistenza ordini in memoria

```dart
// Accesso al carrello
final cart = Provider.of<CartProvider>(context);

// Aggiungere prodotto
cart.addItem(productId, productName, price);

// Ottenere totale
print(cart.totalPrice);
```

## 📡 API Communication

### Endpoints Utilizzati

**Produtti**:
```
GET /api/products              → Carica menù
GET /api/products/category/<id> → Prodotti categoria
```

**Ordini**:
```
POST /api/orders               → Invia ordine
Body: {
  items: [{product_id, quantity, unit_price}],
  total_price: X.XX
}
```

## ⚠️ Gestione Errori

- Try-catch su tutte le richieste API
- SnackBar per errori utente
- Reload button su schermate di errore
- Timeout di 10 secondi

## 📱 Requisiti Dispositivo

- **Android**: 5.0+ (API 21+)
- **iOS**: 12.0+
- **Schermo minimo**: 320x568 (responsivo)
- **Ideale**: 1024x768 (tablet/kiosk)

## 🔒 Sicurezza

- Nessun dato critico in memoria
- HTTP solo per localhost/LAN (dev)
- Validazione input sul client
- User-agent Flutter

## 🐛 Debug

### Hot Reload
```bash
# Durante flutter run, pressare 'r'
# Per full restart, pressare 'R'
```

### Log
```bash
flutter logs
```

### Errori Comuni
- "Connection refused" → Backend non avviato
- "CORS error" → Verificare CORS in Flask
- "Image not loading" → URL immagine non valido

## 📚 Dipendenze

```yaml
dependencies:
  flutter: sdk: flutter
  http: ^1.1.0
  provider: ^6.0.0
  intl: ^0.19.0
  cupertino_icons: ^1.0.8
```

## 🧪 Testing

```bash
# Run tests
flutter test

# Coverage
flutter test --coverage
```

## 🚀 Build e Deploy

### APK
```bash
flutter build apk --release
# Output: build/app/outputs/flutter-app.apk
```

### iOS
```bash
flutter build ios --release
# Output: build/ios/iphoneos/Runner.app
```

### Web
```bash
flutter run -d chrome
# Per build web
flutter build web
```

## 📝 Best Practices

1. **Immagini**: Usare CDN per immagini prodotti
2. **Performance**: Lazy load ai prodotti per scroll veloce
3. **UX**: Loading indicators durante fetch
4. **Testing**: Test su dispositivi reali/emulatori
5. **Monitoraggio**: Loggare errori API

## 📞 Troubleshooting

### "Failed to connect to API"
- Verificare URL baseUrl
- Controllare firewall
- Pinge backend: `ping localhost:5000`

### Immagini non visibili
- Verificare URL immagini in database
- Controllare permessi rete
- Testare URL in browser

### Carrello non aggiorna
- Verificare CartProvider sia fornito correttamente
- Check console per errori
- Riavviare hot reload

## 📄 Licenza

Progetto per uso interno hamburgeria.

---

**Creato**: Febbraio 2026
**Framework**: Flutter 3.11+
**Piattaforme**: Android, iOS, Web

- [Learn Flutter](https://docs.flutter.dev/get-started/learn-flutter)
- [Write your first Flutter app](https://docs.flutter.dev/get-started/codelab)
- [Flutter learning resources](https://docs.flutter.dev/reference/learning-resources)

For help getting started with Flutter development, view the
[online documentation](https://docs.flutter.dev/), which offers tutorials,
samples, guidance on mobile development, and a full API reference.
