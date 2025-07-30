<template>
  <el-menu
    default-active="1"
    class="el-menu-vertical-demo"
    background-color="#1E293B"
    text-color="#F8FAFC"
    active-text-color="#3B82F6"
    router
  >
    <div class="p-4 border-b border-gray-700">
      <h1 class="text-xl font-bold text-white">科研管理系统</h1>
    </div>
    <el-menu-item index="1" route="/">
      <el-icon><Grid /></el-icon>
      <span>仪表盘</span>
    </el-menu-item>
    <el-menu-item index="2" route="/projects">
      <el-icon><FolderOpened /></el-icon>
      <span>科研项目</span>
    </el-menu-item>
    <el-menu-item index="3" route="/papers">
      <el-icon><Document /></el-icon>
      <span>论文管理</span>
    </el-menu-item>
    <el-menu-item index="4" route="/patents">
      <el-icon><Lightbulb /></el-icon>
      <span>专利管理</span>
    </el-menu-item>
    <el-menu-item index="5" route="/team">
      <el-icon><UserFilled /></el-icon>
      <span>研究团队</span>
    </el-menu-item>
    <el-menu-item index="6" route="/funding">
      <el-icon><Money /></el-icon>
      <span>经费管理</span>
    </el-menu-item>
  </el-menu>
</template>

<script lang="ts" setup>
import { Grid, FolderOpened, Document, Lightbulb, UserFilled, Money } from '@element-plus/icons-vue'
</script>

<style scoped>
.el-menu-vertical-demo {
  height: 100vh;
  border-right: none;
}
</style>
    