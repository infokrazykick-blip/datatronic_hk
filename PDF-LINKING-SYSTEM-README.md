# 产品详情页面系统说明

## 项目结构

```
website/
├── data/
│   └── products-pdf-map.json          # 产品与PDF映射数据库（JSON格式）
├── power_inductors.html               # 电源电感器页面
├── comm_magnetic.html                 # 通信磁性元件页面
├── switching_power.html                # 开关电源磁性元件页面
├── transformers_choke.html             # 变压器和扼流圈页面
├── power_transformers.html             # 电力变压器页面
├── current_sense.html                  # 电流传感变压器页面
├── wideband.html                       # 宽带变压器页面
├── lighting.html                       # 照明磁性元件页面
├── medical.html                        # 医疗应用线圈页面
├── product-detail-template.html       # 通用模板（参考用）
├── products.html                       # 产品主页面
├── Active/                             # PDF文件存储文件夹
│   ├── 4257_series.pdf
│   ├── 4258_series.pdf
│   ├── ct317.pdf
│   ├── dr217-1.pdf
│   └── ... (共126+个PDF文件)
└── generate_product_pages.py          # 页面生成脚本
```

## 系统说明

### 1. 数据库映射（products-pdf-map.json）

这是系统的核心数据库，定义了每个产品类别对应的PDF文件：

```json
{
  "products": [
    {
      "id": "power_inductors",
      "en_name": "Power Inductors",
      "jp_name": "パワーインダクタ",
      "cn_name": "电源电感器",
      "description_en": "...",
      "description_jp": "...",
      "description_cn": "...",
      "pdfs": [
        { "series": "4257 Series", "filename": "4257_series.pdf" },
        { "series": "4258 Series", "filename": "4258_series.pdf" },
        ...
      ]
    },
    ...
  ]
}
```

**字段说明：**
- `id`: 产品页面的唯一标识（用于URL）
- `en_name/jp_name/cn_name`: 三种语言的产品名称
- `description_*`: 三种语言的产品描述
- `pdfs`: PDF文件数组，每个包含：
  - `series`: PDF系列名称（显示给用户）
  - `filename`: 实际PDF文件名（指向Active文件夹）

### 2. 产品详情页面

每个产品都有一个独立的HTML页面，包含：

- **顶部导航**：语言切换（EN/JP/中文）
- **产品信息**：标题、描述、PDF数量
- **PDF列表**：显示该产品对应的所有PDF
- **下载链接**：链接到 `Active/` 文件夹中的PDF
- **导航按钮**：上一个/下一个产品（循环导航）

### 3. 多语言支持

所有页面都通过 i18next 支持三种语言：

- **English (EN)**：默认语言
- **日本語 (JP)**：日文
- **中文 (CN)**：简体中文

用户可以在任何页面右上角切换语言，所有内容将实时更新。

### 4. PDF链接约定

所有PDF链接都指向本地 `Active/` 文件夹：

```html
<a href="Active/4257_series.pdf" download>Download PDF</a>
```

**重要：** 确保PDF文件名在 JSON 数据库中与实际文件名完全匹配。

## 使用流程

### 第一步：在 products.html 中添加链接

当前 products.html 中的产品链接指向原始网站。需要改为指向本地页面：

```html
<!-- 原始 -->
<a href="https://datatronic.com.hk/products/power-inductors/">Power Inductors</a>

<!-- 改为 -->
<a href="power_inductors.html">Power Inductors</a>
```

### 第二步：用户访问流程

1. 用户访问 `products.html`
2. 点击某个产品（例如"Power Inductors"）
3. 跳转到 `power_inductors.html`
4. 页面显示该产品对应的所有PDF
5. 用户可以：
   - 下载PDF文件
   - 切换语言查看不同语言的页面
   - 通过上/下按钮浏览其他产品

### 第三步：修改或添加PDF映射

如需添加或修改PDF映射：

1. 编辑 `data/products-pdf-map.json`
2. 在对应产品的 `pdfs` 数组中添加或修改条目：
   ```json
   {
     "series": "4260 Series",
     "filename": "4260_series.pdf"
   }
   ```
3. 重新运行生成脚本更新页面（可选）

## 重新生成页面

如果修改了 `products-pdf-map.json`，可以重新生成所有页面：

```bash
cd /Volumes/Extreme\ Pro/Datatronic/06-Website/website
python3 generate_product_pages.py
```

**注意：** 这将覆盖所有现有的产品页面。如果进行了其他定制，请先备份。

## 页面特性

### 响应式设计
- 桌面版：网格布局，多列显示PDF
- 移动版：单列布局，自适应屏幕宽度

### 无障碍性
- 所有链接都有清晰的文本标签
- 使用语义化HTML标签
- 支持键盘导航
- 适当的颜色对比度

### 性能
- 轻量级HTML结构
- CDN加载的库文件
- 本地PDF存储，无外部依赖
- 快速的页面加载和导航

## 文件修改指南

### 修改页面样式

编辑 `<style>` 部分中的 CSS。例如改变红色主题：

```css
/* 修改前 */
background-color: rgb(216, 26, 41);

/* 修改后 */
background-color: #0066cc;
```

### 修改导航循环

编辑 JavaScript 中的 `allProducts` 数组来改变产品顺序：

```javascript
const allProducts = [
    { id: 'power_inductors', ... },
    { id: 'current_sense', ... },
    // ... 改变顺序，改变产品之间的导航关系
];
```

### 添加新的翻译

在 i18next 配置中添加新的语言键值对：

```javascript
en: { translation: { new_key: 'English text' } },
ja: { translation: { new_key: '日本語のテキスト' } },
zh: { translation: { new_key: '中文文本' } }
```

## 常见问题

### Q: PDF无法下载？
**A:** 检查：
1. PDF文件确实存在于 `Active/` 文件夹
2. `products-pdf-map.json` 中的文件名与实际文件名完全匹配
3. 文件没有被锁定或有权限问题

### Q: 某个产品页面显示为空？
**A:** 检查：
1. `products-pdf-map.json` 中该产品是否有 `pdfs` 数组
2. 对应的HTML文件是否存在
3. 浏览器控制台是否有错误信息

### Q: 如何改变产品的顺序？
**A:** 编辑 `products-pdf-map.json` 中 `products` 数组的顺序，然后重新运行 `generate_product_pages.py`。

## 下一步

1. **更新 products.html 中的链接**
   - 将所有产品链接改为指向本地页面

2. **测试所有页面**
   - 确保所有PDF链接都能正确下载
   - 测试所有三种语言的显示

3. **收集用户反馈**
   - 确保PDF文件映射正确
   - 考虑是否需要添加更多功能（搜索、过滤等）

4. **优化和完善**
   - 收集性能数据
   - 改进用户体验
   - 添加更多功能（如PDF预览、分享等）
