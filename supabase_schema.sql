-- SalesForecaster Database Schema
-- Run this in your Supabase SQL Editor

-- Enable Row Level Security
ALTER DATABASE postgres SET "app.jwt_secret" TO 'your-jwt-secret';

-- Create users table (extends Supabase auth.users)
CREATE TABLE IF NOT EXISTS public.users (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    full_name TEXT,
    company_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create uploads table to track file uploads
CREATE TABLE IF NOT EXISTS public.uploads (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    file_name TEXT NOT NULL,
    file_size INTEGER,
    original_rows INTEGER,
    cleaned_rows INTEGER,
    data_quality_issues JSONB,
    data_insights JSONB,
    pattern_insights JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create forecasts table to store forecast results
CREATE TABLE IF NOT EXISTS public.forecasts (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES public.users(id) ON DELETE CASCADE,
    upload_id UUID REFERENCES public.uploads(id) ON DELETE CASCADE,
    model_used TEXT NOT NULL,
    model_explanation TEXT,
    forecast_data JSONB NOT NULL,
    forecast_insights JSONB,
    confidence_level TEXT,
    forecast_periods INTEGER,
    data_points_used INTEGER,
    low_confidence BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_uploads_user_id ON public.uploads(user_id);
CREATE INDEX IF NOT EXISTS idx_uploads_created_at ON public.uploads(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_forecasts_user_id ON public.forecasts(user_id);
CREATE INDEX IF NOT EXISTS idx_forecasts_upload_id ON public.forecasts(upload_id);
CREATE INDEX IF NOT EXISTS idx_forecasts_created_at ON public.forecasts(created_at DESC);

-- Enable Row Level Security
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.uploads ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.forecasts ENABLE ROW LEVEL SECURITY;

-- Create RLS policies
-- Users can only see their own data
CREATE POLICY "Users can view own profile" ON public.users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE USING (auth.uid() = id);

CREATE POLICY "Users can insert own profile" ON public.users
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Uploads policies
CREATE POLICY "Users can view own uploads" ON public.uploads
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own uploads" ON public.uploads
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own uploads" ON public.uploads
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own uploads" ON public.uploads
    FOR DELETE USING (auth.uid() = user_id);

-- Forecasts policies
CREATE POLICY "Users can view own forecasts" ON public.forecasts
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own forecasts" ON public.forecasts
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own forecasts" ON public.forecasts
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own forecasts" ON public.forecasts
    FOR DELETE USING (auth.uid() = user_id);

-- Create function to handle user creation
CREATE OR REPLACE FUNCTION public.handle_new_user()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO public.users (id, email, full_name)
    VALUES (NEW.id, NEW.email, NEW.raw_user_meta_data->>'full_name');
    RETURN NEW;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Create trigger for new user creation
CREATE OR REPLACE TRIGGER on_auth_user_created
    AFTER INSERT ON auth.users
    FOR EACH ROW EXECUTE FUNCTION public.handle_new_user();

-- Create function to update updated_at timestamp
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create triggers for updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW EXECUTE FUNCTION public.update_updated_at_column();

-- Grant necessary permissions
GRANT USAGE ON SCHEMA public TO anon, authenticated;
GRANT ALL ON public.users TO anon, authenticated;
GRANT ALL ON public.uploads TO anon, authenticated;
GRANT ALL ON public.forecasts TO anon, authenticated;
GRANT USAGE ON SEQUENCE public.users_id_seq TO anon, authenticated;
