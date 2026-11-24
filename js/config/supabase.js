/**
 * Supabase Frontend Configuration
 * Kashinathsa Y. Khatawate Jewellers (KYK Since 1937)
 * 
 * Secure configuration for client-side Supabase integration.
 * In production, values can be provided via window.SUPABASE_CONFIG or replaced during CI/CD.
 */

export const SUPABASE_CONFIG = {
  // Public project URL (e.g. "https://xyzcompany.supabase.co")
  url: (typeof window !== 'undefined' && window.SUPABASE_CONFIG?.url) ? window.SUPABASE_CONFIG.url : "https://your-project.supabase.co",

  // Public Anonymous Key (safe for browser frontend; protected by RLS)
  // NEVER use the service_role key here!
  anonKey: (typeof window !== 'undefined' && window.SUPABASE_CONFIG?.anonKey) ? window.SUPABASE_CONFIG.anonKey : "your-anon-key-placeholder",

  // Optional: Deployed Supabase Edge Function URL for server-validated inquiries + Resend email alerts
  edgeFunctionUrl: (typeof window !== 'undefined' && window.SUPABASE_CONFIG?.edgeFunctionUrl) ? window.SUPABASE_CONFIG.edgeFunctionUrl : "",

  // Indicates whether live credentials have been supplied
  isConfigured: function () {
    return (
      this.url &&
      this.anonKey &&
      !this.url.includes("your-project.supabase.co") &&
      !this.anonKey.includes("placeholder")
    );
  }
};

export default SUPABASE_CONFIG;
