# openai-simple-embeddings

基于OPENAI兼容API接口的embeddings服务封装，以解决langchain_community.vectorstores在使用bge-m3/bge-reranker-v2-m3等模型提供的OPENAI兼容API接口服务时遇到的兼容性问题。

## 安装

```shell
pip install openai-simple-embeddings
```

## 使用

### 配置变量设置

```shell
# OPENAI兼容API服务，可以xinference提供
# 使用OPENAI_EMBEDDINGS_BASE_URL或EMBEDDINGS_BASE_URL设置独立服务地址
export OPENAI_EMBEDDINGS_BASE_URL="http://localhost/v1"
# OPENAI兼容API服务密钥，一般以sk-开头，共16位长
# 使用OPENAI_EMBEDDINGS_API_KEY或EMBEDDINGS_API_KEY设置独立服务密码
export OPENAI_EMBEDDINGS_API_KEY=""
# 默认的文本向量化模型
export OPENAI_EMBEDDINGS_MODEL="bge-m3"
# 向量数据库（以redis-stack为例）
export REDIS_STACK_URL="redis://localhost:6379/0"
# 字符串长度控制
export OPENAI_EMBEDDINGS_MAX_SIZE=1024
```

### 获取文本向量

*代码*
```python
from openai_simple_embeddings.base import get_text_embeddings

r1 = get_text_embeddings("hello")
print(r1)
```

*输出*

```txt
[-0.032024841755628586, 0.023251207545399666, ..., -0.037223849445581436, 0.05963246524333954]
```

### 集成到向量数据库客户端

*代码*
```python
from openai_simple_embeddings.langchain_embeddings import OpenAISimpleEmbeddings
from langchain_community.vectorstores.redis import Redis as LangchainRedisVectorStore
import python_environment_settings

REDIS_STACK_URL = python_environment_settings.get("REDIS_STACK_URL")
index_name = "kb:test"
embeddings = OpenAISimpleEmbeddings()
lrvs = LangchainRedisVectorStore(
    redis_url=REDIS_STACK_URL,
    index_name=index_name,
    key_prefix=index_name,
    embedding=embeddings,
)
uids = lrvs.add_texts(["hello"])
print(uids)
```

*输出*

```txt
['kb:test:984af7f2ffea4d49952af82dd992c8f8']
```

## 关于字符串长度控制

- 模型本身一般没有字符串长度控制。
- 但过长的字符串会导入模型占用内存的增长。
- 默认将字符串长度控制在：1024字。
- 通过`OPENAI_EMBEDDINGS_MAX_SIZE`设置默认最大字符串长度。
- 也可以在函数调用中指定最大字符串长度。
- 注意：所有超过最大长度的字符串将被截断。

## 版本记录

### v0.1.0

- 版本首发。

### v0.1.1

- 允许embeddings模型使用独立的服务地址及密码。

### v0.1.2

- 默认embeddings模型使用独立的服务地址及密码。
