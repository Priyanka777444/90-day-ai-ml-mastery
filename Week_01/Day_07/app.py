"""
MyLife Dashboard
Features: Finance Tracker, Bookshelf with language filter, Read Book, Delete Book
"""

import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date, datetime
import database as db
import open_library_api as books_api
import auth
from theme import inject_theme, login_page_css, panda_banner, panda_banner

auth.init_auth_db()
db.init_database()

st.set_page_config(page_title="MyLife Dashboard", page_icon="✦", layout="wide")
inject_theme()

for key, default in [
    ('logged_in', False), ('user_id', None), ('username', None),
    ('full_name', None),  ('show_register', False),
    ('reading_book', None),   # holds the book row tuple when in reader view
    ('custom_categories', []),  # user-defined expense categories
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─────────────────────────── AUTH ────────────────────────────
if not st.session_state.logged_in:
    if st.session_state.show_register:
        login_page_css()
        st.markdown('<h1 style="text-align:center;margin-bottom:8px;">Register</h1>', unsafe_allow_html=True)
        with st.form("reg"):
            # Two fields side by side to keep the card compact
            r1, r2 = st.columns(2)
            fn = r1.text_input("Full Name")
            un = r2.text_input("Username")
            em = st.text_input("Email")
            pw = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            # "Back to Login" lives INSIDE the form as a plain styled link
            st.markdown(
                """<div style="text-align:center;margin-top:6px;">
                    <span style="font-family:'Raleway',sans-serif;font-size:0.82rem;
                    color:#b97a95;">Already have an account?</span>
                </div>""",
                unsafe_allow_html=True
            )
            if submitted:
                success, uid, msg = auth.register_user(un, em, pw, fn)
                if success:
                    st.success("Registered! Please Login.")
                    st.session_state.show_register = False
                    st.rerun()
                else:
                    st.error(msg)
        # Back to Login button sits right below the card, full width, always visible
        if st.button("← Back to Login", key="back_to_login", use_container_width=True):
            st.session_state.show_register = False
            st.rerun()
        panda_banner()
    else:
        login_page_css()
        st.markdown('<h1 style="text-align:center;margin-bottom:8px;">Login</h1>', unsafe_allow_html=True)
        with st.form("login"):
            un = st.text_input("Username")
            pw = st.text_input("Password", type="password")
            if st.form_submit_button("Login", use_container_width=True):
                success, uid, fn, msg = auth.login_user(un, pw)
                if success:
                    st.session_state.logged_in = True
                    st.session_state.user_id   = uid
                    st.session_state.full_name = fn
                    st.rerun()
                else:
                    st.error(msg)
        if st.button("Need an account? Register →", key="go_register", use_container_width=True):
            st.session_state.show_register = True
            st.rerun()
        panda_banner()
    st.stop()

# ─────────────────────────── HELPERS ─────────────────────────
user_id   = st.session_state.user_id
full_name = st.session_state.full_name

# 12 columns — must match get_books() SELECT exactly
BOOKS_COLS = ['ID','UID','BID','Title','Author','Cover','Shelf','Total','Read','Languages','IA_ID','Added']

LANG_COLORS = {
    "English": "🟦", "Hindi": "🟧", "Spanish": "🟩", "French": "🟪",
    "German":  "🟥", "Chinese": "🟨", "Japanese": "⬜", "Arabic": "🟫",
}

def lang_badges(languages_str):
    if not languages_str:
        return "_Not available_"
    langs = [l.strip() for l in languages_str.split(",") if l.strip()]
    return "  ".join(f"{LANG_COLORS.get(l, '🔹')} {l}" for l in langs[:6])

# ─────────────────────────── SIDEBAR ─────────────────────────
st.sidebar.title(f"👤 {full_name}")
if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in   = False
    st.session_state.reading_book = None
    initial_sidebar_state="expanded"
    st.rerun()

# If a book is being read, show the reader — no nav needed
if st.session_state.reading_book is not None:
    book = st.session_state.reading_book  # tuple of 12 columns

    # ═══════════════════ BOOK READER VIEW ═══════════════════
    if st.button("← Back to Library"):
        st.session_state.reading_book = None
        st.switch_page("📚 Bookshelf")

    book_id_str = book[2]   # e.g. "OL45804W"
    ia_id       = book[10]  # Internet Archive ID (may be empty)

    col_img, col_info = st.columns([1, 3])
    if book[5]:
        col_img.image(book[5], width=160)

    with col_info:
        st.title(book[3])
        st.subheader(f"by {book[4]}")
        st.write(f"📚 Shelf: `{book[6]}`   |   📄 Pages: {book[7] or 'Unknown'}")
        if book[9]:
            st.write(f"🌐 Languages: {lang_badges(book[9])}")

        # Quick shelf update
        shelves = ["Currently Reading", "Want to Read", "Finished"]
        new_shelf = st.selectbox("Move to shelf", shelves, index=shelves.index(book[6]) if book[6] in shelves else 0)
        if st.button("Update Shelf"):
            db.update_book_shelf(book[0], new_shelf)
            # Refresh the cached book tuple
            updated = [b for b in db.get_books(user_id) if b[0] == book[0]]
            if updated:
                st.session_state.reading_book = updated[0]
            st.success("Shelf updated!")
            st.rerun()

    st.markdown("---")

    # Fetch live details from Open Library
    with st.spinner("Loading book details..."):
        details = books_api.get_book_details(book_id_str)

    if details:
        # Description
        st.subheader("📖 About this Book")
        st.write(details['description'])

        if details['first_sentence']:
            st.info(f"**Opening line:** {details['first_sentence']}")

        # Subjects / Tags
        if details['subjects']:
            st.subheader("🏷️ Subjects")
            st.write("  •  ".join(details['subjects']))

        st.markdown("---")

        # Reading options
        st.subheader("📚 Read this Book")

        read_col1, read_col2 = st.columns(2)

        # Option 1: Internet Archive embed (free public domain books)
        # Try ia_id from DB first, fall back to details
        effective_ia = ia_id or ""
        archive_read_url = books_api.get_read_url(effective_ia) if effective_ia else None

        if archive_read_url:
            with read_col1:
                st.success("✅ Full text available via Internet Archive!")
                st.link_button("📖 Read Full Book (Internet Archive)", archive_read_url, use_container_width=True)

                # Embed the reader directly in the app
                st.subheader("In-App Reader")
                embed_url = f"https://archive.org/embed/{effective_ia}?ui=embed"
                st.components.v1.iframe(embed_url, height=600, scrolling=True)
        else:
            with read_col1:
                st.warning("⚠️ Full text not freely available for this book.")
                st.write("This book may be under copyright. You can:")
                st.write("- Borrow it from your local library")
                st.write("- Purchase it from a bookstore")

        with read_col2:
            st.info("🔗 External Links")
            st.link_button(
                "🌐 View on Open Library",
                details['openlibrary_url'],
                use_container_width=True
            )
            if details.get('read_url'):
                st.link_button(
                    "📚 Read on Archive.org",
                    details['read_url'],
                    use_container_width=True
                )
            # Google Books search as fallback
            google_url = f"https://www.google.com/search?q={book[3].replace(' ', '+')}+{book[4].replace(' ', '+')}+read+online+free"
            st.link_button("🔍 Search on Google", google_url, use_container_width=True)
    else:
        st.error("Could not load book details. Please check your internet connection.")

    st.stop()  # Don't render the rest of the app while in reader

# ─────────────────────────── MAIN NAV ────────────────────────
page = st.sidebar.radio("Navigate", ["🏠 Dashboard", "💰 Finance Tracker", "📚 Bookshelf"])

# ═══════════════════════ DASHBOARD ═══════════════════════════
if page == "🏠 Dashboard":
    st.title(f"Hello There, {full_name}")

    expenses = db.get_expenses(user_id)
    books    = db.get_books(user_id)

    c1, c2, c3 = st.columns(3)
    total_exp = sum(e[1] for e in expenses) if expenses else 0
    c1.metric("Total Spent",       f"₹{total_exp:,.2f}")
    c2.metric("Books on Shelf",    len(books))
    c3.metric("Currently Reading", sum(1 for b in books if b[6] == 'Currently Reading'))

    st.markdown("---")
    col_l, col_r = st.columns(2)

    with col_l:
        if expenses:
            df_exp = pd.DataFrame(expenses, columns=['ID','Amount','Category','Desc','Date','Acc','Bank'])
            st.plotly_chart(
                px.pie(df_exp, values='Amount', names='Category', title="Spending by Category"),
                use_container_width=True)

    with col_r:
        if books:
            df_b = pd.DataFrame(books, columns=BOOKS_COLS)
            st.plotly_chart(
                px.bar(df_b.groupby('Shelf').size().reset_index(name='Count'),
                       x='Shelf', y='Count', title="Reading Status"),
                use_container_width=True)
        

# ═══════════════════════ FINANCE TRACKER ═════════════════════
elif page == "💰 Finance Tracker":
    st.title("💰 Finance Tracker")
    accounts = db.get_accounts(user_id)

    if accounts:
        st.subheader("💳 Account Summary")
        cols = st.columns(len(accounts))
        for idx, acc in enumerate(accounts):
            cols[idx].metric(acc[2], f"₹{float(acc[5]):,.2f}", acc[3])
        st.markdown("---")

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "➕ Add Expense", "💵 Add Income", "🔄 Transfer",
        "📋 View Transactions", "🏦 Manage Accounts", "📊 Analytics", "💸Monthly Expense"
    ])

    with tab1:
        if not accounts:
            st.warning("Add an account first!")
        else:
            # ── Category picker lives OUTSIDE the form so session_state works ──
            PRESET_CATEGORIES = ["Food", "Transport", "Bills", "Shopping",
                                  "Entertainment", "Health", "Education", "Other"]

            # Build full list: presets + any saved custom ones + the add-new option
            if 'custom_categories' not in st.session_state:
                st.session_state.custom_categories = []

            all_categories = PRESET_CATEGORIES + st.session_state.custom_categories + ["➕ Add new category..."]

            exp_col1, exp_col2 = st.columns(2)
            cat_choice = exp_col1.selectbox("Category", all_categories, key="exp_cat_select")

            # If user picks "Add new", show inline input + Save button
            if cat_choice == "➕ Add new category...":
                new_cat_col, save_col = exp_col1.columns([3, 1])
                new_cat_name = new_cat_col.text_input(
                    "New category name",
                    placeholder="e.g. Gym, Pet Care, Rent...",
                    key="new_cat_input",
                    label_visibility="collapsed"
                )
                if save_col.button("Save", key="save_cat_btn"):
                    if new_cat_name.strip() and new_cat_name.strip() not in all_categories:
                        st.session_state.custom_categories.append(new_cat_name.strip())
                        st.success(f"✅ '{new_cat_name.strip()}' added to categories!")
                        st.rerun()
                    elif not new_cat_name.strip():
                        st.error("Please type a category name first.")
                    else:
                        st.warning("That category already exists.")
                final_category = new_cat_name.strip() if new_cat_name.strip() else ""
            else:
                final_category = cat_choice

            with st.form("expense_form"):
                col1, col2 = st.columns(2)
                amount     = col1.number_input("Amount (₹)", min_value=0.0)
                # Show the resolved category (read-only inside form)
                col1.markdown(f"**Category:** `{final_category or '— select above —'}`")
                acc_choice = col1.selectbox("Account", [(a[0], a[2]) for a in accounts], format_func=lambda x: x[1])
                ex_date    = col2.date_input("Date", value=date.today())
                desc       = col2.text_input("Description")
                if st.form_submit_button("Add Expense"):
                    if not final_category:
                        st.error("Please select or add a category above.")
                    elif cat_choice == "➕ Add new category...":
                        st.error("Save your new category first, then submit.")
                    elif amount <= 0:
                        st.error("Amount must be greater than 0.")
                    elif amount > db.get_account_balance(acc_choice[0]):
                        st.error("Insufficient balance!")
                    else:
                        db.add_expense(user_id, amount, final_category, desc, str(ex_date), acc_choice[0])
                        st.success("✅ Added!")
                        st.rerun()

    with tab2:
        if not accounts:
            st.warning("Add an account first!")
        else:
            with st.form("income_form"):
                col1, col2 = st.columns(2)
                in_amt = col1.number_input("Amount (₹)", min_value=0.0)
                source = col1.selectbox("Source", ["Salary", "Freelance", "Investment", "Other"])
                in_acc = col1.selectbox("Deposit To", [(a[0], a[2]) for a in accounts], format_func=lambda x: x[1])
                in_dt  = col2.date_input("Date", value=date.today())
                in_ds  = col2.text_input("Description")
                if st.form_submit_button("Add Income"):
                    db.add_income(user_id, in_amt, source, in_ds, str(in_dt), in_acc[0])
                    st.success("✅ Income Added!")
                    st.rerun()

    with tab3:
        if len(accounts) < 2:
            st.info("Need at least 2 accounts to transfer.")
        else:
            with st.form("transfer_form"):
                col1, col2 = st.columns(2)
                f_acc  = col1.selectbox("From", [(a[0], a[2]) for a in accounts], format_func=lambda x: x[1])
                tr_amt = col1.number_input("Amount (₹)", min_value=0.0)
                t_acc  = col2.selectbox("To", [(a[0], a[2]) for a in accounts if a[0] != f_acc[0]], format_func=lambda x: x[1])
                tr_dt  = col2.date_input("Date", value=date.today())
                if st.form_submit_button("Transfer"):
                    if tr_amt > 0 and tr_amt <= db.get_account_balance(f_acc[0]):
                        db.transfer_money(user_id, tr_amt, f_acc[0], t_acc[0], "Transfer", str(tr_dt))
                        st.success("✅ Done!")
                        st.rerun()
                    elif tr_amt > 0:
                        st.error("Insufficient balance!")

    with tab4:
        st.subheader("Transaction History")
        h_type = st.radio("View", ["Expenses", "Income", "Transfers"], horizontal=True)

        if h_type == "Expenses":
            data = db.get_expenses(user_id)
            if data:
                h1,h2,h3,h4,h5 = st.columns([2,2,3,2,1])
                h1.write("**Date**"); h2.write("**Amount**")
                h3.write("**Category**"); h4.write("**Account**"); h5.write("**Del**")
                for exp in data:
                    c1,c2,c3,c4,c5 = st.columns([2,2,3,2,1])
                    c1.write(exp[4]); c2.write(f"₹{float(exp[1]):,.2f}")
                    c3.write(f"{exp[2]} ({exp[3] or '-'})"); c4.write(exp[5])
                    if c5.button("🗑️", key=f"del_exp_{exp[0]}"):
                        db.delete_expense(exp[0])
                        st.success("Deleted!"); st.rerun()
            else:
                st.info("No expense records found.")

        elif h_type == "Income":
            data = db.get_income(user_id)
            if data:
                h1,h2,h3,h4 = st.columns([2,2,3,2])
                h1.write("**Date**"); h2.write("**Amount**")
                h3.write("**Source**"); h4.write("**Account**")
                for inc in data:
                    c1,c2,c3,c4 = st.columns([2,2,3,2])
                    c1.write(inc[3]); c2.write(f"₹{float(inc[0]):,.2f}")
                    c3.write(f"{inc[1]} ({inc[2] or '-'})"); c4.write(inc[4])
            else:
                st.info("No income records found.")

        elif h_type == "Transfers":
            data = db.get_transfers(user_id)
            if data:
                h1,h2,h3,h4 = st.columns([2,2,3,2])
                h1.write("**Date**"); h2.write("**Amount**")
                h3.write("**From**"); h4.write("**To**")
                for tr in data:
                    c1,c2,c3,c4 = st.columns([2,2,3,2])
                    c1.write(tr[0]); c2.write(f"₹{float(tr[1]):,.2f}")
                    c3.write(tr[2]); c4.write(tr[3])
            else:
                st.info("No transfer records found.")

    with tab5:
        st.subheader("Manage Bank Accounts")
        with st.expander("➕ Add New Account"):
            with st.form("add_new_acc"):
                n_name = st.text_input("Account Name")
                n_bank = st.text_input("Bank Name")
                n_type = st.selectbox("Type", ["Savings", "Current", "Cash", "Wallet"])
                n_bal  = st.number_input("Initial Balance", min_value=0.0)
                if st.form_submit_button("Create"):
                    db.add_account(user_id, n_name, n_bank, n_type, n_bal)
                    st.rerun()
        for acc in accounts:
            col_m1, col_m2 = st.columns([4, 1])
            col_m1.write(f"**{acc[2]}** ({acc[3]}) - ₹{acc[5]:,.2f}")
            if col_m2.button("🗑️", key=f"del_acc_{acc[0]}"):
                db.delete_account(acc[0])
                st.rerun()

    with tab6:
        st.subheader("Analytics")
        data = db.get_expenses(user_id)
        if data:
            df_an = pd.DataFrame(data, columns=['ID','Amount','Category','Description','Date','Account','Bank'])
            st.plotly_chart(
                px.pie(df_an, values='Amount', names='Category', title="Spending Distribution"),
                use_container_width=True)
        else:
            st.info("Add some expenses to see analytics!")
    with tab7:
        st.subheader("💸 Monthly Expense")

        today = datetime.today()
        c_month = today.strftime("%Y-%m")

        budget = st.number_input(f"Set Budget for {c_month} (₹)", min_value=0.0)

        if st.button("Save Budget"):
            db.save_monthly_budget(user_id, c_month, budget)  # ← save_monthly_budget
            st.success("Budget Saved ✅")

        saved_budget = db.get_monthly_budget(user_id, c_month)  # ← only 2 args now
        total_expense = db.get_monthly_expense(user_id, c_month)

        if saved_budget and saved_budget > 0:
            remaining = saved_budget - total_expense
            percent_used = (total_expense / saved_budget) * 100

            st.write(f"Budget: ₹{saved_budget:,.2f}")
            st.write(f"Spent: ₹{total_expense:,.2f}")
            st.write(f"Remaining: ₹{remaining:,.2f}")
            st.write(f"Budget Used: {percent_used:.2f}%")

            progress_value = min(total_expense / saved_budget, 1.0)
            st.progress(progress_value)

            if percent_used >= 100:
                st.error("⚠ Budget Exceeded!")
            elif percent_used >= 80:
                st.warning("⚠ You have used more than 80% of your budget.")
        else:
            st.info("No budget set for this month yet.")
        
        st.markdown("---")
        st.subheader("📊 Category Breakdown")

        category_data = db.get_category_expense(user_id, c_month)

        if category_data:
            for category, amount in category_data:
                percent = (amount / total_expense) * 100
                st.write(f"**{category}** — ₹{amount:,.2f} ({percent:.1f}%)")
                st.progress(amount / total_expense)
        else:
            st.info("No expenses this month yet.")

