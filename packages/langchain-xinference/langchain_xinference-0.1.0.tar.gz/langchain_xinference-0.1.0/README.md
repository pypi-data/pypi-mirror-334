# langchain-xinference

This package contains the LangChain integration with Xinference

## Installation

```bash
pip install -U langchain-xinference
```

## Dependence
Install Xinference by using pip as follows. (For more options, see [Installation page](https://inference.readthedocs.io/en/latest/getting_started/installation.html).)

```bash
pip install "xinference[all]"
```

To start a local instance of Xinference, run the following command:

```bash
$ xinference-local
```

## Chat Models

`ChatXinference` class exposes chat models from Xinference.

```python
from langchain_xinference.chat_models import ChatXinference
from langchain.prompts import PromptTemplate

llm = ChatXinference(
  server_url="http://0.0.0.0:9997",  # replace your xinference server url
  model_uid={model_uid}  # replace model_uid with the model UID return from launching the model
         )
prompt = PromptTemplate(input=["country"], template="Q: where can we visit in the capital of {country}? A:")
chain = prompt | llm

chain.invoke(input={"country": "France"})
chain.stream(input={"country": "France"})  #  streaming data
```

## LLMs
`Xinference` class exposes LLMs from Xinference.

```python
from langchain_xinference.llms import Xinference
from langchain.prompts import PromptTemplate

llm = Xinference(
    server_url="http://0.0.0.0:9997",  # replace your xinference server url
    model_uid={model_uid}  # replace model_uid with the model UID return from launching the model
 )
prompt = PromptTemplate(input=["country"], template="Q: where can we visit in the capital of {country}? A:")
chain = prompt | llm
chain.invoke(input={"country": "France"})
```
