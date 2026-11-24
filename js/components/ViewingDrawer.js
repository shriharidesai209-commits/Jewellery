/**
 * Private Viewing Drawer Component
 * Kashinathsa Y. Khatawate Jewellers (KYK Since 1937)
 * 
 * Manages the client's multi-piece selection for private salon viewing,
 * collects boutique/residence consultation preferences with mandatory phone
 * contact, transmits directly to Supabase, and provides WhatsApp escalation.
 */

import { defaultInquiryService } from '../services/inquiryService.js';
import { BRAND } from '../config/brand.js';

export class ViewingDrawer {
  constructor() {
    this.items = [];
    this.drawerEl = null;
    this.badgeEl = null;
    this.isSubmitting = false;
    this.init();
  }

  init() {
    if (typeof document === 'undefined') return;
    if (!document.body) {
      document.addEventListener('DOMContentLoaded', () => this.init());
      return;
    }
    let el = document.getElementById('viewing-drawer-container');
    if (!el) {
      el = document.createElement('div');
      el.id = 'viewing-drawer-container';
      el.className = 'drawer-backdrop hidden';
      document.body.appendChild(el);
    }
    this.drawerEl = el;

    // Close on backdrop click or close button
    this.drawerEl.addEventListener('click', (e) => {
      if (e.target === this.drawerEl || e.target.closest('[data-action="close-drawer"]')) {
        this.close();
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !this.drawerEl.classList.contains('hidden')) {
        this.close();
      }
    });

    this.render();
  }

  setBadgeElement(el) {
    this.badgeEl = el;
    this.updateBadge();
  }

  addItem(product) {
    if (!product) return;
    const exists = this.items.some(item => item.id === product.id);
    if (!exists) {
      this.items.push(product);
      this.updateBadge();
      this.render();
    }
    this.open();
  }

  removeItem(productId) {
    this.items = this.items.filter(item => item.id !== productId);
    this.updateBadge();
    this.render();
  }

  clear() {
    this.items = [];
    this.updateBadge();
    this.render();
  }

  updateBadge() {
    if (this.badgeEl) {
      this.badgeEl.textContent = this.items.length;
      this.badgeEl.setAttribute('aria-label', `${this.items.length} pieces selected`);
      if (this.items.length > 0) {
        this.badgeEl.classList.add('has-items');
      } else {
        this.badgeEl.classList.remove('has-items');
      }
    }
  }

  open() {
    this.render();
    this.drawerEl.classList.remove('hidden');
    document.body.classList.add('modal-open');
  }

  close() {
    this.drawerEl.classList.add('hidden');
    document.body.classList.remove('modal-open');
  }

  _resolveThumb(item) {
    if (!item) return BRAND.logoPath;
    if (item.images) {
      return item.images.listing?.jpg || item.images.listing?.png ||
             item.images.master?.jpg || item.images.master?.png ||
             item.images.featured?.jpg || item.images.featured?.png ||
             item.images.detail?.jpg || BRAND.logoPath;
    }
    return item.thumbnail || BRAND.logoPath;
  }

  render() {
    const count = this.items.length;

    this.drawerEl.innerHTML = `
      <aside class="viewing-drawer" role="dialog" aria-modal="true" aria-label="Private Viewing Consultation Request">
        <div class="drawer-header">
          <div class="drawer-title-group">
            <span class="drawer-sub">${BRAND.shortName.toUpperCase()} SALON &middot; EST. ${BRAND.establishedYear}</span>
            <h3 class="drawer-title">Private Viewing Selection</h3>
          </div>
          <button class="drawer-close-btn" data-action="close-drawer" aria-label="Close private viewing drawer">&times;</button>
        </div>

        <div class="drawer-body">
          ${count === 0 ? this.renderEmpty() : this.renderItemList()}
        </div>

        ${count > 0 ? this.renderFooter() : ''}
      </aside>
    `.trim();

    // Attach remove listeners
    const removeBtns = this.drawerEl.querySelectorAll('[data-action="remove-item"]');
    removeBtns.forEach(btn => {
      btn.addEventListener('click', (e) => {
        const id = e.currentTarget.getAttribute('data-id');
        this.removeItem(id);
      });
    });

    // Attach form submit listener
    const submitBtn = this.drawerEl.querySelector('#btn-submit-viewing-request');
    if (submitBtn) {
      submitBtn.addEventListener('click', (e) => this.handleViewingSubmit(e));
    }
  }

