# 🎯 PDF 链接系统 - 快速导航

欢迎使用 Datatronic PDF 链接系统。这个索引文件将帮助你快速找到所有相关资源。

---

## 📍 入口点

### 用户访问
- **产品主页面：** [products.html](products.html)
- **产品详情页面：**
  - [电源电感器](power_inductors.html)
  - [通信磁性元件](comm_magnetic.html)
  - [开关电源磁性元件](switching_power.html)
  - [变压器和扼流圈](transformers_choke.html)
  - [电力变压器](power_transformers.html)
  - [电流传感变压器](current_sense.html)
  - [宽带变压器](wideband.html)
  - [照明磁性元件](lighting.html)
  - [医疗应用线圈](medical.html)

---

## 📚 文档指南

### 新用户 - 推荐阅读顺序

1. **[PDF-SYSTEM-FINAL-REPORT.md](PDF-SYSTEM-FINAL-REPORT.md)** ⭐ 必读
   - 系统完整介绍
   - 项目成果总结
   - 功能清单
   - 约 15 分钟阅读

2. **[PDF-LINKING-SYSTEM-README.md](PDF-LINKING-SYSTEM-README.md)** ⭐ 推荐
   - 系统架构说明
   - 使用流程
   - 常见问题解答
   - 约 10 分钟阅读

3. **[VERIFICATION-CHECKLIST.md](VERIFICATION-CHECKLIST.md)** 
   - 质量检查清单
   - 测试场景
   - 故障排除指南
   - 约 8 分钟阅读

### 维护人员

- **[IMPLEMENTATION-SUMMARY.md](IMPLEMENTATION-SUMMARY.md)**
  - 完成工作总结
  - 技术细节
  - 代码架构

---

## 🗂️ 文件结构

```
website/
├── 📄 文档文件
│   ├── PDF-SYSTEM-FINAL-REPORT.md          ⭐ 最终报告
│   ├── PDF-LINKING-SYSTEM-README.md         📖 系统说明
│   ├── IMPLEMENTATION-SUMMARY.md            📝 实施总结
│   ├── VERIFICATION-CHECKLIST.md            ✓ 验收清单
│   └── INDEX-CN.md                          📍 本文件 (中文)
│
├── 🌐 产品页面 (9 个)
│   ├── power_inductors.html                 电源电感器
│   ├── comm_magnetic.html                   通信磁性元件
│   ├── switching_power.html                 开关电源磁性元件
│   ├── transformers_choke.html              变压器和扼流圈
│   ├── power_transformers.html              电力变压器
│   ├── current_sense.html                   电流传感变压器
│   ├── wideband.html                        宽带变压器
│   ├── lighting.html                        照明磁性元件
│   └── medical.html                         医疗应用线圈
│
├── 📦 数据和工具
│   ├── data/
│   │   └── products-pdf-map.json            PDF 映射数据库
│   ├── product-detail-template.html         页面模板
│   ├── generate_product_pages.py            页面生成脚本
│   └── products.html                        产品主页面 (待更新链接)
│
└── 📁 PDF 存储
    └── Active/                              126+ 个 PDF 文件
```

---

## 🚀 快速开始

### 第一步：启动本地服务器
```bash
cd /Volumes/Extreme\ Pro/Datatronic/06-Website/website
python3 -m http.server 8000
```

### 第二步：访问页面
```
http://localhost:8000/power_inductors.html
http://localhost:8000/products.html
```

### 第三步：测试功能
- ✓ 点击产品链接
- ✓ 查看 PDF 列表
- ✓ 下载 PDF 文件
- ✓ 切换语言（EN / JP / 中文）

---

## 📋 常见任务

### 任务 1: 添加新的 PDF

**步骤：**
1. 将 PDF 文件复制到 `Active/` 文件夹
2. 编辑 `data/products-pdf-map.json`
3. 在对应产品的 `pdfs` 数组中添加条目
4. 访问产品页面查看新增 PDF

**示例：**
```json
{
  "series": "新系列名称",
  "filename": "新文件名.pdf"
}
```

### 任务 2: 更新 products.html 链接

**当前状态：** 链接指向原始网站  
**需要改为：** 指向本地产品页面

**找到这样的行：**
```html
<a href="https://datatronic.com.hk/products/power-inductors/">
```

**改为：**
```html
<a href="power_inductors.html">
```

### 任务 3: 修改产品描述

**步骤：**
1. 编辑 `data/products-pdf-map.json`
2. 修改 `description_en`、`description_jp` 或 `description_cn` 字段
3. 重新生成页面：`python3 generate_product_pages.py`

