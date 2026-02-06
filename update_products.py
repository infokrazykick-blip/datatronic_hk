#!/usr/bin/env python3
"""
产品数据更新脚本
从 products.csv 读取数据并更新对应的 HTML 子分类页面
支持 PDF 和图片文件
"""

import csv
import os
import re
from pathlib import Path

# 项目根目录
BASE_DIR = Path(__file__).parent

# 子分类名称到 HTML 文件的映射
SUBCATEGORY_TO_HTML = {
    # Power Inductors
    "Inductors, Shielded, SMT": "inductors_shielded_smt.html",
    "Inductors, Shielded, Thru Hole": "inductors_shielded_thru_hole.html",
    "Inductors, Unshielded, SMT": "inductors_unshielded_smt.html",
    "Inductors, Unshielded, Thru Hole": "inductors_unshielded_thru_hole.html",
    
    # Communication Magnetic Components
    "Transformers, Telecom, SMT": "comm_telecom_smt.html",
    "Transformers, Telecom, Thru Hole": "comm_telecom_thru_hole.html",
    
    # Switching Power Magnetic Components
    "Transformers, Current Sense, SMT": "sp_current_sense_smt.html",
    "Transformers, Current Sense, Thru-hole": "sp_current_sense_thru_hole.html",
    "Gate Drive & Pulse XFMR, SMT": "sp_gate_drive_smt.html",
    "Gate Drive & Pulse XFMR, Thru-hole": "sp_gate_drive_thru_hole.html",
    
    # Wideband Transformers
    "Inductors, High Frequency Wirewound": "wb_hf_wirewound.html",
    "Inductors, Air Core": "wb_air_core.html",
    "Transformers, RF, Wideband": "wb_rf.html",
    
    # Power Transformers
    "Three Phase Transformers": "pt_three_phase.html",
    "50/60Hz Step/Control Transformers": "pt_step_control.html",
    "400Hz Transformers": "pt_400hz.html",
    "Audio Transformers": "pt_audio.html",
    "Distribution Transformers 12-200V": "pt_distribution.html",
    "High Power Step Down Transformers": "pt_step_down.html",
    "Isolation Transformers": "pt_isolation.html",
    "Shielded Transformers": "pt_shielded.html",
    "Auto-Transformers": "pt_auto.html",
    "Ferro Resonant/Constant Voltage": "pt_ferro.html",
    
    # Medical
    "Implantable Coils": "implantable_coils.html",
    "Medical Application Coils": "medical_application_coils.html",
    
    # Others
    "MagLev Coils": "maglev_coils.html",
    "Solenoid Coils": "solenoid_coils.html",
    "Fluid Sensors": "fluid.html",
    "Speed Sensors": "speed_sensor.html",
    "Position Sensors": "position_sensor.html",
    "Telemetry Coils": "telemetry_coils.html",
    "Perfect Layer Coils": "perfect_layer_coils.html",
    "Pickup Coils": "pickup_coils.html",
    "Custom Lighting Ballast Transformers": "lighting_custom.html",
    "Flap Ballast Transformers": "lighting_flap.html",
}


