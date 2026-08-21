# Library Management System - Filtering & Search Features

## Overview
Your library management system now includes comprehensive filtering and search capabilities across all major modules. Users can easily find books, manage loans, and track fines using multiple filter options.

---

## 📚 Catalog Filters (Book Search & Browse)

### Available Filters:

1. **Text Search** 🔍
   - Search by book title, author name, ISBN, or description
   - Real-time partial matching (case-insensitive)

2. **Category Filter** 📁
   - Filter books by category (Fiction, Non-Fiction, Science, etc.)
   - Single selection from dropdown

3. **Author Filter** ✍️
   - Filter books by author
   - Browse all available authors

4. **Publication Date Range** 📅
   - Filter by "Published From" date
   - Filter by "Published To" date
   - View books published in specific periods

5. **Availability Filter** ✓
   - "Only Available Books" checkbox
   - Shows only books with copies in stock

6. **Sorting Options** ↕️
   - Title (A-Z)
   - Title (Z-A)
   - Newest First (by publication date)
   - Oldest First (by publication date)
   - Most Available (copies descending)
   - Least Available (copies ascending)

### How to Use:
1. Navigate to **Books Catalog** page
2. Fill in any combination of filters
3. Click **"Apply Filters"** button
4. Click **"Clear Filters"** to reset all

### Example Queries:
- Find all Science Fiction books from 2015-2020
- Find all books by Stephen King that are currently available
- Find all Mystery books sorted by most available copies
- Search for "Python" across title, author, and description

---

## 🔄 Circulation Module Filters

### Loan Filters (API: `/api/circulation/loans/`)

**Query Parameters:**
- `status` - Filter by loan status (borrowed, returned, overdue)
- `user__username` - Filter by user username (partial match)
- `book__title` - Filter by book title (partial match)
- `borrow_date_from` - Loans borrowed on/after this date
- `borrow_date_to` - Loans borrowed on/before this date
- `due_date_from` - Due date on/after this date
- `due_date_to` - Due date on/before this date
- `overdue_only` - Show only overdue loans
- `ordering` - Sort by: -borrow_date, borrow_date, -due_date, due_date
- `search` - Full-text search in book title and username

**Example Requests:**
```
GET /api/circulation/loans/?status=borrowed
GET /api/circulation/loans/?due_date_from=2026-08-20
GET /api/circulation/loans/?overdue_only=true&ordering=-due_date
GET /api/circulation/loans/?book__title=Python&user__username=member1
```

### Fine Filters (API: `/api/circulation/fines/`)

**Query Parameters:**
- `is_paid` - Filter paid vs unpaid fines (true/false)
- `loan__user__username` - Filter by user
- `amount_min` - Fines with amount >= this value
- `amount_max` - Fines with amount <= this value
- `created_from` - Fines created on/after this date
- `created_to` - Fines created on/before this date
- `ordering` - Sort by: -created_at, created_at, -amount, amount
- `search` - Full-text search in username and book title

**Example Requests:**
```
GET /api/circulation/fines/?is_paid=false
GET /api/circulation/fines/?amount_min=50&amount_max=500
GET /api/circulation/fines/?created_from=2026-08-01
GET /api/circulation/fines/?search=member1&ordering=-amount
```

---

## 📖 Books Module Filters

### Simple Book Filters (API: `/api/books/`)

**Query Parameters:**
- `title` - Filter by book title (partial match)
- `author` - Filter by author name (partial match)
- `available_only` - Show only available books (true/false)
- `ordering` - Sort by: title, -title, -available_copies, available_copies
- `search` - Full-text search

**Example Requests:**
```
GET /api/books/?title=Python
GET /api/books/?author=Martin&available_only=true
GET /api/books/?ordering=-available_copies
```

---

## 🎯 API Filter Best Practices

### Combining Filters
You can combine multiple filters in one request:

```
GET /api/circulation/loans/?status=borrowed&due_date_from=2026-08-15&ordering=-due_date
```

### Search vs Filters
- **Filters** - Exact field matching (with operators like >=, <=, icontains)
- **Search** - Full-text search across multiple fields

### Pagination with Filters
Filters work seamlessly with pagination:

```
GET /api/books/?category=1&page=2&page_size=20
```

### Response Format
All filtered API endpoints return paginated results:

```json
{
  "count": 45,
  "next": "http://api/books/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Book Title",
      "author": "Author Name",
      ...
    }
  ]
}
```

---

## 🔧 Filter Implementation Details

### Technologies Used:
- **django-filter** - Advanced filtering backend
- **Django ORM** - Query optimization with select_related()
- **DRF SearchFilter** - Full-text search capability
- **DRF OrderingFilter** - Dynamic sorting

### Files Created/Modified:

**New Files:**
- `catalog/filters.py` - Book filtering logic
- `catalog/forms.py` - Enhanced with BookFilterForm
- `circulation_app/filters.py` - Loan and Fine filtering
- `books/filters.py` - Simple book filtering

**Modified Files:**
- `catalog/views.py` - Added BookFilter to BookViewSet, enhanced book_list_page
- `circulation_app/views.py` - Added LoanViewSet and FineViewSet
- `circulation_app/urls.py` - Registered new ViewSets
- `catalog/templates/catalog/book_list.html` - Added comprehensive filter UI

---

## 📊 Filter Performance

### Query Optimization:
- Uses `select_related()` to minimize database queries
- Filters applied at database level (not in Python)
- Efficient pagination for large result sets

### Recommended Usage:
For best performance with large datasets:
1. Use specific filters over broad searches
2. Sort results consistently
3. Use pagination (default: 20 items per page)
4. Avoid filtering on computed fields when possible

---

## 🚀 Advanced Usage Examples

### Admin/Librarian Tasks:

**Find all overdue loans for follow-up:**
```
GET /api/circulation/loans/?overdue_only=true&ordering=-due_date
```

**Track unpaid fines over $100:**
```
GET /api/circulation/fines/?is_paid=false&amount_min=100&ordering=-amount
```

**Monitor books with low availability:**
```
GET /api/books/?available_only=false&ordering=available_copies
```

### Member Self-Service:

**Find all fantasy books currently available:**
```
GET /api/books/?category=5&available_only=true
```

**View personal loan history:**
```
GET /api/circulation/loans/?user__username=member1&ordering=-borrow_date
```

**Check active loans with soon-due dates:**
```
GET /api/circulation/loans/?status=borrowed&ordering=due_date
```

---

## 🎓 Quick Reference

| Feature | Location | Type |
|---------|----------|------|
| Catalog Book Filters | `/books-page/` | Web Form |
| Book API Filters | `/api/books/` | REST API |
| Loan Filters | `/api/circulation/loans/` | REST API |
| Fine Filters | `/api/circulation/fines/` | REST API |
| Author Filters | `/api/authors/` | REST API |
| Category Filters | `/api/categories/` | REST API |

---

## 📝 Notes

- All filters are case-insensitive for text searches
- Date filters use YYYY-MM-DD format
- Multiple authors/categories require separate API calls
- Filters are chainable for complex queries
- Unauthorized users see limited results based on their role

**Last Updated:** 2026-08-16
