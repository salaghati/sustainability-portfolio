import streamlit as st
import pandas as pd

st.set_page_config(page_title="Game Manager System v2 Portfolio", layout="wide")

st.title("Project Portfolio: Game Manager System v2")
st.markdown("---")

st.header("A. Mô tả dự án và bối cảnh")
st.markdown("""
Hệ thống **Game Manager v2** là một ứng dụng quản lý máy game được thiết kế để hoạt động trên nhiều chi nhánh.
- **Công nghệ:**
    - **Back-end:** Node.js / Express.js
    - **Cơ sở dữ liệu:** SQLite / Sequelize ORM
    - **Front-end:** React.js / Bootstrap
- **Chức năng chính:**
    - Quản lý thông tin máy (tên, mã máy, chi nhánh, loại máy).
    - Nhập và chỉnh sửa giao dịch điểm hàng ngày.
    - Xem lịch sử giao dịch và thống kê.
- **Các tính năng nổi bật:**
    - **Xóa mềm (Soft Delete):** Dữ liệu không bị xóa vĩnh viễn, dễ dàng khôi phục.
    - **Tính toán số dư tự động:** Số dư (balance) được tính toán dựa trên giao dịch mới nhất, đảm bảo tính chính xác.
    - **Quản lý tỷ lệ (Rate Management):** Cho phép thiết lập và thay đổi tỷ lệ quy đổi điểm.
    - **Chế độ Demo:** Cho phép ghi đè dữ liệu để thử nghiệm mà không ảnh hưởng đến dữ liệu thật (Production).
    - **Kiểm soát nhập liệu:** Cảnh báo và chặn ghi đè dữ liệu khi nhập trùng ngày (ở môi trường Production), chỉ cho phép sửa giao dịch gần nhất.
    - **Lịch sử thay đổi:** Lưu lại lịch sử thay đổi dữ liệu theo từng chi nhánh.
    - **Bảo mật:** Sử dụng JWT (JSON Web Token) để xác thực và phân quyền theo vai trò (Admin/User) và theo chi nhánh.
- **API Endpoints:** Cung cấp các API chính cho việc đăng nhập, CRUD cho máy, chi nhánh, giao dịch điểm và xem lịch sử.
""")

st.header("B. Vai trò của Business Analyst (BA)")
st.markdown("""
Trong dự án này, tôi đóng vai trò là Business Analyst, chịu trách nhiệm cho các công việc sau:
- **Thu thập và phân tích yêu cầu:** Làm việc với các bên liên quan để xác định vấn đề cốt lõi như dữ liệu bị ghi đè, khó khăn trong việc theo dõi số dư, và nhu cầu cần một lịch sử giao dịch rõ ràng, minh bạch.
- **Xác định các bên liên quan (Stakeholders):**
    - **Admin:** Quản lý toàn bộ hệ thống.
    - **Nhân viên chi nhánh (Staff):** Người dùng cuối, trực tiếp nhập liệu hàng ngày.
    - **Kế toán (Accountant):** Theo dõi và kiểm tra số liệu.
- **Đề xuất giải pháp:** Dựa trên các vấn đề đã phân tích, tôi đã đề xuất các giải pháp kỹ thuật và quy trình nghiệp vụ như cơ chế chống ghi đè, chế độ demo, và luồng sửa đổi dữ liệu.
- **Tài liệu hóa:** Xây dựng bộ tài liệu nghiệp vụ hoàn chỉnh để đội phát triển và các bên liên quan có cùng một cách hiểu về hệ thống.
""")

st.markdown("---")
st.header("C. Bộ tài liệu dự án")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "BRD/SRS", "User Stories & AC", "Use Case Diagram",
    "BPMN/Flowchart", "ERD", "Wireframes & KPIs"
])

