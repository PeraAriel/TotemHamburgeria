import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Category } from '../models/category';
import { Product } from '../models/product';
import { Order } from '../models/order';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private baseUrl = 'http://localhost:5000/api';
  private readonly timeout = 10000;

  constructor(private http: HttpClient) {}

  // === CATEGORIE ===
  getCategories(): Observable<Category[]> {
    return this.http.get<Category[]>(`${this.baseUrl}/categories`);
  }

  getCategory(id: number): Observable<Category> {
    return this.http.get<Category>(`${this.baseUrl}/categories/${id}`);
  }

  createCategory(name: string, description: string = ''): Observable<any> {
    return this.http.post(`${this.baseUrl}/categories`, { name, description });
  }

  updateCategory(id: number, name: string, description: string = ''): Observable<any> {
    return this.http.put(`${this.baseUrl}/categories/${id}`, { name, description });
  }

  deleteCategory(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/categories/${id}`);
  }

  // === PRODOTTI ===
  getProducts(): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.baseUrl}/products`);
  }

  getProductsByCategory(categoryId: number): Observable<Product[]> {
    return this.http.get<Product[]>(`${this.baseUrl}/products/category/${categoryId}`);
  }

  getProduct(id: number): Observable<Product> {
    return this.http.get<Product>(`${this.baseUrl}/products/${id}`);
  }

  createProduct(product: Omit<Product, 'id'>): Observable<any> {
    return this.http.post(`${this.baseUrl}/products`, product);
  }

  updateProduct(id: number, product: Omit<Product, 'id'>): Observable<any> {
    return this.http.put(`${this.baseUrl}/products/${id}`, product);
  }

  deleteProduct(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/products/${id}`);
  }

  // === ORDINI ===
  getOrders(): Observable<Order[]> {
    return this.http.get<Order[]>(`${this.baseUrl}/orders`);
  }

  getOrder(id: number): Observable<Order> {
    return this.http.get<Order>(`${this.baseUrl}/orders/${id}`);
  }

  updateOrderStatus(id: number, status: string): Observable<any> {
    return this.http.put(`${this.baseUrl}/orders/${id}/status`, { status });
  }

  deleteOrder(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/orders/${id}`);
  }
}
