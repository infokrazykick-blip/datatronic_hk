# Power Transformer Pages 统一改造计划

## 概述
根据参考页面 `inductors_shielded_smt.html` 的标准化结构，对以下10个电力变压器页面进行统一改造：

1. `pt_three_phase.html` - Three Phase Transformers
2. `pt_step_control.html` - 50/60Hz Step/Control Transformers  
3. `pt_400hz.html` - 400Hz Transformers
4. `pt_audio.html` - Audio Transformers
5. `pt_distribution.html` - Distribution Transformers
6. `pt_step_down.html` - Step Down Transformers
7. `pt_isolation.html` - Isolation Transformers
8. `pt_shielded.html` - Shielded Transformers
9. `pt_auto.html` - Auto Transformers
10. `pt_ferro.html` - Ferro Resonant Transformers

---

## 关键改造点

### 1. CSS 样式统一

**替换内容：** 移除旧的 `.product-grid` 和 `.product-card` 相关样式，添加标准的 PDF 列表样式

**新增 CSS 类：**
```css
.pdf-list { 
    display: grid; 
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); 
    gap: 1.5rem; 
    margin-top: 2rem; 
}

.pdf-item { 
    background-color: #f9f9f9; 
    border: 1px solid #e0e0e0; 
    border-radius: 8px; 
    padding: 1.5rem; 
    display: flex; 
    flex-direction: column; 
    justify-content: space-between; 
    transition: all 0.3s ease; 
    border-left: 4px solid rgb(216, 26, 41); 
}

.pdf-item:hover { 
    box-shadow: 0 4px 12px rgba(216, 26, 41, 0.15); 
    transform: translateY(-2px); 
}

.pdf-series-name { 
    font-size: 1rem; 
    font-weight: 600; 
    color: #333130; 
    margin-bottom: 0.5rem; 
    word-break: break-word; 
}

.pdf-filename { 
    font-size: 0.85rem; 
    color: #999; 
    margin-bottom: 1rem; 
    font-family: 'Courier New', monospace; 
    word-break: break-all; 
}

.pdf-download-btn { 
    display: inline-flex; 
    align-items: center; 
    justify-content: center; 
    gap: 0.5rem; 
    padding: 0.75rem 1rem; 
    background-color: rgb(216, 26, 41); 
    color: white; 
    text-decoration: none; 
    border-radius: 4px; 
    font-size: 0.95rem; 
    font-weight: 500; 
    transition: background-color 0.3s ease; 
}

.pdf-download-btn:hover { 
    background-color: #b91f30; 
    color: white; 
    text-decoration: none; 
}
```

**需要删除的样式：**
- `.product-grid` - 旧的二列网格布局
- `.product-card` - 旧的卡片样式
- `.product-icon` - 旧的图标容器
- `.product-card-title` - 旧的卡片标题
- `.product-card-subtitle` - 旧的卡片副标题

**响应式设计更新：**
```css
@media (max-width: 768px) { 
    .pdf-list { grid-template-columns: 1fr; } 
    /* 保留原有的其他响应式规则 */
}
```

---

### 2. HTML 结构改造

#### 当前结构（需要替换的部分）：
```html
<div style="margin-bottom: 2rem; padding: 1.5rem; background-color: #f9f9f9; border-radius: 8px;">
    <h3 style="font-size: 1.3rem; color: #333130; margin-bottom: 1.5rem;">
        <i class="fas fa-file-pdf" style="color: rgb(216, 26, 41); margin-right: 0.5rem;"></i>
        Available Documents
    </h3>
    <div class="products-grid">
        <!-- 旧的卡片结构 -->
        <div style="background-color: white; ...">
            <i class="fas fa-plug" style="font-size: 80px; ..."></i>
            <h4>...</h4>
            <p>...</p>
        </div>
    </div>
</div>
```

