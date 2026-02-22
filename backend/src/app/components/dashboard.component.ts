import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { OrdersComponent } from './orders.component';
import { MenuComponent } from './menu.component';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, OrdersComponent, MenuComponent],
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent {
  activeTab: 'orders' | 'menu' = 'orders';

  switchTab(tab: 'orders' | 'menu') {
    this.activeTab = tab;
  }
}
