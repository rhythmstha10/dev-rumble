# 🔍 Quick Filter Reference Guide

## 📚 Web Interface Filters (User-Friendly)

### Access Point: **Books Catalog** (`/books-page/`)

#### Available Filters:

| Filter | Purpose | Options |
|--------|---------|---------|
| 🔍 **Search** | Find books by title, author, ISBN | Text input (any word) |
| 📁 **Category** | Browse by book type | Dropdown: All Categories, Fiction, Non-Fiction, etc. |
| ✍️ **Author** | Filter by author name | Dropdown: All Authors, J.K. Rowling, George R.R. Martin, etc. |
| 📅 **Published From** | Earliest publication date | Date picker |
| 📅 **Published To** | Latest publication date | Date picker |
| ✓ **Only Available** | Show only books in stock | Checkbox |
| ↕️ **Sort By** | Order results | Title A→Z, Title Z→A, Newest, Oldest, Most/Least Available |

---

## 🔄 REST API Filters (Developers)

### Book Filters
```
GET /api/books/?category=1&title=Python&available_only=true&ordering=-published_date
```

**Parameters:**
- `title` - Book title (partial)
- `author` - Author name (partial)
- `isbn` - ISBN number (partial)
- `category` - Category ID
- `available_only` - true/false
- `published_date_from` - YYYY-MM-DD
- `published_date_to` - YYYY-MM-DD
- `ordering` - title, -title, -published_date, published_date, -available_copies, available_copies
- `search` - Full-text search

### Loan Filters
```
GET /api/circulation/loans/?status=borrowed&overdue_only=true&ordering=-due_date
```

**Parameters:**
- `status` - borrowed, returned, overdue
- `user__username` - Username (partial)
- `book__title` - Book title (partial)
- `borrow_date_from` - YYYY-MM-DD
- `borrow_date_to` - YYYY-MM-DD
- `due_date_from` - YYYY-MM-DD
- `due_date_to` - YYYY-MM-DD
- `overdue_only` - true/false
- `ordering` - -borrow_date, borrow_date, -due_date, due_date
- `search` - Full-text search

### Fine Filters
```
GET /api/circulation/fines/?is_paid=false&amount_min=50&amount_max=500
```

**Parameters:**
- `is_paid` - true/false
- `amount_min` - Minimum amount
- `amount_max` - Maximum amount
- `loan__user__username` - Username (partial)
- `created_from` - YYYY-MM-DD
- `created_to` - YYYY-MM-DD
- `ordering` - -created_at, created_at, -amount, amount
- `search` - Full-text search

---

## 💡 Common Queries

### For Readers:

**"Find Science Fiction books available now"**
```
Web: Category→Fiction, Search→"Science Fiction" ✓ Only Available
API: /api/books/?category=1&search=Science%20Fiction&available_only=true
```

**"Find books by Stephen King published after 2000"**
```
Web: Author→Stephen King, Published From→2000
API: /api/books/?author=4&published_date_from=2000-01-01
```

**"Show all available Fantasy books sorted by newest"**
```
Web: Category→Fantasy, ✓ Only Available, Sort By→Newest First
API: /api/books/?category=6&available_only=true&ordering=-published_date
```

### For Librarians:

**"Find all overdue loans"**
```
API: /api/circulation/loans/?overdue_only=true&ordering=-due_date
```

**"Find unpaid fines over ₹100"**
```
API: /api/circulation/fines/?is_paid=false&amount_min=100&ordering=-amount
```

**"Check books borrowed by member1 this month"**
```
API: /api/circulation/loans/?user__username=member1&borrow_date_from=2026-08-01
```

**"Find all available copies of Python books"**
```
API: /api/books/?search=Python&available_only=true
```

---

## 🎯 Filter Tips

### Web Interface:
- ✓ You can leave filters empty to include all options
- ✓ Combine multiple filters for precise results
- ✓ Click "Clear Filters" to start fresh
- ✓ Page updates with matching results count

### API:
- ✓ Combine filters with `&` separator
- ✓ Use `ordering` for consistent results
- ✓ Add `&page=2` to navigate results
- ✓ Use `&page_size=50` for more results per page

### Search:
- ✓ Case-insensitive (works with any case)
- ✓ Partial matches (e.g., "Harr" finds "Harry Potter")
- ✓ Works across title, author, ISBN, description
- ✓ Web search is smart—no complex syntax needed

### Dates:
- ✓ Format: YYYY-MM-DD (2026-08-16)
- ✓ "From" = on/after that date (≥)
- ✓ "To" = on/before that date (≤)
- ✓ Both can be used together for ranges

---

## 🚀 Example URLs

### Book Browsing:
```
http://localhost:8000/books-page/
http://localhost:8000/books-page/?search=Django
http://localhost:8000/books-page/?category=1&available_only=on
http://localhost:8000/books-page/?author=1&sort_by=-published_date
```

### API Access:
```
http://localhost:8000/api/books/
http://localhost:8000/api/books/?search=Python&available_only=true
http://localhost:8000/api/circulation/loans/?status=borrowed
http://localhost:8000/api/circulation/fines/?is_paid=false
http://localhost:8000/api/authors/?search=Rowling
http://localhost:8000/api/categories/?search=Fiction
```

---

## 📊 Dropdown Options

### Categories:
- All Categories
- Fiction
- Non-Fiction
- Science
- History
- Biography
- Mystery
- Romance
- Poetry
- Self-Help
- Children

### Authors (20 available):
- J.K. Rowling
- George R.R. Martin
- J.R.R. Tolkien
- Stephen King
- Haruki Murakami
- Margaret Atwood
- Chimamanda Ngozi Adichie
- Paulo Coelho
- Neil Gaiman
- Agatha Christie
- ... and 10 more

### Loan Status:
- borrowed
- returned
- overdue

### Sort Options:
- Title (A-Z)
- Title (Z-A)
- Newest First
- Oldest First
- Most Available
- Least Available

---

## 🆘 Troubleshooting

**"No results found"**
→ Try removing filters one at a time
→ Use Clear Filters to start over
→ Check spelling of search terms

**"Too many results"**
→ Add more filters to narrow down
→ Use category and author filters
→ Try text search for more specific matches

**"Date filter not working"**
→ Ensure date format: YYYY-MM-DD
→ Check calendar dates for library's book range

**"Search not finding anything"**
→ Partial matches work (e.g., "Harr" = "Harry")
→ Case-insensitive (any case works)
→ Searches title, author, ISBN, description

---

## 📞 Support

**Need help?** Check the full documentation:
- [FILTERS_DOCUMENTATION.md](FILTERS_DOCUMENTATION.md) - Complete technical guide
- [FILTERS_IMPLEMENTATION_SUMMARY.md](FILTERS_IMPLEMENTATION_SUMMARY.md) - Implementation details

---

**Last Updated:** 2026-08-16 | **Status:** Ready to Use ✅
