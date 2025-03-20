
arkagent-mcp-server 兼容 mcp 协议,可通过vscode，cursor 等支持mcp server的客户端引入使用

vscode 配置方法手动添加：

```
"arkagent-mcp-server": {
    "command": "uvx",
    "args": [
        "arkagent-mcp-server==0.1.0"
    ],
    "env": {
        "agent_key": "app-a14ebb9c649c"
    }
}
```

其中： agent_key  可以通过[iagent](https://www.iagent.cc)中的 api 管理获取
