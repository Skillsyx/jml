<template>
  <div class="preview-page">
    <!-- 顶部标题 -->
    <h1 class="preview-title">标签预览</h1>

    <!-- 打印设置部分 -->
    <div class="print-settings">
      <div class="setting-item">
        <span class="setting-label">选择打印页面：</span>
        <el-select
          v-model="selectedPages"
          multiple
          collapse-tags
          placeholder="请选择页面"
        >
          <el-option
            v-for="i in tableData.length"
            :key="i"
            :label="`第 ${i} 页`"
            :value="i"
          ></el-option>
        </el-select>
      </div>
      <div class="setting-item">
        <el-button @click="selectAllPages">全选</el-button>
        <el-button @click="clearSelectedPages">清空</el-button>
      </div>
    </div>

    <!-- 标签容器 -->
    <div class="labels-container">
      <div
        v-for="(item, index) in tableData"
        :key="index"
        class="label-container"
        :class="{ 'print-hide': !shouldPrintPage(index + 1) }"
      >
        <table class="label-table">
          <!-- 顶部空白行 -->
          <tr>
            <td colspan="4" class="empty-row"></td>
          </tr>
          
          <!-- 公司名称行 -->
          <tr>
            <td colspan="4" class="company-row">
              科米龙（江苏）科技材料有限公司 (008)
            </td>
          </tr>
          
          <!-- 单据号和仓位行 -->
          <tr>
            <td class="label-title">单据号:</td>
            <td class="label-value">{{ item.code }}</td>
            <td class="label-title">仓位:</td>
            <td class="label-value">{{ item.wp }}</td>
          </tr>
          
          <!-- 数量和批号行 -->
          <tr>
            <td class="label-title">数量:</td>
            <td class="label-value">
              {{ item.iQuantity }}{{ item.cComUnitName }}
            </td>
            <td class="label-title">批号:</td>
            <td class="label-value">{{ item.cBatch }}</td>
          </tr>
          
          <!-- 存货编码和名称行 -->
          <tr>
            <td colspan="4" class="inv-code-row">
              <div class="inv-code">{{ item.cInvCode }}</div>
              <div class="inv-name">{{ item.cinvname }}</div>
            </td>
          </tr>

          <!-- 备注和二维码行 -->
          <tr class="remark-row">
            <td class="label-title align-top">备注:</td>
            <td colspan="2" class="remark-cell">{{ item.remark || "" }}</td>
            <td class="qrcode-cell">
              <qrcode-vue
                :value="`${item.cInvCode}|${item.cBatch}|${item.wp}`"
                :size="120"
                level="H"
              />
            </td>
          </tr>
        </table>
        <!-- 页码指示器 -->
        <div class="page-indicator">第 {{ index + 1 }} 页</div>
      </div>
    </div>

    <!-- 打印和返回按钮 -->
    <div class="action-buttons">
      <el-button type="primary" @click="printPage" :disabled="selectedPages.length === 0">打印标签</el-button>
      <el-button @click="goBack">返回查询</el-button>
    </div>
  </div>
</template>

<script>
import QrcodeVue from "qrcode.vue";

export default {
  name: "Preview",
  components: { QrcodeVue },
  data() {
    return {
      tableData: [
        {
          code: "CGDD240421301",
          wp: "KML_21 / 2112",
          cInvCode: "31-PB-F4-4918-KT0",
          cinvname: "科天F4颗粒板 49*18mm (科天水性)",
          iQuantity: 1742,
          cComUnitName: "张",
          cBatch: "BKDGNIGMxnLUM",
          remark: "",
        },{
          code: "CGDD240421301",
          wp: "KML_21 / 2112",
          cInvCode: "31-PB-F4-4918-KT0",
          cinvname: "科天F4颗粒板 49*18mm (科天水性)",
          iQuantity: 1742,
          cComUnitName: "张",
          cBatch: "BKDGNIGMxnLUM",
          remark: "",
        },
        {
          code: "CGDD240421301",
          wp: "KML_21 / 2112",
          cInvCode: "31-PB-F4-4918-KT0",
          cinvname: "科天F4颗粒板 49*18mm (科天水性)",
          iQuantity: 1742,
          cComUnitName: "张",
          cBatch: "BKDGNIGMxnLUM",
          remark: "",
        },{
          code: "CGDD240421301",
          wp: "KML_21 / 2112",
          cInvCode: "31-PB-F4-4918-KT0",
          cinvname: "科天F4颗粒板 49*18mm (科天水性)",
          iQuantity: 1742,
          cComUnitName: "张",
          cBatch: "BKDGNIGMxnLUM",
          remark: "",
        },{
          code: "CGDD240421301",
          wp: "KML_21 / 2112",
          cInvCode: "31-PB-F4-4918-KT0",
          cinvname: "科天F4颗粒板 49*18mm (科天水性)",
          iQuantity: 1742,
          cComUnitName: "张",
          cBatch: "BKDGNIGMxnLUM",
          remark: "",
        },
      ],
      selectedPages: [], // 用于存储选择要打印的页面
    };
  },
  created() {
    // 从路由获取查询结果数据
    const queryData = this.$route.params.queryData;
    if (queryData && queryData.length > 0) {
      this.tableData = queryData;
    }
    
    // 默认全选所有页面
    this.selectAllPages();
  },
  methods: {
    printPage() {
      window.print();
    },
    goBack() {
      this.$router.push("/usage");
    },
    // 检查是否应该打印当前页
    shouldPrintPage(pageNumber) {
      return this.selectedPages.includes(pageNumber);
    },
    // 全选所有页面
    selectAllPages() {
      this.selectedPages = Array.from({ length: this.tableData.length }, (_, i) => i + 1);
    },
    // 清空选择
    clearSelectedPages() {
      this.selectedPages = [];
    },
  },
};
</script>

