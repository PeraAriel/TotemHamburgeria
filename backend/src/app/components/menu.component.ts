import { Component, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';
import { Category } from '../models/category';
import { Product } from '../models/product';

@Component({
  selector: 'app-menu',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './menu.component.html',
  styleUrls: ['./menu.component.css']
})
export class MenuComponent implements OnInit {
  categories: Category[] = [];
  products: Product[] = [];
  filteredProducts: Product[] = [];
  isLoading = true;
  errorMessage = '';
  
  selectedCategoryId: number | null = null;
  showProductForm = false;
  showCategoryForm = false;

  // Form per prodotto
  productForm = {
    id: null as number | null,
    name: '',
    description: '',
    price: 0,
    category_id: null as number | null,
    image_url: ''
  };

  // Form per categoria
  categoryForm = {
    id: null as number | null,
    name: '',
    description: ''
  };

  private apiService = inject(ApiService);

  ngOnInit() {
    this.loadCategories();
    this.loadProducts();
  }

  loadCategories() {
    this.apiService.getCategories().subscribe({
      next: (data) => {
        this.categories = data;
      },
      error: (error) => {
        this.errorMessage = `Errore: ${error.message}`;
      }
    });
  }

  loadProducts() {
    this.apiService.getProducts().subscribe({
      next: (data) => {
        this.products = data;
        this.filterProducts();
        this.isLoading = false;
      },
      error: (error) => {
        this.errorMessage = `Errore: ${error.message}`;
        this.isLoading = false;
      }
    });
  }

  filterProducts() {
    if (this.selectedCategoryId === null) {
      this.filteredProducts = this.products;
    } else {
      this.filteredProducts = this.products.filter(p => p.category_id === this.selectedCategoryId);
    }
  }

  selectCategory(categoryId: number | null) {
    this.selectedCategoryId = categoryId;
    this.filterProducts();
  }

  // === PRODOTTI ===
  openProductForm(product?: Product) {
    this.showProductForm = true;
    if (product) {
      this.productForm = {
        id: product.id,
        name: product.name,
        description: product.description ?? '',
        price: product.price,
        category_id: product.category_id,
        image_url: product.image_url ?? ''
      };
    } else {
      this.productForm = {
        id: null,
        name: '',
        description: '',
        price: 0,
        category_id: this.selectedCategoryId,
        image_url: ''
      };
    }
  }

  closeProductForm() {
    this.showProductForm = false;
    this.productForm = {
      id: null,
      name: '',
      description: '',
      price: 0,
      category_id: null,
      image_url: ''
    };
  }

  saveProduct() {
    if (!this.productForm.name || !this.productForm.category_id || !this.productForm.price) {
      alert('Compila tutti i campi obbligatori');
      return;
    }

    const productData = {
      name: this.productForm.name,
      description: this.productForm.description,
      price: this.productForm.price,
      category_id: this.productForm.category_id,
      image_url: this.productForm.image_url
    };

    if (this.productForm.id) {
      this.apiService.updateProduct(this.productForm.id, productData).subscribe({
        next: () => {
          this.loadProducts();
          this.closeProductForm();
        },
        error: (error) => {
          alert(`Errore: ${error.message}`);
        }
      });
    } else {
      this.apiService.createProduct(productData).subscribe({
        next: () => {
          this.loadProducts();
          this.closeProductForm();
        },
        error: (error) => {
          alert(`Errore: ${error.message}`);
        }
      });
    }
  }

  deleteProduct(product: Product) {
    if (confirm(`Eliminare "${product.name}"?`)) {
      this.apiService.deleteProduct(product.id).subscribe({
        next: () => {
          this.loadProducts();
        },
        error: (error) => {
          alert(`Errore: ${error.message}`);
        }
      });
    }
  }

  // === CATEGORIE ===
  openCategoryForm(category?: Category) {
    this.showCategoryForm = true;
    if (category) {
      this.categoryForm = {
        id: category.id,
        name: category.name,
        description: category.description || ''
      };
    } else {
      this.categoryForm = {
        id: null,
        name: '',
        description: ''
      };
    }
  }

  closeCategoryForm() {
    this.showCategoryForm = false;
    this.categoryForm = {
      id: null,
      name: '',
      description: ''
    };
  }

  saveCategory() {
    if (!this.categoryForm.name) {
      alert('Inserisci il nome della categoria');
      return;
    }

    if (this.categoryForm.id) {
      this.apiService.updateCategory(this.categoryForm.id, this.categoryForm.name, this.categoryForm.description).subscribe({
        next: () => {
          this.loadCategories();
          this.closeCategoryForm();
        },
        error: (error) => {
          alert(`Errore: ${error.message}`);
        }
      });
    } else {
      this.apiService.createCategory(this.categoryForm.name, this.categoryForm.description).subscribe({
        next: () => {
          this.loadCategories();
          this.closeCategoryForm();
        },
        error: (error) => {
          alert(`Errore: ${error.message}`);
        }
      });
    }
  }

  deleteCategory(category: Category) {
    if (confirm(`Eliminare categoria "${category.name}"?`)) {
      this.apiService.deleteCategory(category.id).subscribe({
        next: () => {
          this.loadCategories();
          this.loadProducts();
        },
        error: (error) => {
          alert(`Errore: ${error.message}`);
        }
      });
    }
  }
}
