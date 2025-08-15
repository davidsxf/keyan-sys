// 最简代码，也就是这些字段必须有
export default {
  
  path: "/fighting1",
  redirect: "/fighting1/index",
  meta: {
    title: "加油1",
    // icon: "fighting1",

  },
  children: [
    {
      path: "/fighting1/index",
      name: "Fighting1",
      component: () => import("@/views/fighting1/index.vue"),
      meta: {
        title: "加油1",
        showParent: true
      }
    }
  ]
};