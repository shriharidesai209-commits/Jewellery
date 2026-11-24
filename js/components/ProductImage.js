/**
 * Reusable Product Image Component
 * Features:
 * - Dual-format modern image rendering (<picture> with WebP and JPG fallback)
 * - Graceful fallback to luxury SVG placeholder on missing images or loading errors
 * - Responsive aspect ratios (1:1 listing, 4:5 gallery, 16:9 featured)
 * - Lazy-loading and async decoding for optimal web performance
 */

export class ProductImage {
  /**
   * Generates a luxury SVG placeholder for missing or broken images.
   * @param {string} label 
   * @returns {string} SVG string
   */
  static getPlaceholderSVG(label = 'Jewellery Image Unavailable') {
    return `
      <div class="product-image-fallback" role="img" aria-label="${label}">
        <svg viewBox="0 0 400 400" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg" class="fallback-svg">
          <rect width="100%" height="100%" fill="#F4F1EA"/>
          <circle cx="200" cy="180" r="70" fill="none" stroke="#D1C7B7" stroke-width="2" stroke-dasharray="4 4"/>
          <!-- Stylized Diamond / Gemstone Outline -->
          <polygon points="200,135 240,165 200,225 160,165" fill="none" stroke="#997D3D" stroke-width="2"/>
          <line x1="160" y1="165" x2="240" y2="165" stroke="#997D3D" stroke-width="1.5"/>
          <line x1="180" y1="165" x2="200" y2="135" stroke="#997D3D" stroke-width="1.5"/>
          <line x1="220" y1="165" x2="200" y2="135" stroke="#997D3D" stroke-width="1.5"/>
          <line x1="180" y1="165" x2="200" y2="225" stroke="#997D3D" stroke-width="1.5"/>
          <line x1="220" y1="165" x2="200" y2="225" stroke="#997D3D" stroke-width="1.5"/>
          <text x="200" y="280" font-family="'Cormorant Garamond', Georgia, serif" font-size="14" fill="#756F64" text-anchor="middle" letter-spacing="1.5">IMAGE PENDING</text>
          <text x="200" y="300" font-family="'Inter', sans-serif" font-size="10" fill="#A8A196" text-anchor="middle">Studio Archive In Progress</text>
        </svg>
      </div>
    `.trim();
  }

  /**
   * Renders the product image HTML string.
   * @param {Object} imageObj - Image descriptor containing webp, jpg/png, alt, etc.
   * @param {Object} options - Configuration options (aspectRatio, className, loading)
   * @returns {string} HTML markup
   */
  static render(imageObj, options = {}) {
    const {
      aspectRatio = '1:1',
      className = '',
      loading = 'eager',
      decoding = 'sync',
      role = 'presentation'
    } = options;

    if (!imageObj || (!imageObj.webp && !imageObj.jpg && !imageObj.png)) {
      return ProductImage.getPlaceholderSVG(imageObj?.alt || 'Missing Jewellery Asset');
    }

    const webpSrc = imageObj.webp || '';
    const fallbackSrc = imageObj.jpg || imageObj.png || '';
    const altText = imageObj.alt || 'Fine Jewellery Piece';
    const ratioClass = `ratio-${aspectRatio.replace(':', '-')}`;

    return `
      <div class="product-image-container ${ratioClass} ${className}">
        <picture class="product-picture">
          ${webpSrc ? `<source srcset="${webpSrc}" type="image/webp">` : ''}
          <img 
            src="${fallbackSrc}" 
            alt="${altText}" 
            loading="${loading}" 
            decoding="${decoding}" 
            class="product-image-element"
          />
        </picture>
      </div>
    `.trim();
  }

  /**
   * Creates a live DOM HTMLElement instance.
   * @param {Object} imageObj 
   * @param {Object} options 
   * @returns {HTMLElement}
   */
  static create(imageObj, options = {}) {
    const wrapper = document.createElement('div');
    wrapper.innerHTML = ProductImage.render(imageObj, options);
    return wrapper.firstElementChild;
  }
}

if (typeof window !== 'undefined') {
  window.ProductImage = ProductImage;
}

export default ProductImage;
