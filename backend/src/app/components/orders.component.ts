import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RouterModule, Router } from '@angular/router';
import { ApiService } from '../services/api.service';
import { Order, OrderStatus } from '../models/order';

@Component({
  selector: 'app-orders',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './orders.component.html',
  styleUrls: ['./orders.component.css']
})
export class OrdersComponent implements OnInit {
  orders: Order[] = [];
  filteredOrders: Order[] = [];
  isLoading = true;
  errorMessage = '';
  selectedStatus: 'all' | OrderStatus = 'all';

  private apiService = inject(ApiService);

  statusOptions: OrderStatus[] = ['pending', 'preparing', 'ready', 'completed', 'cancelled'];
  
  getStatusLabel(status: string): string {
    if (status === 'all') return 'Tutti';
    return this.statusLabels[status as OrderStatus] || status;
  }
  
  onStatusChange(status: string) {
    this.selectedStatus = (status === 'all' ? 'all' : status) as 'all' | OrderStatus;
    this.filterOrders();
  }
  statusLabels: { [key in OrderStatus]: string } = {
    pending: 'In Attesa',
    preparing: 'In Preparazione',
    ready: 'Pronto',
    completed: 'Completato',
    cancelled: 'Annullato'
  };

  statusColors: { [key in OrderStatus]: string } = {
    pending: '#ff9800',
    preparing: '#2196f3',
    ready: '#4caf50',
    completed: '#9c27b0',
    cancelled: '#f44336'
  };

  ngOnInit() {
    this.loadOrders();
    // Ricarica ordini ogni 5 secondi
    setInterval(() => this.loadOrders(), 5000);
  }

  loadOrders() {
    this.apiService.getOrders().subscribe({
      next: (data) => {
        this.orders = data;
        this.filterOrders();
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = `Errore: ${error.message}`;
        this.isLoading = false;
      }
    });
  }

  filterOrders() {
    if (this.selectedStatus === 'all') {
      this.filteredOrders = this.orders;
    } else {
      this.filteredOrders = this.orders.filter(o => o.status === this.selectedStatus);
    }
  }

  updateStatus(order: Order, newStatus: OrderStatus) {
    this.apiService.updateOrderStatus(order.id, newStatus).subscribe({
      next: () => {
        order.status = newStatus;
        this.filterOrders();
      },
      error: (error) => {
        this.errorMessage = `Errore nell'aggiornamento: ${error.message}`;
      }
    });
  }

  deleteOrder(order: Order) {
    if (confirm(`Eliminare ordine #${order.order_number}?`)) {
      this.apiService.deleteOrder(order.id).subscribe({
        next: () => {
          this.orders = this.orders.filter(o => o.id !== order.id);
          this.filterOrders();
        },
        error: (error) => {
          this.errorMessage = `Errore nell'eliminazione: ${error.message}`;
        }
      });
    }
  }
}