# ═══════════════════════ BOOKSHELF ═══════════════════════════
elif page == "📚 Bookshelf":
    st.title("📚 My Bookshelf")
    t1, t2 = st.tabs(["🔍 Find Books", "📖 My Library"])

    # ──────────── FIND TAB ────────────
    with t1:
        query = st.text_input("Search Book Title")
        if query:
            with st.spinner("Searching..."):
                results = books_api.search_books(query)

            if not results:
                st.info("No results found. Try a different search term.")

            for b in results:
                with st.container():
                    c1, c2 = st.columns([1, 4])
                    if b['cover_url']:
                        c1.image(b['cover_url'])
                    else:
                        c1.write("📖")

                    c2.write(f"**{b['title']}** by {b['author']}")
                    if b['first_publish_year'] != 'N/A':
                        c2.caption(f"First published: {b['first_publish_year']}")

                    # Language badges
                    langs_list = b.get('languages', [])
                    if langs_list:
                        badges = "  ".join(f"{LANG_COLORS.get(l,'🔹')} {l}" for l in langs_list[:5])
                        if len(langs_list) > 5:
                            badges += f"  *(+{len(langs_list)-5} more)*"
                        c2.caption(f"🌐 Available in: {badges}")
                    else:
                        c2.caption("🌐 Language info not available")

                    # Fulltext badge
                    if b.get('has_fulltext') or b.get('ia_id'):
                        c2.success("📖 Full text available to read!")

                    book_id = b.get('id', b.get('key', 'unknown')).replace("/works/", "")
                    shelf = c2.selectbox(
                        "Add to shelf",
                        ["Currently Reading", "Want to Read", "Finished"],
                        key=f"s_{book_id}"
                    )

                    if c2.button("➕ Add to Library", key=f"b_{book_id}"):
                        langs_str = ",".join(langs_list)
                        ia_id_val = b.get('ia_id') or ""
                        db.add_book(
                            user_id, book_id, b['title'], b['author'],
                            b['cover_url'], shelf, b.get('pages', 0),
                            langs_str, ia_id_val
                        )
                        st.success(f"✅ '{b['title']}' added to '{shelf}'!")

                st.markdown("---")

    # ──────────── LIBRARY TAB ────────────
    with t2:
        books = db.get_books(user_id)

        if not books:
            st.info("Your library is empty. Go to 'Find Books' to add some!")
        else:
            df_b = pd.DataFrame(books, columns=BOOKS_COLS)

            # Filter bar
            st.subheader("🔍 Filter")
            fc1, fc2 = st.columns(2)

            shelf_opts = ["All"] + sorted(df_b['Shelf'].unique().tolist())
            shelf_filter = fc1.selectbox("Shelf", shelf_opts)

            all_langs = set()
            for ls in df_b['Languages'].dropna():
                for l in ls.split(","):
                    l = l.strip()
                    if l:
                        all_langs.add(l)
            lang_opts   = ["All"] + sorted(all_langs)
            lang_filter = fc2.selectbox("Language", lang_opts)

            filtered = df_b.copy()
            if shelf_filter != "All":
                filtered = filtered[filtered['Shelf'] == shelf_filter]
            if lang_filter != "All":
                filtered = filtered[filtered['Languages'].str.contains(lang_filter, na=False)]

            st.markdown(f"Showing **{len(filtered)}** of **{len(df_b)}** books")
            st.markdown("---")

            if filtered.empty:
                st.info("No books match your filter.")
            else:
                for _, row in filtered.iterrows():
                    bc1, bc2, bc3 = st.columns([1, 4, 1])

                    # Cover
                    if row['Cover']:
                        bc1.image(row['Cover'], width=90)
                    else:
                        bc1.write("📖")

                    # Info
                    bc2.write(f"**{row['Title']}**")
                    bc2.write(f"✍️ {row['Author']}")
                    bc2.write(f"📚 `{row['Shelf']}`")
                    if row['Languages']:
                        bc2.caption(f"🌐 {lang_badges(row['Languages'])}")
                    if row['IA_ID']:
                        bc2.caption("✅ Full text available")

                    # Action buttons
                    if bc3.button("📖 Read", key=f"read_{row['ID']}", use_container_width=True):
                        # Find the matching tuple from the original list to pass to reader
                        match = [b for b in books if b[0] == row['ID']]
                        if match:
                            st.session_state.reading_book = match[0]
                            st.rerun()

                    if bc3.button("🗑️ Remove", key=f"del_book_{row['ID']}", use_container_width=True):
                        db.delete_book(row['ID'])
                        st.success(f"'{row['Title']}' removed from library.")
                        st.rerun()

                    st.markdown("---")
    
    