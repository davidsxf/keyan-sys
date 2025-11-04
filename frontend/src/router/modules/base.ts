// 最简代码，也就是这些字段必须有
export default {
  path: "/base",
  meta: {
    title: "基本信息",
    icon: "ep/menu",
    rank: 1
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
    },
    {
      path: "/base/department",
      name: "Department",
      component: () => import("@/views/base/department.vue"),
      meta: {
        title: "部门",
        showParent: true
      }
    },
    {
      path: "/base/team",
      name: "Team",
      component: () => import("@/views/base/team.vue"),
      meta: {
        title: "团队",
        showParent: true
      }
    },
    {
      path: "/base/departmentStats/:id?",
      name: "DepartmentStats",
      component: () => import("@/views/base/departmentStats.vue"),
      meta: {
        title: "部门统计",
        showParent: true,
        showLink: false
      }
    },
    {
      path: "/base/teamStats/:id?",
      name: "TeamStats",
      component: () => import("@/views/base/teamStats.vue"),
      meta: {
        title: "团队统计",
        showParent: true,
        showLink: false
      }
    },
    {
      path: "/base/staff/:id?",
      name: "StaffDetails",
      component: () => import("@/views/base/staffDetails.vue"),
      meta: {
        title: "个人信息与统计",
        showParent: true,
        showLink: false
      }
    },
    {
      path: "/base/staff",
      name: "Staff",
      component: () => import("@/views/base/staff.vue"),
      meta: {
        title: "员工",
        showParent: true
      }
    },
  

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