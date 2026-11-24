// ============================================================================
// Supabase Edge Function: submit-inquiry
// Kashinathsa Y. Khatawate Jewellers (KYK Since 1937)
// Handles server-side validation, Supabase DB insert, and Resend email alerts
// Supports both Individual Product Inquiries & Multi-Piece Salon Viewing Requests
// ============================================================================

import { serve } from "https://deno.land/std@0.168.0/http/server.ts";
import { createClient } from "https://esm.sh/@supabase/supabase-js@2.39.0";

const corsHeaders = {
  "Access-Control-Allow-Origin": "*",
  "Access-Control-Allow-Headers": "authorization, x-client-info, apikey, content-type",
  "Access-Control-Allow-Methods": "POST, OPTIONS",
};

interface SelectedProduct {
  id: string;
  sku?: string;
  name: string;
  category?: string;
  metalType?: string;
  priceDisplay?: string;
  thumbnail?: string;
}

interface InquiryPayload {
  inquiry_type?: "individual_product" | "viewing_appointment";
  customer_name: string;
  email: string;
  phone: string;
  preferred_location?: string;
  product_id?: string;
  product_name?: string;
  product_sku?: string;
  product_category?: string;
  product_metal?: string;
  selected_products?: SelectedProduct[];
  message?: string;
  honeypot?: string; // Bot trap
}

