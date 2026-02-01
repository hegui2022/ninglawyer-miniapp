// 宁律师聊天页面逻辑
const app = getApp()
const API_BASE = 'http://localhost:5000/api/v1/ninglawyer'

Page({
  data: {
    messages: [],              // 消息列表
    inputText: '',              // 输入文本
    isTyping: false,            // 是否正在输入
    isVoiceMode: false,         // 是否为语音模式
    isRecording: false,         // 是否正在录音
    scrollToView: '',           // 滚动到的消息ID
    showHistoryModal: false,    // 是否显示历史记录弹窗
    history: [],                // 历史记录
    sessionId: '',              // 会话ID
    userId: '',                 // 用户ID
    recordingManager: null,     // 录音管理器
    innerAudioContext: null     // 音频播放器
  },

  onLoad() {
    // 初始化数据
    this.setData({
      userId: `user_${Date.now()}`,
      sessionId: `session_${Date.now()}`,
      recordingManager: wx.getRecorderManager(),
      innerAudioContext: wx.createInnerAudioContext()
    })
    
    // 监听录音事件
    this.initRecorder()
    
    // 监听音频播放事件
    this.initAudioPlayer()
  },

  onUnload() {
    // 清理资源
    if (this.data.recordingManager) {
      this.data.recordingManager.stop()
    }
    if (this.data.innerAudioContext) {
      this.data.innerAudioContext.destroy()
    }
  },

  // 初始化录音器
  initRecorder() {
    const recorderManager = this.data.recordingManager
    
    recorderManager.onStop((res) => {
      console.log('录音结束', res)
      this.handleVoiceRecording(res.tempFilePath, res.duration)
    })
    
    recorderManager.onError((err) => {
      console.error('录音失败', err)
      wx.showToast({
        title: '录音失败',
        icon: 'none'
      })
    })
  },

  // 初始化音频播放器
  initAudioPlayer() {
    const audioContext = this.data.innerAudioContext
    
    audioContext.onEnded(() => {
      console.log('音频播放结束')
    })
    
    audioContext.onError((err) => {
      console.error('音频播放失败', err)
      wx.showToast({
        title: '播放失败',
        icon: 'none'
      })
    })
  },

  // 开始录音
  onStartRecord() {
    console.log('开始录音')
    this.setData({
      isRecording: true
    })
    
    this.data.recordingManager.start({
      duration: 60000,  // 最长60秒
      format: 'mp3'
    })
    
    wx.vibrateShort()
  },

  // 停止录音
  onStopRecord() {
    console.log('停止录音')
    if (this.data.isRecording) {
      this.data.recordingManager.stop()
      this.setData({
        isRecording: false
      })
      wx.vibrateShort()
    }
  },

  // 处理录音结果
  handleVoiceRecording(filePath, duration) {
    // 1. 显示用户语音消息
    this.addMessage({
      role: 'user',
      type: 'voice',
      audioUrl: filePath,
      duration: Math.round(duration / 1000)
    })
    
    // 2. 将语音转换为文本（ASR）
    this.recognizeVoice(filePath)
  },

  // 语音识别（ASR）
  async recognizeVoice(filePath) {
    try {
      // 读取音频文件
      const fileSystemManager = wx.getFileSystemManager()
      const audioData = fileSystemManager.readFileSync(filePath, 'base64')
      
      // 调用ASR API
      const res = await wx.request({
        url: `${API_BASE}/voice/recognize`,
        method: 'POST',
        data: {
          audio_base64: audioData,
          user_id: this.data.userId
        },
        header: {
          'content-type': 'application/json'
        }
      })
      
      if (res.data.success) {
        const text = res.data.data.text
        console.log('语音识别结果:', text)
        
        // 3. 发送文本消息
        this.sendMessage(text)
      } else {
        throw new Error(res.data.message || '语音识别失败')
      }
    } catch (err) {
      console.error('语音识别失败', err)
      wx.showToast({
        title: '语音识别失败',
        icon: 'none'
      })
    }
  },

  // 切换语音模式
  onToggleVoiceMode() {
    this.setData({
      isVoiceMode: !this.data.isVoiceMode
    })
  },

  // 输入文本
  onInput(e) {
    this.setData({
      inputText: e.detail.value
    })
  },

  // 发送消息
  onSend() {
    if (!this.data.inputText.trim()) {
      return
    }
    
    this.sendMessage(this.data.inputText)
  },

  // 发送消息
  async sendMessage(text) {
    // 1. 显示用户消息
    this.addMessage({
      role: 'user',
      type: 'text',
      content: text
    })
    
    // 2. 清空输入框
    this.setData({
      inputText: ''
    })
    
    // 3. 显示正在输入
    this.setData({
      isTyping: true
    })
    
    try {
      // 4. 调用流式聊天API
      await this.streamChat(text)
    } catch (err) {
      console.error('发送消息失败', err)
      wx.showToast({
        title: '发送失败',
        icon: 'none'
      })
      this.setData({
        isTyping: false
      })
    }
  },

  // 流式聊天
  async streamChat(query) {
    return new Promise((resolve, reject) => {
      const task = wx.request({
        url: `${API_BASE}/chat/stream`,
        method: 'POST',
        data: {
          query: query,
          user_id: this.data.userId,
          session_id: this.data.sessionId,
          user_type: 'individual'
        },
        header: {
          'content-type': 'application/json'
        },
        responseType: 'text',
        success: (res) => {
          console.log('流式响应', res)
          
          // 隐藏正在输入
          this.setData({
            isTyping: false
          })
          
          // 解析流式响应
          const lines = res.data.split('\n')
          let fullContent = ''
          
          for (const line of lines) {
            if (!line.trim()) continue
            
            try {
              const chunk = JSON.parse(line)
              
              if (chunk.type === 'chunk') {
                // 累积内容
                fullContent += chunk.content
                
                // 更新最后一条助手消息
                this.updateLastAssistantMessage(fullContent)
              } else if (chunk.type === 'end') {
                // 流式结束
                console.log('流式聊天结束', chunk.data)
                resolve()
              } else if (chunk.type === 'error') {
                // 错误
                reject(new Error(chunk.message))
              }
            } catch (e) {
              console.error('解析流式数据失败', e)
            }
          }
        },
        fail: (err) => {
          console.error('请求失败', err)
          this.setData({
            isTyping: false
          })
          reject(err)
        }
      })
    })
  },

  // 添加消息
  addMessage(message) {
    const messages = [...this.data.messages, {
      id: Date.now(),
      ...message
    }]
    
    this.setData({
      messages: messages,
      scrollToView: `msg-${messages[messages.length - 1].id}`
    })
  },

  // 更新最后一条助手消息
  updateLastAssistantMessage(content) {
    const messages = [...this.data.messages]
    const lastMessage = messages[messages.length - 1]
    
    if (lastMessage && lastMessage.role === 'assistant') {
      lastMessage.content = content
    } else {
      // 如果最后一条不是助手消息，添加新的
      messages.push({
        id: Date.now(),
        role: 'assistant',
        type: 'text',
        content: content
      })
    }
    
    this.setData({
      messages: messages,
      scrollToView: `msg-${messages[messages.length - 1].id}`
    })
  },

  // 播放语音
  onPlayVoice(e) {
    const audioUrl = e.currentTarget.dataset.url
    console.log('播放语音', audioUrl)
    
    const audioContext = this.data.innerAudioContext
    audioContext.src = audioUrl
    audioContext.play()
  },

  // 显示历史记录
  onShowHistory() {
    this.loadHistory()
    this.setData({
      showHistoryModal: true
    })
  },

  // 加载历史记录
  async loadHistory() {
    try {
      const res = await wx.request({
        url: `${API_BASE}/history`,
        method: 'GET',
        data: {
          session_id: this.data.sessionId
        },
        header: {
          'content-type': 'application/json'
        }
      })
      
      if (res.data.success) {
        const history = res.data.data.history.map((msg, index) => ({
          id: index,
          role: msg.role,
          content: msg.content,
          time: new Date().toLocaleString()
        }))
        
        this.setData({
          history: history
        })
      }
    } catch (err) {
      console.error('加载历史记录失败', err)
    }
  },

  // 关闭历史记录
  onCloseHistory() {
    this.setData({
      showHistoryModal: false
    })
  },

  // 清除会话
  onClearSession() {
    wx.showModal({
      title: '确认清除',
      content: '确定要清除所有对话记录吗？',
      success: async (res) => {
        if (res.confirm) {
          try {
            await wx.request({
              url: `${API_BASE}/session`,
              method: 'DELETE',
              data: {
                session_id: this.data.sessionId
              },
              header: {
                'content-type': 'application/json'
              }
            })
            
            // 清空本地消息
            this.setData({
              messages: []
            })
            
            wx.showToast({
              title: '已清除',
              icon: 'success'
            })
          } catch (err) {
            console.error('清除会话失败', err)
            wx.showToast({
              title: '清除失败',
              icon: 'none'
            })
          }
        }
      }
    })
  }
})
