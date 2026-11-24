/**
 * Product Catalogue Service
 * Encapsulates all catalogue data fetching, filtering, and validation logic.
 * Avoids hardcoding product logic into UI components.
 */

import { VERIFIED_PRODUCTS, VERIFIED_SILVER_PRODUCTS, ALL_PRODUCTS, CATEGORIES } from '../data/products.js';

export class ProductService {
  constructor(initialProducts = ALL_PRODUCTS) {
    this.products = initialProducts;
    this.goldProducts = VERIFIED_PRODUCTS;
    this.silverProducts = VERIFIED_SILVER_PRODUCTS;
    this.categories = CATEGORIES;
  }

  /**
   * Returns all verified products (Gold and Silver).
   * @returns {Array} List of verified products
   */
  getAllProducts() {
    return [...this.products];
  }

  /**
   * Returns all 22K Gold heritage products.
   * @returns {Array} List of gold products
   */
  getGoldProducts() {
    return this.products.filter(p => !p.metalType || p.metalType.toLowerCase() === 'gold');
  }

  /**
   * Returns all Fine Silver products.
   * @returns {Array} List of silver products
   */
  getSilverProducts() {
    return this.products.filter(p => p.metalType && p.metalType.toLowerCase() === 'silver');
  }

  /**
   * Filter products by metal type.
   * @param {string} metal - 'Gold' or 'Silver'
   * @returns {Array}
   */
  getProductsByMetal(metal) {
    if (!metal || metal.toLowerCase() === 'all') return this.getAllProducts();
    if (metal.toLowerCase() === 'silver') return this.getSilverProducts();
    return this.getGoldProducts();
  }

  /**
   * Find a single product by unique ID.
   * @param {string} id - Product ID (e.g. 'PROD-001', 'SILV-001')
   * @returns {Object|null}
   */
  getProductById(id) {
    if (!id) return null;
    const cleanId = id.trim().toUpperCase();
    return this.products.find(p => p.id.toUpperCase() === cleanId) || null;
  }

  /**
   * Filter products by category and optional metal type.
   * @param {string} category 
   * @param {string|null} metal
   * @returns {Array}
   */
  getProductsByCategory(category, metal = null) {
    let pool = metal ? this.getProductsByMetal(metal) : this.products;

    if (!category || category === this.categories.ALL || category === 'All' || category === 'All Jewellery') {
      return pool;
    }

    if (category === this.categories.GOLD || category === '22K Gold Vault' || category === 'Gold') {
      return this.getGoldProducts();
    }

    if (category === this.categories.SILVER || category === 'Fine Silver Vault' || category === 'Silver') {
      return this.getSilverProducts();
    }

    return pool.filter(p => p.category.toLowerCase() === category.toLowerCase());
  }

  /**
   * Filter products by tag.
   * @param {string} tag
   * @returns {Array}
   */
  getProductsByTag(tag) {
    if (!tag) return this.getAllProducts();
    const cleanTag = tag.trim().toLowerCase();
    return this.products.filter(p => 
      p.tags && p.tags.some(t => t.toLowerCase() === cleanTag)
    );
  }

  /**
   * Retrieve list of unique categories available in the catalogue.
   * @param {string|null} metal - Optional metal scope ('Gold', 'Silver', null)
   * @returns {Array<string>}
   */
  getCategories(metal = null) {
    const pool = metal ? this.getProductsByMetal(metal) : this.products;
    const set = new Set();
    pool.forEach(p => {
      if (p.category) set.add(p.category);
    });
    return [this.categories.ALL, ...Array.from(set)];
  }

  /**
   * Retrieve all unique tags in the catalogue.
   * @returns {Array<string>}
   */
  getAllTags() {
    const set = new Set();
    this.products.forEach(p => {
      if (Array.isArray(p.tags)) {
        p.tags.forEach(t => set.add(t));
      }
    });
    return Array.from(set);
  }

  /**
   * Simple client-side search across name, description, and tags.
   * @param {string} query 
   * @returns {Array}
   */
  search(query) {
    if (!query || !query.trim()) return this.getAllProducts();
    const q = query.trim().toLowerCase();
    return this.products.filter(p => {
      const matchName = p.name.toLowerCase().includes(q);
      const matchShortDesc = p.shortDescription.toLowerCase().includes(q);
      const matchCategory = p.category.toLowerCase().includes(q);
      const matchTags = p.tags && p.tags.some(t => t.toLowerCase().includes(q));
      return matchName || matchShortDesc || matchCategory || matchTags;
    });
  }

  /**
   * Validates product object structure against required schema rules.
   * @param {Object} product 
   * @returns {{ valid: boolean, errors: string[] }}
   */
  static validateProductSchema(product) {
    const errors = [];
    if (!product) return { valid: false, errors: ['Product is null or undefined'] };
    if (!product.id) errors.push('Missing product.id');
    if (!product.name) errors.push('Missing product.name');
    if (!product.category) errors.push('Missing product.category');
    if (!product.images || typeof product.images !== 'object') {
      errors.push('Missing or invalid product.images dictionary');
    } else {
      if (!product.images.listing) errors.push('Missing images.listing');
      if (!product.images.gallery) errors.push('Missing images.gallery');
      if (!product.images.detail) errors.push('Missing images.detail');
    }
    if (product.price !== null && typeof product.price !== 'number') {
      errors.push('Invalid price field (must be null or numeric)');
    }
    return {
      valid: errors.length === 0,
      errors
    };
  }
}

export const defaultProductService = new ProductService();
export default defaultProductService;
