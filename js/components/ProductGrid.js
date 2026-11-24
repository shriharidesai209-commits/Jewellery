/**
 * Reusable Product Grid Component (Stage 2 Luxury Edition)
 * Manages catalogue layout, category filtering controls, product counts, and empty states.
 * Guarantees seamless switching between 22K Gold Heritage and Fine Silver Vault.
 */

import { ProductCard } from './ProductCard.js';
import { defaultProductService } from '../services/productService.js';

export class ProductGrid {
  constructor(containerElement, options = {}) {
    this.container = typeof containerElement === 'string'
      ? document.querySelector(containerElement)
      : containerElement;

    this.service = options.productService || defaultProductService;
    this.currentCategory = options.initialCategory || 'All Jewellery';
    this.currentMetal = options.initialMetal || 'all';
    this.onViewDetails = options.onViewDetails || null;
    this.onInquire = options.onInquire || null;

    this.init();
  }

  init() {
    if (!this.container) return;
    this.render();
  }

  setCategory(category, scrollToGrid = false) {
    this.currentCategory = category || 'All Jewellery';
    
    // Auto-align metal scope if a category is specific to Gold or Silver to prevent empty zero-product states
    const catLower = this.currentCategory.toLowerCase();
    if (catLower.includes('earring') || catLower.includes('choker') || catLower.includes('haar') || catLower === '22k gold vault' || catLower === 'gold') {
      this.currentMetal = 'gold';
    } else if (catLower.includes('silver')) {
      this.currentMetal = 'silver';
    }

    this.render();
    if (scrollToGrid) {
      this._scrollToVault();
    }
  }

  setMetal(metal, scrollToGrid = false) {
    this.currentMetal = metal ? metal.toLowerCase() : 'all';
    this.currentCategory = 'All Jewellery';
    this.render();
    if (scrollToGrid) {
      this._scrollToVault();
    }
  }

  _scrollToVault() {
    const vaultEl = document.getElementById('vault-section') || this.container;
    if (vaultEl && typeof window !== 'undefined') {
      const headerOffset = 90;
      const elementPosition = vaultEl.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
      window.scrollTo({
        top: Math.max(0, offsetPosition),
        behavior: 'smooth'
      });
    }
  }

  render() {
    if (!this.container) return;

    const metalScope = this.currentMetal === 'all' ? null : this.currentMetal;
    const categories = this.service.getCategories(metalScope);
    const products = this.service.getProductsByCategory(this.currentCategory, metalScope);
    const goldCount = this.service.getGoldProducts().length;
    const silverCount = this.service.getSilverProducts().length;
    const totalCount = this.service.getAllProducts().length;

    let assuranceText = '✦ Authenticated Gold & Silver Vault';
    if (this.currentMetal === 'gold') assuranceText = '✦ 22K Gold Handcrafted Vault';
    if (this.currentMetal === 'silver') assuranceText = '✦ 925 Sterling Silver Heirloom Vault';

    this.container.innerHTML = `
      <div class="catalogue-controls" id="catalogue-controls">
        <!-- Metal Selection Tabs (Gold vs Silver Distinction) -->
        <div class="metal-filter-bar" role="tablist" aria-label="Vault Metal Collection">
          <button 
            class="metal-tab ${this.currentMetal === 'all' ? 'active' : ''}" 
            role="tab" 
            aria-selected="${this.currentMetal === 'all'}" 
            data-metal="all">
            All Masterpieces (${totalCount})
          </button>
          <button 
            class="metal-tab ${this.currentMetal === 'gold' ? 'active' : ''}" 
            role="tab" 
            aria-selected="${this.currentMetal === 'gold'}" 
            data-metal="gold">
            ✦ 22K Gold Heritage (${goldCount})
          </button>
          <button 
            class="metal-tab ${this.currentMetal === 'silver' ? 'active' : ''}" 
            role="tab" 
            aria-selected="${this.currentMetal === 'silver'}" 
            data-metal="silver">
            ✦ Fine Silver Vault (${silverCount})
          </button>
        </div>

        <!-- Category Sub-Filters -->
        <div class="category-filter-bar" role="tablist" aria-label="Jewellery Categories">
          ${categories.map(cat => {
            const isActive = cat.toLowerCase() === this.currentCategory.toLowerCase();
            return `
              <button 
                class="category-tab ${isActive ? 'active' : ''}" 
                role="tab" 
                aria-selected="${isActive}" 
                data-category="${cat}">
                ${cat}
              </button>
            `;
          }).join('')}
        </div>
        
        <div class="catalogue-status-meta">
          <span class="catalogue-count">Displaying <strong>${products.length}</strong> authenticated piece${products.length === 1 ? '' : 's'}</span>
          <span class="catalogue-assurance">${assuranceText}</span>
        </div>
      </div>

      <div class="catalogue-grid" id="catalogue-grid-items">
        ${products.length === 0 ? this.renderEmptyState() : ''}
      </div>
    `.trim();

    // Populate grid items with interactive cards
    const gridEl = this.container.querySelector('#catalogue-grid-items');
    if (products.length > 0 && gridEl) {
      products.forEach(prod => {
        const cardEl = ProductCard.create(prod, {
          onViewDetails: (p) => {
            if (this.onViewDetails) this.onViewDetails(p);
          },
          onInquire: (p) => {
            if (this.onInquire) this.onInquire(p);
          }
        });
        gridEl.appendChild(cardEl);
      });
    }

    // Attach metal tab listeners
    const metalTabs = this.container.querySelectorAll('.metal-tab');
    metalTabs.forEach(tab => {
      tab.addEventListener('click', (e) => {
        const metal = e.currentTarget.getAttribute('data-metal');
        this.setMetal(metal, false);
      });
    });

    // Attach category tab listeners
    const tabs = this.container.querySelectorAll('.category-tab');
    tabs.forEach(tab => {
      tab.addEventListener('click', (e) => {
        const cat = e.currentTarget.getAttribute('data-category');
        this.setCategory(cat, false);
      });
    });

    // Reset filter button in empty state
    const resetBtn = this.container.querySelector('[data-action="reset-filter"]');
    if (resetBtn) {
      resetBtn.addEventListener('click', () => {
        this.setMetal('all', false);
      });
    }
  }

  renderEmptyState() {
    return `
      <div class="catalogue-empty-state">
        <div class="empty-icon">✧</div>
        <h3>No Pieces in Selected Category</h3>
        <p>No jewellery pieces currently match this specific curation filter. Please select another category.</p>
        <button class="btn-reset-filter" data-action="reset-filter">View All Vault Masterpieces</button>
      </div>
    `;
  }
}

export default ProductGrid;
