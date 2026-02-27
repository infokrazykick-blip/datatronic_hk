# 🌐 语言持久化快速指南 | Language Persistence Quick Guide

## ✅ 已完成 | Completed

您的网站现已支持**语言选择持久化**！

### 功能说明 | Feature Description
- 用户选择语言后，该选择会被保存
- 用户在网站中导航时，语言选择保持不变
- 用户下次访问网站时，仍会使用上次选择的语言

## 🚀 如何测试 | How to Test

### 步骤 1: 启动本地服务器
```bash
cd "/Volumes/Extreme Pro/Datatronic/06-Website/website"
python3 -m http.server 8000
```

### 步骤 2: 打开网站
访问 `http://localhost:8000`

### 步骤 3: 测试语言切换
1. 点击右上角语言按钮 (显示 "EN")
2. 选择"日本語 (JP)"或"中文 (CN)"
3. 观察页面切换到选择的语言
4. **点击导航链接到其他页面**
5. ✅ **验证：语言仍然是日文/中文！**

## 📋 技术细节 | Technical Details

### 涉及的文件
- **js/common.js** - 核心语言管理函数
- **index.html** - 首页 i18next 初始化
- **其他 56 个 HTML 页面** - 通过脚本自动更新

### 核心实现
```javascript
// 1. 读取保存的语言
const savedLanguage = window.getSavedLanguage();

// 2. 用该语言初始化 i18next
i18next.init({
    lng: savedLanguage,
    ...
});

// 3. 用户选择语言时保存
localStorage.setItem('preferredLanguage', chosenLanguage);
```

## 📝 使用 localStorage 的优势

✅ **简单** - 无需后端或数据库  
✅ **快速** - 本地存储，即时读写  
✅ **隐私友好** - 数据只在用户浏览器中  
✅ **跨页面** - 整个网站域名共享存储  
✅ **持久** - 关闭浏览器后仍保留  

## 🔧 如何清除测试数据

在浏览器开发者工具的"控制台"标签页运行：

```javascript
// 查看当前保存的语言
localStorage.getItem('preferredLanguage')

// 清除所有本地存储
localStorage.clear()

// 查看所有存储项
console.log(localStorage)
```

## 📱 在不同设备上测试

- 🖥️ **桌面浏览器** - localStorage 独立
- 📱 **手机浏览器** - 每个浏览器 App 独立
- 🔄 **跨浏览器** - Chrome 和 Firefox 的 localStorage 是分开的

## ✨ 完成的功能清单

- [x] 修改 `js/common.js` 添加语言保存/加载函数
- [x] 修改 `index.html` 读取保存的语言
- [x] 修改所有其他 56 个 HTML 页面
- [x] 创建语言按钮显示更新函数
- [x] 测试所有文件修改
- [x] 创建测试页面 (LANGUAGE-TEST.html)
- [x] 创建文档

## 🎯 下一步建议 | Recommendations

1. **在多个浏览器测试** - 确保 localStorage 在各个浏览器中正常工作
2. **在手机上测试** - 验证响应式设计中的语言切换
3. **考虑添加"重置语言"按钮** - 让用户轻松恢复默认英文
4. **添加分析追踪** - 了解用户最常选择哪个语言

## 📞 如果有问题 | Troubleshooting

**问题**: 切换语言后页面没有变化  
**解决**: 检查浏览器开发者工具 (F12) → Applications → LocalStorage

**问题**: 语言没有保存  
**解决**: 检查浏览器的隐私设置是否阻止了 localStorage

**问题**: 不同标签页显示不同语言  
**解决**: 这是正常的 - 需要刷新页面才能读取最新的 localStorage

---

💡 **提示**: 打开 `LANGUAGE-TEST.html` 可以快速验证语言持久化是否工作正常！
