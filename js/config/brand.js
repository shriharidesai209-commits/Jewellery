/**
 * Kashinathsa Y. Khatawate Jewellers (KYK Since 1937)
 * Centralized Brand Configuration Module
 * 
 * Defines official brand identity, typography, contact details,
 * WhatsApp actions, and social media references.
 */

export const BRAND = {
  // Official Brand Names
  storeName: "Kashinathsa Y. Khatawate Jewellers",
  shortName: "KYK Jewellers",
  legalName: "M/s. Kashinathasa Y. Khatawate & Sons Jewellery Merchants",
  monogram: "KYK",
  establishedYear: 1937,
  
  // Tagline & Positioning
  tagline: "Haute Joaillerie · 22K Heritage Since 1937",
  subheading: "Heritage 22K Gold & Temple Jewellery Vault · Gadag",
  
  // Location & Certifications
  city: "Gadag",
  state: "Karnataka",
  country: "India",
  pincode: "582 101",
  address: "Javali Bazar, Gadag - 582 101, Karnataka",
  gstin: "29AJTPK8796P1ZL",
  hallmark: "BIS 916 Hallmarked Pure 22K Gold",
  
  // Brand Assets
  logoPath: "assets/branding/IMG_0941.PNG",
  logoAlt: "Kashinathsa Y. Khatawate Jewellers Official Emblem Since 1937",
  instagramQrPath: "assets/branding/IMG_0942.JPG.jpeg",
  instagramQrAlt: "Scan to visit @k.y.khatawate_jewellers_gadag on Instagram",
  
  // Social Media
  instagramHandle: "@k.y.khatawate_jewellers_gadag",
  instagramUrl: "https://www.instagram.com/k.y.khatawate_jewellers_gadag/",
  
  // Verified Store Contacts
  contacts: [
    {
      name: "Venkatesh",
      role: "Store Proprietor & Senior Jeweller",
      displayPhone: "+91 94487 53791",
      rawNumber: "9448753791",
      telLink: "tel:+919448753791",
      // WhatsApp requires international format digits only, no + or spaces
      waNumber: "919448753791",
      waLink: "https://wa.me/919448753791"
    },
    {
      name: "Prajwal",
      role: "Client Relations & Bespoke Consultations",
      displayPhone: "+91 91489 96998",
      rawNumber: "9148996998",
      telLink: "tel:+919148996998",
      // WhatsApp requires international format digits only, no + or spaces
      waNumber: "919148996998",
      waLink: "https://wa.me/919148996998"
    }
  ]
};

export default BRAND;
