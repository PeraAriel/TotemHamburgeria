import 'package:http/http.dart' as http;
import 'dart:convert';
import 'package:totem/models/category.dart';
import 'package:totem/models/product.dart';

class ApiService {
  // Configurare questo URL secondo il vostro setup
  static const String baseUrl = 'https://automatic-happiness-q7vq7767q66r24g97-5000.app.github.dev/api';
  static const Duration timeout = Duration(seconds: 10);

  // === CATEGORIE ===
  static Future<List<Category>> getCategories() async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/categories'))
          .timeout(timeout);

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((item) => Category.fromJson(item)).toList();
      } else {
        throw Exception('Errore nel caricamento categorie: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Errore di connessione: $e');
    }
  }

  // === PRODOTTI ===
  static Future<List<Product>> getProducts() async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/products'))
          .timeout(timeout);

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((item) => Product.fromJson(item)).toList();
      } else {
        throw Exception('Errore nel caricamento prodotti: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Errore di connessione: $e');
    }
  }

  static Future<List<Product>> getProductsByCategory(int categoryId) async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/products/category/$categoryId'))
          .timeout(timeout);

      if (response.statusCode == 200) {
        final List<dynamic> data = json.decode(response.body);
        return data.map((item) => Product.fromJson(item)).toList();
      } else {
        throw Exception('Errore nel caricamento prodotti: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Errore di connessione: $e');
    }
  }

  // === ORDINI ===
  static Future<int> createOrder(List<Map<String, dynamic>> items, double totalPrice) async {
    try {
      final response = await http
          .post(
            Uri.parse('$baseUrl/orders'),
            headers: {'Content-Type': 'application/json'},
            body: json.encode({
              'items': items,
              'total_price': totalPrice,
            }),
          )
          .timeout(timeout);

      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        return data['id'];
      } else {
        throw Exception('Errore nella creazione ordine: ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('Errore di connessione: $e');
    }
  }

  static Future<bool> healthCheck() async {
    try {
      final response = await http
          .get(Uri.parse('$baseUrl/health'))
          .timeout(Duration(seconds: 5));
      return response.statusCode == 200;
    } catch (e) {
      return false;
    }
  }
}
