# 语言选择持久化 | Language Selection Persistence Implementation

## 概述 | Overview
已实现语言选择持久化功能。用户选择日语或中文后，在整个网站的所有页面中都将保持该语言选择，不会在切换页面时重置为英文。

## 実装内容 | Implementation Details

### 1. **js/common.js** 修改
添加以下两个关键函数：

#### `window.getSavedLanguage()`
- 从浏览器的 localStorage 中读取已保存的语言偏好
- 如果没有保存过，默认返回 'en' (英文)

#### `window.changeLanguage(lng)`
- 修改后现在会将语言选择保存到 localStorage
- `localStorage.setItem('preferredLanguage', chosen)`

#### `window.updateLanguageButtonDisplay()`
- 新添加的函数，在页面加载时更新语言按钮的显示
- 确保按钮显示当前正在使用的语言 (EN/JP/CN)

### 2. **index.html** 修改
修改 i18next 初始化代码：
```javascript
// 之前:
i18next.init({
    lng: 'en',
    
// 现在:
const savedLanguage = window.getSavedLanguage ? window.getSavedLanguage() : (localStorage.getItem('preferredLanguage') || 'en');
i18next.init({
    lng: savedLanguage,
```

### 3. **所有其他 HTML 页面** (共 57 个)
使用自动脚本 (`scripts/fix_i18n_language.py`) 修改了以下所有页面的 i18next 初始化：

已修改页面列表:
- `about.html` - 关于我们
- `awards.html` - 荣誉与奖项
- `products.html` - 产品
- `applications.html` - 应用
- `contact.html` - 联系我们
- `catalogue.html` - 产品目录
- 所有产品分类页面
- 所有产品详情页面
- 等等...

## 工作原理 | How It Works

### 流程:
1. **用户打开网站** → 加载 `js/common.js`
2. **js/common.js 加载** → `getSavedLanguage()` 函数可用
3. **页面初始化 i18next** → 调用 `getSavedLanguage()` 获取保存的语言
4. **i18next 应用语言** → 页面显示为保存的语言 (或默认英文)
5. **用户选择语言** → 调用 `changeLanguage(lng)` 
6. **函数保存选择** → `localStorage.setItem('preferredLanguage', chosen)`
7. **用户导航到其他页面** → 步骤 3-4 重复，读取已保存的语言

## localStorage 数据结构
```javascript
localStorage.getItem('preferredLanguage') 
// 返回: 'en', 'ja', 或 'cn'
```

## 测试方法 | Testing

### 方式 1: 自动测试页面
打开：`http://localhost:8000/LANGUAGE-TEST.html`

### 方式 2: 手动测试
1. 打开首页：`http://localhost:8000/index.html`
2. 点击语言按钮 (右上角 "EN")
3. 选择 "JP" 或 "CN"
4. 点击导航菜单链接，如 "About Us"
5. ✅ 验证语言仍为日文/中文

### 方式 3: 浏览器开发者工具
```javascript
// 在浏览器控制台运行:
localStorage.getItem('preferredLanguage')  // 查看保存的语言
localStorage.clear()                        // 清除所有保存
```

## 浏览器兼容性 | Browser Compatibility
- ✅ Chrome / Chromium
- ✅ Firefox  
- ✅ Safari
- ✅ Edge
- localStorage API 在所有现代浏览器中都支持

## 注意事项 | Notes
- localStorage 是本地存储，每个浏览器/设备独立
- 用户清除浏览器数据时会清除该设置
- 页面访问不需要网络连接（仅读取本地 localStorage）
- 无服务器端存储，隐私友好

## 修改的脚本
- `scripts/fix_i18n_language.py` - 批量修改所有 HTML 文件的脚本 (已执行完毕)

## 所有修改文件列表
修改的文件:
1. `/js/common.js` - 核心语言函数
2. `/index.html` - 首页
3. 其他 56 个 HTML 文件 - 通过脚本自动修改

总计: **58 个文件已更新**
