/**
 * Main Application Bootstrap (Stage 2 Luxury Storefront)
 * Coordinates the storefront experience, collection filters, search modal, viewing drawer, and product details.
 * Kashinathsa Y. Khatawate Jewellers (KYK Since 1937)
 */

import { ProductGrid } from './components/ProductGrid.js';
import { defaultProductService } from './services/productService.js';
import { defaultProductModal } from './components/ProductModal.js';
import { defaultViewingDrawer } from './components/ViewingDrawer.js';
import { defaultSearchModal } from './components/SearchModal.js';
import { defaultInquiryModal } from './components/InquiryModal.js';
import { ArchivalGallery } from './components/ArchivalGallery.js';
import { BRAND } from './config/brand.js';

document.addEventListener('DOMContentLoaded', () => {
  const gridContainer = document.getElementById('catalogue-app');
  let gridInstance = null;

  // Initialize the Archival Jewellery Gallery component (20 authenticated photos)
  const galleryApp = document.getElementById('archival-gallery-app');
  let galleryInstance = null;
  if (galleryApp) {
    galleryInstance = new ArchivalGallery(galleryApp);
  }

  // Initialize Private Viewing Badge
  const badgeEl = document.getElementById('viewing-badge-count');
  if (badgeEl) {
    defaultViewingDrawer.setBadgeElement(badgeEl);
  }

  // Initialize the reusable ProductGrid component
  if (gridContainer) {
    gridInstance = new ProductGrid(gridContainer, {
      productService: defaultProductService,
      initialCategory: 'All Jewellery',
      initialMetal: 'all',
      onViewDetails: (product) => {
        defaultProductModal.open(product);
      },
      onInquire: (product) => {
        defaultInquiryModal.open(product);
      }
    });
  }

  // Helper function for offset smooth scrolling under sticky header
  function scrollToElementWithOffset(elementId, offset = 90) {
    const el = document.getElementById(elementId);
    if (el) {
      const elementPosition = el.getBoundingClientRect().top;
      const offsetPosition = elementPosition + window.pageYOffset - offset;
      window.scrollTo({
        top: Math.max(0, offsetPosition),
        behavior: 'smooth'
      });
    }
  }

  // Hook up Direct Inquiry Triggers across all cards, spotlights, CTAs, and navigation
  const inquiryTriggers = document.querySelectorAll('[data-action="open-inquiry"], [data-action="inquire"]');
  inquiryTriggers.forEach(btn => {
    // Only bind if inside static DOM (ProductCard binds its own internal listener)
    if (!btn.closest('.catalogue-grid')) {
      btn.addEventListener('click', (e) => {
        e.preventDefault();
        const prodId = btn.getAttribute('data-product-id') || btn.getAttribute('data-id');
        const prod = prodId ? defaultProductService.getProductById(prodId) : null;
        defaultInquiryModal.open(prod);
      });
    }
  });

  // Hook up Search Triggers
  const searchTriggers = document.querySelectorAll('[data-action="open-search"]');
  searchTriggers.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      defaultSearchModal.open();
    });
  });

  // Hook up Private Viewing Drawer Triggers
  const viewingTriggers = document.querySelectorAll('[data-action="open-viewing-drawer"]');
  viewingTriggers.forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      defaultViewingDrawer.open();
    });
  });

  // Hook up Collection Discovery Cards to Filter Grid
  const collectionLinks = document.querySelectorAll('[data-collection-filter]');
  collectionLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetCat = link.getAttribute('data-collection-filter');
      if (gridInstance) {
        gridInstance.setCategory(targetCat, true);
      }
      closeMobileMenu();
    });
  });

  // Hook up Metal Filter Links (e.g. Fine Silver Vault, 22K Gold Heritage, All Masterpieces)
  const metalLinks = document.querySelectorAll('[data-metal-filter]');
  metalLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetMetal = link.getAttribute('data-metal-filter');
      if (gridInstance) {
        gridInstance.setMetal(targetMetal.toLowerCase(), true);
      }
      closeMobileMenu();
    });
  });

  // Smooth scroll links
  const scrollLinks = document.querySelectorAll('[data-scroll-to]');
  scrollLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      e.preventDefault();
      const targetId = link.getAttribute('data-scroll-to');
      if (targetId === 'vault-section' && gridInstance) {
        gridInstance.setMetal('all', true);
      } else {
        scrollToElementWithOffset(targetId, 90);
      }
      closeMobileMenu();
    });
  });

  // Hero Featured Piece Inspection
  const heroInspectBtn = document.getElementById('btn-hero-inspect-piece');
  if (heroInspectBtn) {
    heroInspectBtn.addEventListener('click', () => {
      const p4 = defaultProductService.getProductById('PROD-004');
      if (p4) defaultProductModal.open(p4, 'featured');
    });
  }

  // Editorial Craftsmanship Inspection Triggers
  const editorialInspectBtns = document.querySelectorAll('[data-inspect-id]');
  editorialInspectBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const pid = btn.getAttribute('data-inspect-id');
      const angle = btn.getAttribute('data-inspect-angle') || 'detail';
      const prod = defaultProductService.getProductById(pid);
      if (prod) defaultProductModal.open(prod, angle);
    });
  });

  // Mobile Menu Toggle
  const mobileMenuToggle = document.getElementById('btn-mobile-menu');
  const mobileNavDrawer = document.getElementById('mobile-nav-drawer');
  const mobileNavClose = document.getElementById('btn-close-mobile-nav');

  function openMobileMenu() {
    if (mobileNavDrawer) {
      mobileNavDrawer.classList.remove('hidden');
      document.body.classList.add('modal-open');
    }
  }

  function closeMobileMenu() {
    if (mobileNavDrawer) {
      mobileNavDrawer.classList.add('hidden');
      document.body.classList.remove('modal-open');
    }
  }

  if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', openMobileMenu);
  }
  if (mobileNavClose) {
    mobileNavClose.addEventListener('click', closeMobileMenu);
  }

  // Header scroll appearance
  const header = document.querySelector('.site-header');
  window.addEventListener('scroll', () => {
    if (window.scrollY > 40) {
      header?.classList.add('scrolled');
    } else {
      header?.classList.remove('scrolled');
    }
  }, { passive: true });

  console.log(`✦ ${BRAND.storeName} (${BRAND.shortName} ${BRAND.establishedYear}) Storefront initialized. 7 verified masterpieces (5 Gold + 2 Silver) ready for private inspection.`);
});