#### 新结构（参考 inductors_shielded_smt.html）：
```html
<div style="margin-bottom: 2rem; padding: 1.5rem; background-color: #f9f9f9; border-radius: 8px;">
    <h2 style="font-size: 1.3rem; margin-bottom: 1.5rem; color: #333130;">
        <i class="fas fa-file-pdf" style="color: rgb(216, 26, 41); margin-right: 0.5rem;"></i>
        <span data-i18n="available_documents">Available Documents</span>
    </h2>
    <div class="pdf-list" id="pdfList">
    </div>
</div>
```

**变化说明：**
- 用 `<h2>` 替代 `<h3>`
- `<div class="products-grid">` 改为 `<div class="pdf-list" id="pdfList">`
- 将"Available Documents"文本改为可国际化的 `<span data-i18n="available_documents">`
- 删除所有硬编码的卡片内容，由 JavaScript 动态渲染

---

### 3. JavaScript 改造

#### 需要添加/修改的函数：

**1. 更新 HTML 结构中的 JavaScript 块**

**替换旧的 renderNavigationLinks 函数调用，添加新的 renderPdfList 函数：**

```javascript
// 新增：PDF 列表渲染函数（如果有 PDF 数据）
function renderPdfList() { 
    const pdfList = document.getElementById('pdfList'); 
    pdfList.innerHTML = ''; 
    productData.pdfs.forEach(pdf => { 
        const pdfItem = document.createElement('div'); 
        pdfItem.className = 'pdf-item'; 
        const specsHtml = pdf.specs ? `<div style="font-size: 0.8rem; color: #666; white-space: pre-line; margin: 0.75rem 0; line-height: 1.4;">${pdf.specs}</div>` : ''; 
        pdfItem.innerHTML = `<div><div class="pdf-series-name">${pdf.series}</div><div class="pdf-filename">${pdf.filename}</div>${specsHtml}</div><a href="Active/${pdf.filename}" class="pdf-download-btn" download><i class="fas fa-download"></i> <span data-i18n="download">Download PDF</span></a>`; 
        pdfList.appendChild(pdfItem); 
    }); 
}
```

**2. 更新 DOMContentLoaded 事件监听：**

```javascript
// 旧方式（缺少 renderPdfList 调用）
document.addEventListener('DOMContentLoaded', () => { 
    updateContent(); 
    renderNavigationLinks(); 
});

// 新方式
document.addEventListener('DOMContentLoaded', () => { 
    updateContent(); 
    renderPdfList();  // 新增
    renderNavigationLinks(); 
});
```

**3. 更新语言变更事件监听：**

```javascript
// 旧方式
document.addEventListener('DOMContentLoaded', () => { /* ... */ });

// 新方式：添加 i18next 语言变更事件
document.addEventListener('DOMContentLoaded', () => { 
    updateContent(); 
    renderPdfList(); 
    renderNavigationLinks(); 
});

i18next.on('languageChanged', () => { 
    updateContent(); 
    renderNavigationLinks(); 
});
```

---

### 4. 各页面特定的 productData 更新

每个页面需要更新其 `productData` 对象中的多语言名称和描述：

| 页面 | 英文名称 | 日文名称 | 中文名称 | productData 中的 en_name | jp_name | cn_name |
|------|--------|--------|--------|------------------------|---------|---------|
| pt_three_phase.html | Three Phase Transformers | 三相トランス | 三相变压器 | ✓ 已有 | ✓ 已有 | ✓ 已有 |
| pt_step_control.html | 50/60Hz Step/Control Transformers | 50/60Hz ステップ/制御トランス | 50/60Hz 调压/控制变压器 | 需更新 | 需更新 | 需更新 |
| pt_400hz.html | 400Hz Transformers | 400Hz トランス | 400Hz 变压器 | 需更新 | 需更新 | 需更新 |
| pt_audio.html | Audio Transformers | オーディオトランス | 音频变压器 | 需更新 | 需更新 | 需更新 |
| pt_distribution.html | Distribution Transformers | 配電トランス | 配电变压器 | 需更新 | 需更新 | 需更新 |
| pt_step_down.html | Step Down Transformers | ステップダウン変圧器 | 降压变压器 | 需更新 | 需更新 | 需更新 |
| pt_isolation.html | Isolation Transformers | 絶縁トランス | 隔离变压器 | 需更新 | 需更新 | 需更新 |
| pt_shielded.html | Shielded Transformers | シールド付き変圧器 | 屏蔽变压器 | 需更新 | 需更新 | 需更新 |
| pt_auto.html | Auto Transformers | 自動変圧器 | 自耦变压器 | 需更新 | 需更新 | 需更新 |
| pt_ferro.html | Ferro Resonant Transformers | フェロ共振トランス | 铁共振变压器 | 需更新 | 需更新 | 需更新 |

