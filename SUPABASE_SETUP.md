# Supabase Integration Setup Guide

This guide will help you set up Supabase for your SalesForecaster application.

## 🚀 Quick Setup

### 1. Database Schema Setup

1. Go to your Supabase project dashboard: https://fkmsfdcqhhyoisfvsfrb.supabase.co
2. Navigate to the **SQL Editor**
3. Copy and paste the contents of `supabase_schema.sql` into the editor
4. Click **Run** to execute the schema

### 2. Authentication Configuration

1. In your Supabase dashboard, go to **Authentication > Settings**
2. Configure your authentication settings:
   - **Site URL**: `http://localhost:3000` (for development)
   - **Redirect URLs**: Add `http://localhost:3000`
   - **Email Templates**: Customize if needed

### 3. Environment Variables (Optional)

For production, you might want to move the Supabase credentials to environment variables:

Create a `.env` file in the `ReactFrontEnd` directory:

```env
VITE_SUPABASE_URL=https://fkmsfdcqhhyoisfvsfrb.supabase.co
VITE_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZrbXNmZGNxaGh5b2lzZnZzZnJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTU3MDgxNTMsImV4cCI6MjA3MTI4NDE1M30.c8NfPUJR4_hlJc73QottMNJM4bFMxBii2STNw_-c27s
```

Then update `src/supabase.js`:

```javascript
const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY
```

## 📊 Database Tables

The schema creates three main tables:

### 1. `users` Table
- Extends Supabase's built-in `auth.users`
- Stores user profile information
- Automatically created when users sign up

### 2. `uploads` Table
- Tracks file uploads and data quality
- Stores metadata about uploaded CSV files
- Links to user accounts

### 3. `forecasts` Table
- Stores forecast results and insights
- Links to uploads and users
- Contains model information and predictions

## 🔐 Security Features

- **Row Level Security (RLS)**: Users can only access their own data
- **Automatic user creation**: New users are automatically added to the `users` table
- **Secure authentication**: Uses Supabase's built-in auth system

## 🎯 Features Added

### Authentication
- ✅ User registration and login
- ✅ Email verification
- ✅ Password reset
- ✅ User profile management

### Data Persistence
- ✅ Save upload metadata
- ✅ Store forecast results
- ✅ Track user activity
- ✅ Data quality insights storage

### User Management
- ✅ Profile settings
- ✅ Account information
- ✅ Sign out functionality

## 🧪 Testing the Integration

1. Start your application: `npm run dev`
2. Navigate to `http://localhost:3000`
3. You should see a login/signup screen
4. Create a new account or sign in
5. Upload a CSV file and generate forecasts
6. Check your Supabase dashboard to see the data being stored

## 🔧 Troubleshooting

### Common Issues

1. **"Invalid API key" error**
   - Verify your Supabase URL and API key are correct
   - Check that the key has the right permissions

2. **"Table doesn't exist" error**
   - Make sure you've run the SQL schema in Supabase
   - Check that the table names match exactly

3. **Authentication not working**
   - Verify your site URL and redirect URLs in Supabase settings
   - Check that email confirmation is configured properly

4. **RLS policies blocking access**
   - Ensure users are properly authenticated
   - Check that the RLS policies are correctly set up

### Debug Mode

To enable debug logging, add this to your browser console:

```javascript
localStorage.setItem('supabase.debug', 'true')
```

## 📈 Next Steps

### Potential Enhancements

1. **Dashboard**: Add a dashboard to view historical forecasts
2. **Data Export**: Export user data and forecasts
3. **Team Management**: Add team/company features
4. **Analytics**: Track usage patterns and performance
5. **Notifications**: Email notifications for forecast completion

### Production Deployment

1. Update environment variables for production
2. Configure proper CORS settings
3. Set up email templates
4. Enable additional security features
5. Set up monitoring and logging

## 📞 Support

If you encounter any issues:

1. Check the Supabase documentation: https://supabase.com/docs
2. Review the console for error messages
3. Verify your database schema is correctly applied
4. Test with a fresh user account

---

**Note**: This integration provides a solid foundation for user management and data persistence. The application now supports multiple users, data history, and secure access control.
