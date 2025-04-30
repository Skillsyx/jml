const products = require('../../data.js')

Page({
  data: {
    activeKey: 0,
    cardList: products,
    filteredCardList: products, // 添加一个新的数组用于存储筛选后的结果
    designTypes: ["全部", "创意背板", "欧洲烤漆板", "同步肤感", "臻木饰面板-奥系列", "臻木饰面板-金系列"]
  },
  
  onLoad(options) {
    // 页面加载时显示所有产品
    this.setData({
      filteredCardList: this.data.cardList
    });
  },
  
  // 侧边栏切换回调
  onSidebarChange(event) {
    const activeKey = event.detail;
    this.setData({ activeKey });
    
    // 根据选中的侧边栏项目筛选产品
    if (activeKey === 0) {
      // 选择"全部"时显示所有产品
      this.setData({
        filteredCardList: this.data.cardList
      });
    } else {
      // 选择具体分类时过滤产品
      const selectedType = this.data.designTypes[activeKey];
      const filtered = this.data.cardList.filter(item => item.designType === selectedType);
      this.setData({
        filteredCardList: filtered
      });
    }
  },
  
  // 搜索框的回调
  onSearch(event) {
    const keyword = event.detail; // 输入的搜索关键词
    console.log('搜索关键词：', keyword);
    
    // 在当前分类中搜索（结合侧边栏和搜索功能）
    let baseList = [];
    
    if (this.data.activeKey === 0) {
      // 如果是"全部"分类，则在所有产品中搜索
      baseList = this.data.cardList;
    } else {
      // 否则在当前选中的分类中搜索
      const selectedType = this.data.designTypes[this.data.activeKey];
      baseList = this.data.cardList.filter(item => item.designType === selectedType);
    }
    
    // 在基础列表中进行关键词搜索（搜索标题、描述等）
    if (keyword) {
      const filtered = baseList.filter(item => 
        item.patternCode.toLowerCase().includes(keyword.toLowerCase()) || 
        item.patternName.toLowerCase().includes(keyword.toLowerCase()) ||
        item.designType.toLowerCase().includes(keyword.toLowerCase())
      );
      this.setData({
        filteredCardList: filtered
      });
    } else {
      // 如果关键词为空，则显示当前分类的所有产品
      this.setData({
        filteredCardList: baseList
      });
    }
    
    wx.showToast({ title: `搜索: ${keyword}`, icon: 'none' });
  },
  
  onCancel() {
    console.log('点击了取消');
    // 重置搜索，显示当前分类的所有产品
    let baseList = [];
    
    if (this.data.activeKey === 0) {
      baseList = this.data.cardList;
    } else {
      const selectedType = this.data.designTypes[this.data.activeKey];
      baseList = this.data.cardList.filter(item => item.designType === selectedType);
    }
    
    this.setData({
      filteredCardList: baseList
    });
  },

  //卡片点击处理函数
  onCardClick(event) {
    const { patternCode, patternName, designType, imageUrl } = event.currentTarget.dataset;
    
    // 构建传递的参数
    const desc = `${patternCode} ${patternName}`;
    
    // 跳转到详情页并传递参数
    wx.navigateTo({
      url: `/pages/product-detail/product-detail?desc=${encodeURIComponent(desc)}&thumb=${encodeURIComponent(imageUrl)}&title=${encodeURIComponent(designType)}`
    });
  },
});