// 最简代码，也就是这些字段必须有
export default {
  path: "/base",
  meta: {
    title: "基本信息",
    icon: "ep/menu"    
  },
  children: [
    {
      path: "/base/category",
      name: "Category",

      component: () => import("@/views/base/category.vue"),
      meta: {
        title: "类别",
        showParent: true
      }
    },
    {
      path: "/base/org",
      name: "Org",
      component: () => import("@/views/base/org.vue"),
      meta: {
        title: "组织",
        showParent: true
      }
    }
    // {
    //   path: "/base/effort",
    //   name: "Effort",
    //   component: () => import("@/views/base/effort.vue"),
    //   meta: {
    //     title: "努力",
    //     showParent: true
    //   }
    // }
  ]
};