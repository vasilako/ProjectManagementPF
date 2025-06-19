# 🚀 ProjectManagementPF

## 📁 Project Overview

A Django-based web application to manage products with categories, images, and a clean, responsive UI using Bootstrap.

---

## ✅ Completed Work (Day 1)

- **Project setup**: Django project `ProjectManagementPF`, apps: `core`, `products`, `users`, `orders`.
- **Git**: `.gitignore`, `main` and `develop` branches, feature workflow, commit hygiene.
- **Media & Static**:
  - Configured `MEDIA_URL`, `MEDIA_ROOT` and static settings.
  - Example static folder with placeholder image (`static/img/product-placeholder.png`).
- **Models**:
  - Extended `Product` model with `image = ImageField(upload_to='products/%Y/%m/%d', blank=True, null=True)`.
- **Migrations & Pillow**:
  - Installed Pillow (using `--only-binary :all:` to avoid compile issues on macOS).
- **Admin**:
  - Registered `Category` and `Product` with customized admin classes.
- **Templates**:
  - Global `base.html` with Bootstrap CSS/JS, FontAwesome, navbar (menu icon, centered logo, admin/messages links).
  - `components/messages.html` and `components/navbar.html` included in layout.
  - `_product_card.html` partial for product display cards.
  - `product_list.html` rendering responsive grid (4 cards/row), truncated description, read-more link, category & price footer.
  - Multiline truncate CSS + `… Ampliar` link.
- **Views & URLs**:
  - `HomeView`, `ProductListView`, `ProductDetailView` definitions.
  - URL routing set up in `config/urls.py`, `core/urls.py`, `products/urls.py`.
  - 404 handling via home as root.
- **Testing**:
  - Manual checks of home, products page, collapse menu, media serving.

---

## 🛠️ Setup Instructions

1. Clone the repository:

   ```bash
   git clone https://github.com/vasilako/ProjectManagementPF.git
   cd ProjectManagementPF
   ```

2. Create virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:

   ```bash
   pip install --only-binary :all: -r requirements.txt
   ```

4. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

5. Create or change superuser:

   ```bash
   python manage.py createsuperuser
   # or
   python manage.py changepassword <username>
   ```

6. Run the development server:

   ```bash
   python manage.py runserver
   ```

---

## 📄 requirements.txt

```txt
Django>=5.2
Pillow
```

(*Adjust versions as needed*)

---

## ✅ Task List for Tomorrow

### 🔹 Feature: Product Detail with Image Viewer

- Implement `ProductDetailView`.
- Create `product_detail.html`:
  - Display full-size image (or placeholder).
  - Show name (centered), category, full description, price badge.
  - Add back-navigation link.
- Optional: gallery support if multiple images per product.

### 🔹 UI/UX Polish

- Ensure collapse menu overlay responsive behavior.
- Add animated button hover for price badge.
- Add footer template partial.

### 🔹 Data & Tests

- Create JSON fixture (`products/fixtures/products.json`) with 10 sample products + categories.
- Add basic test: product list loads 200 OK, product detail loads existing product.

### 🔹 Documentation

- Add Mac setup instructions for Pillow to README.
- Describe Git flow, branches (`develop`, `feature/*`).

---

## ✅ Branch and Commit Workflow

- Work on: `feature/product-detail-view`
- After finishing tasks:
  ```bash
  git add .
  git commit -m "feat: add product detail view and template"
  git push -u origin feature/product-detail-view
  ```
- Open PR to `develop`, get it reviewed, then merge.

