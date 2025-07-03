import streamlit as st
import pandas as pd
import sqlite3
import time
import json
import requests
from streamlit_lottie import st_lottie
import plotly.graph_objects as go
import plotly.express as px

# Page config
st.set_page_config(
    page_title="🔮 SQL Whisperer",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for dark theme and animations
st.markdown("""
<style>
.stApp {
        color: white;
        background-color: #1e1e1e;
    }
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a2e 50%, #16213e 100%);
        font-family: 'Inter', sans-serif;
    }
    
    /* Main container */
    .main-container {
        background: linear-gradient(135deg, rgba(26, 26, 46, 0.9) 0%, rgba(22, 33, 62, 0.9) 100%);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Title Animation */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 20px #667eea;
        }
        to {
            text-shadow: 0 0 30px #764ba2, 0 0 40px #764ba2;
        }
    }
    
    .subtitle {
        text-align: center;
        color: #a0a0a0;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        animation: fadeIn 1s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    /* Input Section */
    .input-section {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 2rem;
        margin: 2rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .input-section:hover {
        background: rgba(255, 255, 255, 0.08);
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* Custom Button */
    .custom-button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        border: none;
        border-radius: 10px;
        color: white;
        padding: 12px 30px;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .custom-button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(102, 126, 234, 0.4);
        background: linear-gradient(45deg, #764ba2 0%, #667eea 100%);
    }
    
    /* SQL Output */
    .sql-output {
        background: #1e1e1e;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
        font-family: 'Monaco', 'Consolas', monospace;
        position: relative;
        overflow: hidden;
    }
    
    .sql-output::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, #667eea, #764ba2);
        animation: shimmer 2s infinite;
    }
    
    @keyframes shimmer {
        0% { transform: translateX(-100%); }
        100% { transform: translateX(100%); }
    }
    
    /* Loading Animation */
    .loading-spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #667eea;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Typing Animation */
    .typing-animation {
        overflow: hidden;
        border-right: .15em solid #667eea;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .05em;
        animation: typing 3.5s steps(40, end), blink-caret .75s step-end infinite;
    }
    
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #667eea; }
    }
    
    /* Result Table */
    .result-table {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        backdrop-filter: blur(5px);
    }
    
    /* Sidebar Styles */
    .css-1d391kg {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
    }
    
    /* Hide Streamlit Menu */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Custom Metrics */
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 1rem;
        text-align: center;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: scale(1.05);
        background: rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

def load_lottie_url(url: str):
    """Load Lottie animation from URL"""
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

def init_database():
    """Initialize mock database with sample data"""
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # Create sample tables
    cursor.execute('''
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE,
            city TEXT,
            signup_date DATE
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            customer_id INTEGER,
            product_name TEXT,
            quantity INTEGER,
            price REAL,
            order_date DATE,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT,
            price REAL,
            stock INTEGER
        )
    ''')
    
    # Insert sample data
    customers_data = [
        (1, 'Alice Johnson', 'alice@email.com', 'New York', '2023-01-15'),
        (2, 'Bob Smith', 'bob@email.com', 'Los Angeles', '2023-02-20'),
        (3, 'Carol Davis', 'carol@email.com', 'Chicago', '2023-03-10'),
        (4, 'David Wilson', 'david@email.com', 'Houston', '2023-04-05'),
        (5, 'Eva Brown', 'eva@email.com', 'Phoenix', '2023-05-12')
    ]
    
    orders_data = [
        (1, 1, 'Laptop', 1, 999.99, '2023-01-20'),
        (2, 2, 'Mouse', 2, 29.99, '2023-02-25'),
        (3, 1, 'Keyboard', 1, 79.99, '2023-03-15'),
        (4, 3, 'Monitor', 1, 299.99, '2023-03-20'),
        (5, 4, 'Laptop', 1, 1199.99, '2023-04-10'),
        (6, 5, 'Headphones', 1, 149.99, '2023-05-15'),
        (7, 2, 'Webcam', 1, 89.99, '2023-06-01'),
        (8, 3, 'Tablet', 1, 399.99, '2023-06-10')
    ]
    
    products_data = [
        (1, 'Laptop', 'Electronics', 999.99, 50),
        (2, 'Mouse', 'Electronics', 29.99, 100),
        (3, 'Keyboard', 'Electronics', 79.99, 75),
        (4, 'Monitor', 'Electronics', 299.99, 30),
        (5, 'Headphones', 'Electronics', 149.99, 60),
        (6, 'Webcam', 'Electronics', 89.99, 40),
        (7, 'Tablet', 'Electronics', 399.99, 25)
    ]
    
    cursor.executemany('INSERT INTO customers VALUES (?, ?, ?, ?, ?)', customers_data)
    cursor.executemany('INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)', orders_data)
    cursor.executemany('INSERT INTO products VALUES (?, ?, ?, ?, ?)', products_data)
    
    conn.commit()
    return conn

def generate_mock_sql(prompt):
    """Generate mock SQL based on prompt keywords"""
    prompt_lower = prompt.lower()
    
    if 'top' in prompt_lower and ('order' in prompt_lower or 'sale' in prompt_lower):
        if 'revenue' in prompt_lower or 'price' in prompt_lower:
            return "SELECT o.product_name, SUM(o.price * o.quantity) as total_revenue FROM orders o GROUP BY o.product_name ORDER BY total_revenue DESC LIMIT 10;"
        else:
            return "SELECT o.product_name, COUNT(*) as order_count FROM orders o GROUP BY o.product_name ORDER BY order_count DESC LIMIT 10;"
    
    elif 'customer' in prompt_lower:
        if 'city' in prompt_lower:
            return "SELECT city, COUNT(*) as customer_count FROM customers GROUP BY city ORDER BY customer_count DESC;"
        else:
            return "SELECT * FROM customers ORDER BY signup_date DESC;"
    
    elif 'product' in prompt_lower:
        return "SELECT * FROM products ORDER BY price DESC;"
    
    elif 'recent' in prompt_lower or 'latest' in prompt_lower:
        return "SELECT c.name, o.product_name, o.price, o.order_date FROM orders o JOIN customers c ON o.customer_id = c.id ORDER BY o.order_date DESC LIMIT 10;"
    
    else:
        return f"SELECT * FROM orders WHERE product_name LIKE '%{prompt.split()[0] if prompt.split() else 'laptop'}%' LIMIT 10;"

def execute_query(conn, query):
    """Execute SQL query and return results"""
    try:
        df = pd.read_sql_query(query, conn)
        return df, None
    except Exception as e:
        return None, str(e)

# Initialize session state
if 'db_conn' not in st.session_state:
    st.session_state.db_conn = init_database()

if 'query_history' not in st.session_state:
    st.session_state.query_history = []

# Main App
def main():
    # Load Lottie animations
    lottie_ai = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_fcfjwiyb.json")  # AI animation
    lottie_loading = load_lottie_url("https://assets9.lottiefiles.com/packages/lf20_p8bfn5to.json")  # Loading animation
    
    # Header
    st.markdown("""
    <div class="main-container">
        <h1 class="main-title">🔮 SQL Whisperer</h1>
        <p class="subtitle">Transform natural language into powerful SQL queries with AI magic</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # Theme toggle (placeholder)
        theme = st.selectbox("🎨 Theme", ["Dark Cosmic", "Midnight Blue", "Purple Haze"], index=0)
        
        st.markdown("---")
        
        # Database info
        st.markdown("### 📊 Database Info")
        st.info("Connected to in-memory SQLite database with sample e-commerce data")
        
        # Quick stats
        if st.session_state.db_conn:
            cursor = st.session_state.db_conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM customers")
            customer_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM orders")
            order_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM products")
            product_count = cursor.fetchone()[0]
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("👥 Customers", customer_count)
            with col2:
                st.metric("🛒 Orders", order_count)
            with col3:
                st.metric("📦 Products", product_count)
        
        st.markdown("---")
        
        # Feedback
        st.markdown("### 💬 Feedback")
        if st.button("🐛 Report Issue"):
            st.balloons()
            st.success("Thank you! Issue reported.")
        
        if st.button("⭐ Rate App"):
            st.balloons()
            st.success("Thank you for your feedback!")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Input section
        st.markdown("""
        <div class="input-section">
        """, unsafe_allow_html=True)
        
        st.markdown("### 💭 Natural Language Query")
        
        # Sample prompts
        sample_prompts = [
            "Show top 10 products by revenue",
            "List all customers from New York",
            "Find recent orders in the last month",
            "Show customer distribution by city",
            "Display highest priced products"
        ]
        
        selected_sample = st.selectbox("🎯 Try a sample query:", ["Custom query..."] + sample_prompts)
        
        if selected_sample != "Custom query...":
            user_input = selected_sample
        else:
            user_input = st.text_area(
                "",
                placeholder="e.g., Show me the top 10 customers by total spending...",
                height=100,
                key="user_input"
            )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Generate button
        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
        with col_btn2:
            if st.button("✨ Generate SQL Magic", key="generate_btn", use_container_width=True):
                if user_input:
                    # Show loading animation
                    with st.spinner("🔮 Conjuring SQL magic..."):
                        time.sleep(2)  # Simulate AI processing time
                        
                        # Generate mock SQL
                        generated_sql = generate_mock_sql(user_input)
                        st.session_state.current_sql = generated_sql
                        st.session_state.current_prompt = user_input
                else:
                    st.warning("Please enter a query first!")
        
        # Display generated SQL
        if 'current_sql' in st.session_state:
            st.markdown("### 🎯 Generated SQL Query")
            st.markdown(f"""
            <div class="sql-output">
                <code>{st.session_state.current_sql}</code>
            </div>
            """, unsafe_allow_html=True)
            
            # Execute button
            col_exec1, col_exec2, col_exec3 = st.columns([1, 2, 1])
            with col_exec2:
                if st.button("🚀 Execute Query", key="execute_btn", use_container_width=True):
                    with st.spinner("⚡ Executing query..."):
                        time.sleep(1)
                        
                        # Execute query
                        df, error = execute_query(st.session_state.db_conn, st.session_state.current_sql)
                        
                        if error:
                            st.error(f"Query Error: {error}")
                        else:
                            st.session_state.current_results = df
                            st.session_state.query_history.append({
                                'prompt': st.session_state.current_prompt,
                                'sql': st.session_state.current_sql,
                                'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                            })
    
    with col2:
        # Display Lottie animation
        if lottie_ai:
            st_lottie(lottie_ai, height=200, key="ai_animation")
        
        # Query tips
        st.markdown("### 💡 Query Tips")
        tips = [
            "🎯 Be specific with your requirements",
            "📊 Use terms like 'top', 'highest', 'recent'",
            "🔍 Mention specific columns or filters",
            "📈 Ask for aggregations like 'total', 'count'",
            "🗓️ Include date ranges when needed"
        ]
        
        for tip in tips:
            st.markdown(f"• {tip}")
    
    # Results section
    if 'current_results' in st.session_state and st.session_state.current_results is not None:
        st.markdown("---")
        st.markdown("### 📊 Query Results")
        
        df = st.session_state.current_results
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📝 Rows", len(df))
        with col2:
            st.metric("📋 Columns", len(df.columns))
        with col3:
            if df.select_dtypes(include=['number']).empty:
                st.metric("🔢 Numeric Cols", 0)
            else:
                st.metric("🔢 Numeric Cols", len(df.select_dtypes(include=['number']).columns))
        with col4:
            st.metric("💾 Size (KB)", f"{df.memory_usage(deep=True).sum() / 1024:.1f}")
        
        # Display table
        st.dataframe(df, use_container_width=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"query_results_{int(time.time())}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Visualization suggestion
        if len(df.columns) >= 2 and not df.empty:
            st.markdown("### 📈 Quick Visualization")
            
            numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
            text_cols = df.select_dtypes(include=['object']).columns.tolist()
            
            if numeric_cols and text_cols:
                # Create a simple bar chart
                if len(df) <= 20:  # Only for reasonable number of rows
                    fig = px.bar(
                        df.head(10), 
                        x=text_cols[0], 
                        y=numeric_cols[0],
                        title=f"{numeric_cols[0]} by {text_cols[0]}",
                        template="plotly_dark"
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    # Query History
    if st.session_state.query_history:
        st.markdown("---")
        st.markdown("### 📜 Query History")
        
        with st.expander("View Previous Queries", expanded=False):
            for i, query in enumerate(reversed(st.session_state.query_history[-5:])):  # Show last 5
                st.markdown(f"""
                **{query['timestamp']}**  
                *Prompt:* {query['prompt']}  
                *SQL:* `{query['sql']}`
                """)
                st.markdown("---")

if __name__ == "__main__":
    main()
