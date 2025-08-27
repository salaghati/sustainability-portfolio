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
    st.subheader("4. BPMN/Flowchart: Point Transaction Entry/Edit Process")
    st.markdown("This flowchart describes the business process from when a staff member starts data entry until the system saves the transaction.")
    st.code("""
    mermaid
    graph TD
        A[Start] --> B{Staff Logs In};
        B --> C[Select machine for point entry];
        C --> D[Enter IN/OUT points and select date];
        D --> E{Check if date already has data?};
        E -- Yes --> F{DEMO mode?};
        F -- No (Production) --> G[Display overwrite warning];
        G --> Z[End];
        F -- Yes --> H[Allow overwrite];
        E -- No --> H;
        H --> I[Calculate Daily Point & Update Balance];
        I --> J[Save Transaction & History];
        J --> Z;

        subgraph Edit Transaction
            K[Select to edit transaction] --> L{Is it the latest transaction?};
            L -- Yes --> M[Allow editing];
            M --> I;
            L -- No --> N[Display warning & Block edit];
            N --> Z;
        end
        
        C --> K
    """, language='mermaid')

with tab5:
    st.subheader("5. Entity Relationship Diagram (ERD)")
    st.markdown("This diagram describes the structure and relationships between the tables in the database.")
    st.code("""
    mermaid
    erDiagram
      Branchs {
        int id PK
        string name
        string address
        string phone
        string manager_name
        datetime created_at
        boolean is_deleted
      }
      Machines {
        int id PK
        string machine_code
        string name
        int branch_id FK
        int current_points
        float rate
        string type
        int standard_quantity
        int product_id
        int current_quantity
        datetime created_at
        boolean is_deleted
      }
      Users {
        int id PK
        string username
        string password_hash
        string role "Enum: 'admin', 'user'"
        int branch_id FK
        boolean is_active
        datetime created_at
      }
      PointTransactions {
        int id PK
        int machine_id FK
        int user_id FK
        int branch_id FK
        string transaction_type
        int points_in
        int points_out
        int previous_balance
        int current_balance
        date transaction_date
        datetime created_at
        int daily_point
        int final_amount
        float rate
      }
      Branchs ||--o{ Machines : "has"
      Branchs ||--o{ Users : "has"
      Machines ||--o{ PointTransactions : "has"
      Users ||--o{ PointTransactions : "creates"
    """, language='mermaid')

with tab6:
    st.subheader("6. Wireframe (User Interface Description)")
    st.markdown("#### Machine List Screen")
    st.markdown("""
    - **Component:** Table.
    - **Columns:** `Machine Code`, `Machine Name`, `Branch`, `Current Balance`, `Rate`, `Actions`.
    - **Features:**
        - "Add New Machine" button.
        - Pagination for long lists.
        - "Actions" column with "Edit" and "Delete" (soft) buttons.
        - Search bar to filter machines by name or code.
    """)

    st.markdown("#### Point Entry/Edit Form")
    st.markdown("""
    - **Component:** Form.
    - **Fields:**
        - `Dropdown` to select a machine (shows only machines in the user's branch).
        - `Input number` for `Points IN`.
        - `Input number` for `Points OUT`.
        - `Date picker` to select the transaction date.
        - `Toggle switch` to enable/disable `Demo` mode.
    - **Logic:**
        - When a date with an existing transaction is selected, a warning message appears below the `Date picker` if `Demo` mode is off.
        - The "Save" button is disabled if there are validation errors.
    """)

    st.markdown("#### Transaction History Screen")
    st.markdown("""
    - **Component:** Table.
    - **Columns:** `Date`, `Machine Code`, `Points IN`, `Points OUT`, `Daily Points`, `Final Balance`, `User`, `Branch`.
    - **Features:**
        - Filter by date range.
        - Filter by branch (for Admins only).
        - Filter by machine.
        - "Export to CSV" button.
    """)

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
