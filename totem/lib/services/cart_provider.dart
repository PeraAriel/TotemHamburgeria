import 'package:flutter/material.dart';
import 'package:totem/models/cart_item.dart';

class CartProvider extends ChangeNotifier {
  final Map<int, CartItem> _items = {};

  Map<int, CartItem> get items => _items;

  double get totalPrice {
    return _items.values.fold(0, (sum, item) => sum + item.totalPrice);
  }

  int get itemCount {
    return _items.values.fold(0, (sum, item) => sum + item.quantity);
  }

  void addItem(int productId, String productName, double price) {
    if (_items.containsKey(productId)) {
      _items[productId]!.quantity++;
    } else {
      _items[productId] = CartItem(
        productId: productId,
        productName: productName,
        unitPrice: price,
      );
    }
    notifyListeners();
  }

  void removeItem(int productId) {
    _items.remove(productId);
    notifyListeners();
  }

  void updateQuantity(int productId, int quantity) {
    if (_items.containsKey(productId)) {
      if (quantity <= 0) {
        removeItem(productId);
      } else {
        _items[productId]!.quantity = quantity;
        notifyListeners();
      }
    }
  }

  void clear() {
    _items.clear();
    notifyListeners();
  }

  List<Map<String, dynamic>> getOrderItems() {
    return _items.values
        .map((item) => item.toJson())
        .toList();
  }
}
