# 👨‍💼 Portfolio Data Analyst: Sustainability Social Media

> **Dự án phân tích dữ liệu mạng xã hội về sustainability với Streamlit dashboard**

Portfolio này thể hiện kỹ năng Data Analyst qua việc xây dựng dashboard tương tác để phân tích 3000+ bài đăng mạng xã hội về chủ đề sustainability. Bao gồm analysis về engagement metrics, hashtag performance, sentiment và xu hướng theo thời gian.

![Portfolio Dashboard](screenshots/dashboard_overview.png)
*Dashboard tổng quan với KPI và biểu đồ xu hướng*

![Trends Analysis](screenshots/trends_analysis.png)
*Phân tích hashtag và time heatmap*

## 🚀 Quickstart

### 1. Cài đặt dependencies

```bash
# Clone/download project
git clone <repo-url>
cd "Social Media Data"

# Tạo virtual environment (khuyến nghị)
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Cài đặt packages
pip install -r requirements.txt
```

### 2. Chạy ứng dụng

```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại `http://localhost:8501`

### 3. Sử dụng

- **Trang chính**: Xem portfolio và thông tin cá nhân
- **Overview**: KPI tổng quan và xu hướng chính  
- **Trends**: Phân tích hashtag, topic và time optimization
- **Upload dữ liệu**: Có thể upload CSV riêng hoặc dùng dataset mẫu

## 📊 Data Schema

Dataset chứa **3000+ bài đăng** về sustainability từ các nền tảng mạng xã hội chính:

### Cột chính

| Cột | Kiểu dữ liệu | Mô tả |
|-----|-------------|-------|
| `post_id` | string | ID duy nhất của bài đăng |
| `post_date` | datetime | Ngày/giờ đăng bài (YYYY-MM-DD) |
| `platform` | string | Nền tảng: Facebook, Instagram, LinkedIn, TikTok, X |
| `hashtag` | string | Hashtag chính của bài đăng |
| `post_text` | string | Nội dung bài đăng |
| `post_sentiment` | string | Cảm xúc: Positive, Neutral, Negative |
| `climate_topic` | string | Chủ đề sustainability: Waste Reduction, Energy Storage, etc. |
| `call_to_action` | string | Loại CTA trong bài đăng |

### Engagement Metrics

| Cột | Kiểu dữ liệu | Mô tả |
|-----|-------------|-------|
| `engagement_likes` | int | Số lượt thích |
| `engagement_shares` | int | Số lượt chia sẻ |
| `engagement_comments` | int | Số bình luận |
| `user_followers` | int | Số follower của user |
| `engagement_total` | int | Tổng engagement (tính toán) |
| `engagement_rate` | float | ER = total_engagement / followers |

### User Info

| Cột | Kiểu dữ liệu | Mô tả |
|-----|-------------|-------|
| `user_id` | string | ID user |
| `username` | string | Tên user |
| `user_location` | string | Vị trí địa lý |

## 🏗️ Cấu trúc Project

```
Social Media Data/
├── app.py                          # Trang chính - Portfolio & About Me
├── pages/
│   ├── 01_Overview.py             # Dashboard tổng quan 
│   └── 02_Trends.py               # Phân tích xu hướng nâng cao
├── utils.py                       # Data processing utilities
├── charts.py                      # Altair chart functions
├── requirements.txt               # Python dependencies
├── .python-version               # Python 3.11
├── .streamlit/
│   └── config.toml               # Streamlit configuration
├── sustainability_social_media_posts.csv  # Dataset
├── [CV]-[Data Analyst]-[Trinh Anh Tu].pdf # Resume
└── README.md                     # Documentation
```

## 🎯 Tính năng chính

### 📊 Analytics Features

- **KPI Dashboard**: Tổng bài đăng, engagement rate TB, tổng engagement
- **Time Series**: Xu hướng engagement theo thời gian
- **Platform Analysis**: So sánh hiệu suất các nền tảng
- **Sentiment Analysis**: Phân bố cảm xúc bài đăng
- **Hashtag Performance**: Top hashtag theo volume và ER
- **Topic Insights**: Chủ đề sustainability phổ biến
- **Time Heatmap**: Tối ưu thời gian đăng bài
- **CTA Analysis**: Hiệu quả các call-to-action

### 🔧 Technical Features

- **Multipage App**: Navigation giữa các trang phân tích
- **Interactive Filters**: Lọc theo platform, sentiment, thời gian
- **Data Upload**: Upload CSV custom hoặc dùng dataset mẫu
- **Caching**: @st.cache_data cho hiệu suất tối ưu
- **Responsive Design**: Layout wide, mobile-friendly
- **Export Data**: Download filtered CSV và summary stats

## 🚀 Deploy

### Streamlit Community Cloud

1. **Push code lên GitHub**:
   ```bash
   git add .
   git commit -m "Deploy ready"
   git push origin main
   ```

2. **Deploy trên Streamlit Cloud**:
   - Truy cập [share.streamlit.io](https://share.streamlit.io)
   - Connect GitHub account
   - Chọn repository và branch `main`
   - Main file path: `app.py`
   - Click **"Deploy"**

3. **Configuration**:
   - Python version: 3.11 (từ `.python-version`)
   - Dependencies: Tự động install từ `requirements.txt`
   - Streamlit config: Áp dụng từ `.streamlit/config.toml`

### Local Development

```bash
# Development server
streamlit run app.py

# Production-like
streamlit run app.py --server.port 8501 --server.headless true
```

## 📁 Data Requirements

Để sử dụng với dataset riêng, CSV cần có **các cột bắt buộc**:

- `post_id`, `post_date`, `platform`
- `engagement_likes`, `engagement_shares`, `engagement_comments`
- `user_followers`

**Cột optional**: `post_sentiment`, `climate_topic`, `hashtag`, `call_to_action`

Ứng dụng sẽ tự động tính toán `engagement_total` và `engagement_rate`.

## 🛠️ Tech Stack

- **Backend**: Python 3.11
- **Framework**: Streamlit 1.36.0  
- **Data Processing**: Pandas 2.2.2
- **Visualization**: Altair 5.3.0
- **Deployment**: Streamlit Community Cloud

## 👤 About

**Trịnh Anh Tú** - Data Analyst  
📧 Email: trinhanhtu01@gmail.com  
💼 LinkedIn: [linkedin.com/in/tú-trịnh](https://linkedin.com/in/tú-trịnh)  
💻 GitHub: [github.com/salaghati](https://github.com/salaghati)

---

*Portfolio này được xây dựng để thể hiện kỹ năng phân tích dữ liệu, xây dựng dashboard và triển khai ứng dụng web với Python & Streamlit.*
# Trigger for Streamlit Cloud sync
