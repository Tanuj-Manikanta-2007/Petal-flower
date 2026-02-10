# PetalCart UI/UX Design System Documentation

## Overview
This document outlines the cohesive design system implemented across the PetalCart website, ensuring a consistent and professional user experience throughout all authentication, form, and payment processes.

---

## Design Philosophy

### Color Palette
- **Primary Rose**: `#d88195` - Main brand color, used for buttons and highlights
- **Secondary Rose**: `#c76b83` - Complementary shade for gradients
- **Dark Rose**: `#b0556f` - Hover states and accents
- **Neutral Gray**: `#333` - Primary text color
- **Light Gray**: `#666` - Secondary text
- **Pale Gray**: `#999` - Placeholder and help text
- **Soft Gray**: `#f5f7fa` - Background gradient (light side)
- **Cool Gray**: `#c3cfe2` - Background gradient (dark side)
- **Success Green**: `#4CAF50` - Success messages
- **Error Red**: `#f44336` - Error states
- **Warning Yellow**: `#FFC107` - Warning messages

### Typography
- **Font Family**: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
- **Headings**: Font-weight 600-700, letter-spacing 0.5px
- **Body**: Font-weight 400-500, 16px base size
- **Labels**: Font-weight 600, 14px, uppercase, 0.5px letter-spacing

### Effects & Interactions
- **Glass Morphism**: Frosted glass effect with backdrop blur
- **Gradients**: Linear gradients on buttons and headers
- **Shadows**: Subtle box-shadows for depth (0 8px 32px rgba(0,0,0,0.1))
- **Transitions**: Cubic-bezier(0.4, 0, 0.2, 1) for smooth animations
- **Hover States**: Translate(-2 to -4px), enhanced shadows
- **Focus States**: 4px rgba color ring, border highlight

---

## Component Styles

### Forms & Input Elements

#### Form Container
```
- Max-width: 600px for standard forms
- Centered on page with 40px top/bottom margin
- 20px side padding for mobile
```

#### Form Controls
- **Padding**: 14px 16px
- **Border**: 2px solid #e0e0e0
- **Border-radius**: 10px
- **Background**: rgba(255,255,255,0.7)
- **Focus**: Border color → #d88195, box-shadow: 0 0 0 4px rgba(216,129,149,0.1)

#### Form Groups
- **Margin-bottom**: 25px
- **Label margin-bottom**: 8px
- **Label styling**: Uppercase, 14px, 600 weight, 0.5px letter-spacing

#### Form Rows (Two-Column Layout)
```css
display: grid;
grid-template-columns: 1fr 1fr;
gap: 20px;
```
Mobile (≤768px): Single column

### Buttons