with tab1:
    st.subheader("1. Business Requirements Document (BRD) / Software Requirements Specification (SRS)")
    st.markdown("#### 1.1. Mục tiêu dự án")
    st.markdown("""
    - **Giảm sai lệch dữ liệu:** Giảm thiểu sai sót về điểm số do việc nhập trùng hoặc ghi đè dữ liệu không kiểm soát.
    - **Quản lý số dư chính xác:** Đảm bảo số dư (balance) của từng máy được tính toán và cập nhật một cách chính xác theo thời gian thực.
    - **Truy vết lịch sử:** Cung cấp khả năng truy vết lịch sử giao dịch và các thay đổi dữ liệu một cách rõ ràng, minh bạch.
    """)
    st.markdown("#### 1.2. Phạm vi dự án")
    st.markdown("""
    - **Trong phạm vi (In-scope):**
        - Quản lý máy và chi nhánh (Thêm, sửa, xóa mềm).
        - Nhập và chỉnh sửa giao dịch điểm.
        - Phân quyền người dùng theo vai trò và chi nhánh.
        - Tính năng xóa mềm cho các thực thể chính.
        - Chế độ Demo/Production để kiểm soát ghi đè dữ liệu.
    - **Ngoài phạm vi (Out-of-scope):**
        - Tích hợp với các hệ thống kế toán bên ngoài.
        - Báo cáo tài chính chi tiết.
        - Quản lý kho vật tư đi kèm máy.
    """)
    st.markdown("#### 1.3. Các giả định")
    st.markdown("""
    - Mỗi máy chỉ thuộc về duy nhất một chi nhánh tại một thời điểm.
    - Người dùng chỉ được phép chỉnh sửa giao dịch điểm mới nhất của một máy.
    - Dữ liệu quan trọng (máy, chi nhánh, giao dịch) không bị xóa vĩnh viễn khỏi hệ thống (áp dụng xóa mềm).
    - Hệ thống có kết nối mạng ổn định để đồng bộ dữ liệu giữa client và server.
    """)
    st.markdown("#### 1.4. Yêu cầu chức năng (Functional Requirements)")
    st.markdown("""
    - **FR1: Xác thực và phân quyền:**
        - Hệ thống phải cho phép người dùng đăng nhập bằng username và password.
        - Hệ thống phải phân quyền dựa trên vai trò (Admin, User) và chi nhánh. Admin có toàn quyền, User chỉ thao tác được trên chi nhánh của mình.
    - **FR2: Quản lý chi nhánh (Admin):**
        - Admin có thể thêm, xem, sửa, và xóa mềm chi nhánh.
    - **FR3: Quản lý máy (Admin):**
        - Admin có thể thêm, xem, sửa, xóa mềm máy và gán máy vào một chi nhánh.
    - **FR4: Quản lý giao dịch điểm (User):**
        - User có thể nhập điểm (points_in, points_out) cho một máy tại chi nhánh của mình theo ngày.
        - Hệ thống phải tự động tính toán số dư (`current_balance`) và điểm trong ngày (`daily_point`).
    - **FR5: Kiểm soát ghi đè:**
        - Ở chế độ Production, hệ thống phải chặn người dùng nhập giao dịch cho một ngày đã có dữ liệu và hiển thị cảnh báo.
        - Ở chế độ Demo, hệ thống cho phép ghi đè.
    - **FR6: Chỉnh sửa giao dịch:**
        - User chỉ được phép chỉnh sửa giao dịch gần nhất của một máy.
    - **FR7: Xem lịch sử:**
        - Cả Admin và User đều có thể xem lịch sử giao dịch của các máy (User chỉ xem được máy trong chi nhánh của mình).
    """)
    st.markdown("#### 1.5. Yêu cầu phi chức năng (Non-Functional Requirements)")
    st.markdown("""
    - **NFR1: Bảo mật:**
        - Mật khẩu người dùng phải được băm (hashed) trước khi lưu vào CSDL.
        - Mọi request đến API phải được xác thực bằng JWT.
    - **NFR2: Hiệu năng:**
        - Thời gian phản hồi của API cho các thao tác CRUD cơ bản phải dưới 500ms.
        - Giao diện người dùng phải tải xong trong vòng 3 giây.
    - **NFR3: Khả năng phục hồi:**
        - Tính năng xóa mềm phải cho phép khôi phục lại dữ liệu đã xóa một cách dễ dàng.
    - **NFR4: Tính khả dụng:**
        - Hệ thống phải hoạt động 99% thời gian (trừ thời gian bảo trì theo kế hoạch).
    """)

