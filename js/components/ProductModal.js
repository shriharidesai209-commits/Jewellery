/**
 * Reusable Product Detail Modal Component (Upgraded Stage 2)
 * Features:
 * - Multi-angle verified asset switching (listing, gallery, featured, detail, master)
 * - Click-to-zoom high-resolution visual examination
 * - Comprehensive verified craftsmanship specifications
 * - Direct integration with Private Viewing Drawer
 */

import { ProductImage } from './ProductImage.js';
import { defaultViewingDrawer } from './ViewingDrawer.js';
import { defaultInquiryModal } from './InquiryModal.js';

export class ProductModal {
  constructor() {
    this.modalEl = null;
    this.activeProduct = null;
    this.activeAngle = 'listing';
    this.isZoomed = false;
    this.init();
  }

  init() {
    if (typeof document === 'undefined') return;
    if (!document.body) {
      document.addEventListener('DOMContentLoaded', () => this.init());
      return;
    }
    let el = document.getElementById('product-detail-modal');
    if (!el) {
      el = document.createElement('div');
      el.id = 'product-detail-modal';
      el.className = 'modal-backdrop hidden';
      el.setAttribute('role', 'dialog');
      el.setAttribute('aria-modal', 'true');
      document.body.appendChild(el);
    }
    this.modalEl = el;

    this.modalEl.addEventListener('click', (e) => {
      if (e.target === this.modalEl || e.target.closest('[data-action="close-modal"]')) {
        this.close();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !this.modalEl.classList.contains('hidden')) {
        this.close();
      }
    });
  }

  open(product, initialAngle = 'listing') {
    if (!product) return;
    this.activeProduct = product;
    this.activeAngle = initialAngle;
    this.isZoomed = false;
    this.render();
    this.modalEl.classList.remove('hidden');
    document.body.classList.add('modal-open');
  }

  close() {
    this.modalEl.classList.add('hidden');
    document.body.classList.remove('modal-open');
    this.activeProduct = null;
    this.isZoomed = false;
  }

