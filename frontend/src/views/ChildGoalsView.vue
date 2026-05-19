<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ChildGoalsView.vue -->

<template>
  <AppLayout>

    <div class="space-y-8">

      <!-- HEADER -->

      <div>

        <h1 class="text-3xl font-bold">
          Daily Goals 🎯
        </h1>

        <p class="text-slate-500 mt-2">
          Complete lessons every day and build your learning streak
        </p>

      </div>

      <!-- GOAL CARD -->

      <div class="bg-white border rounded-2xl p-8">

        <div class="flex items-center justify-between mb-6">

          <div>

            <p class="text-slate-500">
              Today's Goal
            </p>

            <h2 class="text-5xl font-bold mt-2 text-blue-600">
              {{ completedToday }} / {{ dailyGoal }}
            </h2>

          </div>

          <div class="text-6xl">
            🎯
          </div>

        </div>

        <!-- PROGRESS BAR -->

        <div
          class="
            w-full
            h-5
            bg-slate-100
            rounded-full
            overflow-hidden
          "
        >

          <div
            class="
              h-full
              bg-blue-600
              rounded-full
              transition-all
            "
            :style="{
              width: `${goalPercent}%`
            }"
          />

        </div>

        <div class="mt-4 flex justify-between text-sm">

          <span class="text-slate-500">
            Daily completion progress
          </span>

          <span class="font-semibold">
            {{ goalPercent }}%
          </span>

        </div>

      </div>

      <!-- STREAK -->

      <div
        class="
          grid
          grid-cols-1
          md:grid-cols-2
          gap-6
        "
      >

        <!-- CURRENT STREAK -->

        <div class="bg-white border rounded-2xl p-6">

          <div class="flex items-center justify-between">

            <div>

              <p class="text-slate-500">
                Current Streak
              </p>

              <h2 class="text-5xl font-bold mt-3 text-orange-500">
                🔥 {{ currentStreak }}
              </h2>

            </div>

            <div class="text-5xl">
              📅
            </div>

          </div>

          <p class="text-slate-500 mt-5">
            Keep learning daily to increase your streak
          </p>

        </div>

        <!-- BEST STREAK -->

        <div class="bg-white border rounded-2xl p-6">

          <div class="flex items-center justify-between">

            <div>

              <p class="text-slate-500">
                Best Streak
              </p>

              <h2 class="text-5xl font-bold mt-3 text-green-600">
                🏆 {{ bestStreak }}
              </h2>

            </div>

            <div class="text-5xl">
              ⭐
            </div>

          </div>

          <p class="text-slate-500 mt-5">
            Your personal learning record
          </p>

        </div>

      </div>

      <!-- DAILY TASKS -->

      <div class="bg-white border rounded-2xl p-6">

        <h2 class="text-2xl font-bold mb-6">
          Today's Tasks
        </h2>

        <div class="space-y-4">

          <div
            v-for="task in tasks"
            :key="task.id"
            class="
              border
              rounded-2xl
              p-5
              flex
              items-center
              justify-between
            "
          >

            <div class="flex items-center gap-4">

              <div
                class="
                  w-12
                  h-12
                  rounded-full
                  flex
                  items-center
                  justify-center
                  text-2xl
                "
                :class="
                  task.completed
                    ? 'bg-green-100'
                    : 'bg-slate-100'
                "
              >

                {{ task.icon }}

              </div>

              <div>

                <h3 class="font-semibold text-lg">
                  {{ task.title }}
                </h3>

                <p class="text-slate-500 text-sm mt-1">
                  {{ task.description }}
                </p>

              </div>

            </div>

            <div
              class="
                px-4
                py-2
                rounded-full
                text-sm
                font-semibold
              "
              :class="
                task.completed
                  ? 'bg-green-100 text-green-700'
                  : 'bg-orange-100 text-orange-700'
              "
            >

              {{ task.completed ? "Completed" : "Pending" }}

            </div>

          </div>

        </div>

      </div>

      <!-- MOTIVATION -->

      <div
        class="
          bg-gradient-to-r
          from-blue-600
          to-indigo-600
          rounded-2xl
          p-8
          text-white
        "
      >

        <h2 class="text-2xl font-bold">
          Keep Going 🚀
        </h2>

        <p class="mt-3 text-blue-100">
          Small progress every day leads to big achievements.
        </p>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { computed, onMounted } from "vue"

import AppLayout from "@/layouts/AppLayout.vue"

import { useLessonsStore } from "@/stores/lessons"

const lessonsStore = useLessonsStore()

onMounted(async () => {
  await lessonsStore.fetchAllLessons()
})

/* GOAL SETTINGS */

const dailyGoal = 3

/* STREAKS */

const currentStreak = 5

const bestStreak = 12

/* LESSONS */

const completedToday = computed(() => {

  return lessonsStore.lessons.filter(
    lesson => lesson.status === "completed"
  ).length
})

const goalPercent = computed(() => {

  return Math.min(
    Math.round(
      (completedToday.value / dailyGoal) * 100
    ),
    100
  )
})

/* TASKS */

const tasks = computed(() => [

  {
    id: 1,
    title: "Complete 1 lesson",
    description: "Finish at least one lesson today",
    icon: "📚",
    completed: completedToday.value >= 1,
  },

  {
    id: 2,
    title: "Reach daily goal",
    description: `Complete ${dailyGoal} lessons`,
    icon: "🎯",
    completed: completedToday.value >= dailyGoal,
  },

  {
    id: 3,
    title: "Keep your streak",
    description: "Study every day without skipping",
    icon: "🔥",
    completed: currentStreak.value > 0,
  },
])
</script>