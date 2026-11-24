-- ============================================================================
-- Kashinathsa Y. Khatawate Jewellers (KYK Since 1937)
-- Database Schema: Customer Inquiries & Lead Management
-- Migration: 20261124_create_inquiries_table.sql
-- Supports both Individual Product Inquiries and Multi-Piece Viewing Appointments
-- ============================================================================

-- 1. Create Inquiries Table
CREATE TABLE IF NOT EXISTS public.inquiries (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT timezone('utc'::text, now()),
    inquiry_type TEXT NOT NULL DEFAULT 'individual_product' CHECK (inquiry_type IN ('individual_product', 'viewing_appointment')),
    customer_name TEXT NOT NULL CHECK (char_length(trim(customer_name)) >= 2),
    email TEXT NOT NULL CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'),
    phone TEXT NOT NULL CHECK (char_length(trim(phone)) >= 7),
    preferred_location TEXT,
    product_id TEXT,
    product_name TEXT,
    selected_products JSONB DEFAULT '[]'::jsonb,
    message TEXT,
    status TEXT NOT NULL DEFAULT 'new' CHECK (status IN ('new', 'contacted', 'appointment_scheduled', 'closed', 'spam')),
    notification_status TEXT NOT NULL DEFAULT 'pending' CHECK (notification_status IN ('pending', 'delivered', 'failed', 'unconfigured')),
    metadata JSONB DEFAULT '{}'::jsonb
);

-- If table already exists in an earlier schema, safely add missing columns
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'inquiries' AND column_name = 'inquiry_type') THEN
        ALTER TABLE public.inquiries ADD COLUMN inquiry_type TEXT NOT NULL DEFAULT 'individual_product' CHECK (inquiry_type IN ('individual_product', 'viewing_appointment'));
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'inquiries' AND column_name = 'preferred_location') THEN
        ALTER TABLE public.inquiries ADD COLUMN preferred_location TEXT;
    END IF;
    IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_schema = 'public' AND table_name = 'inquiries' AND column_name = 'selected_products') THEN
        ALTER TABLE public.inquiries ADD COLUMN selected_products JSONB DEFAULT '[]'::jsonb;
    END IF;
END $$;

-- 2. Performance Indexes
CREATE INDEX IF NOT EXISTS idx_inquiries_created_at ON public.inquiries(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_inquiries_type ON public.inquiries(inquiry_type);
CREATE INDEX IF NOT EXISTS idx_inquiries_product_id ON public.inquiries(product_id);
CREATE INDEX IF NOT EXISTS idx_inquiries_status ON public.inquiries(status);
CREATE INDEX IF NOT EXISTS idx_inquiries_email ON public.inquiries(email);

-- 3. Row Level Security (RLS) Configuration - MANDATORY
ALTER TABLE public.inquiries ENABLE ROW LEVEL SECURITY;

-- 4. RLS Policy: Allow Public Anonymous Submissions (INSERT Only)
DROP POLICY IF EXISTS "Allow public anonymous inquiry submission" ON public.inquiries;
CREATE POLICY "Allow public anonymous inquiry submission" 
    ON public.inquiries 
    FOR INSERT 
    TO anon, authenticated
    WITH CHECK (
        char_length(trim(customer_name)) >= 2 AND
        char_length(trim(phone)) >= 7 AND
        status = 'new'
    );

-- 5. RLS Policy: Staff / Authenticated Management (SELECT, UPDATE)
DROP POLICY IF EXISTS "Allow authenticated staff to read inquiries" ON public.inquiries;
CREATE POLICY "Allow authenticated staff to read inquiries"
    ON public.inquiries
    FOR SELECT
    TO authenticated
    USING (true);

DROP POLICY IF EXISTS "Allow authenticated staff to update inquiries" ON public.inquiries;
CREATE POLICY "Allow authenticated staff to update inquiries"
    ON public.inquiries
    FOR UPDATE
    TO authenticated
    USING (true)
    WITH CHECK (true);

-- 6. Comments for Documentation
COMMENT ON TABLE public.inquiries IS 'Customer purchase inquiries and private viewing appointment requests for KYK Jewellers.';
COMMENT ON COLUMN public.inquiries.id IS 'Unique identifier for each customer inquiry.';
COMMENT ON COLUMN public.inquiries.inquiry_type IS 'Type of request: individual_product (single piece) or viewing_appointment (multi-piece salon viewing).';
COMMENT ON COLUMN public.inquiries.customer_name IS 'Customer full name provided in inquiry form.';
COMMENT ON COLUMN public.inquiries.email IS 'Validated contact email address of the customer.';
COMMENT ON COLUMN public.inquiries.phone IS 'Mandatory contact telephone / WhatsApp number (min 7 digits).';
COMMENT ON COLUMN public.inquiries.preferred_location IS 'Chosen boutique or private salon consultation location for viewing requests.';
COMMENT ON COLUMN public.inquiries.product_id IS 'Catalogue product code for single-piece inquiries, or VIEWING summary code.';
COMMENT ON COLUMN public.inquiries.product_name IS 'Descriptive title of the jewellery masterpiece.';
COMMENT ON COLUMN public.inquiries.selected_products IS 'Array of product objects for multi-piece viewing appointments.';
COMMENT ON COLUMN public.inquiries.message IS 'Customer request, bespoke sizing or salon appointment inquiry.';
COMMENT ON COLUMN public.inquiries.status IS 'Administrative lead status (new, contacted, appointment_scheduled, closed, spam).';
COMMENT ON COLUMN public.inquiries.notification_status IS 'Delivery status of owner email alert (pending, delivered, failed, unconfigured).';
