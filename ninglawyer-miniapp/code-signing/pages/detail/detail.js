// 合同详情页面
Page({
  data: {
    contract: null,
    showShareMenu: false
  },
  
  onLoad(options) {
    if (options.content) {
      const contract = JSON.parse(decodeURIComponent(options.content));
      this.setData({ contract });
    }
  },
  
  onEdit() {
    const contract = this.data.contract;
    if (contract.status === 'signed') {
      wx.showToast({
        title: '已签署的合同不能修改',
        icon: 'none'
      });
      return;
    }
    
    const content = encodeURIComponent(JSON.stringify(contract));
    wx.navigateTo({
      url: `/pages/draft/draft?template=${content}`
    });
  },
  
  onDelete() {
    const contract = this.data.contract;
    
    wx.showModal({
      title: '确认删除',
      content: '确定要删除这份合同吗？',
      success: (res) => {
        if (res.confirm) {
          const contracts = wx.getStorageSync('contracts') || [];
          const filteredContracts = contracts.filter(c => c.id !== contract.id);
          wx.setStorageSync('contracts', filteredContracts);
          
          wx.showToast({
            title: '删除成功',
            icon: 'success'
          });
          
          setTimeout(() => {
            wx.navigateBack();
          }, 1500);
        }
      }
    });
  },
  
  onShare() {
    const contract = this.data.contract;
    
    this.setData({
      showShareMenu: true
    });
  },
  
  onCloseShare() {
    this.setData({
      showShareMenu: false
    });
  },
  
  onShareWechat() {
    wx.showToast({
      title: '分享到微信',
      icon: 'none'
    });
    this.onCloseShare();
  },
  
  onShareFriend() {
    wx.showToast({
      title: '分享给朋友',
      icon: 'none'
    });
    this.onCloseShare();
  },
  
  onDownload() {
    wx.showToast({
      title: '下载中...',
      icon: 'loading'
    });
    
    setTimeout(() => {
      wx.showToast({
        title: '下载成功',
        icon: 'success'
      });
    }, 2000);
  },
  
  onStatusText(status) {
    const statusMap = {
      'draft': '草稿',
      'signed': '已签署',
      'expired': '已过期'
    };
    return statusMap[status] || status;
  },
  
  onStatusColor(status) {
    const colorMap = {
      'draft': '#FF9800',
      'signed': '#07C160',
      'expired': '#F44336'
    };
    return colorMap[status] || '#999999';
  }
});
