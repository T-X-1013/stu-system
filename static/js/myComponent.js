export default {
  props: {
    result: Array // 假设result是一个数组
  },
  methods: {
    openConfirm() {
      this.$confirm('确定要查看详情吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        // 用户点击了确定按钮
        // 在这里可以执行你想要的操作，比如跳转到详情页面等
        // 这里只是演示了一个提示信息
        this.$message({
          type: 'info',
          message: '已经点击了确定按钮'
        });
      }).catch(() => {
        // 用户点击了取消按钮
        // 这里可以不做任何操作，或者根据需要进行其他处理
        this.$message({
          type: 'info',
          message: '已经点击了取消按钮'
        });
      });
    }
  }
};