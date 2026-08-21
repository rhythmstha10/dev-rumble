# 🎯 Filter Features - Quick Visual Reference

## 📊 Filter Matrix

### Where to Find Each Filter?

```
FILTER TYPE          | WEB UI        | API BOOKS  | API LOANS  | API FINES  | API AUTHORS | API CATEGORIES
─────────────────────┼───────────────┼────────────┼────────────┼────────────┼─────────────┼────────────────
🔍 Text Search       | ✓ (Title)     | ✓          | ✓          | ✓          | ✓           | ✓
📁 Category          | ✓             | ✓          | ✗          | ✗          | ✗           | ✗
✍️ Author           | ✓             | ✓          | ✗          | ✗          | ✗           | ✗
✓ Availability      | ✓             | ✓          | ✗          | ✗          | ✗           | ✗
📅 Date Range       | ✓             | ✓          | ✓          | ✓          | ✗           | ✗
📖 Status           | ✗             | ✗          | ✓          | ✗          | ✗           | ✗
💰 Amount Range     | ✗             | ✗          | ✗          | ✓          | ✗           | ✗
↕️ Sorting          | ✓ (6 options) | ✓          | ✓          | ✓          | ✓           | ✓
```

---

## 🔍 Detailed Filter Breakdown

### 1️⃣ CATALOG - Book Listing (`/books-page/`)

```
┌─────────────────────────────────────────────┐
│         📚 BOOK CATALOG FILTERS             │
├─────────────────────────────────────────────┤
│                                             │
│  🔍 SEARCH BOX                              │
│  ├─ Searches: Title, Author, ISBN, Desc    │
│  └─ Case-insensitive, partial match        │
│                                             │
│  📁 CATEGORY DROPDOWN                       │
│  ├─ Options: All, Fiction, Non-Fiction     │
│  ├─ Science, History, Biography            │
│  ├─ Mystery, Romance, Poetry               │
│  ├─ Self-Help, Children                    │
│  └─ Single selection only                  │
│                                             │
│  ✍️ AUTHOR DROPDOWN                         │
│  ├─ 20 authors available                   │
│  └─ Single selection only                  │
│                                             │
│  📅 DATE PICKERS                            │
│  ├─ Published From (date)                  │
│  ├─ Published To (date)                    │
│  └─ Both optional, combinable              │
│                                             │
│  ✓ CHECKBOX                                 │
│  └─ "Only Available Books" toggle           │
│                                             │
│  ↕️ SORT OPTIONS (6 choices)                │
│  ├─ Title (A-Z)                             │
│  ├─ Title (Z-A)                             │
│  ├─ Newest First                            │
│  ├─ Oldest First                            │
│  ├─ Most Available                          │
│  └─ Least Available                         │
│                                             │
│  📊 RESULTS COUNTER                         │
│  └─ Shows total matching books              │
│                                             │
└─────────────────────────────────────────────┘
```

### 2️⃣ CIRCULATION - Loans (`/api/circulation/loans/`)

```
┌─────────────────────────────────────────────┐
│         🔄 LOAN FILTERS (API)               │
├─────────────────────────────────────────────┤
│                                             │
│  status=VALUE                               │
│  ├─ borrowed: Active loans                 │
│  ├─ returned: Completed loans              │
│  └─ overdue: Past due date                 │
│                                             │
│  user__username=TEXT                        │
│  └─ Partial match on username              │
│                                             │
│  book__title=TEXT                           │
│  └─ Partial match on book title            │
│                                             │
│  borrow_date_from=DATE                      │
│  borrow_date_to=DATE                        │
│  └─ Filter by borrow date range            │
│                                             │
│  due_date_from=DATE                         │
│  due_date_to=DATE                           │
│  └─ Filter by due date range               │
│                                             │
│  overdue_only=TRUE/FALSE                    │
│  └─ Show only overdue loans                │
│                                             │
│  search=TEXT                                │
│  └─ Full-text search                       │
│                                             │
│  ordering=FIELD                             │
│  ├─ -borrow_date (Most Recent)             │
│  ├─ borrow_date (Oldest)                   │
│  ├─ -due_date (Due Soon)                   │
│  └─ due_date (Due Later)                   │
│                                             │
└─────────────────────────────────────────────┘
```

### 3️⃣ CIRCULATION - Fines (`/api/circulation/fines/`)

```
┌─────────────────────────────────────────────┐
│         💰 FINE FILTERS (API)               │
├─────────────────────────────────────────────┤
│                                             │
│  is_paid=TRUE/FALSE                         │
│  ├─ true: Paid fines                       │
│  └─ false: Unpaid fines                    │
│                                             │
│  loan__user__username=TEXT                  │
│  └─ Partial match on username              │
│                                             │
│  amount_min=NUMBER                          │
│  amount_max=NUMBER                          │
│  └─ Filter by amount range                 │
│                                             │
│  created_from=DATE                          │
│  created_to=DATE                            │
│  └─ Filter by creation date                │
│                                             │
│  search=TEXT                                │
│  └─ Full-text search                       │
│                                             │
│  ordering=FIELD                             │
│  ├─ -created_at (Most Recent)              │
│  ├─ created_at (Oldest)                    │
│  ├─ -amount (Highest)                      │
│  └─ amount (Lowest)                        │
│                                             │
└─────────────────────────────────────────────┘
```

