/**
 * MCP (Model Context Protocol) 客户端
 * 用于管理模型上下文和工具调用
 */

const { request } = require('./request');

/**
 * MCP 客户端
 */
class MCPClient {
  constructor(options = {}) {
    this.baseUrl = options.baseUrl || '/api/mcp';
    this.sessionId = options.sessionId || this.generateSessionId();
    this.context = options.context || {};
    this.tools = options.tools || [];
    this.history = [];
  }

  /**
   * 生成会话 ID
   */
  generateSessionId() {
    return `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
  }

  /**
   * 初始化 MCP 会话
   */
  async init() {
    try {
      const res = await request({
        url: `${this.baseUrl}/init`,
        method: 'POST',
        data: {
          sessionId: this.sessionId,
          context: this.context,
          tools: this.tools
        }
      });

      console.log('MCP 会话初始化成功', res);
      return res.data;
    } catch (err) {
      console.error('MCP 会话初始化失败', err);
      throw err;
    }
  }

  /**
   * 发送消息到 MCP
   * @param {string} message - 用户消息
   * @param {object} metadata - 元数据
   */
  async sendMessage(message, metadata = {}) {
    try {
      // 添加到历史记录
      this.history.push({
        role: 'user',
        content: message,
        timestamp: Date.now(),
        metadata
      });

      const res = await request({
        url: `${this.baseUrl}/message`,
        method: 'POST',
        data: {
          sessionId: this.sessionId,
          message,
          history: this.history,
          context: this.context,
          metadata
        }
      });

      // 添加助手回复到历史
      if (res.data.response) {
        this.history.push({
          role: 'assistant',
          content: res.data.response,
          timestamp: Date.now(),
          metadata: res.data.metadata || {}
        });
      }

      // 处理工具调用
      if (res.data.toolCalls && res.data.toolCalls.length > 0) {
        await this.handleToolCalls(res.data.toolCalls);
      }

      return res.data;
    } catch (err) {
      console.error('MCP 发送消息失败', err);
      throw err;
    }
  }

  /**
   * 处理工具调用
   * @param {array} toolCalls - 工具调用列表
   */
  async handleToolCalls(toolCalls) {
    for (const toolCall of toolCalls) {
      try {
        const result = await this.executeTool(toolCall);
        
        // 将工具结果发送回 MCP
        await this.sendToolResult(toolCall.id, result);
      } catch (err) {
        console.error(`工具调用失败: ${toolCall.name}`, err);
      }
    }
  }

  /**
   * 执行工具
   * @param {object} toolCall - 工具调用
   */
  async executeTool(toolCall) {
    const { name, parameters } = toolCall;
    
    // 查找工具
    const tool = this.tools.find(t => t.name === name);
    if (!tool) {
      throw new Error(`工具不存在: ${name}`);
    }

    // 执行工具
    return await tool.execute(parameters);
  }

  /**
   * 发送工具结果
   * @param {string} toolCallId - 工具调用 ID
   * @param {any} result - 工具结果
   */
  async sendToolResult(toolCallId, result) {
    try {
      const res = await request({
        url: `${this.baseUrl}/tool-result`,
        method: 'POST',
        data: {
          sessionId: this.sessionId,
          toolCallId,
          result
        }
      });

      // 添加工具结果到历史
      if (res.data.response) {
        this.history.push({
          role: 'tool',
          content: JSON.stringify(result),
          toolCallId,
          timestamp: Date.now()
        });

        this.history.push({
          role: 'assistant',
          content: res.data.response,
          timestamp: Date.now()
        });
      }

      return res.data;
    } catch (err) {
      console.error('MCP 发送工具结果失败', err);
      throw err;
    }
  }

  /**
   * 更新上下文
   * @param {object} context - 上下文信息
   */
  async updateContext(context) {
    try {
      this.context = { ...this.context, ...context };

      const res = await request({
        url: `${this.baseUrl}/context`,
        method: 'PUT',
        data: {
          sessionId: this.sessionId,
          context: this.context
        }
      });

      console.log('MCP 上下文更新成功', res);
      return res.data;
    } catch (err) {
      console.error('MCP 上下文更新失败', err);
      throw err;
    }
  }

  /**
   * 获取历史记录
   * @param {number} limit - 限制数量
   */
  getHistory(limit = 10) {
    return this.history.slice(-limit * 2); // user + assistant pairs
  }

  /**
   * 清空历史记录
   */
  clearHistory() {
    this.history = [];
    return this.updateContext({ historyCleared: true });
  }

  /**
   * 获取上下文
   */
  getContext() {
    return this.context;
  }

  /**
   * 添加工具
   * @param {object} tool - 工具定义
   */
  addTool(tool) {
    this.tools.push(tool);
  }

  /**
   * 移除工具
   * @param {string} toolName - 工具名称
   */
  removeTool(toolName) {
    this.tools = this.tools.filter(t => t.name !== toolName);
  }

  /**
   * 获取所有工具
   */
  getTools() {
    return this.tools;
  }

  /**
   * 结束会话
   */
  async endSession() {
    try {
      const res = await request({
        url: `${this.baseUrl}/end`,
        method: 'POST',
        data: {
          sessionId: this.sessionId
        }
      });

      console.log('MCP 会话结束', res);
      return res.data;
    } catch (err) {
      console.error('MCP 结束会话失败', err);
      throw err;
    }
  }

  /**
   * 流式发送消息
   * @param {string} message - 消息
   * @param {function} onChunk - 分块回调
   * @param {object} metadata - 元数据
   */
  async streamMessage(message, onChunk, metadata = {}) {
    // 注意：微信小程序的 wx.request 不支持真正的流式传输
    // 这里使用模拟实现
    
    const response = await this.sendMessage(message, metadata);
    const fullText = response.response || '';
    
    // 模拟流式输出
    const chunkSize = 10;
    const chunks = [];
    for (let i = 0; i < fullText.length; i += chunkSize) {
      chunks.push(fullText.slice(i, i + chunkSize));
    }
    
    for (let i = 0; i < chunks.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 30));
      onChunk(chunks[i], i === chunks.length - 1);
    }
    
    return response;
  }
}

/**
 * 创建 MCP 客户端实例
 * @param {object} options - 配置选项
 */
function createMCPClient(options = {}) {
  return new MCPClient(options);
}

module.exports = {
  MCPClient,
  createMCPClient
};