#### Primary Button (CTAs)
- **Background**: `linear-gradient(135deg, #d88195, #c76b83)`
- **Color**: White, 16px, 600 weight, uppercase
- **Padding**: 14px 28px (large: 18px 40px)
- **Border-radius**: 10px (large: 12px)
- **Box-shadow**: 0 4px 15px rgba(216,129,149,0.3)
- **Hover**: Translate(-3px), enhanced shadow
- **Active**: Translate(-1px)
- **Disabled**: Gray (#ccc) background, no shadow

#### Secondary Button (Alternatives)
- **Background**: rgba(216,129,149,0.1)
- **Border**: 2px solid #d88195
- **Color**: #d88195
- **Hover**: Solid background with white text

### Cards & Containers

#### Glass Card
- **Background**: rgba(255,255,255,0.9)
- **Backdrop-filter**: blur(10px)
- **Border**: 1px solid rgba(0,0,0,0.1)
- **Border-radius**: 15px-20px
- **Box-shadow**: 0 8px 32px rgba(0,0,0,0.1)

#### Payment Summary Card
- **Sticky positioning** on desktop
- **Top**: 100px offset
- **Padding**: 30px
- **Responsive**: Static on mobile

### Messages & Alerts

#### Alert Base Styles
- **Padding**: 16px 20px
- **Border-left**: 4px solid (color by type)
- **Border-radius**: 12px
- **Display**: Flex with gap: 12px
- **Animation**: Slide-in 0.3s ease

#### Message Types
1. **Success**: Green (#4CAF50 border, rgba(76,175,80,0.1) background)
2. **Error**: Red (#f44336 border, rgba(244,67,54,0.1) background)
3. **Warning**: Yellow (#FFC107 border, rgba(255,193,7,0.1) background)
4. **Info**: Blue (#2196F3 border, rgba(33,150,243,0.1) background)

---

## Page-Specific Styling

### Payment Page (`payment.html`)

#### Layout Structure
```
┌─────────────────────────────────────┐
│       Payment Header (Full-width)    │
├─────────────────┬───────────────────┤
│                 │                   │
│ Order Summary   │  Payment Form     │
│ (Sticky)        │  (Full Width on   │
│                 │   Mobile)         │
│                 │                   │
└─────────────────┴───────────────────┘
```

#### Order Summary
- Grid layout: `1fr 1fr` on desktop, `1fr` on mobile
- **Info Row Styling**:
  - Padding: 15px
  - Background: rgba(216,129,149,0.05)
  - Border-left: 4px solid #d88195
  - Hover: Translate(5px)

#### Payment Form
- **Heading**: 24px, 600 weight, bottom border 2px
- **Form Rows**: Grid 2-column (mobile: 1-column)
- **Security Notice**: 
  - Background: rgba(76,175,80,0.05)
  - Border: 2px solid #4CAF50
  - Green text (#2e7d32)
  - Flex layout with SVG icon

#### Payment Button
- **Style**: Large primary button variant
- **Content**: Icon + Text + Amount badge
- **Amount Badge**: 
  - Background: rgba(0,0,0,0.2)
  - Padding: 6px 12px
  - Border-radius: 8px

### Form Pages (`form.html`)

#### Form Card
- **Max-width**: 600px
- **Centered**: margin: 40px auto
- **Heading**: 24px-28px, with bottom underline
- **Underline**: 
  - Width: 60px
  - Height: 3px
  - Gradient: #d88195 → #c76b83
  - Centered below heading

#### Field Groups
- Margin-bottom: 25px
- Label styling as above
- Help text: 13px, #999, margin-top: 5px
- Error text: 12px, #f44336, margin-top: 6px

#### Password Toggle
- Position: Relative container
- Button: Positioned absolutely right: 12px
- No background/border
- 👁️ emoji icon (toggles 👁️‍🗨️ when visible)

#### Validation States
- **Valid**: Border-color: #4CAF50
- **Invalid**: Border-color: #f44336
- **Focus**: Border-color: #d88195, ring shadow

---

## Responsive Breakpoints

### Desktop (1200px+)
- Payment: 2-column layout
- Form rows: 2-column
- Full spacing and sizing

### Tablet (768px - 1023px)
- Payment: Single column layout
- Order summary: Not sticky
- Form rows: Single column
- Reduced padding: 25px → 20px

### Mobile (≤768px)
- Payment: Single column, stacked
- Forms: Full width with 15px padding
- Form rows: Single column
- Button: Full width
- Font sizes: Reduced by 1-2px
- Heading: 32px (payment), 22px (forms)

### Small Mobile (≤480px)
- Form card padding: 20px
- All controls: Responsive sizing
- Labels: 13px
- Input padding: 12px 14px
- Button: 14px, flex-direction: column
- Summary: Flex-direction: column

---

## CSS Classes Reference

### Utility Classes
```
.glass-card          - Frosted glass effect container
.form-container      - Wrapper for form pages (600px max-width, centered)
.form-card          - Card container for forms
.form-control       - Standard input/textarea/select
.form-group         - Input + label wrapper
.form-row           - Two-column grid layout
.form-buttons       - Button container (flex layout)
.btn                - Base button class
.btn-primary        - Main CTA button
.btn-secondary      - Alternative button
.btn-large          - Large button variant
.alert              - Base alert styling
.alert-success      - Green alert
.alert-error        - Red alert
.alert-warning      - Yellow alert
.alert-info         - Blue alert
.spinner            - Loading indicator animation
.payment-container  - Max-width 1200px, centered
.payment-wrapper    - Grid layout for payment page
.order-summary      - Order details card
.payment-form-section - Form container
.security-notice    - Security info box
.info-row           - Individual order info line
```

### State Classes
```
.form-loading       - Opacity 0.6, pointer-events none
.has-success        - Valid form field highlighting
.has-error          - Invalid form field highlighting
.is-disabled        - Disabled button/input styling
.form-check         - Checkbox/radio wrapper
```

---

## Animation & Transitions

### Keyframe Animations
```css
@keyframes fadeIn {
    from { opacity: 0; transform: translateY(-20px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(-10px); }
    to   { opacity: 1; transform: translateY(0); }
}

@keyframes pulse {
    0%, 100% { box-shadow: 0 0 0 0 rgba(255,193,7,0.7); }
    50%      { box-shadow: 0 0 0 8px rgba(255,193,7,0); }
}

@keyframes spin {
    to { transform: rotate(360deg); }
}
```

### Transition Timing
- **Standard**: `all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`
- **Hover**: `all 0.3s ease`
- **Focus**: `all 0.3s cubic-bezier(0.4, 0, 0.2, 1)`

---

## Authentication Forms Integration

### Updated Forms (forms.py)

#### All Form Classes Include:
1. **Custom Widgets**: All inputs use `form-control` class
2. **Placeholders**: Descriptive hints for users
3. **Accessibility**: Labels, help text, error messages
4. **Validation**: Built-in Django form validation

#### Forms Updated:
- `accounts.RegisterForm` - User registration
- `petalcart.ShopRegisterForm` - Flower shop registration
- `petalcart.FlowerForm` - Add flower
- `petalcart.CommentForm` - Leave comments
- `shop.ShopRegisterForm` - Alternative shop registration
- `shop.FlowerForm` - Shop flower management
- `shop.FlowerStockForm` - Manage stock
- `shop.StockForm` - Stock with filtering

---

## Files Modified

### CSS Files Created/Updated
1. **`static/css/forms.css`** - Comprehensive form styling (600+ lines)
2. **`static/css/payment.css`** - Payment page specific styles (400+ lines)

### HTML Files Updated
1. **`templates/payment.html`** - Complete redesign with billing form
2. **`templates/form.html`** - Enhanced with consistent styling

### Python Files Updated
1. **`accounts/forms.py`** - Enhanced RegisterForm with widgets
2. **`petalcart/forms.py`** - All forms updated with styling
3. **`shop/forms.py`** - All forms updated with styling

---

## Usage Guidelines

### For Developers
1. Always use `form-control` class on inputs
2. Wrap inputs in `form-group` or `field-group`
3. Use `form-row` for 2-column layouts
4. Apply `btn-primary` to main CTAs
5. Use semantic HTML5 input types
6. Include validation and error handling

### For Designers
1. Maintain the rose/pink color gradient (#d88195 → #c76b83)
2. Keep shadow depth consistent
3. Use glass morphism for card-like elements
4. Ensure minimum 44px touch targets on mobile
5. Maintain 1.5 line-height for readability
6. Test all animations at 60fps

### For QA
1. Test forms on devices: Desktop, Tablet, Phone
2. Verify all interactive states: hover, focus, active, disabled
3. Check accessibility: keyboard navigation, screen readers
4. Validate responsive design at all breakpoints
5. Test payment form with real data
6. Verify error messages and success alerts

---

## Browser Support
- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: All major (iOS Safari, Chrome Mobile)

## Accessibility Features
- Semantic HTML structure
- ARIA labels and descriptions
- Keyboard navigation support
- Color contrast ratios > 4.5:1
- Focus indicators visible
- Error messages associated with fields
- Help text for complex inputs

---

## Future Enhancements
1. Dark mode variant color palette
2. Additional animation presets
3. Extended component library
4. Design tokens system
5. Storybook documentation
6. Form templates gallery
