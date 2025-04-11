<template>
    <div class="preview-page">
      <!-- 顶部标题 -->
      <h1 class="preview-title">标签预览</h1>
      <!-- 单个标签卡片 -->
      <div class="labels-container">
        <div v-for="(item, index) in tableData" :key="index" class="a4-label">
          <!-- 公司名称区域 -->
          <div class="label-company">
            科米龙（江苏）科技材料有限公司 (008)
          </div>
          <!-- 信息区域 -->
          <div class="label-info">
            <div class="info-row">
              <div class="info-cell label-title">单据号：</div>
              <div class="info-cell label-value">{{ item.code }}</div>
              <div class="info-cell label-title">仓库：</div>
              <div class="info-cell label-value">{{ item.wp }}</div>
            </div>
            <div class="info-row">
              <div class="info-cell label-title">数量：</div>
              <div class="info-cell label-value">{{ item.iQuantity }}</div>
              <div class="info-cell label-title">批号：</div>
              <div class="info-cell label-value">{{ item.cBatch }}</div>
            </div>
          </div>
          <!-- 存货编码 -->
          <div class="label-invcode">
            {{ item.cInvCode }}
          </div>
          <!-- 存货名称 -->
          <div class="label-invname">
            {{ item.cinvname }}
          </div>
          <!-- 备注 -->
          <div class="label-remark">
            备注：{{ item.remark || '' }}
          </div>
          <!-- 二维码区域 -->
          <div class="label-qrcode-section">
            <qrcode-vue :value="`${item.cInvCode}|${item.cBatch}|${item.wp}`" :size="120" />
          </div>
        </div>
      </div>
      <!-- 打印按钮 -->
      <div class="print-btn-container">
        <el-button type="primary" @click="printPage">打印</el-button>
      </div>
    </div>
  </template>
  
  <script>
  import QrcodeVue from 'qrcode.vue';
  
  export default {
    name: "Preview",
    components: { QrcodeVue },
    data() {
      return {
        // 示例数据
        tableData: [
          {
            code: "CGDD240421301",
            wp: "仓库1",
            cInvCode: "31-PB-F4-4918-KT0",
            cinvname: "科天F4颗粒板 49*18mm (科天水性)",
            iQuantity: 1742,
            cComUnitName: "张",
            cBatch: "BKDGNIGMxnuLUM",
            remark: "备注信息示例"
          }
        ]
      };
    },
    methods: {
      printPage() {
        window.print();
      }
    }
  };
  </script>
  
  <style scoped>
  /* 页面整体设置 */
  .preview-page {
    padding: 20px;
    background-color: #f5f5f5;
    min-height: 100vh;
    box-sizing: border-box;
    font-family: "Microsoft YaHei", sans-serif;
  }
  
  /* 顶部标题 */
  .preview-title {
    text-align: center;
    margin-bottom: 20px;
    font-size: 14pt; /* 根据缩放比例设置 */
    color: #000;
  }
  
  /* 标签容器 */
  .labels-container {
    display: flex;
    flex-wrap: wrap;
    gap: 10px;
    overflow-x: visible;
    padding-bottom: 10px;
  }
  
  /* A4 标签卡片，实际尺寸以设计为准 */
  .a4-label {
    width: 1122px;  /* 原始 A4 横板近似宽度 */
    height: 793px;  /* 原始 A4 横板近似高度 */
    background-color: #fff;
    border: 2px solid #000; /* 黑色边框 */
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    box-sizing: border-box;
    padding: 20px;
    position: relative;
  }
  
  /* 公司名称，字体 100pt 缩小40% -> 60pt */
  .label-company {
    text-align: center;
    font-size: 60pt;
    font-weight: bold;
    color: #000;
    margin-bottom: 10px;
    border-bottom: 2px solid #000; /* 边框线 */
    padding-bottom: 5px;
  }
  
  /* 信息区域 */
  .label-info {
    margin: 10px 0;
  }
  .info-row {
    display: flex;
    margin-bottom: 5px;
  }
  .info-cell {
    flex: 1;
    display: flex;
    align-items: center;
    box-sizing: border-box;
  }
  /* 信息标题，48pt 缩小40% -> 29pt */
  .label-title {
    font-size: 29pt;
    font-weight: bold;
    color: #000;
    margin-right: 5px;
  }
  /* 信息值，90pt 缩小40% -> 54pt */
  .label-value {
    font-size: 54pt;
    color: #000;
  }
  
  /* 存货编码，115pt 缩小40% -> 69pt */
  .label-invcode {
    text-align: center;
    font-size: 69pt;
    font-weight: bold;
    color: #000;
    margin: 10px 0;
  }
  
  /* 存货名称，48pt 缩小40% -> 29pt */
  .label-invname {
    text-align: center;
    font-size: 29pt;
    color: #000;
    margin-bottom: 10px;
  }
  
  /* 备注，58pt 缩小40% -> 35pt */
  .label-remark {
    font-size: 35pt;
    color: #000;
    margin-bottom: 10px;
  }
  
  /* 二维码区域 */
  .label-qrcode-section {
    position: absolute;
    bottom: 20px;
    right: 20px;
    text-align: center;
  }
  
  /* 打印按钮区域 */
  .print-btn-container {
    text-align: center;
    margin-top: 20px;
  }
  
  /* 打印时设置 */
  @media print {
    @page {
      size: A4 landscape;
      margin: 10mm;
    }
    .print-btn-container {
      display: none;
    }
  }
  </style>
  