  async handleViewingSubmit(e) {
    e.preventDefault();
    if (this.isSubmitting) return;

    const nameInput = this.drawerEl.querySelector('#viewing-name');
    const emailInput = this.drawerEl.querySelector('#viewing-email');
    const phoneInput = this.drawerEl.querySelector('#viewing-phone');
    const locationInput = this.drawerEl.querySelector('#viewing-location');
    const messageInput = this.drawerEl.querySelector('#viewing-message');
    const feedbackEl = this.drawerEl.querySelector('#viewing-feedback');
    const submitBtn = this.drawerEl.querySelector('#btn-submit-viewing-request');

    const customer_name = nameInput?.value.trim() || '';
    const email = emailInput?.value.trim() || '';
    const phone = phoneInput?.value.trim() || '';
    const preferred_location = locationInput?.value || 'KYK Flagship Boutique — Javali Bazar, Gadag';
    const message = messageInput?.value.trim() || `Private salon viewing requested for ${this.items.length} selected masterpieces at ${preferred_location}.`;

    const selected_products = this.items.map(p => ({
      id: p.id,
      sku: p.id,
      name: p.name,
      category: p.category || 'Heritage Piece',
      metalType: p.metalType || '22K Gold',
      priceDisplay: p.priceDisplay || 'Price Upon Request',
      thumbnail: this._resolveThumb(p)
    }));

    const payload = {
      inquiry_type: 'viewing_appointment',
      customer_name,
      email,
      phone,
      preferred_location,
      message,
      product_id: `VIEWING-${this.items.length}-PIECES`,
      product_name: `Private Viewing Selection (${this.items.length} Pieces)`,
      selected_products
    };

    // Client-side validation check
    const validation = defaultInquiryService.validate(payload);
    if (!validation.isValid) {
      if (feedbackEl) {
        const firstErr = Object.values(validation.errors)[0];
        feedbackEl.textContent = firstErr;
        feedbackEl.className = 'drawer-feedback error';
        feedbackEl.classList.remove('hidden');
      }
      return;
    }

    // Set submitting state
    this.isSubmitting = true;
    if (submitBtn) {
      submitBtn.disabled = true;
      submitBtn.textContent = 'Securing Consultation Slot...';
    }
    if (feedbackEl) feedbackEl.classList.add('hidden');

    try {
      const res = await defaultInquiryService.submitInquiry(payload);
      this.renderSuccess(res, payload);
    } catch (err) {
      console.error('Viewing submission error:', err);
      if (feedbackEl) {
        feedbackEl.textContent = 'Network interruption. Please reach out via WhatsApp or call us directly.';
        feedbackEl.className = 'drawer-feedback error';
        feedbackEl.classList.remove('hidden');
      }
      if (submitBtn) {
        submitBtn.disabled = false;
        submitBtn.textContent = 'Request Salon Viewing Appointment';
      }
    } finally {
      this.isSubmitting = false;
    }
  }

  renderSuccess(result, payload) {
    const refId = result.inquiry_id || 'KYK-VIEW-' + Date.now();
    const count = payload.selected_products.length;
    const primaryContact = BRAND.contacts[0];

    const drawerBody = this.drawerEl.querySelector('.drawer-body');
    const drawerFooter = this.drawerEl.querySelector('.drawer-footer');
    if (drawerFooter) drawerFooter.remove();

    if (drawerBody) {
      drawerBody.innerHTML = `
        <div class="viewing-success-pane">
          <div class="viewing-success-icon">
            <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#997D3D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>
          <h4 class="viewing-success-title">Private Viewing Consultation Secured</h4>
          <p class="viewing-success-sub">
            Thank you, <strong>${payload.customer_name}</strong>. Your private consultation request for <strong>${count} masterpiece${count > 1 ? 's' : ''}</strong> has been prioritized in our salon register.
          </p>

          <!-- Gallery of Selected Pieces in Confirmation -->
          <div class="viewing-success-items-list">
            ${payload.selected_products.map(p => `
              <div class="drawer-item-row" style="background:#FFFFFF; margin-bottom:8px;">
                <div class="drawer-item-thumb">
                  <img src="${p.thumbnail || BRAND.logoPath}" alt="${p.name}" onerror="this.onerror=null;this.src='${BRAND.logoPath}'">
                </div>
                <div class="drawer-item-info">
                  <span class="drawer-item-sku">${p.sku || p.id}</span>
                  <h5 class="drawer-item-name" style="font-size:0.92rem;">${p.name}</h5>
                  <span class="drawer-item-metal">${p.metalType || '22K Gold'} &middot; ${p.category}</span>
                </div>
              </div>
            `).join('')}
          </div>

          <div class="viewing-summary-card">
            <div class="summary-line">
              <span class="lbl">Reference ID:</span>
              <span class="val font-mono">${refId}</span>
            </div>
            <div class="summary-line">
              <span class="lbl">Consultation Location:</span>
              <span class="val">${payload.preferred_location}</span>
            </div>
            <div class="summary-line">
              <span class="lbl">Contact Phone:</span>
              <span class="val">${payload.phone}</span>
            </div>
          </div>

          <div class="viewing-direct-escalation">
            <p class="escalation-note">Connect directly on WhatsApp to coordinate immediate timing:</p>
            <a href="https://wa.me/${primaryContact.waNumber}?text=Namaste%20Venkatesh-ji%2C%20I%20have%20requested%20a%20Private%20Viewing%20for%20${count}%20pieces%20(Ref%3A%20${refId})%20at%20${encodeURIComponent(payload.preferred_location)}."
               target="_blank" rel="noopener noreferrer" class="btn-viewing-wa">
              <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
              WhatsApp ${primaryContact.name} (${primaryContact.displayPhone})
            </a>
          </div>

          <div class="viewing-success-actions">
            <button class="btn-viewing-done" data-action="finish-viewing">Return to Vault</button>
          </div>
        </div>
      `;

      const doneBtn = drawerBody.querySelector('[data-action="finish-viewing"]');
      if (doneBtn) {
        doneBtn.addEventListener('click', () => {
          this.clear();
          this.close();
        });
      }
    }
  }

