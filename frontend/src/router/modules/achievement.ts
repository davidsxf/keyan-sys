// 成果管理模块路由配置
export default {
  path: "/achievement",
  meta: {
    title: "成果管理",
    icon: "ep:document-copy",
    showParent: true
  },
  children: [
    {
      path: "/achievement/journal",
      name: "Journal",
      component: () => import("@/views/achievement/journal.vue"),
      meta: {
        title: "期刊管理",
        showParent: true
      }
    },
    {
      path: "/achievement/author",
      name: "Author",
      component: () => import("@/views/achievement/author.vue"),
      meta: {
        title: "作者管理",
        showParent: true
      }
    },

    {
      path: "/achievement/paper",
      name: "Paper",
      component: () => import("@/views/achievement/paper.vue"),
      meta: {
        title: "论文管理",
        showParent: true
      }
    },
    {
      path: "/achievement/stats",
      name: "AchievementStats",
      component: () => import("@/views/achievement/statistics.vue"),
      meta: {
        title: "成果统计",
        showParent: true
      }
    }
    // 以下为预留路由，对应后端已实现的API功能
    // 当创建相应的Vue组件时，取消注释并完善路径
    /*
  
  
    {
      path: "/achievement/stats",
      name: "AchievementStats",
      component: () => import("@/views/achievement/stats.vue"),
      meta: {
        title: "成果统计",
        showParent: true
      }
    }
    */
  ]
};