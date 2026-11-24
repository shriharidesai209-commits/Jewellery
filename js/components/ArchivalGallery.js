/**
 * Archival Jewellery Gallery Slider Component
 * Kashinathsa Y. Khatawate Jewellers (KYK Since 1937), Gadag
 * 
 * Features:
 * - 20 authenticated original archival photographs with zero AI / zero stock / zero GrabCut.
 * - Smooth horizontal sliding track with scroll snap and touch swipe support.
 * - Previous / Next navigation controls with keyboard and accessibility support.
 * - Category filter pills (All, Haars & Pendants, Chokers, Earrings, Macro Details, Sacred Heirlooms).
 * - Live slide index indicator (e.g. "01 / 20").
 * - High-resolution Lightbox Inspection modal with deep zoom & direct inquiry handoff.
 */

import { GALLERY_PHOTOS } from '../data/galleryPhotos.js';
import { defaultInquiryModal } from './InquiryModal.js';
import { BRAND } from '../config/brand.js';

export class ArchivalGallery {
  constructor(container, options = {}) {
    this.container = typeof container === 'string' ? document.querySelector(container) : container;
    this.photos = options.photos || GALLERY_PHOTOS;
    this.currentFilter = 'All';
    this.activePhotoIndex = 0;
    this.filteredPhotos = [...this.photos];
    this.lightboxEl = null;

    if (this.container) {
      this.init();
    }
  }

  init() {
    this.render();
    this.setupEvents();
    this.setupLightbox();
  }

  render() {
    const categories = ['All', 'Temple Haars & Neckpieces', 'Chokers & Collars', 'Earrings & Jhumkas', 'Craftsmanship & Macro Details', 'Sacred Articles & Heirlooms'];

    this.container.innerHTML = `
      <div class="archival-gallery-wrapper">
        <div class="gallery-header-row">
          <div class="gallery-header-text">
            <span class="section-eyebrow">✦ EST. 1937 ATELIER ARCHIVE ✦</span>
            <h3 class="gallery-main-title">The 1937 Archival Jewellery Gallery</h3>
            <p class="gallery-main-subtitle">
              A curated retrospective of 20 authenticated heirloom creations, traditional temple haars, bridal chokers, and optical macro craftsmanship from our Gadag atelier.
            </p>
          </div>
          <div class="gallery-nav-controls">
            <button class="gallery-nav-btn btn-prev" aria-label="Previous archival photographs" title="Scroll left">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 18 9 12 15 6"></polyline></svg>
            </button>
            <div class="gallery-counter">
              <span class="counter-current">01</span>
              <span class="counter-sep">/</span>
              <span class="counter-total">${String(this.filteredPhotos.length).padStart(2, '0')}</span>
            </div>
            <button class="gallery-nav-btn btn-next" aria-label="Next archival photographs" title="Scroll right">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="9 18 15 12 9 6"></polyline></svg>
            </button>
          </div>
        </div>

        <div class="gallery-filter-bar" role="tablist" aria-label="Gallery category filters">
          ${categories.map(cat => `
            <button class="gallery-filter-pill ${cat === this.currentFilter ? 'active' : ''}" 
                    data-gallery-filter="${cat}" 
                    role="tab" 
                    aria-selected="${cat === this.currentFilter}">
              ${cat === 'All' ? `All Archival (${this.photos.length})` : cat}
            </button>
          `).join('')}
        </div>

        <div class="gallery-slider-viewport" tabindex="0" aria-label="Archival jewellery photo carousel">
          <div class="gallery-slider-track" id="gallery-track">
            ${this.renderSlides()}
          </div>
        </div>

        <div class="gallery-swipe-hint">
          <span>&larr; Drag or swipe to explore all 20 archival photographs &rarr;</span>
        </div>
      </div>
    `;
  }

