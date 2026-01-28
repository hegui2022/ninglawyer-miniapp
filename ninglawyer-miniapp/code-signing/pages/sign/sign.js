// 合同签署页面
Page({
  data: {
    contract: null,
    partyASigned: false,
    partyBSigned: false,
    currentSigner: null, // 'partyA' or 'partyB'
    canvasWidth: 0,
    canvasHeight: 200,
    isDrawing: false,
    lastX: 0,
    lastY: 0,
    hasSignature: false,
    signing: false
  },
  
  onLoad(options) {
    if (options.content) {
      const contract = JSON.parse(decodeURIComponent(options.content));
      this.setData({ contract });
      
      // 获取系统信息，设置 canvas 宽度
      const systemInfo = wx.getSystemInfoSync();
      this.setData({
        canvasWidth: systemInfo.windowWidth - 64
      });
    }
  },
  
  onReady() {
    this.ctx = wx.createCanvasContext('signature');
    this.ctx.setLineWidth(3);
    this.ctx.setLineCap('round');
    this.ctx.setLineJoin('round');
    this.ctx.setStrokeStyle('#000000');
  },
  
  // 开始签署甲方
  onSignPartyA() {
    this.setData({
      currentSigner: 'partyA',
      hasSignature: false
    });
    
    wx.showModal({
      title: '提示',
      content: '请甲方代表签署',
      showCancel: false
    });
    
    // 清空画布
    this.clearCanvas();
  },
  
  // 开始签署乙方
  onSignPartyB() {
    this.setData({
      currentSigner: 'partyB',
      hasSignature: false
    });
    
    wx.showModal({
      title: '提示',
      content: '请乙方签署',
      showCancel: false
    });
    
    // 清空画布
    this.clearCanvas();
  },
  
  // 触摸开始
  onTouchStart(e) {
    if (!this.data.currentSigner) return;
    
    const { x, y } = e.touches[0];
    this.setData({
      isDrawing: true,
      lastX: x,
      lastY: y
    });
  },
  
  // 触摸移动
  onTouchMove(e) {
    if (!this.data.isDrawing || !this.data.currentSigner) return;
    
    const { x, y } = e.touches[0];
    
    this.ctx.beginPath();
    this.ctx.moveTo(this.data.lastX, this.data.lastY);
    this.ctx.lineTo(x, y);
    this.ctx.stroke();
    this.ctx.draw(true);
    
    this.setData({
      lastX: x,
      lastY: y,
      hasSignature: true
    });
  },
  
  // 触摸结束
  onTouchEnd() {
    this.setData({ isDrawing: false });
  },
  
  // 清空画布
  clearCanvas() {
    const { canvasWidth, canvasHeight } = this.data;
    this.ctx.clearRect(0, 0, canvasWidth, canvasHeight);
    this.ctx.draw(false);
    this.setData({ hasSignature: false });
  },
  
  // 确认签名
  onConfirmSignature() {
    if (!this.data.hasSignature) {
      wx.showToast({
        title: '请先签名',
        icon: 'none'
      });
      return;
    }
    
    wx.showLoading({ title: '保存中...' });
    
    // 导出图片
    wx.canvasToTempFilePath({
      canvasId: 'signature',
      success: (res) => {
        const signaturePath = res.tempFilePath;
        
        if (this.data.currentSigner === 'partyA') {
          this.setData({
            partyASigned: true,
            partyASignature: signaturePath,
            currentSigner: null
          });
        } else {
          this.setData({
            partyBSigned: true,
            partyBSignature: signaturePath,
            currentSigner: null
          });
        }
        
        wx.hideLoading();
        wx.showToast({
          title: '签名成功',
          icon: 'success'
        });
      },
      fail: () => {
        wx.hideLoading();
        wx.showToast({
          title: '保存失败',
          icon: 'none'
        });
      }
    });
  },
  
  // 取消签名
  onCancelSignature() {
    this.clearCanvas();
    this.setData({
      currentSigner: null,
      hasSignature: false
    });
  },
  
  // 完成签署
  onFinish() {
    if (!this.data.partyASigned) {
      wx.showToast({
        title: '请先签署甲方',
        icon: 'none'
      });
      return;
    }
    
    if (!this.data.partyBSigned) {
      wx.showToast({
        title: '请先签署乙方',
        icon: 'none'
      });
      return;
    }
    
    wx.showModal({
      title: '确认签署',
      content: '确认双方都已签署完成吗？签署后将无法修改。',
      success: (res) => {
        if (res.confirm) {
          this.saveContract();
        }
      }
    });
  },
  
  // 保存合同
  saveContract() {
    this.setData({ signing: true });
    
    const contract = {
      ...this.data.contract,
      partyASignature: this.data.partyASignature,
      partyBSignature: this.data.partyBSignature,
      status: 'signed',
      signedAt: new Date().toISOString()
    };
    
    // 保存到本地
    const contracts = wx.getStorageSync('contracts') || [];
    contracts.unshift(contract);
    wx.setStorageSync('contracts', contracts);
    
    setTimeout(() => {
      this.setData({ signing: false });
      
      wx.showToast({
        title: '签署成功',
        icon: 'success'
      });
      
      setTimeout(() => {
        wx.switchTab({
          url: '/pages/record/record'
        });
      }, 1500);
    }, 1000);
  },
  
  // 查看详情
  onDetail() {
    const contract = this.data.contract;
    const content = encodeURIComponent(JSON.stringify(contract));
    
    wx.navigateTo({
      url: `/pages/preview/preview?content=${content}`
    });
  }
});
