#!/usr/bin/env python3
import re
import os

# 文件配置
files_config = {
    'pt_step_control.html': {'title': '50/60Hz Step/Control Transformers', 'jp_title': '50/60Hzステップ/制御トランス', 'cn_title': '50/60Hz阶跃/控制变压器', 'index': 5},
    'pt_400hz.html': {'title': '400Hz Transformers', 'jp_title': '400Hz変圧器', 'cn_title': '400Hz变压器', 'index': 6},
    'pt_audio.html': {'title': 'Audio Transformers', 'jp_title': 'オーディオ変圧器', 'cn_title': '音频变压器', 'index': 7},
    'pt_distribution.html': {'title': 'Distribution Transformers', 'jp_title': '配電変圧器', 'cn_title': '配电变压器', 'index': 8},
    'pt_step_down.html': {'title': 'Step Down Transformers', 'jp_title': 'ステップダウン変圧器', 'cn_title': '降压变压器', 'index': 9},
    'pt_isolation.html': {'title': 'Isolation Transformers', 'jp_title': '隔離変圧器', 'cn_title': '隔离变压器', 'index': 10},
    'pt_shielded.html': {'title': 'Shielded Transformers', 'jp_title': 'シールド変圧器', 'cn_title': '屏蔽变压器', 'index': 11},
    'pt_auto.html': {'title': 'Auto Transformers', 'jp_title': '自動変圧器', 'cn_title': '自动变压器', 'index': 12},
    'pt_ferro.html': {'title': 'Ferro Resonant Transformers', 'jp_title': 'フェロ共振変圧器', 'cn_title': '铁谐变压器', 'index': 13},
}

base_dir = '/Volumes/Extreme Pro/Datatronic/06-Website/datatronic.hk'

# CSS样式替换
old_css = r'\.pdf-count \{ display: inline-block; background-color: #f0f0f0; padding: 0\.25rem 0\.75rem; border-radius: 20px; font-size: 0\.85rem; color: #666; margin-top: 1rem; \}\.product-grid \{ display: grid; grid-template-columns: 1fr 1fr; gap: 2rem; margin-top: 2rem; \}\.product-card \{ background: #f9f9f9; border: 1px solid #e0e0e0; border-radius: 8px; padding: 2rem; text-align: center; transition: all 0\.3s ease; border-top: 4px solid #D81A29; \}\.product-card:hover \{ box-shadow: 0 4px 12px rgba\(216, 26, 41, 0\.15\); transform: translateY\(-2px\); \}\s+\.product-icon \{ width: 80px; height: 80px; margin: 0 auto 1rem; background: linear-gradient\(135deg, #D81A29 0%, #B01620 100%\); border-radius: 8px; display: flex; align-items: center; justify-content: center; color: white; font-size: 2rem; \}\.product-card-title \{ font-size: 1\.2rem; font-weight: 600; color: #333130; margin-bottom: 0\.5rem; \}\.product-card-subtitle \{ font-size: 0\.9rem; color: #999; margin-bottom: 0\.5rem; \}'

new_css = '.pdf-count { display: inline-block; background-color: #f0f0f0; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; color: #666; margin-top: 1rem; }.pdf-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem; }.pdf-item { background-color: #f9f9f9; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; border-left: 4px solid rgb(216, 26, 41); }.pdf-item:hover { box-shadow: 0 4px 12px rgba(216, 26, 41, 0.15); transform: translateY(-2px); }.pdf-series-name { font-size: 1rem; font-weight: 600; color: #333130; margin-bottom: 0.5rem; word-break: break-word; }.pdf-filename { font-size: 0.85rem; color: #999; margin-bottom: 1rem; font-family: \'Courier New\', monospace; word-break: break-all; }.pdf-download-btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.75rem 1rem; background-color: rgb(216, 26, 41); color: white; text-decoration: none; border-radius: 4px; font-size: 0.95rem; font-weight: 500; transition: background-color 0.3s ease; }.pdf-download-btn:hover { background-color: #b91f30; color: white; text-decoration: none; }'

for filename, config in files_config.items():
    filepath = os.path.join(base_dir, filename)
    if not os.path.exists(filepath):
        print(f"Skipping {filename} - file not found")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 更新标题 - 找到第一个 <h1> 标签
    title_pattern = r'<h1 class="product-title">[^<]*</h1>'
    content = re.sub(title_pattern, f'<h1 class="product-title" id="productTitle">{config["title"]}</h1>', content, count=1)
    
    # 更新产品描述
    desc_pattern = r'<p class="product-description">[^<]*</p>'
    content = re.sub(desc_pattern, f'<p class="product-description" id="productDescription">Product details for {config["title"]}</p>', content, count=1)
    
    # 更新 PDF 计数
    pdf_count_pattern = r'<span class="pdf-count">[^<]*</span>'
    content = re.sub(pdf_count_pattern, '<span class="pdf-count" id="pdfCount">PDF Files: 0</span>', content, count=1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"Updated {filename}")

print("Done!")
