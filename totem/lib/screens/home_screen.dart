import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:intl/intl.dart';
import 'package:totem/models/product.dart';
import 'package:totem/services/api_service.dart';
import 'package:totem/services/cart_provider.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({Key? key}) : super(key: key);

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  int selectedCategoryId = 0;
  List<Product> products = [];
  bool isLoading = true;
  String errorMessage = '';

  @override
  void initState() {
    super.initState();
    _loadProducts();
  }

  Future<void> _loadProducts() async {
    try {
      setState(() {
        isLoading = true;
        errorMessage = '';
      });

      final loadedProducts = await ApiService.getProducts();
      setState(() {
        products = loadedProducts;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        errorMessage = 'Errore: ${e.toString()}';
        isLoading = false;
      });
    }
  }

  List<Product> get filteredProducts {
    if (selectedCategoryId == 0) {
      return products;
    }
    return products.where((p) => p.categoryId == selectedCategoryId).toList();
  }

  @override
  Widget build(BuildContext context) {
    final cartProvider = Provider.of<CartProvider>(context);
    final currencyFormat = NumberFormat.currency(locale: 'it_IT', symbol: '€');

    return Scaffold(
      backgroundColor: Colors.grey[100],
      appBar: AppBar(
        title: const Text('Totem Hamburgeria'),
        backgroundColor: Colors.deepOrange,
        elevation: 0,
        actions: [
          Stack(
            children: [
              IconButton(
                icon: const Icon(Icons.shopping_cart),
                onPressed: () {
                  Navigator.of(context).pushNamed('/cart');
                },
              ),
              if (cartProvider.itemCount > 0)
                Positioned(
                  right: 0,
                  top: 0,
                  child: Container(
                    decoration: BoxDecoration(
                      color: Colors.red,
                      borderRadius: BorderRadius.circular(10),
                    ),
                    constraints: const BoxConstraints(
                      minWidth: 20,
                      minHeight: 20,
                    ),
                    child: Center(
                      child: Text(
                        '${cartProvider.itemCount}',
                        style: const TextStyle(
                          color: Colors.white,
                          fontSize: 12,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                  ),
                ),
            ],
          ),
        ],
      ),
      body: isLoading
          ? Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  const CircularProgressIndicator(color: Colors.deepOrange),
                  const SizedBox(height: 16),
                  const Text('Caricamento menu...'),
                ],
              ),
            )
          : errorMessage.isNotEmpty
              ? Center(
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      const Icon(Icons.error_outline, color: Colors.red, size: 48),
                      const SizedBox(height: 16),
                      Text(errorMessage),
                      const SizedBox(height: 16),
                      ElevatedButton(
                        onPressed: _loadProducts,
                        child: const Text('Riprova'),
                      ),
                    ],
                  ),
                )
              : Column(
                  children: [
                    // Filtri per categoria
                    SingleChildScrollView(
                      scrollDirection: Axis.horizontal,
                      padding: const EdgeInsets.all(8),
                      child: Row(
                        children: [
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 4),
                            child: FilterChip(
                              selected: selectedCategoryId == 0,
                              label: const Text('Tutti'),
                              onSelected: (selected) {
                                setState(() {
                                  selectedCategoryId = 0;
                                });
                              },
                            ),
                          ),
                          ...products
                              .map((p) => p.categoryId)
                              .toSet()
                              .map((categoryId) {
                                final categoryName = products
                                    .firstWhere((p) => p.categoryId == categoryId)
                                    .categoryName;
                                return Padding(
                                  padding: const EdgeInsets.symmetric(horizontal: 4),
                                  child: FilterChip(
                                    selected: selectedCategoryId == categoryId,
                                    label: Text(categoryName ?? 'N/A'),
                                    onSelected: (selected) {
                                      setState(() {
                                        selectedCategoryId = categoryId;
                                      });
                                    },
                                  ),
                                );
                              }),
                        ],
                      ),
                    ),
                    // Griglia prodotti
                    Expanded(
                      child: GridView.builder(
                        padding: const EdgeInsets.all(8),
                        gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                          crossAxisCount: 2,
                          childAspectRatio: 0.75,
                          crossAxisSpacing: 8,
                          mainAxisSpacing: 8,
                        ),
                        itemCount: filteredProducts.length,
                        itemBuilder: (context, index) {
                          final product = filteredProducts[index];
                          return _buildProductCard(product, currencyFormat, cartProvider);
                        },
                      ),
                    ),
                  ],
                ),
    );
  }

  Widget _buildProductCard(Product product, NumberFormat format, CartProvider cartProvider) {
    return Card(
      elevation: 2,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Expanded(
            child: Container(
              color: Colors.grey[300],
              child: product.imageUrl != null && product.imageUrl!.isNotEmpty
                  ? Image.network(
                      product.imageUrl!,
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) {
                        return Center(
                          child: Icon(
                            Icons.fastfood,
                            size: 48,
                            color: Colors.grey[400],
                          ),
                        );
                      },
                    )
                  : Center(
                      child: Icon(
                        Icons.fastfood,
                        size: 48,
                        color: Colors.grey[400],
                      ),
                    ),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(8),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(
                  product.name,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                  style: const TextStyle(
                    fontWeight: FontWeight.bold,
                    fontSize: 12,
                  ),
                ),
                if (product.description != null && product.description!.isNotEmpty)
                  Text(
                    product.description!,
                    maxLines: 1,
                    overflow: TextOverflow.ellipsis,
                    style: TextStyle(
                      fontSize: 10,
                      color: Colors.grey[600],
                    ),
                  ),
                const SizedBox(height: 4),
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Text(
                      format.format(product.price),
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        fontSize: 14,
                        color: Colors.deepOrange,
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.add_shopping_cart, size: 18),
                      onPressed: () {
                        cartProvider.addItem(
                          product.id,
                          product.name,
                          product.price,
                        );
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text('${product.name} aggiunto al carrello'),
                            duration: const Duration(seconds: 1),
                          ),
                        );
                      },
                      padding: EdgeInsets.zero,
                      constraints: const BoxConstraints(),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