  renderEmpty() {
    return `
      <div class="drawer-empty-state">
        <div class="drawer-empty-icon">✦</div>
        <h4>Your Selection is Empty</h4>
        <p>Select any verified piece from the collection to request private salon inspection and tailored valuation details.</p>
        <button class="btn-drawer-browse" data-action="close-drawer">Browse Catalogue</button>
      </div>
    `;
  }

  renderItemList() {
    return `
      <div class="drawer-items-list">
        <p class="drawer-count-label">${this.items.length} Masterpiece${this.items.length === 1 ? '' : 's'} Selected for Private Inspection:</p>
        ${this.items.map(item => `
          <div class="drawer-item-row" data-id="${item.id}">
            <div class="drawer-item-thumb">
              <picture>
                ${item.images?.listing?.webp ? `<source srcset="${item.images.listing.webp}" type="image/webp">` : ''}
                <img src="${this._resolveThumb(item)}" alt="${item.name}" loading="eager" decoding="sync" onerror="this.onerror=null;this.src='${BRAND.logoPath}'">
              </picture>
            </div>
            <div class="drawer-item-info">
              <span class="drawer-item-sku">${item.id}</span>
              <h5 class="drawer-item-name">${item.name}</h5>
              <span class="drawer-item-metal">${item.metalType || item.metadata?.purity || '22K Gold'} &middot; ${item.category}</span>
              <span class="drawer-item-price">${item.priceDisplay}</span>
            </div>
            <button class="drawer-item-remove" data-action="remove-item" data-id="${item.id}" title="Remove piece">&times;</button>
          </div>
        `).join('')}
      </div>
    `;
  }

  renderFooter() {
    return `
      <div class="drawer-footer">
        <form class="drawer-inquiry-form" onsubmit="return false;" novalidate>
          <h5 class="form-heading">Consultation Arrangement</h5>
          <div id="viewing-feedback" class="drawer-feedback hidden" role="alert"></div>

          <div class="form-row">
            <label for="viewing-name" class="drawer-field-label">Full Name <span class="required-star">*</span></label>
            <input type="text" id="viewing-name" class="drawer-input" placeholder="e.g. Radhika Deshmukh" required autocomplete="name" />
          </div>

          <div class="form-row-2">
            <div class="form-col">
              <label for="viewing-email" class="drawer-field-label">Email <span class="required-star">*</span></label>
              <input type="email" id="viewing-email" class="drawer-input" placeholder="name@domain.com" required autocomplete="email" />
            </div>
            <div class="form-col">
              <label for="viewing-phone" class="drawer-field-label">Phone / WhatsApp <span class="required-star">*</span></label>
              <input type="tel" id="viewing-phone" class="drawer-input" placeholder="+91 98765 43210" required autocomplete="tel" />
            </div>
          </div>

          <div class="form-row">
            <label for="viewing-location" class="drawer-field-label">Preferred Boutique / Salon Location <span class="required-star">*</span></label>
            <select id="viewing-location" class="drawer-select">
              <option value="KYK Flagship Boutique — Javali Bazar, Gadag">KYK Flagship Boutique — Javali Bazar, Gadag</option>
              <option value="Private Salon Consultation — Hubballi / Dharwad">Private Salon Consultation — Hubballi / Dharwad</option>
              <option value="Private Salon Consultation — Bengaluru">Private Salon Consultation — Bengaluru</option>
              <option value="Bespoke Residence Appointment">Bespoke Residence Appointment</option>
            </select>
          </div>

          <div class="form-row">
            <label for="viewing-message" class="drawer-field-label">Special Requests (Optional)</label>
            <input type="text" id="viewing-message" class="drawer-input" placeholder="e.g. specific dates, timings, or bespoke requests" />
          </div>

          <button type="submit" id="btn-submit-viewing-request" class="btn-submit-viewing">
            Request Private Salon Viewing Appointment
          </button>
          <span class="drawer-guarantee">Confidential Consultation &middot; 100% Authenticity Assured &middot; Est. 1937</span>
        </form>
      </div>
    `;
  }
}

export const defaultViewingDrawer = new ViewingDrawer();
export default defaultViewingDrawer;
