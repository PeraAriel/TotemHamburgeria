import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:totem/services/cart_provider.dart';
import 'package:totem/screens/home_screen.dart';
import 'package:totem/screens/cart_screen.dart';

void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => CartProvider()),
      ],
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Totem Hamburgeria',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepOrange),
        useMaterial3: true,
      ),
      home: const HomeScreen(),
      routes: {
        '/cart': (context) => const CartScreen(),
      },
    );
  }
}