with tab2:
    st.subheader("2. User Stories & Acceptance Criteria (AC)")

    st.info("Role: Nhân viên chi nhánh (Staff)")
    st.markdown("""
    > **As a**- Nhân viên chi nhánh,
    > **I want to**- nhập điểm cuối ngày cho các máy thuộc chi nhánh của tôi,
    - **So that**- tôi có thể lưu lại kết quả kinh doanh và hệ thống tự động tính toán số dư.
    """)
    st.text("""
    AC 1: Given môi trường hệ thống là "Production",
    When tôi nhập điểm cho một máy vào một ngày đã có dữ liệu,
    Then hệ thống phải hiển thị cảnh báo "Dữ liệu cho ngày này đã tồn tại" và không cho phép lưu.

    AC 2: Given môi trường hệ thống là "Demo",
    When tôi nhập điểm cho một máy vào một ngày đã có dữ liệu,
    Then hệ thống phải cho phép ghi đè dữ liệu cũ và lưu lại giao dịch mới.

    AC 3: Given tôi đang chỉnh sửa một giao dịch,
    When giao dịch đó không phải là giao dịch mới nhất của máy,
    Then hệ thống phải vô hiệu hóa nút "Lưu" và hiển thị thông báo "Chỉ được phép sửa giao dịch mới nhất".
    """)

    st.info("Role: Quản trị viên (Admin)")
    st.markdown("""
    > **As an**- Admin,
    > **I want to**- xem lịch sử giao dịch điểm của tất cả các máy trên toàn hệ thống,
    - **So that**- tôi có thể kiểm tra, đối chiếu và giám sát hoạt động của tất cả các chi nhánh.
    """)
    st.text("""
    AC 1: Given tôi đã đăng nhập với vai trò Admin,
    When tôi truy cập trang Lịch sử,
    Then hệ thống phải hiển thị một bảng dữ liệu chứa tất cả giao dịch từ mọi chi nhánh.

    AC 2: Given tôi đang xem trang Lịch sử,
    When tôi sử dụng bộ lọc theo chi nhánh hoặc theo máy,
    Then bảng dữ liệu phải được cập nhật tương ứng với lựa chọn của tôi.
    """)

    st.info("Role: Kế toán (Accountant)")
    st.markdown("""
    > **As an**- Accountant,
    > **I want to**- xem báo cáo số dư cuối ngày của tất cả các máy,
    - **So that**- tôi có thể thực hiện công việc đối soát tài chính.
    """)
    st.text("""
    AC 1: Given tôi đã đăng nhập với vai trò Kế toán,
    When tôi truy cập trang Báo cáo,
    Then hệ thống phải hiển thị số dư (`current_balance`) gần nhất của tất cả các máy đang hoạt động.
    """)

with tab3:
    st.subheader("3. Use Case Diagram")
    st.markdown("Sơ đồ mô tả các hành động chính mà các tác nhân (actors) có thể thực hiện trên hệ thống.")
    st.code("""
    mermaid
    graph TD
        subgraph "Game Manager System v2"
            UC1(Đăng nhập)
            UC2(Quản lý Chi nhánh)
            UC3(Quản lý Máy)
            UC4(Nhập Giao dịch Điểm)
            UC5(Sửa Giao dịch Điểm)
            UC6(Xem Lịch sử)
        end

        Admin --o UC1
        Admin --o UC2
        Admin --o UC3
        Admin --o UC6

        Staff[Nhân viên Chi nhánh] --o UC1
        Staff --o UC4
        Staff --o UC5
        Staff --o UC6

        System --|> UC1 : include
        System --|> UC4 : include
        System --|> UC5 : include

        UC2 --|> Admin
        UC3 --|> Admin
        UC4 --|> Staff
        UC5 --|> Staff
    """, language='mermaid')

with tab4:
    st.subheader("4. BPMN/Flowchart: Quy trình Nhập/Sửa Giao dịch Điểm")
    st.markdown("Lưu đồ mô tả quy trình nghiệp vụ từ lúc nhân viên bắt đầu nhập liệu cho đến khi hệ thống lưu lại giao dịch.")
    st.code("""
    mermaid
    graph TD
        A[Bắt đầu] --> B{Nhân viên Đăng nhập};
        B --> C[Chọn máy cần nhập điểm];
        C --> D[Nhập điểm IN/OUT và chọn ngày];
        D --> E{Kiểm tra ngày đã có dữ liệu?};
        E -- Có --> F{Chế độ DEMO?};
        F -- Không (Production) --> G[Hiển thị cảnh báo ghi đè];
        G --> Z[Kết thúc];
        F -- Có --> H[Cho phép ghi đè];
        E -- Không --> H;
        H --> I[Tính Daily Point & Cập nhật Balance];
        I --> J[Lưu Transaction & History];
        J --> Z;

        subgraph Sửa Transaction
            K[Chọn sửa transaction] --> L{Transaction mới nhất?};
            L -- Có --> M[Cho phép sửa];
            M --> I;
            L -- Không --> N[Hiển thị cảnh báo & Chặn sửa];
            N --> Z;
        end
        
        C --> K
    """, language='mermaid')

