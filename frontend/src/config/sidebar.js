// C:\Users\Developer\PycharmProjects\devrange\frontend\src\config\sidebar.js

export const sidebarConfig = {

  parent: [

    {
      label: "Dashboard",
      path: "/dashboard",
      icon: "🏠",
    },

    {
      label: "Children",
      path: "/children",
      icon: "👨‍👩‍👧",
    },


    {
      label: "Lessons",
      path: "/lessons",
      icon: "📚",
    },

    {
      label: "Billing",
      path: "/billing",
      icon: "💳",
    },

  ],

  child: [

    {
      label: "My Lessons",
      path: "/lessons",
      icon: "📚",
    },

    {
      label: "Progress",
      path: "/progress",
      icon: "📊",
    },

    {
      label: "Achievements",
      path: "/achievements",
      icon: "🏆",
    },

    {
      label: "Daily Goal",
      path: "/goals",
      icon: "🎯",
    },
  ],

  teacher: [

    {
      label: "Dashboard",
      path: "/dashboard",
      icon: "🏠",
    },

    {
      label: "Students",
      path: "/students",
      icon: "👨‍🎓",
    },

    {
      label: "Groups",
      path: "/groups",
      icon: "👥",
    },
  ],

  admin: [

    {
      label: "Dashboard",
      path: "/dashboard",
      icon: "🏠",
    },

    {
      label: "Users",
      path: "/users",
      icon: "👤",
    },

    {
      label: "Analytics",
      path: "/analytics",
      icon: "📈",
    },
  ],
}