def parse_products_csv(csv_path):
    """
    解析 products.csv 文件
    返回: {子分类名称: {"description": 描述, "products": [{"series": 系列名, "specs": 规格}]}}
    """
    data = {}
    current_category = None
    current_subcategory = None
    current_description = None
    
    with open(csv_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式解析CSV格式
    lines = content.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        if not line or line == ',':
            i += 1
            continue
        
        # 解析CSV行
        row = []
        if '"' in line:
            # 处理带引号的多行内容
            parts = []
            in_quotes = False
            current_field = ""
            
            while i < len(lines):
                for char in lines[i]:
                    if char == '"':
                        in_quotes = not in_quotes
                    elif char == ',' and not in_quotes:
                        parts.append(current_field.strip())
                        current_field = ""
                    else:
                        current_field += char
                
                if not in_quotes:
                    parts.append(current_field.strip())
                    row = parts
                    break
                else:
                    current_field += '\n'
                    i += 1
        else:
            row = [field.strip() for field in line.split(',')]
        
        # 分析行类型
        if len(row) >= 1:
            col1 = row[0].strip('"').strip() if row[0] else ""
            col2 = row[1].strip('"').strip() if len(row) > 1 and row[1] else ""
            
            # 检查是否是子分类标题
            if col1 and not col2:
                # 可能是大类、子分类或描述
                clean_name = col1.strip(',').strip()
                
                # 检查是否匹配已知的子分类
                for subcategory_name in SUBCATEGORY_TO_HTML.keys():
                    if clean_name == subcategory_name or clean_name.lower() == subcategory_name.lower():
                        current_subcategory = subcategory_name
                        if current_subcategory not in data:
                            data[current_subcategory] = {"description": "", "products": []}
                        break
                else:
                    # 可能是大类或描述
                    if current_subcategory and not data[current_subcategory]["description"]:
                        # 这可能是描述
                        data[current_subcategory]["description"] = clean_name
                    else:
                        current_category = clean_name
                        current_subcategory = None
            
            elif col1 and col2:
                # 这是产品系列行 (Series, Specs)
                if current_subcategory:
                    data[current_subcategory]["products"].append({
                        "series": col1,
                        "specs": col2
                    })
        
        i += 1
    
    return data


def generate_pdfs_array(products):
    """
    生成 JavaScript pdfs 数组字符串
    """
    if not products:
        return "[]"
    
    items = []
    for p in products:
        series = p['series'].replace("'", "\\'").replace('\n', '\\n')
        specs = p['specs'].replace("'", "\\'").replace('\n', '\\n') if p.get('specs') else ''
        
        # 根据系列名生成文件名（小写，空格替换为下划线或连字符）
        # 注意：实际文件名可能需要手动映射
        filename_base = p['series'].lower().replace(' ', '-').replace('/', '-')
        
        items.append(f"{{ series: '{series}', specs: '{specs}' }}")
    
    return "[\n            " + ",\n            ".join(items) + "\n        ]"


def update_html_file(html_path, subcategory_data, dry_run=True):
    """
    更新 HTML 文件中的 productData.pdfs 数组
    """
    if not os.path.exists(html_path):
        return None, f"文件不存在: {html_path}"
    
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否包含 productData
    if 'productData' not in content:
        return None, f"未找到 productData: {html_path}"
    
    products = subcategory_data.get('products', [])
    
    if dry_run:
        return len(products), f"将更新 {len(products)} 个产品"
    
    # 实际更新逻辑会更复杂，需要保留现有的文件名映射
    return len(products), "已更新"


def analyze_csv(csv_path):
    """
    分析 CSV 文件并生成报告
    """
    data = parse_products_csv(csv_path)
    
    print("=" * 70)
    print("📊 CSV 数据分析报告")
    print("=" * 70)
    
    total_products = 0
    matched_subcategories = []
    unmatched_subcategories = []
    
    for subcategory, info in data.items():
        product_count = len(info.get('products', []))
        total_products += product_count
        
        if subcategory in SUBCATEGORY_TO_HTML:
            html_file = SUBCATEGORY_TO_HTML[subcategory]
            html_path = BASE_DIR / html_file
            exists = "✅" if html_path.exists() else "❌"
            matched_subcategories.append((subcategory, html_file, product_count, exists))
        else:
            unmatched_subcategories.append((subcategory, product_count))
    
    print(f"\n📁 已匹配的子分类 ({len(matched_subcategories)}):")
    print("-" * 70)
    for subcategory, html_file, count, exists in matched_subcategories:
        print(f"  {exists} {subcategory}")
        print(f"      ➜ {html_file} ({count} 个产品)")
    
    if unmatched_subcategories:
        print(f"\n⚠️  未匹配的子分类 ({len(unmatched_subcategories)}):")
        print("-" * 70)
        for subcategory, count in unmatched_subcategories:
            print(f"  ❓ {subcategory} ({count} 个产品)")
    
    print(f"\n📈 统计:")
    print(f"  - 总子分类数: {len(data)}")
    print(f"  - 已匹配: {len(matched_subcategories)}")
    print(f"  - 未匹配: {len(unmatched_subcategories)}")
    print(f"  - 总产品数: {total_products}")
    print("=" * 70)
    
    return data


def show_products_detail(data):
    """
    显示每个子分类的产品详情
    """
    print("\n" + "=" * 70)
    print("📋 产品详情")
    print("=" * 70)
    
    for subcategory, info in data.items():
        products = info.get('products', [])
        if not products:
            continue
            
        print(f"\n📂 {subcategory} ({len(products)} 个产品)")
        print("-" * 50)
        
        for i, p in enumerate(products[:5], 1):  # 只显示前5个
            print(f"  {i}. {p['series']}")
        
        if len(products) > 5:
            print(f"  ... 还有 {len(products) - 5} 个产品")


def main():
    """主函数"""
    csv_path = BASE_DIR / "data" / "products.csv"
    
    print("\n🔧 Datatronic 产品数据更新工具")
    print("=" * 70)
    print(f"📂 CSV 文件: {csv_path}")
    print(f"📁 工作目录: {BASE_DIR}")
    
    # 分析 CSV
    data = analyze_csv(csv_path)
    
    # 显示产品详情
    show_products_detail(data)
    
    print("\n" + "=" * 70)
    print("✅ 分析完成！")
    print("\n💡 下一步操作:")
    print("  1. 检查上述匹配是否正确")
    print("  2. 如需更新，请运行: python update_products.py --update")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--update":
        print("🔄 开始更新模式...")
        # TODO: 实现实际更新逻辑
    else:
        main()