with tab5:
    st.subheader("5. Entity Relationship Diagram (ERD)")
    st.markdown("Sơ đồ mô tả cấu trúc và mối quan hệ giữa các bảng trong cơ sở dữ liệu.")
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
    st.subheader("6. Wireframe (Mô tả giao diện người dùng)")
    st.markdown("#### Màn hình Danh sách máy")
    st.markdown("""
    - **Component:** Bảng (Table).
    - **Các cột:** `Mã máy`, `Tên máy`, `Chi nhánh`, `Số dư hiện tại`, `Tỷ lệ`, `Hành động`.
    - **Tính năng:**
        - Nút "Thêm máy mới".
        - Phân trang nếu danh sách dài.
        - Cột "Hành động" có các nút "Sửa" và "Xóa" (mềm).
        - Thanh tìm kiếm để lọc máy theo tên hoặc mã.
    """)

    st.markdown("#### Form Nhập/Sửa điểm")
    st.markdown("""
    - **Component:** Formulaire.
    - **Các trường:**
        - `Dropdown` để chọn máy (chỉ hiển thị máy trong chi nhánh của user).
        - `Input number` cho `Điểm IN`.
        - `Input number` cho `Điểm OUT`.
        - `Date picker` để chọn ngày giao dịch.
        - `Toggle switch` để bật/tắt chế độ `Demo`.
    - **Logic:**
        - Khi chọn một ngày đã có giao dịch, một thông báo cảnh báo sẽ hiện ra bên dưới `Date picker` nếu chế độ `Demo` đang tắt.
        - Nút "Lưu" sẽ bị vô hiệu hóa nếu có lỗi validation.
    """)

    st.markdown("#### Màn hình Lịch sử Giao dịch")
    st.markdown("""
    - **Component:** Bảng (Table).
    - **Các cột:** `Ngày`, `Mã máy`, `Điểm IN`, `Điểm OUT`, `Điểm trong ngày`, `Số dư cuối`, `Người nhập`, `Chi nhánh`.
    - **Tính năng:**
        - Bộ lọc theo khoảng thời gian.
        - Bộ lọc theo chi nhánh (chỉ dành cho Admin).
        - Bộ lọc theo máy.
        - Nút "Export to CSV".
    """)

    st.subheader("7. KPIs và Báo cáo")
    st.markdown("Các chỉ số dùng để đo lường hiệu quả của hệ thống sau khi triển khai:")
    
    kpi_data = {
        'KPI': [
            "Số lượng giao dịch bị chặn ghi đè",
            "Tỷ lệ sai lệch số dư",
            "Thời gian nhập liệu trung bình",
            "Số lượng máy hoạt động theo chi nhánh",
            "Tỷ lệ chỉnh sửa giao dịch"
        ],
        'Mô tả': [
            "Đo lường hiệu quả của tính năng chống ghi đè ở môi trường Production.",
            "So sánh số dư trên hệ thống và số dư thực tế, kỳ vọng giảm theo thời gian.",
            "Thời gian trung bình một nhân viên cần để hoàn thành việc nhập điểm cho một máy.",
            "Thống kê số máy có giao dịch phát sinh trong tháng, theo từng chi nhánh.",
            "Số lần một giao dịch bị chỉnh sửa. Tỷ lệ cao có thể chỉ ra quy trình nhập liệu có vấn đề."
        ],
        'Mục tiêu': [
            "Tăng lên (chứng tỏ tính năng hiệu quả)",
            "Giảm > 90%",
            "Giảm 50% (so với làm thủ công)",
            "N/A",
            "Giảm thiểu"
        ]
    }
    kpi_df = pd.DataFrame(kpi_data)
    st.table(kpi_df)

st.markdown("---")
st.header("D. Bài học rút ra")
st.success("""
- **Tầm quan trọng của việc xác định đúng "pain point":** Việc tập trung giải quyết vấn đề cốt lõi (ghi đè dữ liệu) đã mang lại giá trị lớn nhất cho người dùng cuối.
- **Phân tách môi trường Demo và Production là cần thiết:** Giải pháp này giúp dung hòa giữa nhu cầu đào tạo, thử nghiệm của người dùng mới và yêu cầu về tính toàn vẹn dữ liệu của hệ thống.
- **Tài liệu hóa rõ ràng giúp giảm thiểu hiểu lầm:** Bộ tài liệu chi tiết (BRD, Use Case, BPMN...) đã giúp đội phát triển và các bên liên quan có chung một cách hiểu, giảm thời gian trao đổi và sửa lỗi không cần thiết.
""")