**注：** 大部分页面当前的 `pdfs: []` 为空数组，这是正确的。如果需要添加 PDF 数据，格式应为：
```javascript
pdfs: [
    { 
        series: 'Series Name', 
        filename: 'filename.pdf', 
        specs: 'Optional specifications text' 
    },
    // ...
]
```

---

### 5. allProducts 数组规范化

**当前问题：** 某些页面的 `allProducts` 数组不完整或排序不同

**标准格式：** 所有 pt_*.html 页面应使用以下完整的 allProducts 数组：

```javascript
const allProducts = [ 
    { id: 'power_inductors', name_en: 'Power Inductors', name_jp: 'パワーインダクタ', name_cn: '电源电感器' }, 
    { id: 'comm_magnetic', name_en: 'Communication Magnetic Components', name_jp: '通信用磁気部品', name_cn: '通信磁性元件' }, 
    { id: 'switching_power', name_en: 'Switching Power Magnetic Components', name_jp: 'スイッチング電源磁気部品', name_cn: '开关电源磁性元件' }, 
    { id: 'transformers_choke', name_en: 'Transformers and Choke Coils', name_jp: 'トランス及びチョークコイル', name_cn: '变压器和扼流圈' }, 
    { id: 'power_transformers', name_en: 'Power Transformers', name_jp: 'パワー変圧器', name_cn: '电力变压器' }, 
    { id: 'current_sense', name_en: 'Current Sense Transformers', name_jp: 'カレントセンス変圧器', name_cn: '电流传感变压器' }, 
    { id: 'wideband', name_en: 'Wideband Transformers', name_jp: 'ワイドバンド変圧器', name_cn: '宽带变压器' },
    { id: 'inductors_shielded_smt', name_en: 'Inductors, Shielded, SMT', name_jp: '屏蔽貼片電感', name_cn: '屏蔽贴片电感' },
    { id: 'inductors_shielded_thru_hole', name_en: 'Inductors, Shielded, Thru Hole', name_jp: '屏蔽插件電感', name_cn: '屏蔽插件电感' },
    { id: 'inductors_unshielded_smt', name_en: 'Inductors, Unshielded, SMT', name_jp: '非屏蔽貼片電感', name_cn: '非屏蔽贴片电感' },
    { id: 'inductors_unshielded_thru_hole', name_en: 'Inductors, Unshielded, Thru-hole', name_jp: '非屏蔽插件電感', name_cn: '非屏蔽插件电感' },
    { id: 'transformers_telecom_smt', name_en: 'Transformers, Telecom, SMT', name_jp: '通信用貼片變壓器', name_cn: '通信贴片变压器' },
    { id: 'transformers_telecom_thru_hole', name_en: 'Transformers, Telecom, Thru Hole', name_jp: '通信用插件變壓器', name_cn: '通信插件变压器' }
];
```

---

### 6. 特殊注意事项

#### 每个文件的 currentIndex 设置
`renderNavigationLinks()` 函数中的 `currentIndex` 需要根据该页面在 allProducts 数组中的位置设置：

