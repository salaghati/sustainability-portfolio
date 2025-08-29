import streamlit as st
import pandas as pd

st.set_page_config(page_title="Game Manager System v2 Portfolio", layout="wide")

st.title("Project Portfolio: Game Manager System v2")
st.markdown("---")

st.header("A. Project Description and Context")
st.markdown("""
The **Game Manager v2** system is an application designed to manage gaming machines across multiple branches.
- **Technology Stack:**
    - **Back-end:** Node.js / Express.js
    - **Database:** SQLite / Sequelize ORM
    - **Front-end:** React.js / Bootstrap
- **Core Functionality:**
    - Manage machine information (name, machine code, branch, type).
    - Enter and edit daily point transactions.
    - View transaction history and statistics.
- **Key Features:**
    - **Soft Delete:** Data is never permanently deleted, allowing for easy recovery.
    - **Automatic Balance Calculation:** The balance is calculated based on the latest transaction, ensuring accuracy.
    - **Rate Management:** Allows for setting and changing point conversion rates.
    - **Demo Mode:** Permits data overwriting for testing purposes without affecting production data.
    - **Data Entry Control:** Prevents and warns against data overwriting for duplicate dates (in Production mode) and only allows the most recent transaction to be edited.
    - **Change History:** Logs data changes on a per-branch basis.
    - **Security:** Utilizes JWT (JSON Web Token) for authentication and role-based (Admin/User) and branch-based authorization.
- **API Endpoints:** Provides key APIs for login, CRUD operations for machines, branches, point transactions, and history viewing.
""")

st.header("B. Role of the Business Analyst (BA)")
st.markdown("""
In this project, I served as the Business Analyst, with the following responsibilities:
- **Requirements Gathering and Analysis:** Worked with stakeholders to identify core problems such as data overwriting, difficulty in tracking balances, and the need for a clear, transparent transaction history.
- **Stakeholder Identification:**
    - **Admin:** Manages the entire system.
    - **Branch Staff:** End-users responsible for daily data entry.
    - **Accountant:** Monitors and audits the data.
- **Solution Proposal:** Based on the analysis, I proposed technical solutions and business processes, such as the anti-overwrite mechanism, a demo mode, and the data modification workflow.
- **Documentation:** Created a complete set of business documents to ensure the development team and stakeholders had a shared understanding of the system.
""")

st.markdown("---")
st.header("C. Project Documentation")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "BRD/SRS", "User Stories & AC", "Use Case Diagram",
    "BPMN/Flowchart", "ERD", "Wireframes & KPIs"
])

with tab1:
    st.subheader("1. Business Requirements Document (BRD) / Software Requirements Specification (SRS)")
    st.markdown("#### 1.1. Project Objectives")
    st.markdown("""
    - **Reduce Data Discrepancies:** Minimize point discrepancies caused by duplicate entries or uncontrolled data overwrites.
    - **Ensure Accurate Balance Management:** Guarantee that each machine's balance is calculated and updated accurately in real-time.
    - **Provide Traceable History:** Offer the ability to clearly and transparently trace transaction history and data changes.
    """)
    st.markdown("#### 1.2. Project Scope")
    st.markdown("""
    - **In-scope:**
        - Machine and branch management (Add, Edit, Soft Delete).
        - Point transaction entry and editing.
        - Role-based and branch-based user authorization.
        - Soft delete functionality for key entities.
        - Demo/Production modes to control data overwriting.
    - **Out-of-scope:**
        - Integration with external accounting systems.
        - Detailed financial reporting.
        - Inventory management for machine-related supplies.
    """)
    st.markdown("#### 1.3. Assumptions")
    st.markdown("""
    - Each machine belongs to only one branch at any given time.
    - Users are only allowed to edit the most recent point transaction for a machine.
    - Critical data (machines, branches, transactions) is not permanently deleted from the system (soft delete is applied).
    - The system requires a stable network connection to synchronize data between the client and server.
    """)
    st.markdown("#### 1.4. Functional Requirements")
    st.markdown("""
    - **FR1: Authentication and Authorization:**
        - The system must allow users to log in with a username and password.
        - The system must enforce permissions based on roles (Admin, User) and branch. Admins have full access; Users can only operate within their assigned branch.
    - **FR2: Branch Management (Admin):**
        - Admins can add, view, edit, and soft-delete branches.
    - **FR3: Machine Management (Admin):**
        - Admins can add, view, edit, soft-delete machines, and assign them to a branch.
    - **FR4: Point Transaction Management (User):**
        - Users can enter points (points_in, points_out) for a machine in their branch by date.
        - The system must automatically calculate the `current_balance` and `daily_point`.
    - **FR5: Overwrite Control:**
        - In Production mode, the system must prevent users from entering a transaction on a date that already has data and must display a warning.
        - In Demo mode, the system allows data overwriting.
    - **FR6: Transaction Editing:**
        - Users are only allowed to edit the most recent transaction for a machine.
    - **FR7: History Viewing:**
        - Both Admins and Users can view the transaction history for machines (Users can only see machines in their own branch).
    """)
    st.markdown("#### 1.5. Non-Functional Requirements")
    st.markdown("""
    - **NFR1: Security:**
        - User passwords must be hashed before being stored in the database.
        - All API requests must be authenticated using JWT.
    - **NFR2: Performance:**
        - API response time for basic CRUD operations must be under 500ms.
        - The user interface must load within 3 seconds.
    - **NFR3: Recoverability:**
        - The soft delete feature must allow for easy restoration of deleted data.
    - **NFR4: Availability:**
        - The system must be operational 99% of the time (excluding planned maintenance).
    """)

