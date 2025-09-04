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
    st.markdown("Below are the actual interfaces of the developed Game Manager System v2 application:")

    # Machine List Screen
    st.markdown("#### 6.1. Machine List Screen")
    st.markdown("""
    **Functional Description:**
    - **Component:** Table displaying list of gaming machines
    - **Columns:** `Machine Code`, `Machine Name`, `Branch`, `Current Balance`, `Rate`, `Actions`
    - **Features:**
        - "Add New Machine" button to add new machines
        - Pagination for long lists
        - "Actions" column with "Edit" and "Delete" (soft delete) buttons
        - Search bar to filter machines by name or code
    """)
    
    # Hiển thị hình ảnh mới nhất
    try:
        st.image("assets/machine_list_new_interface.png", caption="Machine List Screen - Actual Interface", use_container_width=True)
    except:
        st.info("📸 Please capture screenshot of Machine List screen and save as 'machine_list_new_interface.png' in assets/ folder")

    st.markdown("---")

    # Point Entry/Edit Form  
    st.markdown("#### 6.2. Point Entry/Edit Form")
    st.markdown("""
    **Functional Description:**
    - **Component:** Daily point data entry form
    - **Fields:**
        - `Dropdown` to select machine (shows only machines in user's branch)
        - `Input number` for `Points IN`
        - `Input number` for `Points OUT`  
        - `Date picker` to select transaction date
        - `Toggle switch` to enable/disable `Demo` mode
    - **Business Logic:**
        - When selecting a date with existing transaction, shows warning if `Demo` mode is off
        - "Save" button is disabled if there are validation errors
    """)
    
    try:
        st.image("assets/point_entry_form_interface.png", caption="Point Entry Form - Actual Interface", use_container_width=True)
    except:
        st.info("📸 Please capture screenshot of Point Entry/Edit Form screen and save as 'point_entry_form_interface.png' in assets/ folder")

    st.markdown("---")

    # Transaction History Screen
    st.markdown("#### 6.3. Transaction History Screen")
    st.markdown("""
    **Functional Description:**
    - **Component:** Table displaying point transaction history
    - **Columns:** `Date`, `Machine Code`, `Points IN`, `Points OUT`, `Daily Points`, `Final Balance`, `User`, `Branch`
    - **Features:**
        - Filter by date range
        - Filter by branch (Admin only)
        - Filter by specific machine
        - "Export to CSV" button to export data
    """)
    
    try:
        st.image("assets/transaction_history_interface.png", caption="Transaction History Screen - Actual Interface", use_container_width=True)
    except:
        st.info("📸 Please capture screenshot of Transaction History screen and save as 'transaction_history_interface.png' in assets/ folder")

    st.markdown("---")

    # Login Screen
    st.markdown("#### 6.4. Login Screen")
    st.markdown("""
    **Functional Description:**
    - **Component:** Authentication login form
    - **Fields:** Username, Password, Branch selection
    - **Features:**
        - JWT authentication
        - Role-based access (Admin/User)
        - Branch-based authorization
        - Remember login session
    """)
    
    try:
        st.image("assets/login_screen_interface.png", caption="Login Screen - Actual Interface", use_container_width=True)
    except:
        st.info("📸 Login screen screenshot (login_screen_interface.png)")

    st.markdown("---")

    # Additional Management Screens
    st.markdown("#### 6.5. Additional Management Screens")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### Product Management")
        st.markdown("""
        - CRUD operations for products
        - Prize information management
        - Quantity and value configuration
        """)
        try:
            st.image("assets/product_management_interface.png", caption="Product Management", use_container_width=True)
        except:
            st.info("🛍️ Product management screenshot")
        
        st.markdown("##### Daily Audit")  
        st.markdown("""
        - Product quantity auditing
        - Record actual vs system inventory
        - Discrepancy reporting
        """)
        try:
            st.image("assets/daily_audit_interface.png", caption="Daily Audit", use_container_width=True)
        except:
            st.info("📊 Daily audit screenshot")
    
    with col2:
        st.markdown("##### Warehouse Management")
        st.markdown("""
        - Product stock management
        - Inventory in/out operations
        - Out-of-stock alerts
        """)
        try:
            st.image("assets/warehouse_management_interface.png", caption="Warehouse Management", use_container_width=True)
        except:
            st.info("📦 Warehouse management screenshot")
        
        st.markdown("##### Reports & Advance Payments")
        st.markdown("""
        - **Reports:** Revenue, branch-wise statistics
        - **Advance Payments:** Manage advance transactions
        - Export data to CSV/Excel
        """)
        try:
            st.image("assets/reports_advance_payments_interface.png", caption="Reports & Advance Payments", use_container_width=True)
        except:
            st.info("💰 Reports & advance payments screenshot")

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
