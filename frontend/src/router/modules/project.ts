// 最简代码，也就是这些字段必须有
export default {
  path: "/project",
  meta: {
    title: "项目",
    icon: "ep/project",
    showParent: true
  },
  children: [
    {
      path: "/project/project",
      name: "Project",
      component: () => import("@/views/project/project.vue"),
      meta: {
        title: "项目",
        showParent: true
      }
    },
    // {
    //   path: "/base/org",
    //   name: "Org",
    //   component: () => import("@/views/base/org.vue"),
    //   meta: {
    //     title: "组织",
    //     showParent: true
    //   }
    // },
    // {
    //   path: "/base/department",
    //   name: "Department",
    //   component: () => import("@/views/base/department.vue"),
    //   meta: {
    //     title: "部门",
    //     showParent: true
    //   }
    // },
    // {
    //   path: "/base/team",
    //   name: "Team",
    //   component: () => import("@/views/base/team.vue"),
    //   meta: {
    //     title: "团队",
    //     showParent: true
    //   }
    // },
    // {
    //   path: "/base/staff",
    //   name: "Staff",
    //   component: () => import("@/views/base/staff.vue"),
    //   meta: {
    //     title: "员工",
    //     showParent: true
    //   }
    // },

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