### 任务 4: 添加新的语言

**步骤：**
1. 在 `data/products-pdf-map.json` 中为新语言添加字段
2. 在页面的 i18next 配置中添加新语言
3. 在语言按钮中添加新选项
4. 重新生成所有页面

### 任务 5: 修改页面样式

**修改单个页面：** 编辑 HTML 文件的 `<style>` 部分  
**修改所有页面：** 编辑 `product-detail-template.html`，然后运行生成脚本

---

## 🔍 故障排除

### 问题 1: 打开页面时看不到内容

**检查：**
1. 是否正确启动了本地服务器？
2. URL 是否正确？ (例如：http://localhost:8000/)
3. 浏览器是否禁用了 JavaScript？

**解决方案：**
```bash
# 确保服务器运行中
python3 -m http.server 8000
```

### 问题 2: PDF 无法下载

**检查：**
1. 文件是否存在于 `Active/` 文件夹？
2. 文件名是否与 JSON 中的名称完全匹配？
3. 文件是否有读取权限？

**解决方案：**
```bash
# 查看 Active 文件夹中的文件
ls -lh Active/ | grep "filename.pdf"

# 检查文件权限
chmod 644 Active/*.pdf
```

### 问题 3: 语言显示不正确

**检查：**
1. 浏览器是否支持 JavaScript？
2. i18next 库是否正确加载？
3. 是否有浏览器缓存问题？

**解决方案：**
```javascript
// 在浏览器控制台检查
i18next.language  // 应该显示当前语言代码
i18next.t('power_inductors')  // 应该显示翻译结果
```

---

## 📞 获取帮助

### 查看完整文档
1. **系统概述** → [PDF-SYSTEM-FINAL-REPORT.md](PDF-SYSTEM-FINAL-REPORT.md)
2. **使用指南** → [PDF-LINKING-SYSTEM-README.md](PDF-LINKING-SYSTEM-README.md)
3. **故障排除** → [VERIFICATION-CHECKLIST.md](VERIFICATION-CHECKLIST.md)

### 常见问题答案
- **如何添加新产品？** 见上方"快速开始"
- **如何修改页面样式？** 编辑 HTML 中的 `<style>` 部分
- **如何支持新语言？** 编辑 JSON 和 i18next 配置

---

## 📊 系统信息

| 项目 | 值 |
|------|-----|
| **系统版本** | 1.0.0 |
| **产品类别数** | 9 |
| **PDF 文件数** | 126+ |
| **支持语言** | 英文、日文、中文 |
| **页面数量** | 9 个产品页面 |
| **页面大小** | 16-19 KB (单个) |
| **加载时间** | < 500ms |
| **最后更新** | 2026-01-11 |

---

## ✅ 检查清单

完成这些步骤，确保系统正常工作：

- [ ] 启动本地服务器
- [ ] 访问 http://localhost:8000/power_inductors.html
- [ ] 查看 PDF 列表
- [ ] 下载一个 PDF
- [ ] 切换语言到日文和中文
- [ ] 点击"下一个"导航到其他产品
- [ ] 返回 products.html
- [ ] 所有功能都正常

---

## 🎓 学习资源

### 技术栈
- **前端框架** → Bootstrap 5.3.3
- **多语言** → i18next 23.15.1
- **图标库** → FontAwesome 5.15.4
- **数据格式** → JSON
- **自动化** → Python 3

### 官方文档
- [Bootstrap 官方文档](https://getbootstrap.com/)
- [i18next 官方文档](https://www.i18next.com/)
- [JSON 规范](https://www.json.org/)

---

## 📅 版本历史

### v1.0.0 (2026-01-11)
- ✓ 初始版本发布
- ✓ 9 个产品页面完成
- ✓ 126+ PDF 映射完成
- ✓ 三语言支持完成
- ✓ 完整文档编写

---

## 💡 提示

- 💾 定期备份 `data/products-pdf-map.json` 文件
- 🔍 修改前先测试页面功能
- 📱 在手机上测试响应式设计
- 🌐 确保浏览器启用 JavaScript
- ⚡ 使用最新版本的浏览器获得最佳体验

---

## 📧 联系方式

如有问题或建议，请查阅文档或联系技术支持团队。

**预计响应时间：** 24 小时  
**支持渠道：** 技术文档、问题追踪系统

---

**最后更新：** 2026年1月11日  
**文档版本：** 1.0  
**维护者：** Datatronic 技术团队

---

*欢迎使用 PDF 链接系统！祝您使用愉快。*

👉 **[现在开始](http://localhost:8000/products.html)** (请确保已启动本地服务器)