  renderSlides() {
    return this.filteredPhotos.map((photo, index) => `
      <article class="gallery-slide-card" data-photo-id="${photo.id}" data-index="${index}">
        <div class="gallery-card-media" data-action="open-lightbox" data-id="${photo.id}">
          <div class="gallery-img-container">
            <img src="${photo.sourceImage}" 
                 alt="${photo.title}" 
                 loading="lazy" 
                 class="gallery-slide-img"
                 onerror="this.onerror=null; this.src='${BRAND.logoPath}';">
          </div>
          <span class="gallery-slide-badge">${photo.badge}</span>
          <button class="gallery-expand-btn" aria-label="Inspect high resolution photograph" title="Expand view">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="15 3 21 3 21 9"></polyline><polyline points="9 21 3 21 3 15"></polyline><line x1="21" y1="3" x2="14" y2="10"></line><line x1="3" y1="21" x2="10" y2="14"></line></svg>
          </button>
        </div>
        <div class="gallery-card-body">
          <div class="gallery-card-meta">
            <span class="gallery-card-category">${photo.category}</span>
            <span class="gallery-card-res">${photo.width}&times;${photo.height}px</span>
          </div>
          <h4 class="gallery-card-title">${photo.title}</h4>
          <p class="gallery-card-desc">${photo.description}</p>
          <div class="gallery-card-footer">
            <button class="btn-gallery-inspect" data-action="open-lightbox" data-id="${photo.id}">
              Inspect Photo &rarr;
            </button>
            <button class="btn-gallery-inquire" data-action="gallery-inquire" data-id="${photo.id}">
              Inquire on Design
            </button>
          </div>
        </div>
      </article>
    `).join('');
  }

  setupEvents() {
    const track = this.container.querySelector('#gallery-track');
    const prevBtn = this.container.querySelector('.btn-prev');
    const nextBtn = this.container.querySelector('.btn-next');
    const counterCurrent = this.container.querySelector('.counter-current');

    // Scroll buttons
    if (prevBtn && track) {
      prevBtn.addEventListener('click', () => {
        const card = track.querySelector('.gallery-slide-card');
        const scrollAmount = card ? (card.offsetWidth + 24) * 2 : 400;
        track.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
      });
    }

    if (nextBtn && track) {
      nextBtn.addEventListener('click', () => {
        const card = track.querySelector('.gallery-slide-card');
        const scrollAmount = card ? (card.offsetWidth + 24) * 2 : 400;
        track.scrollBy({ left: scrollAmount, behavior: 'smooth' });
      });
    }

    // Update counter on scroll
    if (track && counterCurrent) {
      let scrollTimer = null;
      track.addEventListener('scroll', () => {
        clearTimeout(scrollTimer);
        scrollTimer = setTimeout(() => {
          const cards = track.querySelectorAll('.gallery-slide-card');
          const trackLeft = track.getBoundingClientRect().left;
          let closestIdx = 0;
          let minDiff = Infinity;
          cards.forEach((card, idx) => {
            const diff = Math.abs(card.getBoundingClientRect().left - trackLeft);
            if (diff < minDiff) {
              minDiff = diff;
              closestIdx = idx;
            }
          });
          counterCurrent.textContent = String(closestIdx + 1).padStart(2, '0');
        }, 80);
      }, { passive: true });
    }

    // Filter pills
    const filterPills = this.container.querySelectorAll('[data-gallery-filter]');
    filterPills.forEach(pill => {
      pill.addEventListener('click', (e) => {
        e.preventDefault();
        const cat = pill.getAttribute('data-gallery-filter');
        this.setFilter(cat);
      });
    });

    // Touch swipe handling
    let touchStartX = 0;
    let touchEndX = 0;
    if (track) {
      track.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
      }, { passive: true });

