// pages/chat/chat.js
const app = getApp()

Page({
  data: {
    messages: [],
    inputText: '',
    isTyping: false,
    showRecorder: false,
    isRecording: false,
    isPlayingAudio: false,
    scrollIntoView: '',
    loadingMore: false,
    recorderManager: null,
    innerAudioContext: null,
    quickTags: [
      '我被拖欠工资了怎么办？',
      '离婚财产怎么分？',
      '借钱不还怎么维权？',
      '签合同要注意什么？',
      '公司不给交社保',
      '工伤赔偿标准',
      '租房纠纷怎么办',
      '如何申请法律援助'
    ]
  },

  onLoad() {
    console.log('聊天页面加载')
    
    // 初始化录音管理器
    this.initRecorder()
    
    // 初始化音频播放器
    this.initAudioPlayer()
    
    // 加载消息历史
    this.loadMessages()
  },

  onShow() {
    // 滚动到底部
    this.scrollToBottom()
  },

  onUnload() {
    // 停止录音
    if (this.data.recorderManager) {
      this.data.recorderManager.stop()
    }
    
    // 停止播放
    if (this.data.innerAudioContext) {
      this.data.innerAudioContext.stop()
    }
  },

  // 初始化录音管理器
  initRecorder() {
    const recorderManager = wx.getRecorderManager()
    
    recorderManager.onStop((res) => {
      console.log('录音结束', res)
      const { tempFilePath, duration } = res
      
      if (this.data.showRecorder && !this.data.isRecording) {
        return // 取消录音
      }
      
      // 发送语音消息
      this.sendVoiceMessage(tempFilePath, duration)
    })
    
    recorderManager.onError((err) => {
      console.error('录音错误', err)
      wx.showToast({
        title: '录音失败',
        icon: 'none'
      })
      this.setData({ showRecorder: false, isRecording: false })
    })
    
    this.setData({ recorderManager })
  },

  // 初始化音频播放器
  initAudioPlayer() {
    const innerAudioContext = wx.createInnerAudioContext()
    
    innerAudioContext.onPlay(() => {
      console.log('开始播放音频')
      this.setData({ isPlayingAudio: true })
    })
    
    innerAudioContext.onEnded(() => {
      console.log('音频播放结束')
      this.setData({ isPlayingAudio: false })
    })
    
    innerAudioContext.onError((err) => {
      console.error('音频播放错误', err)
      this.setData({ isPlayingAudio: false })
      wx.showToast({
        title: '音频播放失败',
        icon: 'none'
      })
    })
    
    this.setData({ innerAudioContext })
  },

  // 加载消息历史
  loadMessages() {
    const messages = app.globalData.messageHistory || []
    this.setData({ messages })
  },

  // 保存消息历史
  saveMessages() {
    app.saveMessageHistory(this.data.messages)
  },

  // 输入内容变化
  onInput(e) {
    this.setData({
      inputText: e.detail.value
    })
  },

  // 清空输入
  clearInput() {
    this.setData({ inputText: '' })
  },

  // 输入框获得焦点
  onInputFocus() {
    // 可以在这里做一些处理
  },

  // 输入框失去焦点
  onInputBlur() {
    // 可以在这里做一些处理
  },

  // 发送快捷标签
  sendQuickTag(e) {
    const tag = e.currentTarget.dataset.tag
    this.setData({ inputText: tag })
    this.sendMessage()
  },

  // 发送文本消息
  async sendMessage() {
    const text = this.data.inputText.trim()
    if (!text) return

    // 添加用户消息
    this.addMessage('user', text)
    
    // 清空输入框
    this.setData({ inputText: '' })
    
    // 发送请求
    await this.sendRequest(text)
  },

  // 发送语音消息
  async sendVoiceMessage(filePath, duration) {
    console.log('发送语音消息', filePath, duration)
    
    // 添加用户消息（显示语音占位符）
    this.addMessage('user', `[语音 ${Math.floor(duration / 1000)}秒]`)
    
    // 将语音上传到服务器
    try {
      const res = await wx.uploadFile({
        url: app.globalData.baseUrl + '/upload',
        filePath: filePath,
        name: 'voice',
        header: {
          'content-type': 'multipart/form-data'
        }
      })
      
      const data = JSON.parse(res.data)
      if (data.success) {
        // 发送语音URL给后端识别
        await this.sendRequest('', data.url)
      } else {
        wx.showToast({
          title: '语音上传失败',
          icon: 'none'
        })
      }
    } catch (e) {
      console.error('上传语音失败', e)
      wx.showToast({
        title: '语音上传失败',
        icon: 'none'
      })
    }
  },

  // 发送请求到后端
  async sendRequest(message, voiceUrl = null) {
    // 显示打字中
    this.setData({ isTyping: true })
    
    try {
      const res = await wx.request({
        url: app.globalData.baseUrl + '/chat',
        method: 'POST',
        data: {
          message: message,
          voice_url: voiceUrl,
          session_id: app.globalData.sessionId
        },
        header: {
          'content-type': 'application/json'
        },
        timeout: 30000
      })
      
      const data = res.data
      console.log('后端返回', data)
      
      // 隐藏打字中
      this.setData({ isTyping: false })
      
      if (data.success) {
        // 添加律师回复
        this.addMessage('lawyer', data.text, data.audio_url)
      } else {
        wx.showToast({
          title: data.error || '请求失败',
          icon: 'none'
        })
      }
    } catch (e) {
      console.error('请求失败', e)
      this.setData({ isTyping: false })
      wx.showToast({
        title: '网络错误',
        icon: 'none'
      })
    }
  },

  // 添加消息
  addMessage(role, content, audioUrl = null) {
    const message = {
      id: Date.now() + Math.random(),
      role,
      content,
      audioUrl,
      audioDuration: null
    }
    
    this.setData({
      messages: [...this.data.messages, message]
    })
    
    // 保存到历史
    this.saveMessages()
    
    // 滚动到底部
    this.scrollToBottom()
  },

  // 滚动到底部
  scrollToBottom() {
    setTimeout(() => {
      if (this.data.messages.length > 0) {
        const lastMsgId = this.data.messages[this.data.messages.length - 1].id
        this.setData({
          scrollIntoView: 'msg-' + lastMsgId
        })
      }
    }, 100)
  },

  // 开始录音
  startRecord() {
    console.log('开始录音')
    
    // 检查录音权限
    wx.getSetting({
      success: (res) => {
        if (!res.authSetting['scope.record']) {
          wx.authorize({
            scope: 'scope.record',
            success: () => {
              this.beginRecord()
            },
            fail: () => {
              wx.showModal({
                title: '提示',
                content: '需要录音权限才能使用语音功能',
                confirmText: '去设置',
                success: (res) => {
                  if (res.confirm) {
                    wx.openSetting()
                  }
                }
              })
            }
          })
        } else {
          this.beginRecord()
        }
      }
    })
  },

  // 开始录音
  beginRecord() {
    this.data.recorderManager.start({
      format: 'mp3',
      duration: 60000,
      sampleRate: 16000
    })
    this.setData({ showRecorder: true, isRecording: true })
  },

  // 结束录音
  endRecord() {
    if (this.data.isRecording) {
      this.data.recorderManager.stop()
      this.setData({ showRecorder: false, isRecording: false })
    }
  },

  // 取消录音
  cancelRecord() {
    if (this.data.isRecording) {
      this.data.recorderManager.stop()
      this.setData({ showRecorder: false, isRecording: false })
    }
  },

  // 录音移动
  onRecordMove(e) {
    const touch = e.touches[0]
    const moveY = touch.clientY
    const startY = this.data.recordStartY || 0
    
    if (startY - moveY > 50) {
      // 上滑取消
      this.setData({ showRecorder: false, isRecording: false })
    }
  },

  // 播放音频
  playAudio(e) {
    const url = e.currentTarget.dataset.url
    console.log('播放音频', url)
    
    // 停止当前播放
    if (this.data.innerAudioContext) {
      this.data.innerAudioContext.stop()
    }
    
    // 设置音频源并播放
    this.data.innerAudioContext.src = url
    this.data.innerAudioContext.play()
  },

  // 加载更多历史
  loadMoreHistory() {
    // 实现加载更多历史消息
    console.log('加载更多历史')
  },

  // 下拉刷新
  onPullDownRefresh() {
    this.loadMessages()
    setTimeout(() => {
      wx.stopPullDownRefresh()
    }, 1000)
  }
})