serve(async (req: Request) => {
  // 1. Handle CORS Preflight
  if (req.method === "OPTIONS") {
    return new Response("ok", { headers: corsHeaders });
  }

  if (req.method !== "POST") {
    return new Response(JSON.stringify({ error: "Method not allowed" }), {
      status: 405,
      headers: { ...corsHeaders, "Content-Type": "application/json" },
    });
  }

  try {
    const body: InquiryPayload = await req.json();

    // 2. Bot / Spam Protection (Honeypot field)
    if (body.honeypot && body.honeypot.trim() !== "") {
      return new Response(
        JSON.stringify({ success: true, message: "Inquiry received" }),
        { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const inquiry_type = body.inquiry_type || "individual_product";
    const customer_name = (body.customer_name || "").trim();
    const email = (body.email || "").trim().toLowerCase();
    const phone = (body.phone || "").trim();
    const preferred_location = (body.preferred_location || "").trim();
    const message = (body.message || "").trim();

    // 3. Server-side Validation
    const errors: Record<string, string> = {};

    if (!customer_name || customer_name.length < 2) {
      errors.customer_name = "Customer name must be at least 2 characters.";
    }

    const emailRegex = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;
    if (!email || !emailRegex.test(email)) {
      errors.email = "Please provide a valid email address.";
    }

    const phoneRegex = /^[0-9+() -]{7,20}$/;
    if (!phone || !phoneRegex.test(phone)) {
      errors.phone = "Please provide a valid phone or WhatsApp number (at least 7 digits).";
    }

    let finalProductId = body.product_id || "";
    let finalProductName = body.product_name || "";
    const selected_products = body.selected_products || [];

    if (inquiry_type === "viewing_appointment") {
      if (!Array.isArray(selected_products) || selected_products.length === 0) {
        errors.selected_products = "At least one jewellery piece must be selected for a viewing appointment.";
      }
      if (!finalProductId) {
        finalProductId = `VIEWING-${selected_products.length}-PIECES`;
      }
      if (!finalProductName) {
        finalProductName = `Private Viewing Selection (${selected_products.length} Pieces)`;
      }
    } else {
      if (!finalProductId || !finalProductName) {
        errors.product = "Product reference (ID and name) is required.";
      }
      if (!message || message.length < 5) {
        errors.message = "Inquiry message must be at least 5 characters.";
      }
    }

    if (Object.keys(errors).length > 0) {
      return new Response(JSON.stringify({ error: "Validation failed", details: errors }), {
        status: 400,
        headers: { ...corsHeaders, "Content-Type": "application/json" },
      });
    }

    // 4. Initialize Supabase Client
    const supabaseUrl = Deno.env.get("SUPABASE_URL");
    const supabaseServiceKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || Deno.env.get("SUPABASE_ANON_KEY");

    if (!supabaseUrl || !supabaseServiceKey) {
      return new Response(
        JSON.stringify({ error: "Supabase environment variables not configured on server" }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const supabase = createClient(supabaseUrl, supabaseServiceKey);

    // 5. Insert Inquiry into Database
    const { data: inquiryData, error: dbError } = await supabase
      .from("inquiries")
      .insert([
        {
          inquiry_type,
          customer_name,
          email,
          phone,
          preferred_location: preferred_location || null,
          product_id: finalProductId,
          product_name: finalProductName,
          selected_products: inquiry_type === "viewing_appointment" ? selected_products : [],
          message: message || (inquiry_type === "viewing_appointment" ? `Private salon consultation requested for ${selected_products.length} pieces at ${preferred_location || 'Gadag Boutique'}` : ""),
          status: "new",
          notification_status: "pending",
          metadata: {
            user_agent: req.headers.get("user-agent") || "unknown",
            submitted_at: new Date().toISOString(),
          },
        },
      ])
      .select("id, created_at, status")
      .single();

    if (dbError) {
      console.error("Database insert error:", dbError);
      return new Response(
        JSON.stringify({ error: "Failed to persist inquiry in database", details: dbError.message }),
        { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
      );
    }

    const inquiryId = inquiryData.id;
    const createdAt = inquiryData.created_at;

    // 6. Owner Email Notification via Resend
    const resendApiKey = Deno.env.get("RESEND_API_KEY");
    const ownerEmail = Deno.env.get("OWNER_NOTIFICATION_EMAIL") || "kykjewellers1937@gmail.com";
    const senderEmail = Deno.env.get("NOTIFICATION_FROM_EMAIL") || "inquiries@kykjewellers.com";

    let notificationStatus = "unconfigured";

    if (resendApiKey) {
      try {
        const formattedDate = new Date(createdAt).toLocaleString("en-IN", {
          timeZone: "Asia/Kolkata",
          dateStyle: "full",
          timeStyle: "short",
        });

        const isViewing = inquiry_type === "viewing_appointment";
        const emailSubject = isViewing
          ? `[KYK Salon Viewing Request] ${selected_products.length} Pieces — from ${customer_name}`
          : `[KYK Inquiry] ${finalProductName} — from ${customer_name}`;

        const viewingItemsHtml = isViewing
          ? `
            <h4 style="color: #1A1A1A; margin-top: 18px; margin-bottom: 8px;">Selected Masterpieces (${selected_products.length}):</h4>
            <table style="width: 100%; border-collapse: collapse; margin-bottom: 16px; font-size: 13px;">
              <thead>
                <tr style="background: #EAE5DB; text-align: left;">
                  <th style="padding: 8px; border: 1px solid #CCC;">SKU</th>
                  <th style="padding: 8px; border: 1px solid #CCC;">Masterpiece Name</th>
                  <th style="padding: 8px; border: 1px solid #CCC;">Metal / Category</th>
                </tr>
              </thead>
              <tbody>
                ${selected_products
                  .map(
                    (p) => `
                  <tr>
                    <td style="padding: 8px; border: 1px solid #CCC; font-family: monospace;">${p.sku || p.id}</td>
                    <td style="padding: 8px; border: 1px solid #CCC; font-weight: bold; color: #997D3D;">${p.name}</td>
                    <td style="padding: 8px; border: 1px solid #CCC;">${p.metalType || "22K Gold"} &middot; ${p.category || "Jewellery"}</td>
                  </tr>`
                  )
                  .join("")}
              </tbody>
            </table>
          `
          : "";

        const emailHtml = `
          <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 24px; border: 1px solid #997D3D; background: #FAF8F5;">
            <div style="text-align: center; border-bottom: 2px solid #997D3D; padding-bottom: 16px;">
              <h2 style="color: #1A1A1A; margin: 0; letter-spacing: 2px;">KASHINATHSA Y. KHATAWATE JEWELLERS</h2>
              <p style="color: #997D3D; margin: 4px 0 0 0; font-size: 13px; font-weight: bold;">HAUTE JOAILLERIE &middot; SINCE 1937 &middot; GADAG</p>
            </div>
            
            <h3 style="color: #1A1A1A; margin-top: 24px;">
              ${isViewing ? "✦ New Private Viewing Consultation Request" : "✦ New Customer Product Inquiry"}
            </h3>
            <p style="font-size: 14px; color: #555;">
              ${isViewing 
                ? "A client has scheduled a private viewing appointment for their curated jewellery selection:" 
                : "An exclusive customer inquiry was submitted through the online vault storefront:"}
            </p>
            
            <table style="width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px;">
              <tr style="background: #F0EDE6;">
                <td style="padding: 10px; font-weight: bold; width: 35%;">Inquiry Reference ID:</td>
                <td style="padding: 10px; font-family: monospace;">${inquiryId}</td>
              </tr>
              <tr>
                <td style="padding: 10px; font-weight: bold;">Inquiry Type:</td>
                <td style="padding: 10px;">${isViewing ? "Private Salon Viewing Appointment" : "Individual Piece Inquiry"}</td>
              </tr>
              <tr style="background: #F0EDE6;">
                <td style="padding: 10px; font-weight: bold;">Submission Time:</td>
                <td style="padding: 10px;">${formattedDate} (IST)</td>
              </tr>
              ${isViewing ? `
              <tr>
                <td style="padding: 10px; font-weight: bold;">Preferred Location:</td>
                <td style="padding: 10px; color: #997D3D; font-weight: bold;">${preferred_location || "Gadag Boutique"}</td>
              </tr>
              ` : `
              <tr>
                <td style="padding: 10px; font-weight: bold;">Interested Piece:</td>
                <td style="padding: 10px; color: #997D3D; font-weight: bold;">${finalProductName} (${finalProductId})</td>
              </tr>
              `}
              <tr style="background: #F0EDE6;">
                <td style="padding: 10px; font-weight: bold;">Customer Name:</td>
                <td style="padding: 10px;">${customer_name}</td>
              </tr>
              <tr>
                <td style="padding: 10px; font-weight: bold;">Email Address:</td>
                <td style="padding: 10px;"><a href="mailto:${email}">${email}</a></td>
              </tr>
              <tr style="background: #F0EDE6;">
                <td style="padding: 10px; font-weight: bold;">Phone / WhatsApp:</td>
                <td style="padding: 10px;">
                  <a href="tel:${phone}">${phone}</a> | 
                  <a href="https://wa.me/${phone.replace(/[^0-9]/g, "")}">Open WhatsApp</a>
                </td>
              </tr>
              <tr>
                <td style="padding: 10px; font-weight: bold; vertical-align: top;">Client Message:</td>
                <td style="padding: 10px; white-space: pre-wrap;">${message || "No special message entered"}</td>
              </tr>
            </table>

            ${viewingItemsHtml}

            <div style="margin-top: 24px; padding: 12px; background: #FFFFFF; border-left: 4px solid #997D3D; font-size: 13px; color: #666;">
              <strong>Store Action:</strong> Please contact the client within 24 hours at <strong>${phone}</strong> to confirm their confidential viewing.
            </div>

            <p style="font-size: 11px; color: #999; margin-top: 24px; text-align: center;">
              M/s. Kashinathsa Y. Khatawate Jewellers &middot; Est. 1937 &middot; Javali Bazar, Gadag, Karnataka
            </p>
          </div>
        `;

        const resendRes = await fetch("https://api.resend.com/emails", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${resendApiKey}`,
          },
          body: JSON.stringify({
            from: senderEmail,
            to: [ownerEmail],
            reply_to: email,
            subject: emailSubject,
            html: emailHtml,
          }),
        });

        if (resendRes.ok) {
          notificationStatus = "delivered";
        } else {
          notificationStatus = "failed";
          const errText = await resendRes.text();
          console.warn("Resend email delivery failed:", errText);
        }
      } catch (emailErr) {
        notificationStatus = "failed";
        console.warn("Resend fetch exception:", emailErr);
      }

      await supabase
        .from("inquiries")
        .update({ notification_status: notificationStatus })
        .eq("id", inquiryId);
    } else {
      console.log("RESEND_API_KEY is not set. Inquiry saved with notification_status='unconfigured'.");
    }

    // 7. Successful Response
    return new Response(
      JSON.stringify({
        success: true,
        inquiry_id: inquiryId,
        inquiry_type,
        created_at: createdAt,
        product_id: finalProductId,
        product_name: finalProductName,
        notification_status: notificationStatus,
        message: "Your inquiry has been successfully recorded in our vault system. A senior jeweller from Kashinathsa Y. Khatawate Jewellers will be in touch shortly.",
      }),
      { status: 200, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  } catch (err) {
    console.error("Unexpected Edge Function error:", err);
    return new Response(
      JSON.stringify({ error: "Internal server error processing inquiry", message: String(err) }),
      { status: 500, headers: { ...corsHeaders, "Content-Type": "application/json" } }
    );
  }
});
