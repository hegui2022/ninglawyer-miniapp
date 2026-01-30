const app = getApp()

Page({
  data: {
    files: []
  },

  chooseFile() {
    wx.chooseMessageFile({
      count: 10,
      type: 'file',
      success: (res) => {
        res.tempFiles.forEach(file => {
          this.uploadFile(file)
        })
      }
    })
  },

  uploadFile(file) {
    const id = Date.now()
    const fileItem = {
      id,
      name: file.name,
      size: this.formatSize(file.size),
      status: 'uploading'
    }

    this.setData({
      files: [...this.data.files, fileItem]
    })

    const token = app.globalData.token || wx.getStorageSync('token')

    wx.uploadFile({
      url: app.globalData.apiBase + '/api/files/upload',
      filePath: file.path,
      name: 'file',
      formData: { category: 'evidence' },
      header: { 'Authorization': `Bearer ${token}` },
      success: (res) => {
        const data = JSON.parse(res.data)
        this.updateFileStatus(id, data.success ? 'success' : 'error')
      },
      fail: () => {
        this.updateFileStatus(id, 'error')
      }
    })
  },

  updateFileStatus(id, status) {
    const files = this.data.files.map(f => {
      if (f.id === id) f.status = status
      return f
    })
    this.setData({ files })
  },

  formatSize(bytes) {
    if (bytes < 1024) return bytes + ' B'
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB'
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB'
  }
})
