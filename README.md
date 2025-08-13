## Portfolio Data Analyst: Sustainability Social Media

### 1) Mục tiêu dự án
- Xây dựng portfolio thể hiện kỹ năng DA qua phân tích dữ liệu bài đăng mạng xã hội về sustainability: hành vi tương tác, hashtag, chủ đề, sentiment, nền tảng, CTA.
- Triển khai web dashboard bằng Streamlit để khám phá dữ liệu, trình bày insight và KPI.

### 2) Cài đặt môi trường
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

### 3) Chạy ứng dụng Streamlit
```bash
streamlit run app.py
```

Ứng dụng mặc định đọc file CSV tại đường dẫn tuyệt đối sau (bạn có thể đổi trong sidebar):
`/Users/macm1/Documents/Practice DA/Social Media Data/sustainability_social_media_posts.csv`

### 4) Lộ trình phân tích gợi ý
- Làm sạch và tạo chỉ số: `engagement_total`, `engagement_rate` = (likes+shares+comments)/followers.
- Phân tích theo thời gian, nền tảng, sentiment, hashtag, chủ đề (`climate_topic`), CTA, địa điểm.
- Xây dựng dashboard: Overview KPI, Trend, Platform performance, Sentiment & Topic, Hashtag.

### 5) Notebook EDA
- Notebook mẫu tại `notebooks/EDA.ipynb` (đọc file, kiểm tra schema, EDA ban đầu).

### 6) Cấu trúc tệp
```
.
├── app.py
├── README.md
├── requirements.txt
├── sustainability_social_media_posts.csv
└── notebooks/
    └── EDA.ipynb
```