<style scoped>
/* 页面整体设置 */
.preview-page {
  padding: 20px;
  background-color: #f8f8f8;
  min-height: 100vh;
  box-sizing: border-box;
  font-family: "Microsoft YaHei", sans-serif;
  color: #000;
}

/* 顶部标题 */
.preview-title {
  text-align: center;
  margin-bottom: 20px;
  font-size: 24px;
  color: #333;
}

/* 打印设置区域 */
.print-settings {
  background-color: #fff;
  padding: 15px;
  border-radius: 5px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 25px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
}

.setting-item {
  display: flex;
  align-items: center;
  margin: 5px 0;
}

.setting-label {
  font-weight: bold;
  margin-right: 10px;
}

/* 标签容器 */
.labels-container {
  display: flex;
  flex-wrap: wrap;
  gap: 30px;
  justify-content: center;
  margin-bottom: 30px;
}

/* 每个标签的容器 */
.label-container {
  width: 100%;
  max-width: 800px;
  margin-bottom: 30px;
  box-shadow: 0 3px 10px rgba(0, 0, 0, 0.15);
  background-color: #fff;
  border-radius: 5px;
  overflow: hidden;
  position: relative;
}

/* 页码指示器 */
.page-indicator {
  position: absolute;
  top: 5px;
  right: 10px;
  background-color: #007bff;
  color: white;
  padding: 3px 8px;
  border-radius: 3px;
  font-size: 12px;
  font-weight: bold;
  z-index: 10;
}

/* 标签表格样式 */
.label-table {
  width: 100%;
  border-collapse: collapse;
  border: 2px solid #333;
  color: #000;
  table-layout: fixed;
}

.label-table td {
  border: 1px solid #555;
  padding: 10px 15px;
  color: #000;
}

/* 空白行 */
.empty-row {
  height: 40px;
  border-bottom: 1px dashed #888;
  background-color: #f9f9f9;
}

/* 公司名称行 */
.company-row {
  text-align: center;
  font-size: 28px;
  font-weight: bold;
  padding: 25px 0;
  color: #000;
  background-color: #f0f0f0;
  border-bottom: 2px solid #333;
}

/* 标题单元格 */
.label-title {
  width: 20%;
  font-weight: bold;
  font-size: 18px;
  text-align: right;
  color: #333;
  padding: 15px;
  background-color: #f7f7f7;
}

/* 值单元格 */
.label-value {
  width: 30%;
  font-size: 22px;
  font-weight: bold;
  overflow: hidden;
  text-overflow: ellipsis;
  color: #000;
  padding: 15px;
}

/* 存货编码和名称行 */
.inv-code-row {
  text-align: center;
  padding: 25px 15px;
  background-color: #f0f0f0;
  border-top: 2px solid #333;
  border-bottom: 2px solid #333;
}

.inv-code {
  font-size: 44px;
  font-weight: bold;
  color: #000;
  margin-bottom: 10px;
  letter-spacing: 2px;
}

.inv-name {
  font-size: 18px;
  color: #333;
  font-weight: 500;
}

/* 备注行特殊处理 */
.remark-row td:first-child {
  vertical-align: top;
  padding-top: 15px;
}

/* 备注单元格 */
.remark-cell {
  font-size: 16px;
  color: #000;
  vertical-align: top;
  padding-top: 15px;
  height: 110px;
  background-color: #fff;
}

/* 二维码单元格 */
.qrcode-cell {
  text-align: center;
  vertical-align: middle;
  width: 150px;
  background-color: #fff;
  padding: 10px;
}

/* 顶部对齐 */
.align-top {
  vertical-align: top;
}

/* 按钮容器 */
.action-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 30px;
}

/* 打印隐藏 */
.print-hide {
  display: none;
}

/* 打印时的样式 */
@media print {
  @page {
    size: A4 landscape;
    margin: 5mm; /* 设置上下左右边距为5mm */
  }

  body {
    margin: 0;
    padding: 0;
  }

  .preview-title,
  .print-settings,
  .action-buttons,
  .page-indicator {
    display: none;
  }

  .preview-page {
    padding: 0;
    background-color: white;
    color: #000;
  }

  .labels-container {
    gap: 0;
    display: block;
  }

  .label-container {
    width: 100%;
    max-width: none;
    page-break-after: always;
    box-shadow: none;
    margin: 0 auto;
    padding: 0;
    height: calc(100vh - 10mm); /* 考虑到页边距 */
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 0;
  }

  .label-table {
    width: 100%;
    height: 98%;
    border: 2px solid #000 !important;
  }

  .label-table td {
    border: 1px solid #000 !important;
  }

  /* 确保打印时所有文本和边框可见 */
  * {
    color: #000 !important;
    background-color: transparent !important;
  }
  
  /* 优化打印时的表格边框 */
  .company-row {
    border-bottom: 2px solid #000 !important;
  }
  
  .inv-code-row {
    border-top: 2px solid #000 !important;
    border-bottom: 2px solid #000 !important;
  }

  /* 移除页眉页脚 */
  @page :first {
    margin-top: 5mm;
  }

  @page :left {
    margin-left: 5mm;
  }

  @page :right {
    margin-right: 5mm;
  }

  @page :last {
    margin-bottom: 5mm;
  }
  
  /* 保留选中页面，隐藏未选中页面 */
  .print-hide {
    display: none !important;
  }
}
</style>