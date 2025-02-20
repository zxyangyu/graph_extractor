# graph_extractor

`GraphExtractor` 类是一个用于处理和提取图结构数据的工具。以下是该类的主要功能和组件说明：

### 主要属性
- **api_key**: 用于验证API请求的身份验证密钥。
- **base_url**: API的基础URL，用于指定请求发送到的具体位置。
- **model**: 使用的语言模型名称或标识符，比如 `"gpt-3.5-turbo"`。

## Install

**Install**

```shell
# clone this repo first
cd graph_extractor
pip install -r requirements.txt
```


> **Please set API key and BASE_URL and MODEL name in environment:
> `export API_KEY="sk-..."`
> `export BASE_URL="https://..."`
> `export MODEL="gpt-4o-mini"`
> **

**Example Usage:**
```python
import os
from graph_extractor import GraphExtractor
API_KEY = os.environ["API_KEY"]
BASE_URL = os.environ["BASE_URL"]
MODEL=os.environ["MODEL"]
processor = GraphExtractor(API_KEY, BASE_URL, MODEL)
with open("book.txt", encoding="utf-8-sig") as f:
    scope = f.read()
graph_json = processor.extraction(scope)
print(graph_json)

```
**run demo**
```shell
# Place the text that needs to be extracted into a knowledge graph in the root directory
python demo.py
```