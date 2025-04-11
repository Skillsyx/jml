<template>
  <div class="page">
    <!-- 查询表单区域 -->
    <section class="form-section">
      <el-form
        :model="form"
        label-position="left"
        label-width="85px"
        class="query-form"
      >
        <h2 class="form-title">标签查询</h2>
        <el-form-item label="单据号：">
          <el-input v-model="form.ordercode" placeholder="请输入单据号" />
        </el-form-item>
        <!-- 使用 el-row 和 el-col 让起始、结束行号在同一行 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="起始行号：">
              <el-input-number
                v-model="form.startnum"
                :min="1"
                placeholder="请输入起始行号"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="结束行号：">
              <el-input-number
                v-model="form.endnum"
                :min="1"
                placeholder="请输入结束行号"
              />
            </el-form-item>
          </el-col>
        </el-row>
        <!-- 新增选择器：公司 -->
        <el-form-item label="公司：">
          <el-select v-model="form.company" placeholder="请选择公司">
            <el-option
              v-for="item in companies"
              :key="item.key"
              :label="item.value"
              :value="item.value"
            >
            </el-option>
          </el-select>
        </el-form-item>
        <!-- 提交按钮区域 -->
        <el-form-item class="btn-row">
          <el-button type="primary" @click="handleSubmit">提交</el-button>
        </el-form-item>
      </el-form>
    </section>

    <!-- 表格展示区域 -->
    <section class="table-section">
      <el-table :data="tableData" style="width: 100%; height: 100%">
        <el-table-column prop="code" label="单据号"  width="250"  />
        <el-table-column prop="wp" label="仓库"  width="250" />
        <el-table-column prop="cInvCode" label="存货编码"  />
        <el-table-column prop="cinvname" label="存货名称"  />
        <!-- <el-table-column prop="address" label="货位" /> -->
        <el-table-column prop="iQuantity" label="数量"  width="250"/>
        <el-table-column prop="cComUnitName" label="单位" width="250" />
        <el-table-column prop="cBatch" label="批号" width="250" />
      </el-table>
    </section>
  </div>
</template>
  
  <script>
  import axios from 'axios'
export default {
  name: "QueryAndTable",
  data() {
    return {
      // 表单数据
      form: {
        ordercode: "",
        startnum: 1,
        endnum: 999,
        company: "科米龙（江苏）科技材料有限公司",
      },
      companies: [
        { key: "金米龙（江苏）", value: "金米龙（江苏）科技材料有限公司" },
        { key: "科米龙（江苏）", value: "科米龙（江苏）科技材料有限公司" },
      ],
      // 示例的表格数据
      tableData: [],
    };
  },
  methods: {
    async handleSubmit() {
      if (
        !this.form.ordercode ||
        !this.form.startnum ||
        !this.form.endnum ||
        !this.form.company
      ) {
        this.$message.error("请填写完整信息");
        return;
      }
      const params = {
        ordercode: this.form.ordercode,
        startnum: this.form.startnum,
        endnum: this.form.endnum,
        company: this.form.company,
      };

      console.log(params);

      try {
        const response = await axios.post(
          "http://localhost:9889/api/getTableData",
          params
        );
        this.tableData = response.data || [];
        console.log(this.tableData);
        
        if (this.tableData.length === 0) {
          this.$message.warning("没有查询到数据");
        }
      } catch (error) {
        this.$message.error("查询失败: " + error.message);
      }
    },
  },
};
</script>
  
  <style scoped>
/* 整个页面使用 flex 布局，垂直排列 */
.page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: #f5f5f5;
  box-sizing: border-box;
  padding-bottom: 5px; /* 新增留白 */
  padding-left: 5px;
  padding-right: 5px;
}

/* 查询表单区域：不设置固定高度，让内容自适应 */
.form-section {
  background-color: #fff;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

/* 控制表单宽度和居中 */
.query-form {
  max-width: 600px;
  margin: 0 auto;
}

/* 表单标题 */
.form-title {
  text-align: center;
  color: #333;
  margin-top: 20px;
  margin-bottom: 20px;
  font-size: 1.5em;
}

/* 提交按钮区域 */
.btn-row {
  text-align: center;
}
.btn-row .el-button {
  width: 150px;
}

/* 表格区域：占据剩余空间并允许内部滚动 */
.table-section {
  flex: 1;
  background-color: #fff;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden; /* 防止页面整体滚动 */
}

/* 内部 el-table 设置高度为 100%，使其占满父容器 */
.table-section .el-table {
  height: 100%;
}
</style>
  