| 页面文件 | 页面名称 | currentIndex 值 | 说明 |
|---------|---------|---------------|------|
| pt_three_phase.html | power_transformers | 4 | 在 allProducts 中的索引位置 |
| pt_step_control.html | 应在 power_transformers 周围 | 需确定 | - |
| pt_400hz.html | 应在 power_transformers 周围 | 需确定 | - |
| pt_audio.html | 应在 power_transformers 周围 | 需确定 | - |
| pt_distribution.html | 应在 power_transformers 周围 | 需确定 | - |
| pt_step_down.html | 应在 power_transformers 周围 | 需确定 | - |
| pt_isolation.html | 应在 power_transformers 周围 | 需确定 | - |
| pt_shielded.html | 应在 power_transformers 周围 | 需确定 | - |
| pt_auto.html | 应在 power_transformers 周围 | 需确定 | - |
| pt_ferro.html | 应在 power_transformers 周围 | 需确定 | - |

**当前情况：** 这些 pt_*.html 页面在 allProducts 中的顺序和索引需要统一确定。建议按照产品类别分组放在 power_transformers 相邻的位置。

---

## 修改步骤总结

### 第一步：CSS 样式替换
1. 移除 `.products-grid`、`.product-card`、`.product-icon`、`.product-card-title`、`.product-card-subtitle` 样式
2. 添加 `.pdf-list`、`.pdf-item`、`.pdf-series-name`、`.pdf-filename`、`.pdf-download-btn` 样式
3. 更新媒体查询中的响应式规则

### 第二步：HTML 结构改造
1. 将 `<div class="products-grid">` 改为 `<div class="pdf-list" id="pdfList">`
2. 删除所有硬编码的卡片 `<div>` 元素
3. 保留 PDF 列表头部（`<h2>`、图标、文本）
4. 将硬编码文本改为国际化标记 `data-i18n`

### 第三步：JavaScript 改造
1. 添加 `renderPdfList()` 函数
2. 更新 `DOMContentLoaded` 事件监听，添加 `renderPdfList()` 调用
3. 添加 `i18next.on('languageChanged', ...)` 事件监听

### 第四步：productData 和 allProducts 更新
1. 确保每个页面的 productData 有正确的多语言名称
2. 统一 allProducts 数组内容
3. 检查和更新 currentIndex 值

### 第五步：验证
1. 检查每个页面是否正确显示
2. 测试语言切换功能
3. 检查响应式设计是否正常
4. 验证导航链接是否正确

---

## 实现优先级

**高优先级（必须修改）：**
- CSS 样式改造（影响所有页面的外观）
- HTML 结构改造（PDF 列表容器）
- JavaScript renderPdfList 函数添加

**中优先级（应该修改）：**
- i18next.on('languageChanged') 事件添加
- productData 多语言翻译更新
- currentIndex 统一规范

**低优先级（建议优化）：**
- allProducts 数组顺序调整
- 页面之间的导航逻辑优化

---

## 文件修改顺序建议

1. **pt_three_phase.html** - 已有基本结构，改造相对简单
2. **pt_step_control.html** - 已有 product-grid，结构类似
3. **pt_400hz.html** - 按照相同模式继续
4. **pt_audio.html**
5. **pt_distribution.html**
6. **pt_step_down.html**
7. **pt_isolation.html**
8. **pt_shielded.html**
9. **pt_auto.html**
10. **pt_ferro.html**

---

## 验证检查清单

- [ ] 所有 pt_*.html 页面都使用 `.pdf-list` 容器
- [ ] 所有页面都有 `renderPdfList()` 函数
- [ ] 所有页面都监听 `i18next.on('languageChanged')`
- [ ] 所有页面的 productData 都有三语言翻译
- [ ] 导航链接 currentIndex 值正确
- [ ] 样式表中的颜色保持一致（#D81A29 或 rgb(216, 26, 41)）
- [ ] 响应式设计在移动设备上正常显示
- [ ] 所有页面的页脚和侧栏功能正常
