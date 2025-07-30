<template>
  <aside class="w-64 bg-gray-800 text-white h-screen fixed overflow-y-auto">
    <div class="p-4 border-b border-gray-700">
      <h1 class="text-xl font-bold">科研管理系统</h1>
    </div>
    <nav class="p-4">
      <ul>
        <li class="mb-1">
          <router-link to="/" class="flex items-center p-2 rounded-lg hover:bg-gray-700 transition-colors">
            <i class="fa fa-dashboard mr-3"></i>
            <span>仪表盘</span>
          </router-link>
        </li>
        <li class="mb-1">
          <router-link to="/projects" class="flex items-center p-2 rounded-lg hover:bg-gray-700 transition-colors">
            <i class="fa fa-folder-open mr-3"></i>
            <span>科研项目</span>
          </router-link>
        </li>
        <li class="mb-1">
          <router-link to="/papers" class="flex items-center p-2 rounded-lg hover:bg-gray-700 transition-colors">
            <i class="fa fa-file-text-o mr-3"></i>
            <span>论文管理</span>
          </router-link>
        </li>
        <li class="mb-1">
          <router-link to="/patents" class="flex items-center p-2 rounded-lg hover:bg-gray-700 transition-colors">
            <i class="fa fa-lightbulb-o mr-3"></i>
            <span>专利管理</span>
          </router-link>
        </li>
        <li class="mb-1">
          <router-link to="/team" class="flex items-center p-2 rounded-lg hover:bg-gray-700 transition-colors">
            <i class="fa fa-users mr-3"></i>
            <span>研究团队</span>
          </router-link>
        </li>
        <li class="mb-1">
          <router-link to="/funding" class="flex items-center p-2 rounded-lg hover:bg-gray-700 transition-colors">
            <i class="fa fa-money mr-3"></i>
            <span>经费管理</span>
          </router-link>
        </li>
      </ul>
    </nav>
  </aside>
</template>

<script lang="ts" setup>
import { RouterLink } from 'vue-router'
</script>

<style scoped>
.router-link-active {
  background-color: #4A5568;
}
</style>
    