---

## 🎯 Common Filter Combinations

### Scenario 1: Find Available Science Books
```
WEB: Category=Science + ✓ Only Available + Sort=Newest
API: /api/books/?category=3&available_only=true&ordering=-published_date
```

### Scenario 2: Track Overdue Loans
```
API: /api/circulation/loans/?status=overdue&ordering=-due_date
```

### Scenario 3: Find Unpaid Fines Over ₹100
```
API: /api/circulation/fines/?is_paid=false&amount_min=100&ordering=-amount
```

### Scenario 4: Books by Stephen King (Available)
```
WEB: Author=Stephen King + ✓ Only Available
API: /api/books/?author=4&available_only=true
```

### Scenario 5: Recent Books (Published 2020+)
```
WEB: Published From=2020-01-01 + Sort=Newest First
API: /api/books/?published_date_from=2020-01-01&ordering=-published_date
```

---

## 📈 Filter Comparison Chart

### By Complexity:

```
SIMPLE          | MEDIUM            | COMPLEX
════════════════╪═══════════════════╪════════════════════════════
Available Only  | Category Filter   | Multi-filter API queries
Author Filter   | Date Range        | Custom sort + search
Category Filter | Text Search       | Combined with pagination
Single Dropdown | 2-3 Filters       | 5+ filters combined
```

### By Use Case:

```
READER TASKS                    | LIBRARIAN TASKS
══════════════════════════════════════════════════════════════════
Find book by title              | Track overdue loans
Browse by category              | Identify unpaid fines
Find available books            | Monitor loan patterns
Search by author                | Generate reports
Sort by newest/oldest           | Analyze availability
```

---

## 🔗 Access Quick Links

### Web Interface:
- Book Catalog: `http://localhost:8000/books-page/`
- Add Book: `http://localhost:8000/books-page/add/`

### API Endpoints (JSON):
- Books: `http://localhost:8000/api/books/`
- Authors: `http://localhost:8000/api/authors/`
- Categories: `http://localhost:8000/api/categories/`
- Loans: `http://localhost:8000/api/circulation/loans/`
- Fines: `http://localhost:8000/api/circulation/fines/`

### API Documentation:
- Swagger UI: `http://localhost:8000/api/docs/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

---

## ⚡ Quick API Recipe Book

### Get all available books
```bash
curl "http://localhost:8000/api/books/?available_only=true"
```

### Get books by category (Fiction = ID 1)
```bash
curl "http://localhost:8000/api/books/?category=1"
```

### Get author's works
```bash
curl "http://localhost:8000/api/books/?author=1"  # ID 1 = J.K. Rowling
```

### Search across all fields
```bash
curl "http://localhost:8000/api/books/?search=Python"
```

### Sort by availability
```bash
curl "http://localhost:8000/api/books/?ordering=-available_copies"
```

### Get overdue loans
```bash
curl "http://localhost:8000/api/circulation/loans/?overdue_only=true"
```

### Get unpaid fines
```bash
curl "http://localhost:8000/api/circulation/fines/?is_paid=false"
```

### Get fines in amount range
```bash
curl "http://localhost:8000/api/circulation/fines/?amount_min=50&amount_max=500"
```

### Complex query
```bash
curl "http://localhost:8000/api/books/?category=1&available_only=true&ordering=-published_date&page=1"
```

---

## 📱 Mobile-Friendly Tips

### For Smaller Screens:
- ✓ Filters stack vertically
- ✓ One filter per row
- ✓ Touch-friendly dropdowns
- ✓ Full-width search box
- ✓ Large buttons for easy clicking

### Responsive Breakpoints:
- Desktop (1200px+): 2-column filter layout
- Tablet (768-1199px): 2-column layout
- Mobile (<768px): Single column layout

---

## 🏆 Best Practices

### For Web Interface:
1. Start with broad search, then filter
2. Use category filter first for speed
3. Combine filters for precision
4. Use "Clear Filters" to reset
5. Check results counter

### For API Queries:
1. Add `ordering` for consistent results
2. Include `page_size` for control
3. Combine filters with `&`
4. Test in browser first
5. Use pagination for large results

---

## 📊 Performance Tips

### To Speed Up Searches:
- Use specific filters (don't leave everything blank)
- Filter by category before doing text search
- Sort by indexed fields (title, date, copies)
- Use pagination (don't request all results)
- Combine 2-3 filters max for API queries

### Query Examples:
```
SLOW:  /api/books/?search=the
FAST:  /api/books/?category=1&search=Python&available_only=true

SLOW:  /api/books/?page_size=10000
FAST:  /api/books/?page_size=50&page=1
```

---

## ✅ Filter Verification

### Test These Combinations:

```
✓ Search: "Harry" → Should find Harry Potter books
✓ Category: "Fiction" → Should filter by category
✓ Author: Any author → Should show their books
✓ Date Range: 2010-2020 → Should filter by year
✓ Available Only: Checked → Should exclude unavailable
✓ Sort: "Newest First" → Should order by date descending
✓ Overdue Loans: API filter → Should show only overdue
✓ Unpaid Fines: API filter → Should show only unpaid
```

---

**Last Updated:** 2026-08-16 | **All Filters Ready** ✅
