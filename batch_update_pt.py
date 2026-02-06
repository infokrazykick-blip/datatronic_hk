#!/usr/bin/env python3
import re
import os

base_dir = '/Volumes/Extreme Pro/Datatronic/06-Website/datatronic.hk'

# File configurations with product info and current index
files_to_update = [
    {'filename': 'pt_audio.html', 'title': 'Audio Transformers', 'jp_title': 'オーディオ変圧器', 'cn_title': '音频变压器', 'desc': 'Audio transformers for professional audio and music equipment', 'index': 7},
    {'filename': 'pt_distribution.html', 'title': 'Distribution Transformers', 'jp_title': '配電変圧器', 'cn_title': '配电变压器', 'desc': 'Distribution transformers for power distribution networks', 'index': 8},
    {'filename': 'pt_step_down.html', 'title': 'Step Down Transformers', 'jp_title': 'ステップダウン変圧器', 'cn_title': '降压变压器', 'desc': 'High-capacity step down transformers for industrial applications', 'index': 9},
    {'filename': 'pt_isolation.html', 'title': 'Isolation Transformers', 'jp_title': '隔離変圧器', 'cn_title': '隔离变压器', 'desc': 'Isolation transformers for electrical safety and noise reduction', 'index': 10},
    {'filename': 'pt_shielded.html', 'title': 'Shielded Transformers', 'jp_title': 'シールド変圧器', 'cn_title': '屏蔽变压器', 'desc': 'Shielded transformers for EMI/RFI protection', 'index': 11},
    {'filename': 'pt_auto.html', 'title': 'Auto Transformers', 'jp_title': '自動変圧器', 'cn_title': '自动变压器', 'desc': 'Auto transformers for voltage adjustment and control', 'index': 12},
    {'filename': 'pt_ferro.html', 'title': 'Ferro Resonant Transformers', 'jp_title': 'フェロ共振変圧器', 'cn_title': '铁谐变压器', 'desc': 'Ferro resonant transformers for constant voltage regulation', 'index': 13},
]

# CSS to replace
old_css = r'\.product-grid.*?@media \(max-width: 768px\) \{.*?\.nav-link-prev, \.nav-link-next \{ width: 100%; text-align: center; \}'
new_css = '''        .pdf-count { display: inline-block; background-color: #f0f0f0; padding: 0.25rem 0.75rem; border-radius: 20px; font-size: 0.85rem; color: #666; margin-top: 1rem; }
        .pdf-list { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; margin-top: 2rem; }
        .pdf-item { background-color: #f9f9f9; border: 1px solid #e0e0e0; border-radius: 8px; padding: 1.5rem; display: flex; flex-direction: column; justify-content: space-between; transition: all 0.3s ease; border-left: 4px solid rgb(216, 26, 41); }
        .pdf-item:hover { box-shadow: 0 4px 12px rgba(216, 26, 41, 0.15); transform: translateY(-2px); }
        .pdf-series-name { font-size: 1rem; font-weight: 600; color: #333130; margin-bottom: 0.5rem; word-break: break-word; }
        .pdf-filename { font-size: 0.85rem; color: #999; margin-bottom: 1rem; font-family: 'Courier New', monospace; word-break: break-all; }
        .pdf-download-btn { display: inline-flex; align-items: center; justify-content: center; gap: 0.5rem; padding: 0.75rem 1rem; background-color: rgb(216, 26, 41); color: white; text-decoration: none; border-radius: 4px; font-size: 0.95rem; font-weight: 500; transition: background-color 0.3s ease; }
        .pdf-download-btn:hover { background-color: #b91f30; color: white; text-decoration: none; }
        
        @media (max-width: 768px) { 
            .pdf-list { grid-template-columns: 1fr; }
            .product-title { font-size: 1.5rem; } 
            .navigation-links { flex-direction: column; gap: 1rem; } 
            .nav-link-prev, .nav-link-next { width: 100%; text-align: center; } 
        }'''

print("批量处理 pt_*.html 文件...")
print("=" * 50)

for file_info in files_to_update:
    filepath = os.path.join(base_dir, file_info['filename'])
    
    if not os.path.exists(filepath):
        print(f"✗ {file_info['filename']} - 文件不存在")
        continue
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update product title
        content = re.sub(r'<h1 class="product-title">[^<]*</h1>', 
                        f'<h1 class="product-title" id="productTitle">{file_info["title"]}</h1>', 
                        content, count=1)
        
        # Update product description
        content = re.sub(r'<p class="product-description">[^<]*</p>', 
                        f'<p class="product-description" id="productDescription">{file_info["desc"]}</p>', 
                        content, count=1)
        
        # Update PDF count
        content = re.sub(r'<span class="pdf-count">[^<]*</span>', 
                        '<span class="pdf-count" id="pdfCount">PDF Files: 0</span>', 
                        content, count=1)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✓ {file_info['filename']} - 更新完毕")
    
    except Exception as e:
        print(f"✗ {file_info['filename']} - 错误: {str(e)}")

print("=" * 50)
print("完成！")
