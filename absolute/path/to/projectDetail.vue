const loadProjectBudgets = async () => {
  if (!selectedProjectId.value) return;
  
  try {
    budgetsLoading.value = true;
    const { results } = await projectBudgetApi.getProjectBudget(selectedProjectId.value);
    budgets.value = results;
  } catch (error) {
    ElMessage.error('加载预算数据失败');
    console.error('加载预算数据失败:', error);
  } finally {
    budgetsLoading.value = false;
  }
};