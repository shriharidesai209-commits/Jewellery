/**
 * Customer Product Inquiry Modal
 * Kashinathsa Y. Khatawate Jewellers (KYK Since 1937)
 * 
 * Accessible, luxury-styled inquiry dialog that binds the selected product
 * context, validates input, transmits to the inquiry service, and provides
 * direct telephone/WhatsApp escalation.
 * 
 * Guarantees 100% robust rendering of original jewellery photographs across
 * all 5 Gold and 2 Silver masterpieces with graceful fallback to client crest.
 */

import { defaultInquiryService } from '../services/inquiryService.js';
import { defaultProductService } from '../services/productService.js';
import { BRAND } from '../config/brand.js';

export class InquiryModal {
  constructor() {
    this.modalEl = null;
    this.currentProduct = null;
    this.isSubmitting = false;
    this.init();
  }

  init() {
    if (typeof document === 'undefined') return;
    if (!document.body) {
      document.addEventListener('DOMContentLoaded', () => this.init());
      return;
    }

    let el = document.getElementById('kyk-inquiry-modal');
    if (!el) {
      el = document.createElement('div');
      el.id = 'kyk-inquiry-modal';
      el.className = 'inquiry-modal-backdrop hidden';
      el.setAttribute('role', 'dialog');
      el.setAttribute('aria-modal', 'true');
      el.setAttribute('aria-label', 'Product Inquiry and Private Salon Viewing');
      document.body.appendChild(el);
    }
    this.modalEl = el;

    // Close on backdrop click
    this.modalEl.addEventListener('click', (e) => {
      if (e.target === this.modalEl) {
        this.close();
      }
    });

    // Close on Escape
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !this.modalEl.classList.contains('hidden')) {
        this.close();
      }
    });
  }

  open(product) {
    // Resolve product if passed as an ID string or incomplete object
    let resolvedProduct = null;
    if (typeof product === 'string') {
      resolvedProduct = defaultProductService.getProductById(product);
    } else if (product && product.id) {
      resolvedProduct = defaultProductService.getProductById(product.id) || product;
    } else if (product) {
      resolvedProduct = product;
    }

    this.currentProduct = resolvedProduct || {
      id: 'KYK-GENERAL',
      name: 'Bespoke 22K Gold & Fine Silver Jewellery Consultation',
      category: 'Haute Joaillerie & Sacred Heirlooms',
      metalType: '22K Gold / 925 Silver'
    };

    this.isSubmitting = false;
    this.renderForm();
    this.modalEl.classList.remove('hidden');
    document.body.classList.add('modal-open');

    // Focus first input
    setTimeout(() => {
      const nameInput = this.modalEl.querySelector('#inquiry-customer-name');
      if (nameInput) nameInput.focus();
    }, 100);
  }

  close() {
    this.modalEl.classList.add('hidden');
    document.body.classList.remove('modal-open');
    this.currentProduct = null;
    this.isSubmitting = false;
  }

  _resolveProductImage(p) {
    if (!p) return BRAND.logoPath;
    if (p.images) {
      return p.images.listing?.jpg || p.images.listing?.png ||
             p.images.master?.jpg || p.images.master?.png ||
             p.images.featured?.jpg || p.images.featured?.png ||
             p.images.detail?.jpg || p.images.detail?.png || BRAND.logoPath;
    }
    if (p.sourceImage || p.image) {
      return p.sourceImage || p.image;
    }
    return BRAND.logoPath;
  }

  renderForm() {
    const p = this.currentProduct;
    const thumbnail = this._resolveProductImage(p);
    const metalLabel = p.metalType || (p.metadata?.purity ? p.metadata.purity : '22K Gold');
    const isSilver = String(metalLabel).toLowerCase().includes('silver') || (p.id && p.id.startsWith('SILV'));
    const hallmarkText = isSilver ? '925 Sterling Silver Heirloom' : BRAND.hallmark;

    this.modalEl.innerHTML = `
      <div class="inquiry-dialog">
        <div class="inquiry-header">
          <div class="inquiry-brand-badge">
            <img src="${BRAND.logoPath}" alt="${BRAND.shortName}" class="inquiry-logo-thumb">
            <div class="inquiry-brand-text">
              <span class="inquiry-brand-title">${BRAND.storeName}</span>
              <span class="inquiry-brand-sub">EST. ${BRAND.establishedYear} &middot; GADAG, KARNATAKA</span>
            </div>
          </div>
          <button class="inquiry-close-btn" data-action="close-inquiry" aria-label="Close inquiry modal">&times;</button>
        </div>

        <div class="inquiry-product-context">
          <img src="${thumbnail}" alt="${p.name}" class="inquiry-prod-img" onerror="this.onerror=null;this.src='${BRAND.logoPath}'">
          <div class="inquiry-prod-info">
            <span class="inquiry-prod-cat">${p.category || 'Heritage Masterpiece'} &middot; ${metalLabel}</span>
            <h4 class="inquiry-prod-name">${p.name}</h4>
            <span class="inquiry-prod-id">Ref: ${p.id} &middot; ${hallmarkText}</span>
          </div>
        </div>

        <form id="kyk-inquiry-form" class="inquiry-form" novalidate>
          <!-- Honeypot spam defense field (hidden from genuine users) -->
          <div style="display:none !important;" aria-hidden="true">
            <input type="text" id="inquiry-honeypot" name="website_trap" tabindex="-1" autocomplete="off">
          </div>

          <div id="inquiry-feedback-area" class="inquiry-feedback-banner hidden" role="alert"></div>

          <div class="form-group">
            <label for="inquiry-customer-name">Full Name <span class="required-star">*</span></label>
            <input type="text" id="inquiry-customer-name" name="customer_name" required placeholder="e.g. Radhika Deshmukh" autocomplete="name">
            <span class="field-error" id="err-customer-name"></span>
          </div>

          <div class="form-row-2">
            <div class="form-group">
              <label for="inquiry-email">Email Address <span class="required-star">*</span></label>
              <input type="email" id="inquiry-email" name="email" required placeholder="name@domain.com" autocomplete="email">
              <span class="field-error" id="err-email"></span>
            </div>

            <div class="form-group">
              <label for="inquiry-phone">Phone / WhatsApp Number <span class="required-star">*</span></label>
              <input type="tel" id="inquiry-phone" name="phone" required placeholder="+91 98765 43210" autocomplete="tel">
              <span class="field-error" id="err-phone"></span>
            </div>
          </div>

          <div class="form-group">
            <label for="inquiry-message">Inquiry Message or Bespoke Request <span class="required-star">*</span></label>
            <textarea id="inquiry-message" name="message" rows="3" required placeholder="Please let us know your requirements, questions about pricing, or bespoke appointment preferences..."></textarea>
            <span class="field-error" id="err-message"></span>
          </div>

          <div class="inquiry-actions-row">
            <button type="submit" id="btn-submit-inquiry" class="btn-transmit-inquiry">
              <span class="btn-text">Transmit Private Inquiry</span>
              <span class="btn-spinner hidden" aria-hidden="true"></span>
            </button>
          </div>

          <div class="inquiry-direct-contacts">
            <span class="direct-contact-label">Prefer immediate assistance? Connect directly with our proprietors:</span>
            <div class="direct-contact-pills">
              ${BRAND.contacts.map(c => `
                <div class="direct-contact-pill">
                  <span class="contact-name"><strong>${c.name}:</strong></span>
                  <a href="${c.telLink}" class="contact-action-btn" title="Call ${c.name}">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
                    ${c.displayPhone}
                  </a>
                  <a href="${c.waLink}" target="_blank" rel="noopener noreferrer" class="contact-action-btn wa-btn" title="WhatsApp ${c.name}">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
                    WhatsApp
                  </a>
                </div>
              `).join('')}
            </div>
          </div>
        </form>
      </div>
    `.trim();

    // Attach Close Listeners
    const closeBtn = this.modalEl.querySelector('[data-action="close-inquiry"]');
    if (closeBtn) closeBtn.addEventListener('click', () => this.close());

    // Attach Form Submit Listener
    const form = this.modalEl.querySelector('#kyk-inquiry-form');
    if (form) {
      form.addEventListener('submit', (e) => this.handleFormSubmit(e));
    }
  }

  async handleFormSubmit(e) {
    e.preventDefault();
    if (this.isSubmitting) return;

    this.clearErrors();

    const form = e.target;
    const customer_name = form.customer_name.value.trim();
    const email = form.email.value.trim();
    const phone = form.phone.value.trim();
    const message = form.message.value.trim();
    const honeypot = form.website_trap.value.trim();

    const payload = {
      inquiry_type: 'individual_product',
      customer_name,
      email,
      phone,
      product_id: this.currentProduct.id,
      product_sku: this.currentProduct.id,
      product_name: this.currentProduct.name,
      product_category: this.currentProduct.category || 'Heritage Masterpiece',
      product_metal: this.currentProduct.metalType || '22K Gold',
      message,
      honeypot
    };

    // Client-side quick check
    const validation = defaultInquiryService.validate(payload);
    if (!validation.isValid) {
      this.displayErrors(validation.errors);
      return;
    }

    this.setSubmitting(true);

    try {
      const result = await defaultInquiryService.submitInquiry(payload);

      if (result.success) {
        this.renderSuccess(result, payload);
      } else {
        this.showFeedbackBanner(result.error || 'Failed to submit inquiry. Please try again.', 'error');
        if (result.details) this.displayErrors(result.details);
      }
    } catch (err) {
      this.showFeedbackBanner('An unexpected network error occurred. Please contact us directly via WhatsApp or phone.', 'error');
    } finally {
      this.setSubmitting(false);
    }
  }

  renderSuccess(result, payload) {
    const p = this.currentProduct;
    const refId = result.inquiry_id || 'KYK-REF-' + Date.now();
    const submissionTime = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    const thumbnail = this._resolveProductImage(p);
    const metalLabel = p.metalType || '22K Gold';

    this.modalEl.innerHTML = `
      <div class="inquiry-dialog inquiry-success-dialog">
        <div class="inquiry-header">
          <div class="inquiry-brand-badge">
            <img src="${BRAND.logoPath}" alt="${BRAND.shortName}" class="inquiry-logo-thumb">
            <span class="inquiry-brand-title">${BRAND.storeName}</span>
          </div>
          <button class="inquiry-close-btn" data-action="close-inquiry" aria-label="Close modal">&times;</button>
        </div>

        <div class="inquiry-success-body">
          <div class="success-icon-wrap">
            <svg width="44" height="44" viewBox="0 0 24 24" fill="none" stroke="#997D3D" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
              <polyline points="22 4 12 14.01 9 11.01"></polyline>
            </svg>
          </div>

          <h3 class="success-title">Inquiry Successfully Registered</h3>
          <p class="success-subtitle">
            Thank you, <strong>${payload.customer_name}</strong>. Your inquiry has been secured in our private salon registry.
          </p>

          <!-- Verified Product Photographic Context in Confirmation -->
          <div class="inquiry-product-context inquiry-success-context">
            <img src="${thumbnail}" alt="${p.name}" class="inquiry-prod-img" onerror="this.onerror=null;this.src='${BRAND.logoPath}'">
            <div class="inquiry-prod-info">
              <span class="inquiry-prod-cat">${p.category || 'Heritage Piece'} &middot; ${metalLabel}</span>
              <h4 class="inquiry-prod-name">${p.name}</h4>
              <span class="inquiry-prod-id">Ref: ${p.id} &middot; Registered at ${submissionTime} IST</span>
            </div>
          </div>

          <div class="inquiry-reference-card">
            <div class="ref-row">
              <span class="ref-label">Reference ID:</span>
              <span class="ref-value font-mono">${refId}</span>
            </div>
            <div class="ref-row">
              <span class="ref-label">Inquiry Type:</span>
              <span class="ref-value">Individual Piece Inquiry</span>
            </div>
            <div class="ref-row">
              <span class="ref-label">Registered Phone:</span>
              <span class="ref-value">${payload.phone}</span>
            </div>
            <div class="ref-row">
              <span class="ref-label">Next Step:</span>
              <span class="ref-value">Senior Jeweller Consultation within 24 Hours</span>
            </div>
          </div>

          <div class="success-direct-actions">
            <p class="success-direct-note">Need an instant response? Chat directly with our proprietor on WhatsApp:</p>
            <div class="success-btn-group">
              <a href="https://wa.me/${BRAND.contacts[0].waNumber}?text=Namaste%20Venkatesh-ji%2C%20I%20have%20inquired%20about%20${encodeURIComponent(p.name)}%20(Ref%3A%20${refId})%20on%20your%20website." 
                 target="_blank" rel="noopener noreferrer" class="btn-success-wa">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
                WhatsApp Venkatesh (+91 94487 53791)
              </a>
              <button class="btn-success-close" data-action="close-inquiry">Return to Vault</button>
            </div>
          </div>
        </div>
      </div>
    `.trim();

    // Attach Close Listeners
    const closeBtns = this.modalEl.querySelectorAll('[data-action="close-inquiry"]');
    closeBtns.forEach(b => b.addEventListener('click', () => this.close()));
  }

  setSubmitting(isSubmitting) {
    this.isSubmitting = isSubmitting;
    const btn = this.modalEl.querySelector('#btn-submit-inquiry');
    if (!btn) return;
    const textSpan = btn.querySelector('.btn-text');
    const spinner = btn.querySelector('.btn-spinner');

    if (isSubmitting) {
      btn.disabled = true;
      if (textSpan) textSpan.textContent = 'Transmitting to Vault...';
      if (spinner) spinner.classList.remove('hidden');
    } else {
      btn.disabled = false;
      if (textSpan) textSpan.textContent = 'Transmit Private Inquiry';
      if (spinner) spinner.classList.add('hidden');
    }
  }

  displayErrors(errors) {
    for (const [field, msg] of Object.entries(errors)) {
      const errEl = this.modalEl.querySelector(`#err-${field.replace('_', '-')}`);
      if (errEl) {
        errEl.textContent = msg;
        errEl.style.display = 'block';
      }
    }
  }

  clearErrors() {
    const errEls = this.modalEl.querySelectorAll('.field-error');
    errEls.forEach(el => {
      el.textContent = '';
      el.style.display = 'none';
    });
    const feedback = this.modalEl.querySelector('#inquiry-feedback-area');
    if (feedback) {
      feedback.classList.add('hidden');
      feedback.textContent = '';
    }
  }

  showFeedbackBanner(msg, type = 'error') {
    const feedback = this.modalEl.querySelector('#inquiry-feedback-area');
    if (feedback) {
      feedback.textContent = msg;
      feedback.className = `inquiry-feedback-banner ${type}`;
      feedback.classList.remove('hidden');
    }
  }
}

export const defaultInquiryModal = new InquiryModal();
export default defaultInquiryModal;
