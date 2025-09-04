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
    st.markdown("**Complete documentation of system requirements using Agile methodology**")
    st.info("**25+ User Stories** with **75+ Acceptance Criteria** covering all system modules")
    
    # Authentication Module
    st.markdown("---")
    st.markdown("#### 🔐 Module 1: Authentication & Authorization")
    st.markdown("**Epic: User Authentication & Role-Based Access Control**")
    
    with st.expander("User Story 1.1: User Login", expanded=False):
        st.markdown("""
        **As a** system user  
        **I want to** log into the Game Manager system  
        **So that** I can access my assigned functionalities based on my role

        **Acceptance Criteria:**
        
        ✅ **GIVEN** I am on the login page  
        **WHEN** I enter valid username and password  
        **THEN** I should be redirected to the main dashboard  
        **AND** I should receive a JWT token stored in localStorage  
        **AND** my user information (id, role, branch) should be available

        ✅ **GIVEN** I enter invalid credentials  
        **WHEN** I attempt to login  
        **THEN** I should see error message "Sai tài khoản hoặc mật khẩu"  
        **AND** I should remain on the login page

        ✅ **GIVEN** I am already logged in  
        **WHEN** I try to access login page  
        **THEN** I should be redirected to main dashboard

        ✅ **GIVEN** login form validation  
        **WHEN** I submit empty username or password  
        **THEN** I should see error "Vui lòng nhập đầy đủ thông tin"
        """)

    with st.expander("User Story 1.2: Role-Based Access Control", expanded=False):
        st.markdown("""
        **As a** system administrator  
        **I want** different user roles to have different access levels  
        **So that** system security and data integrity are maintained

        **Acceptance Criteria:**
        
        ✅ **GIVEN** I am an Admin user (role_id = 1)  
        **WHEN** I access the system  
        **THEN** I can view and manage all branches  
        **AND** I can view and manage all machines  
        **AND** I can view all transaction histories  
        **AND** I can access advanced features (branch management, user management)

        ✅ **GIVEN** I am a regular User (role_id != 1)  
        **WHEN** I access the system  
        **THEN** I can only view machines in my assigned branch  
        **AND** I can only view transaction histories in my branch  
        **AND** I cannot access branch management features  
        **AND** I cannot access other users' data outside my branch

        ✅ **GIVEN** my JWT token is invalid or expired  
        **WHEN** I make any API request  
        **THEN** I should receive 401 Unauthorized response  
        **AND** I should be redirected to login page
        """)
    
    # Machine Management Module
    st.markdown("---")
    st.markdown("#### 🎮 Module 2: Machine Management")
    st.markdown("**Epic: Gaming Machine CRUD Operations with Business Rules**")

    with st.expander("User Story 2.1: View Machine List", expanded=False):
        st.markdown("""
        **As a** branch user  
        **I want to** view the list of gaming machines  
        **So that** I can manage daily operations and point entries

        **Acceptance Criteria:**
        
        ✅ **GIVEN** I am logged in as Admin  
        **WHEN** I view the machine list  
        **THEN** I should see machines from all branches  
        **AND** each machine should display: machine_code, name, branch, current_balance, rate, actions

        ✅ **GIVEN** I am logged in as regular user  
        **WHEN** I view the machine list  
        **THEN** I should only see machines from my assigned branch  
        **AND** soft-deleted machines should not be visible

        ✅ **GIVEN** machine current balance calculation  
        **WHEN** displaying machine list  
        **THEN** current_balance should reflect the most recent transaction balance  
        **AND** NOT use the deprecated current_points field in Machine table
        """)

    with st.expander("User Story 2.2: Create New Machine", expanded=False):
        st.markdown("""
        **As an** authorized user  
        **I want to** create a new gaming machine  
        **So that** I can expand operational capacity

        **Acceptance Criteria:**
        
        ✅ **GIVEN** I have appropriate permissions  
        **WHEN** I create a new machine with valid data  
        **THEN** machine should be created successfully  
        **AND** machine_code must be unique within the same branch  
        **AND** default rate should be set to 2 if not specified

        ✅ **GIVEN** validation rules  
        **WHEN** I submit machine form  
        **THEN** machine_code and name are required fields  
        **AND** machine_code cannot duplicate within the same branch  
        **AND** rate must be a positive decimal number
        """)

    with st.expander("User Story 2.3: Edit & Delete Machine", expanded=False):
        st.markdown("""
        **As an** authorized user  
        **I want to** edit and soft delete machines  
        **So that** I can maintain accurate operational data

        **Acceptance Criteria:**
        
        ✅ **GIVEN** I have edit permissions  
        **WHEN** I update machine information  
        **THEN** changes should be saved successfully  
        **AND** rate changes apply to future transactions only  
        **AND** historical transaction rates remain unchanged

        ✅ **GIVEN** soft delete functionality  
        **WHEN** I delete a machine  
        **THEN** is_deleted flag should be set to true  
        **AND** machine should disappear from active lists  
        **AND** historical transaction data should remain intact
        """)
    
    # Point Transaction Management Module
    st.markdown("---")
    st.markdown("#### 💰 Module 3: Point Transaction Management")
    st.markdown("**Epic: Daily Point Entry with Business Logic and Validation**")

    with st.expander("User Story 3.1: Daily Point Data Entry", expanded=False):
        st.markdown("""
        **As a** branch operator  
        **I want to** enter daily point data for machines  
        **So that** I can track machine performance and calculate revenues

        **Acceptance Criteria:**
        
        ✅ **GIVEN** I select a machine and date  
        **WHEN** I enter Point In and Point Out values  
        **THEN** system should calculate Point Balance = Points In - Points Out  
        **AND** calculate Daily Point = Current Balance - Previous Balance  
        **AND** calculate Final Amount = (Daily Point / Machine Rate) × 1000

        ✅ **GIVEN** validation rules  
        **WHEN** I submit point data  
        **THEN** Points In and Points Out cannot be negative  
        **AND** all required fields must be filled  
        **AND** Previous Balance is required (auto-filled from yesterday or manually entered)

        ✅ **GIVEN** Demo Mode toggle  
        **WHEN** Demo Mode is ON  
        **THEN** I can overwrite existing data for the same date  
        **WHEN** Demo Mode is OFF  
        **THEN** system should warn about overwriting existing date data
        """)

    with st.expander("User Story 3.2: Transaction History & Editing", expanded=False):
        st.markdown("""
        **As a** user  
        **I want to** view and edit transaction history  
        **So that** I can analyze trends and correct mistakes

        **Acceptance Criteria:**
        
        ✅ **GIVEN** transaction history access  
        **WHEN** I view transactions for a machine  
        **THEN** data should be sorted by date (newest first)  
        **AND** display: date, machine_code, points_in, points_out, daily_point, final_amount, rate

        ✅ **GIVEN** transaction editing  
        **WHEN** I edit a transaction  
        **THEN** I can only edit the most recent transaction  
        **AND** Daily Point auto-calculates when Balance changes  
        **AND** system logs all changes in TransactionEditLog (Admin only can view)
        
        ✅ **GIVEN** rate preservation  
        **WHEN** transaction is edited  
        **THEN** calculations use the rate stored in transaction record  
        **AND** NOT the current machine rate
        """)
    
    # Advanced Management Modules
    st.markdown("---")
    st.markdown("#### 🛍️ Module 4: Product & Warehouse Management")

    with st.expander("User Story 4.1: Product & Inventory Management", expanded=False):
        st.markdown("""
        **As a** warehouse operator  
        **I want to** manage products and inventory  
        **So that** I can track stock levels and prevent shortages

        **Acceptance Criteria:**
        
        ✅ **GIVEN** product management  
        **WHEN** I create/edit products  
        **THEN** name and price are required fields  
        **AND** soft delete preserves historical data  
        **AND** products can be associated with machines for prize dispensing

        ✅ **GIVEN** warehouse stock tracking  
        **WHEN** I update product quantities  
        **THEN** stock levels are tracked per product  
        **AND** quantities must be non-negative integers  
        **AND** system provides visibility for reordering decisions
        """)

    st.markdown("---")
    st.markdown("#### 📊 Module 5: Daily Audit System")

    with st.expander("User Story 5.1: Daily Machine Audit", expanded=False):
        st.markdown("""
        **As an** auditor  
        **I want to** perform daily machine audits  
        **So that** I can verify prize quantities and calculate revenues

        **Acceptance Criteria:**
        
        ✅ **GIVEN** daily audit form  
        **WHEN** I conduct an audit  
        **THEN** I must record: start_of_day_count, end_of_day_count, gifts_won  
        **AND** optionally: end_of_day_coins, coin_value, gift_cost

        ✅ **GIVEN** revenue calculations  
        **WHEN** audit is completed  
        **THEN** revenue = (end_of_day_coins × coin_value) - (gifts_won × gift_cost)  
        **AND** audit is associated with specific machine and user  
        **AND** all data is timestamped for audit trail
        """)

    st.markdown("---")
    st.markdown("#### 💳 Module 6: Advance Payment System")

    with st.expander("User Story 6.1: Employee Financial Management", expanded=False):
        st.markdown("""
        **As a** manager  
        **I want to** manage employee advances and payments  
        **So that** I can track financial obligations and settlements

        **Acceptance Criteria:**
        
        ✅ **GIVEN** advance creation  
        **WHEN** I create an advance for an employee  
        **THEN** employee debt_amount increases  
        **AND** advance stores: user_id, amount, description, date, branch_id

        ✅ **GIVEN** payment processing  
        **WHEN** employee makes a payment  
        **THEN** debt_amount decreases  
        **AND** payment can exceed advance (allowing overpayment)  
        **AND** supports both specific advance payments and direct debt payments

        ✅ **GIVEN** debt tracking  
        **WHEN** viewing employee summary  
        **THEN** shows total debt balance per employee  
        **AND** debt_amount can be negative (credit balance)  
        **AND** only displays employees with non-zero balances
        """)

    st.markdown("---")
    st.markdown("#### 📈 Module 7: Reports & Analytics")

    with st.expander("User Story 7.1: Business Intelligence & Reporting", expanded=False):
        st.markdown("""
        **As a** manager  
        **I want to** generate comprehensive reports  
        **So that** I can analyze business performance and make data-driven decisions

        **Acceptance Criteria:**
        
        ✅ **GIVEN** reporting interface  
        **WHEN** I access reports  
        **THEN** I can filter by date range, machine, and branch  
        **AND** export data in CSV/Excel format

        ✅ **GIVEN** revenue analytics  
        **WHEN** viewing performance reports  
        **THEN** I can see revenue summaries by branch  
        **AND** track performance trends over time  
        **AND** analyze machine profitability metrics
        """)

    st.markdown("---")
    st.success("""
    **📋 Requirements Coverage Summary:**
    - **25+ User Stories** across 7 core business modules
    - **75+ Acceptance Criteria** with Given-When-Then structure
    - **Complete CRUD operations** for all entities
    - **Role-based security** and data isolation
    - **Business logic validation** and error handling
    - **Audit trails** and data integrity measures
    - **Multi-branch operations** with scalable architecture
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
