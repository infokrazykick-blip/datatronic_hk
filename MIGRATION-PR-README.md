📋 Migration PR 使用说明

概览
- 使用 `.github/PULL_REQUEST_TEMPLATE.md` 来提交迁移的 PR（包含迁移清单与检查项）。
- 在提交前，请本地运行 `python3 scripts/check_migration.py` 来捕获缺失项或大文件警告。

关于媒体与大文件
- 请勿把 >5MB 的文件直接推到 Git。推荐方案：
  - 上传到 S3（并在 `assets.txt` 中列出 URL）
  - 或使用 Netlify Large Media / Git LFS，PR 中需标注下载方法

运行检查示例
```bash
python3 scripts/check_migration.py
```

合并前核对要点
- 确保 `sitemap-urls-full.csv` 包含 `url` 列
- `assets.txt` 列出媒体 URL（如适用）
- 提供 3 个页面截图或对比样本在 PR 描述中

如果你想我直接创建迁移分支和 PR，请把爬虫结果推到 `migrate/` 并回复“已 push”。
