// 最简代码，也就是这些字段必须有
export default {
  
  path: "/test",
  redirect: "/test/index",
  meta: {
    title: "测试页面"  
  },
  children: [
    {
      path: "/test/index",
      name: "Test",
      component: () => import("@/views/test.vue"),
      meta: {
        title: "API测试",
        showParent: true
      }
    }
  ]
};