with tab2:
    st.subheader("2. User Stories & Acceptance Criteria (AC)")

    st.info("Role: Branch Staff")
    st.markdown("""
    > **As a**- Branch Staff member,
    > **I want to**- enter end-of-day points for the machines in my branch,
    - **So that**- I can record business results and have the system automatically calculate the balance.
    """)
    st.text("""
    AC 1: Given the system environment is "Production",
    When I enter points for a machine on a date that already has data,
    Then the system must display a warning "Data for this date already exists" and prevent saving.

    AC 2: Given the system environment is "Demo",
    When I enter points for a machine on a date that already has data,
    Then the system must allow overwriting the old data and save the new transaction.

    AC 3: Given I am editing a transaction,
    When that transaction is not the latest one for the machine,
    Then the system must disable the "Save" button and display the message "Only the latest transaction can be edited".
    """)

    st.info("Role: Administrator")
    st.markdown("""
    > **As an**- Administrator,
    > **I want to**- view the point transaction history for all machines across the entire system,
    - **So that**- I can check, reconcile, and monitor the operations of all branches.
    """)
    st.text("""
    AC 1: Given I am logged in as an Admin,
    When I access the History page,
    Then the system must display a data table containing all transactions from every branch.

    AC 2: Given I am viewing the History page,
    When I use the filter by branch or by machine,
    Then the data table must update according to my selection.
    """)

    st.info("Role: Accountant")
    st.markdown("""
    > **As an**- Accountant,
    > **I want to**- view the end-of-day balance report for all machines,
    - **So that**- I can perform financial reconciliation tasks.
    """)
    st.text("""
    AC 1: Given I am logged in as an Accountant,
    When I access the Reports page,
    Then the system must display the latest `current_balance` for all active machines.
    """)

with tab3:
    st.subheader("3. Use Case Diagram")
    st.markdown("This diagram describes the main actions that actors can perform on the system.")
    st.image("assets/use_case_diagram.png", caption="Use Case Diagram for Game Manager System v2")

with tab4:
    st.subheader("4. BPMN/Flowcharts")
    st.markdown("This section illustrates the key business processes within the Game Manager system.")

    # Create navigation tabs for different flowcharts
    bpmn_tab1, bpmn_tab2 = st.tabs([
        "Point Transaction Process", 
        "Machine Management Process"
    ])

    with bpmn_tab1:
        st.markdown("##### Process: Entering and Editing Point Transactions")
        st.markdown("This flowchart describes the core daily operation: how a staff member inputs or edits point data, and how the system validates and processes it, including handling Demo vs. Production modes.")
        st.image("assets/flowchart.png", caption="BPMN Flowchart for the Transaction Process")

    with bpmn_tab2:
        st.markdown("##### Process: Machine Creation, Update, and Deletion")
        st.markdown("This flowchart outlines the administrative task of managing machines. It shows the workflow for an Admin to create, modify, or soft-delete a machine, including system validation steps.")
        st.image("assets/process_Machinemanagement.png", caption="BPMN Flowchart for the Machine Management Process")

with tab5:
    st.subheader("5. Entity Relationship Diagram (ERD)")
    st.markdown("This diagram describes the complete data structure, including tables for products and edit logs, and shows the relationships between them.")
    st.image("assets/ERD.png", caption="Complete Entity Relationship Diagram for Game Manager v2")

