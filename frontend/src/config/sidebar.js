// C:\Users\Developer\PycharmProjects\devrange\frontend\src\config\sidebar.js

export const sidebarConfig = {

  parent: [

    {
      label: "Панель управления",
      path: "/dashboard",
      icon: "🏠",
    },

    {
      label: "Ученики",
      path: "/children",
      icon: "👨‍👩‍👧",
    },


    {
      label: "Задания",
      path: "/lessons",
      icon: "📚",
    },

    {
      label: "Тарифы и оплата",
      path: "/billing",
      icon: "💳",
    },

  ],

  child: [

    {
      label: "Мои задания",
      path: "/lessons",
      icon: "📚",
    },

    {
      label: "Мой прогресс",
      path: "/progress",
      icon: "📊",
    },

    {
      label: "Мои достижения",
      path: "/achievements",
      icon: "🏆",
    },

    {
      label: "Ежедневные цели",
      path: "/goals",
      icon: "🎯",
    },
  ],

  teacher: [

    {
      label: "Панель управлени",
      path: "/dashboard",
      icon: "🏠",
    },

    {
      label: "Ученики",
      path: "/students",
      icon: "👨‍🎓",
    },

    {
      label: "Группы",
      path: "/groups",
      icon: "👥",
    },
  ],

  admin: [

    {
      label: "Панель управления",
      path: "/dashboard",
      icon: "🏠",
    },

    {
      label: "Пользователи",
      path: "/users",
      icon: "👤",
    },

    {
      label: "Аналитика",
      path: "/analytics",
      icon: "📈",
    },
  ],
}