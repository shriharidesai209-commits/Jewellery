/**
 * Live Search Modal Component
 * Connects directly to ProductService for real-time querying across jewellery names, descriptions, and tags.
 */

import { defaultProductService } from '../services/productService.js';
import { defaultProductModal } from './ProductModal.js';

export class SearchModal {
  constructor() {
    this.modalEl = null;
    this.service = defaultProductService;
    this.init();
  }

  init() {
    if (typeof document === 'undefined') return;
    if (!document.body) {
      document.addEventListener('DOMContentLoaded', () => this.init());
      return;
    }
    let el = document.getElementById('search-modal-container');
    if (!el) {
      el = document.createElement('div');
      el.id = 'search-modal-container';
      el.className = 'search-backdrop hidden';
      document.body.appendChild(el);
    }
    this.modalEl = el;

    this.modalEl.addEventListener('click', (e) => {
      if (e.target === this.modalEl || e.target.closest('[data-action="close-search"]')) {
        this.close();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !this.modalEl.classList.contains('hidden')) {
        this.close();
      }
    });
  }

  open() {
    this.render();
    this.modalEl.classList.remove('hidden');
    document.body.classList.add('modal-open');
    const input = this.modalEl.querySelector('#search-query-input');
    if (input) {
      setTimeout(() => input.focus(), 80);
    }
  }

  close() {
    this.modalEl.classList.add('hidden');
    document.body.classList.remove('modal-open');
  }

  render() {
    this.modalEl.innerHTML = `
      <div class="search-dialog" role="dialog" aria-label="Search Catalogue">
        <div class="search-header">
          <div class="search-input-wrapper">
            <span class="search-icon">🔍</span>
            <input 
              type="text" 
              id="search-query-input" 
              class="search-input" 
              placeholder="Search by jewellery piece, gemstone, or style (e.g. Ruby, Jhumka, Choker, Haar)..." 
              autocomplete="off"
            />
            <button class="search-clear-btn" id="btn-clear-search" aria-label="Clear search input">&times;</button>
          </div>
          <button class="search-close-btn" data-action="close-search" aria-label="Close search">&times;</button>
        </div>

        <div class="search-results-area" id="search-results-area">
          ${this.renderResults(this.service.getAllProducts(), '')}
        </div>
      </div>
    `.trim();

    const input = this.modalEl.querySelector('#search-query-input');
    const clearBtn = this.modalEl.querySelector('#btn-clear-search');
    const resultsArea = this.modalEl.querySelector('#search-results-area');

    if (input) {
      input.addEventListener('input', (e) => {
        const query = e.target.value;
        const matches = this.service.search(query);
        resultsArea.innerHTML = this.renderResults(matches, query);
        this.attachResultListeners();
      });
    }

    if (clearBtn && input) {
      clearBtn.addEventListener('click', () => {
        input.value = '';
        input.focus();
        resultsArea.innerHTML = this.renderResults(this.service.getAllProducts(), '');
        this.attachResultListeners();
      });
    }

    this.attachResultListeners();
  }

  attachResultListeners() {
    const resultRows = this.modalEl.querySelectorAll('.search-result-row');
    resultRows.forEach(row => {
      row.addEventListener('click', (e) => {
        const id = row.getAttribute('data-id');
        const prod = this.service.getProductById(id);
        if (prod) {
          this.close();
          defaultProductModal.open(prod);
        }
      });
    });
  }

  renderResults(products, query) {
    if (products.length === 0) {
      return `
        <div class="search-empty">
          <p>No jewellery pieces match <em>"${query}"</em>.</p>
          <span class="search-hint">Try searching for <strong>Ruby</strong>, <strong>Jhumka</strong>, <strong>Haar</strong>, or <strong>Choker</strong>.</span>
        </div>
      `;
    }

    const titlePrefix = query ? `Matching Pieces (${products.length}):` : 'Curated Verified Pieces:';

    return `
      <div class="search-results-list">
        <span class="search-results-label">${titlePrefix}</span>
        ${products.map(p => `
          <div class="search-result-row" data-id="${p.id}">
            <picture class="search-result-thumb-pic">
              ${p.images?.listing?.webp ? `<source srcset="${p.images.listing.webp}" type="image/webp">` : ''}
              <img class="search-result-thumb" src="${p.images?.listing?.jpg || p.images?.listing?.png || ''}" alt="${p.name}" loading="eager" decoding="sync">
            </picture>
            <div class="search-result-content">
              <span class="search-result-sku">${p.id} · ${p.category}</span>
              <h5 class="search-result-title">${p.name}</h5>
              <p class="search-result-desc">${p.shortDescription}</p>
            </div>
            <div class="search-result-action">
              <span class="search-view-label">Inspect Piece &rarr;</span>
            </div>
          </div>
        `).join('')}
      </div>
    `;
  }
}

export const defaultSearchModal = new SearchModal();
export default defaultSearchModal;