with tab6:
    st.subheader("6. Wireframes - App Screenshots")
    st.markdown("Dưới đây là giao diện thực tế của ứng dụng Game Manager System v2 đã được phát triển:")

    # Machine List Screen
    st.markdown("#### 6.1. Machine List Screen (Màn hình Danh sách Máy)")
    st.markdown("""
    **Mô tả chức năng:**
    - **Component:** Table hiển thị danh sách các máy game
    - **Columns:** `Machine Code`, `Machine Name`, `Branch`, `Current Balance`, `Rate`, `Actions`
    - **Features:**
        - Nút "Add New Machine" để thêm máy mới
        - Phân trang cho danh sách dài
        - Cột "Actions" với các nút "Edit" và "Delete" (soft delete)
        - Thanh tìm kiếm để lọc máy theo tên hoặc mã
    """)
    
    # Hiển thị hình ảnh nếu file tồn tại
    try:
        st.image("assets/machine_list_screen.png", caption="Machine List Screen - Giao diện thực tế", use_container_width=True)
    except:
        st.info("📸 Hãy chụp screenshot màn hình Machine List và lưu với tên 'machine_list_screen.png' vào thư mục assets/")

    st.markdown("---")

    # Point Entry/Edit Form  
    st.markdown("#### 6.2. Point Entry/Edit Form (Form Nhập/Sửa Điểm)")
    st.markdown("""
    **Mô tả chức năng:**
    - **Component:** Form nhập liệu điểm số hàng ngày
    - **Fields:**
        - `Dropdown` để chọn máy (chỉ hiển thị máy trong chi nhánh của user)
        - `Input number` cho `Points IN` (điểm vào)
        - `Input number` cho `Points OUT` (điểm ra)  
        - `Date picker` để chọn ngày giao dịch
        - `Toggle switch` để bật/tắt chế độ `Demo`
    - **Business Logic:**
        - Khi chọn ngày đã có giao dịch, hiển thị cảnh báo nếu tắt chế độ `Demo`
        - Nút "Save" bị vô hiệu hóa nếu có lỗi validation
    """)
    
    try:
        st.image("assets/point_entry_form.png", caption="Point Entry Form - Giao diện thực tế", use_container_width=True)
    except:
        st.info("📸 Hãy chụp screenshot màn hình Point Entry/Edit Form và lưu với tên 'point_entry_form.png' vào thư mục assets/")

    st.markdown("---")

    # Transaction History Screen
    st.markdown("#### 6.3. Transaction History Screen (Màn hình Lịch sử Giao dịch)")
    st.markdown("""
    **Mô tả chức năng:**
    - **Component:** Table hiển thị lịch sử các giao dịch điểm
    - **Columns:** `Date`, `Machine Code`, `Points IN`, `Points OUT`, `Daily Points`, `Final Balance`, `User`, `Branch`
    - **Features:**
        - Lọc theo khoảng thời gian
        - Lọc theo chi nhánh (chỉ dành cho Admin)
        - Lọc theo máy cụ thể
        - Nút "Export to CSV" để xuất dữ liệu
    """)
    
    try:
        st.image("assets/transaction_history_screen.png", caption="Transaction History Screen - Giao diện thực tế", use_container_width=True)
    except:
        st.info("📸 Hãy chụp screenshot màn hình Transaction History và lưu với tên 'transaction_history_screen.png' vào thư mục assets/")

    st.markdown("---")

    # Optional: Login và Dashboard screens
    st.markdown("#### 6.4. Các màn hình bổ sung (Tùy chọn)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Login Screen**")
        try:
            st.image("assets/login_screen.png", caption="Login Screen", use_container_width=True)
        except:
            st.info("📸 Screenshot màn hình đăng nhập (login_screen.png)")
    
    with col2:
        st.markdown("**Dashboard/Home Screen**")
        try:
            st.image("assets/dashboard_screen.png", caption="Dashboard Screen", use_container_width=True) 
        except:
            st.info("📸 Screenshot màn hình tổng quan (dashboard_screen.png)")

    st.subheader("7. KPIs and Reports")
    st.markdown("Metrics to measure the system's effectiveness post-deployment:")
    
    kpi_data = {
        'KPI': [
            "Number of Overwrite-Blocked Transactions",
            "Balance Discrepancy Rate",
            "Average Data Entry Time",
            "Active Machines per Branch",
            "Transaction Edit Rate"
        ],
        'Description': [
            "Measures the effectiveness of the anti-overwrite feature in the Production environment.",
            "Compares system balance with actual balance, expected to decrease over time.",
            "The average time a staff member needs to complete point entry for one machine.",
            "Tracks the number of machines with transactions in a month, broken down by branch.",
            "The number of times a transaction is edited. A high rate may indicate issues in the data entry process."
        ],
        'Target': [
            "Increase (proves feature effectiveness)",
            "Decrease by >90%",
            "Decrease by 50% (vs. manual process)",
            "N/A",
            "Minimize"
        ]
    }
    kpi_df = pd.DataFrame(kpi_data)
    st.table(kpi_df)

st.markdown("---")
st.header("D. Skills Acquired")
st.success("""
- **Business Problem Analysis:** Successfully identified and addressed the core user pain point (data overwriting), which delivered the highest value to end-users and guaranteed data integrity.
- **Solution Design & Requirements Management:** Designed a practical solution by separating Demo and Production environments. This approach balanced user training needs with the critical requirement for data integrity.
- **Technical Documentation & Communication:** Authored comprehensive documentation (BRD, Use Cases, BPMN, ERD) that fostered a shared understanding between stakeholders and the development team, significantly reducing ambiguity and rework.
""")