      track.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        const diff = touchStartX - touchEndX;
        if (Math.abs(diff) > 40) {
          const card = track.querySelector('.gallery-slide-card');
          const step = card ? card.offsetWidth + 16 : 300;
          track.scrollBy({ left: diff > 0 ? step : -step, behavior: 'smooth' });
        }
      }, { passive: true });
    }

    // Lightbox & Inquiry Triggers
    this.container.addEventListener('click', (e) => {
      const inspectBtn = e.target.closest('[data-action="open-lightbox"]');
      if (inspectBtn) {
        e.preventDefault();
        const pid = inspectBtn.getAttribute('data-id');
        this.openLightbox(pid);
        return;
      }

      const inquireBtn = e.target.closest('[data-action="gallery-inquire"]');
      if (inquireBtn) {
        e.preventDefault();
        const pid = inquireBtn.getAttribute('data-id');
        const photo = this.photos.find(p => p.id === pid);
        if (photo) {
          defaultInquiryModal.open({
            id: photo.id,
            name: `${photo.title} (${photo.badge})`,
            category: photo.category,
            metalType: photo.category.includes('Silver') ? '925 Fine Silver' : '22K Gold Archival Design',
            sourceImage: photo.sourceImage
          });
        }
      }
    });

    // Keyboard navigation
    track?.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') {
        nextBtn?.click();
      } else if (e.key === 'ArrowLeft') {
        prevBtn?.click();
      }
    });
  }

  setFilter(category) {
    this.currentFilter = category;
    if (category === 'All') {
      this.filteredPhotos = [...this.photos];
    } else {
      this.filteredPhotos = this.photos.filter(p => p.category === category);
    }
    this.render();
    this.setupEvents();
  }

  setupLightbox() {
    let lb = document.getElementById('archival-gallery-lightbox');
    if (!lb) {
      lb = document.createElement('div');
      lb.id = 'archival-gallery-lightbox';
      lb.className = 'gallery-lightbox-backdrop hidden';
      lb.setAttribute('role', 'dialog');
      lb.setAttribute('aria-modal', 'true');
      lb.setAttribute('aria-label', 'Archival Photograph High Resolution Inspector');
      document.body.appendChild(lb);
    }
    this.lightboxEl = lb;

    this.lightboxEl.addEventListener('click', (e) => {
      if (e.target === this.lightboxEl || e.target.closest('.lightbox-close-btn')) {
        this.closeLightbox();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !this.lightboxEl.classList.contains('hidden')) {
        this.closeLightbox();
      }
    });
  }

  openLightbox(photoId) {
    const photo = this.photos.find(p => p.id === photoId);
    if (!photo || !this.lightboxEl) return;

    this.lightboxEl.innerHTML = `
      <div class="gallery-lightbox-dialog">
        <button class="lightbox-close-btn" aria-label="Close high-res inspector">&times;</button>
        <div class="lightbox-content-grid">
          <div class="lightbox-img-wrapper">
            <img src="${photo.sourceImage}" alt="${photo.title}" class="lightbox-hero-img">
            <span class="lightbox-zoom-hint">Original 100% Client Photograph &bull; Unaltered Fidelity</span>
          </div>
          <div class="lightbox-details-col">
            <div class="lightbox-brand-tag">KASHINATHSA Y. KHATAWATE JEWELLERS &bull; GADAG</div>
            <span class="lightbox-badge">${photo.badge}</span>
            <h3 class="lightbox-title">${photo.title}</h3>
            <div class="lightbox-specs">
              <div class="spec-row">
                <span class="spec-label">Archive ID</span>
                <span class="spec-val">${photo.id}</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Category</span>
                <span class="spec-val">${photo.category}</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Resolution</span>
                <span class="spec-val">${photo.width} &times; ${photo.height} px (Full Uncompressed)</span>
              </div>
              <div class="spec-row">
                <span class="spec-label">Provenance</span>
                <span class="spec-val">Atelier Archive (${photo.originalRaw})</span>
              </div>
            </div>
            <p class="lightbox-desc">${photo.description}</p>
            <div class="lightbox-tags">
              ${photo.tags.map(t => `<span class="tag-pill">#${t}</span>`).join('')}
            </div>
            <div class="lightbox-actions">
              <button class="btn-lightbox-inquire" id="btn-lb-inquire">
                Inquire About Bespoke Crafting &rarr;
              </button>
              <button class="btn-lightbox-wa" id="btn-lb-wa">
                Consult via WhatsApp
              </button>
            </div>
          </div>
        </div>
      </div>
    `;

    const inqBtn = this.lightboxEl.querySelector('#btn-lb-inquire');
    inqBtn?.addEventListener('click', () => {
      this.closeLightbox();
      defaultInquiryModal.open({
        id: photo.id,
        name: `${photo.title} (${photo.badge})`,
        category: photo.category,
        metalType: photo.category.includes('Silver') ? '925 Fine Silver' : '22K Gold Archival Design',
        sourceImage: photo.sourceImage
      });
    });

    const waBtn = this.lightboxEl.querySelector('#btn-lb-wa');
    waBtn?.addEventListener('click', () => {
      const msg = encodeURIComponent(`Namaskara, I am interested in inquiring about the archival design "${photo.title}" (Ref: ${photo.id}) from the KYK 1937 Archive.`);
      window.open(`https://wa.me/919448753791?text=${msg}`, '_blank');
    });

    this.lightboxEl.classList.remove('hidden');
    document.body.classList.add('modal-open');
  }

  closeLightbox() {
    if (this.lightboxEl) {
      this.lightboxEl.classList.add('hidden');
      document.body.classList.remove('modal-open');
    }
  }
}
