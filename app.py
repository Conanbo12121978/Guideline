import streamlit as st
import json
import os

# โหลดข้อมูล guideline
@st.cache_data
def load_data():
    with open('index.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

# UI
st.set_page_config(page_title="Guideline PDF Search", layout="wide")
st.title("🔍 ค้นหาแนวทางการรักษา (Clinical Guidelines)")

# Sidebar Filters
st.sidebar.header("📂 ตัวกรอง")
categories = sorted(set(d['category'] for d in data))
selected_category = st.sidebar.selectbox("เลือกหมวดหมู่", ["ทั้งหมด"] + categories)

years = sorted(set(d['year'] for d in data), reverse=True)
selected_year = st.sidebar.selectbox("เลือกปี", ["ทั้งหมด"] + [str(y) for y in years])

# Search bar
search_query = st.text_input("🔎 ค้นหาด้วยคำสำคัญ", "")

# Filter logic
def filter_data(entry):
    if selected_category != "ทั้งหมด" and entry['category'] != selected_category:
        return False
    if selected_year != "ทั้งหมด" and str(entry['year']) != selected_year:
        return False
    if search_query:
        search_text = search_query.lower()
        if (search_text in entry['title'].lower() or
            any(search_text in kw.lower() for kw in entry['keywords'])):
            return True
        else:
            return False
    return True

filtered = list(filter(filter_data, data))

# Show results
if not filtered:
    st.warning("ไม่พบข้อมูลที่ตรงกับการค้นหา")
else:
    for item in filtered:
        with st.container():
            st.subheader(item['title'])
            st.markdown(f"📁 **หมวดหมู่**: {item['category']} | 📅 **ปี**: {item['year']}")
            st.markdown(f"🔖 **คำค้น**: {', '.join(item['keywords'])}")
            pdf_path = item['file']
            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    btn = st.download_button(
                        label="📥 ดาวน์โหลด PDF",
                        data=f,
                        file_name=os.path.basename(pdf_path),
                        mime="application/pdf"
                    )
            else:
                st.error("❌ ไม่พบไฟล์ PDF")
            st.markdown("---")
