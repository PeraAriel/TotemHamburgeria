export interface OrderItem {
  id: number;
  product_id: number;
  quantity: number;
  unit_price: number;
  name?: string;
  description?: string;
}

export type OrderStatus = 'pending' | 'preparing' | 'ready' | 'completed' | 'cancelled';

export interface Order {
  id: number;
  order_number: number;
  status: OrderStatus;
  total_price: number;
  created_at?: string;
  updated_at?: string;
  items?: OrderItem[];
}
