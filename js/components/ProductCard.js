/**
 * Reusable Product Card Component (Stage 2 Luxury Edition)
 * Encapsulates the visual presentation and interaction of an individual catalogue item.
 */

import { ProductImage } from './ProductImage.js';

export class ProductCard {
  /**
   * Generates the product card markup string.
   * @param {Object} product - Verified product catalogue object
   * @param {Object} options - Customization options
   * @returns {string} HTML string
   */
  static render(product, options = {}) {
    if (!product) return '';

    const {
      showTags = true,
      showDescription = true,
      className = ''
    } = options;

    const listingImage = product.images?.listing || null;
    const imageHtml = ProductImage.render(listingImage, {
      aspectRatio: '1:1',
      className: 'card-listing-image',
      loading: 'eager',
      decoding: 'sync'
    });

    const tagsHtml = showTags && Array.isArray(product.tags)
      ? `<div class="product-card-tags">
          ${product.tags.slice(0, 3).map(t => `<span class="product-tag">${t}</span>`).join('')}
         </div>`
      : '';

    const priceText = product.priceDisplay || 'Price Upon Request';
    const metalBadge = product.metadata?.purity ? `<span class="badge-metal">${product.metadata.purity}</span>` : '';
    const gemstoneText = product.metadata?.gemstones ? `<div class="card-stones">${product.metadata.gemstones}</div>` : '';

    return `
      <article class="product-card ${className}" data-product-id="${product.id}">
        <div class="product-card-media" data-action="view-details" data-id="${product.id}">
          ${imageHtml}
          <div class="product-card-badges">
            <span class="badge-category">${product.category}</span>
            ${metalBadge}
          </div>
          <button class="quick-view-btn" data-action="view-details" data-id="${product.id}" aria-label="Quick View of ${product.name}">
            <span>Inspect Masterpiece</span>
          </button>
        </div>
        
        <div class="product-card-body">
          <div class="product-card-header">
            <span class="product-sku">${product.id}</span>
            <h3 class="product-title" data-action="view-details" data-id="${product.id}">${product.name}</h3>
          </div>

          ${gemstoneText}

          ${showDescription && product.shortDescription ? `
            <p class="product-card-desc">${product.shortDescription}</p>
          ` : ''}

          ${tagsHtml}

          <div class="product-card-footer">
            <div class="product-price-box">
              <span class="price-label">CONFIDENTIAL VALUATION</span>
              <span class="price-value">${priceText}</span>
            </div>
            <button class="btn-inquire" data-action="inquire" data-id="${product.id}" data-name="${product.name}" title="Add to private viewing salon list">
              + Inquire
            </button>
          </div>
        </div>
      </article>
    `.trim();
  }

  /**
   * Creates an interactive HTMLElement instance for the product card.
   * @param {Object} product 
   * @param {Object} callbacks - { onViewDetails, onInquire }
   * @returns {HTMLElement}
   */
  static create(product, callbacks = {}) {
    const temp = document.createElement('div');
    temp.innerHTML = ProductCard.render(product);
    const element = temp.firstElementChild;

    // Attach click listener for details view
    if (typeof callbacks.onViewDetails === 'function') {
      const clickables = element.querySelectorAll('[data-action="view-details"]');
      clickables.forEach(el => {
        el.addEventListener('click', (e) => {
          e.preventDefault();
          callbacks.onViewDetails(product);
        });
      });
    }

    // Attach click listener for inquiry
    if (typeof callbacks.onInquire === 'function') {
      const inquireBtn = element.querySelector('[data-action="inquire"]');
      if (inquireBtn) {
        inquireBtn.addEventListener('click', (e) => {
          e.stopPropagation();
          callbacks.onInquire(product);
        });
      }
    }

    return element;
  }
}

export default ProductCard;
