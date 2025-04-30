// product-detail.js
Page({
  data: {
    desc: '',     // 保留原来的完整描述
    ccode: '',    // 用于存储patternCode
    cname: '',    // 用于存储patternName
    thumb: '',
    title: '',
    totalQty: 0,   // 总库存
    show: true,   // 默认不显示弹出框
    loading: false,
    // 新增尺寸库存列表
    sizeList: []   // [{size: "规格1", qty: 10}, {size: "规格2", qty: 20}]
  },
  
  onLoad: function(options) {
    // 接收并解码传递的参数
    if (options.desc) {
      const descStr = decodeURIComponent(options.desc);
      
      // 保存完整的desc
      this.setData({
        desc: descStr
      });
      
      // 按第一个空格拆分desc字符串
      const spaceIndex = descStr.indexOf(' ');
      if (spaceIndex !== -1) {
        const ccode = descStr.substring(0, spaceIndex);
        const cname = descStr.substring(spaceIndex + 1);
        
        this.setData({
          ccode: ccode,
          cname: cname
        });
      } else {
        // 如果没有空格，则全部设为ccode
        this.setData({
          ccode: descStr,
          cname: ''
        });
      }
    }
    
    if (options.thumb) {
      this.setData({
        thumb: decodeURIComponent(options.thumb)
      });
    }
    
    if (options.title) {
      this.setData({
        title: decodeURIComponent(options.title)
      });
    }
    
    this.queryInventoyr();
  },
  
  // 点击图片切换弹出框显示状态
  toggleActionSheet() {
    this.setData({
      show: !this.data.show
    });
  },
  
  // 关闭弹出框
  onClose() {
    this.setData({ show: false });
  },
  
  queryInventoyr: function() {
    if(!this.data.ccode){
      return;
    }
    
    this.setData({ loading: true });
  
    wx.request({
      url: 'http://172.16.1.102:8998/inventory/query',
      method: 'GET',
      data: {
        ccode: this.data.ccode
      },
      success: (res) => {
        console.log('库存查询结果', res.data);
        
        if(res.data && Array.isArray(res.data)) {
          // 按size分组汇总qty
          const sizeMap = new Map();
          let totalQty = 0;
          
          // 遍历API返回的数据
          for(let i = 0; i < res.data.length; i++) {
            const item = res.data[i];
            const size = item.size || '无';  // 如果没有size，默认为"无"
            const qty = parseFloat(item.qty) || 0;
            
            // 累加总库存
            totalQty += qty;
            
            // 按size分组
            if(sizeMap.has(size)) {
              sizeMap.set(size, sizeMap.get(size) + qty);
            } else {
              sizeMap.set(size, qty);
            }
          }
          
          // 将Map转为数组，用于渲染表格
          const sizeList = Array.from(sizeMap, ([size, qty]) => ({size, qty}));
          
          this.setData({
            totalQty: totalQty,
            sizeList: sizeList.length > 0 ? sizeList : [{size: '无', qty: 0}]
          });
        } else {
          // 没有数据时设置默认值
          this.setData({
            totalQty: 0,
            sizeList: [{size: '无', qty: 0}]
          });
        }
      },
      fail: (err) => {
        console.error('库存查询失败:', err);
        this.setData({ 
          totalQty: 0,
          sizeList: [{size: '无', qty: 0}],
          loading: false
        });
      },
      complete: () => {
        this.setData({ loading: false });
      }
    });
  }
});