  render() {
    const p = this.activeProduct;
    if (!p) return;

    const currentImgObj = p.images[this.activeAngle] || p.images.listing;
    const aspect = currentImgObj.aspectRatio || '1:1';
    
    const angles = [
      { key: 'listing', label: '1:1 Studio Card', desc: '1600x1600' },
      { key: 'gallery', label: '4:5 Portrait', desc: '1600x2000' },
      { key: 'featured', label: '16:9 Editorial', desc: '1920x1080' },
      { key: 'detail', label: 'Macro Craftsmanship', desc: '1200x1200' },
      { key: 'master', label: 'Isolated Master', desc: 'Original Cut' }
    ].filter(a => !!p.images[a.key]);

    const angleHtml = angles.map(a => `
      <button 
        class="angle-pill ${this.activeAngle === a.key ? 'active' : ''}" 
        data-angle="${a.key}">
        <span class="angle-pill-title">${a.label}</span>
        <span class="angle-pill-dim">${a.desc}</span>
      </button>
    `).join('');

    const mainImageHtml = ProductImage.render(currentImgObj, {
      aspectRatio: aspect,
      className: `modal-hero-image ${this.isZoomed ? 'zoomed-in' : ''}`,
      loading: 'eager'
    });

    const meta = p.metadata || {};

    this.modalEl.innerHTML = `
      <div class="modal-dialog">
        <button class="modal-close-btn" data-action="close-modal" aria-label="Close inspection modal">&times;</button>
        
        <div class="modal-layout">
          <!-- Left Column: Visual Showcase -->
          <div class="modal-visual-column">
            <div class="modal-image-stage" id="modal-image-stage" title="Click to zoom / reset perspective">
              ${mainImageHtml}
              <div class="zoom-indicator-tag">
                <span>${this.isZoomed ? '🔍 Click to Reset View' : '🔍 Click to Zoom In'}</span>
              </div>
            </div>
            
            <div class="modal-angles-selector">
              <div class="angles-header">
                <span class="angles-label">AUTHENTICATED ANGLE PERSPECTIVES:</span>
                <span class="angles-note">Phase 2 V2 Remediated Studio Assets</span>
              </div>
              <div class="angles-buttons">
                ${angleHtml}
              </div>
            </div>
          </div>

          <!-- Right Column: Product Detail & Craftsmanship -->
          <div class="modal-info-column">
            <div class="modal-header">
              <div class="modal-sku-badge">${p.id} · ${p.category.toUpperCase()}</div>
              <h2 class="modal-product-title">${p.name}</h2>
              <div class="modal-category">Purity: ${meta.purity || '22K Gold (91.6%)'} · Authentic Indian Heritage</div>
            </div>

            <div class="modal-price-box">
              <span class="modal-price-label">CONFIDENTIAL ESTIMATE</span>
              <span class="modal-price-val">${p.priceDisplay || 'Price Upon Request'}</span>
              <span class="modal-availability">● ${p.availability}</span>
            </div>

            <div class="modal-description">
              <h4>Design & Provenance</h4>
              <p>${p.fullDescription}</p>
            </div>

            <div class="modal-specs-section">
              <h4>Craftsmanship Specifications</h4>
              <table class="specs-table">
                <tbody>
                  <tr><th>Precious Metal</th><td>${meta.metal || '22K Yellow Gold'}</td></tr>
                  <tr><th>Gold Purity</th><td>${meta.purity || '91.6% Hallmarked Gold'}</td></tr>
                  <tr><th>Gemstone Inlay</th><td>${meta.gemstones || 'Pure Precious Metalwork'}</td></tr>
                  <tr><th>Technique</th><td>${meta.craftsmanship || 'Traditional Repoussé & Filigree'}</td></tr>
                  <tr><th>Fastening</th><td>${meta.closure || 'Handmade Clasp / Traditional Dori'}</td></tr>
                  <tr><th>Curated Vault</th><td>${meta.collection || 'Heritage Masterpiece'}</td></tr>
                  <tr><th>Source Asset</th><td><code>${p.sourceHero}</code> (100% Geometry Fidelity)</td></tr>
                </tbody>
              </table>
            </div>

            <div class="modal-actions-dual">
              <button class="btn-primary-viewing" id="btn-modal-direct-salon" data-id="${p.id}">
                Inquire About This Piece &rarr;
              </button>
              <button class="btn-secondary-salon" id="btn-modal-add-viewing" data-id="${p.id}">
                + Add to Viewing Selection
              </button>
            </div>
            <div id="modal-viewing-feedback" class="modal-viewing-toast hidden" role="status"></div>
            <p class="modal-guarantee-note">✦ Confidential Inquiry &middot; Direct Artisan Response &middot; Zero Speculative Reconstructions</p>
          </div>
        </div>
      </div>
    `.trim();

    // Attach angle switch listener
    const angleBtns = this.modalEl.querySelectorAll('.angle-pill');
    angleBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const nextAngle = e.currentTarget.getAttribute('data-angle');
        this.activeAngle = nextAngle;
        this.isZoomed = false;
        this.render();
      });
    });

    // Attach zoom toggle listener on stage
    const stage = this.modalEl.querySelector('#modal-image-stage');
    if (stage) {
      stage.addEventListener('click', () => {
        this.isZoomed = !this.isZoomed;
        this.render();
      });
    }

    // Attach "Add to Private Viewing Selection"
    const addViewingBtn = this.modalEl.querySelector('#btn-modal-add-viewing');
    if (addViewingBtn) {
      addViewingBtn.addEventListener('click', () => {
        defaultViewingDrawer.addItem(p);
        const toast = this.modalEl.querySelector('#modal-viewing-feedback');
        if (toast) {
          toast.textContent = `✓ Added to Private Viewing Selection (${defaultViewingDrawer.items.length} piece${defaultViewingDrawer.items.length === 1 ? '' : 's'})`;
          toast.classList.remove('hidden');
          setTimeout(() => toast.classList.add('hidden'), 3500);
        }
      });
    }

    // Attach "Inquire About This Piece" -> Direct Individual Product Inquiry
    const directSalonBtn = this.modalEl.querySelector('#btn-modal-direct-salon');
    if (directSalonBtn) {
      directSalonBtn.addEventListener('click', () => {
        this.close();
        defaultInquiryModal.open(p, 'individual_product');
      });
    }
  }
}

export const defaultProductModal = new ProductModal();
export default defaultProductModal;
