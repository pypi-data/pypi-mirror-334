# Husky Spider utils

## 安装

```bash
pip uninstall husky-spider-utils
pip install husky-spider-utils
```
## 介绍
本库简单实现了selenium和requests的结合，并封装了少部分常用selenium功能。使用SeleniumSession相关方法会自动更新cookies(session和selenium互通)

## 使用

```python
from husky_spider_utils import SeleniumSession
session = SeleniumSession(selenium_init_url="https://cn.bing.com")
session.selenium_get("https://cn.bing.com")
```

