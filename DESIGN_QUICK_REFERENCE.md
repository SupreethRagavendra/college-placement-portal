# KIT Design Quick Reference Guide

## 🎨 Color Palette

### Primary Colors
```css
--kit-orange: #f97316    /* Primary accent, buttons */
--kit-purple: #7e22ce    /* Headers, navigation */
--kit-crimson: #dc2626   /* Important highlights */
```

### Gradients
```css
/* Orange Button Gradient */
background: linear-gradient(135deg, #f97316 0%, #ea580c 100%);

/* Purple Header Gradient */
background: linear-gradient(135deg, #7e22ce 0%, #581c87 100%);

/* Page Background */
background: linear-gradient(135deg, #faf5ff 0%, #fff7ed 100%);
```

## 🔧 Common Classes

### Buttons
```html
<!-- Primary Button (Orange) -->
<a href="#" class="kit-btn">Click Me</a>

<!-- Outline Button -->
<a href="#" class="kit-btn-outline">Secondary</a>

<!-- Bootstrap + KIT -->
<button class="btn kit-btn">Submit</button>
```

### Cards
```html
<!-- Feature Card with Hover -->
<div class="kit-card">
    <h4>Title</h4>
    <p>Content here...</p>
</div>
```

### Containers
```html
<!-- Content Wrapper (Auto-styled in layout) -->
<div class="content-wrapper">
    <!-- Your content -->
</div>

<!-- With Curved Borders -->
<div class="kit-curve">
    <!-- Curved all sides -->
</div>
```

## 📐 Spacing & Sizing

### Border Radius
- Cards: `20px`
- Buttons: `25-30px`
- Small elements: `8px`
- Logo containers: `50%` (circular)

### Common Padding
- Cards: `2rem`
- Buttons: `12px 30px`
- Sections: `3-5rem` vertical

## 🖼️ Logo Usage

### Navbar/Light Backgrounds
```html
<img src="{{ asset('css/logo1-removebg-preview.png') }}" 
     alt="KIT Logo" 
     style="height: 50px;">
```

### Dark Backgrounds (Footer)
```html
<img src="{{ asset('css/logo1-removebg-preview.png') }}" 
     alt="KIT Logo" 
     style="height: 60px; filter: brightness(0) invert(1);">
```

## 🎭 Animations

### Hover Effects (Auto-applied)
- **Cards**: Lift up (`translateY(-10px)`)
- **Buttons**: Scale up (`scale(1.05)`)
- **Links**: Color transition

### Custom Animations
```html
<!-- Floating Animation -->
<div class="floating">
    <img src="..." alt="...">
</div>

<!-- Pulse Effect -->
<div class="kit-pulse">
    <span>Loading...</span>
</div>
```

## 📱 Responsive Breakpoints

```css
/* Mobile First Approach */
/* Base styles for mobile */

@media (min-width: 768px) {
    /* Tablet styles */
}

@media (min-width: 992px) {
    /* Desktop styles */
}
```

## 🏗️ Page Structure

### Typical Page Layout
```blade
@extends('layouts.app')

@section('header')
    <h1>Page Title</h1>
@endsection

@section('content')
    <!-- Your content here -->
    <div class="row">
        <div class="col-md-6">
            <div class="kit-card">
                <!-- Card content -->
            </div>
        </div>
    </div>
@endsection
```

### Welcome/Landing Page
```blade
<!-- Hero Section -->
<section class="hero-section">
    <!-- Purple gradient with patterns -->
</section>

<!-- Features -->
<section class="py-5">
    <div class="container">
        <div class="row">
            <div class="col-md-3">
                <div class="feature-card">
                    <div class="feature-icon">
                        <i class="fas fa-icon"></i>
                    </div>
                    <h4>Title</h4>
                    <p>Description</p>
                </div>
            </div>
        </div>
    </div>
</section>
```

## 🎯 Common Patterns

### Feature Icon
```html
<div class="feature-icon">
    <i class="fas fa-graduation-cap"></i>
</div>
```

### Stats Card
```html
<div class="stats-card">
    <div class="stats-number">500+</div>
    <p class="text-muted">Students Placed</p>
</div>
```

### Gradient Text
```css
.gradient-heading {
    background: linear-gradient(135deg, #f97316 0%, #7e22ce 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
```

## 🔗 Important Files

| File | Purpose |
|------|---------|
| `tailwind.config.js` | Color definitions |
| `resources/css/app.css` | Custom styles |
| `resources/views/layouts/app.blade.php` | Main layout |
| `resources/views/layouts/navigation.blade.php` | Navbar |
| `resources/views/welcome.blade.php` | Landing page |

## ⚡ Quick Tips

1. **Always use KIT colors** from the palette
2. **Maintain 20px border radius** for cards
3. **Use purple for headers**, orange for CTAs
4. **Include hover effects** on interactive elements
5. **Keep gradients consistent** with documented ones
6. **Logo in footer** should be inverted (white)

## 🚀 Build Commands

```bash
# Development
npm run dev

# Production Build
npm run build

# Watch Mode
npm run watch
```

## 📋 Checklist for New Pages

- [ ] Use `@extends('layouts.app')`
- [ ] Add appropriate `@section('header')` with page title
- [ ] Use `.kit-card` for card containers
- [ ] Apply `.kit-btn` for primary actions
- [ ] Include `.kit-btn-outline` for secondary actions
- [ ] Add hover effects on interactive elements
- [ ] Test responsive design on mobile
- [ ] Ensure color contrast for accessibility

## 🎨 Color Accessibility

| Background | Safe Text Colors |
|-----------|------------------|
| White (`#ffffff`) | Purple, Orange, Dark Gray |
| Purple (`#7e22ce`) | White only |
| Orange (`#f97316`) | White only |
| Light Purple (`#faf5ff`) | Purple, Dark text |

## 🔍 Common Issues & Solutions

### Issue: Buttons not showing gradient
**Solution:** Ensure you have `@vite(['resources/css/app.css'])` in your layout

### Issue: Logo not appearing
**Solution:** Check that `logo1-removebg-preview.png` exists in `public/css/`

### Issue: Colors not matching
**Solution:** Use exact hex codes from this guide

### Issue: Hover effects not working
**Solution:** Ensure transition CSS is loaded from app.css

---

**Quick Copy-Paste Snippets**

```html
<!-- Orange CTA Button -->
<a href="#" class="kit-btn">
    <i class="fas fa-rocket me-2"></i> Get Started
</a>

<!-- Feature Card -->
<div class="kit-card">
    <div class="feature-icon">
        <i class="fas fa-check"></i>
    </div>
    <h4 class="fw-bold mb-3">Feature Title</h4>
    <p class="text-muted">Description goes here</p>
</div>

<!-- Purple Section Header -->
<div class="page-header kit-pattern">
    <div class="container">
        <h1>Section Title</h1>
    </div>
</div>
```

---

**Version:** 1.0  
**Last Updated:** {{ date('Y-m-d') }}

