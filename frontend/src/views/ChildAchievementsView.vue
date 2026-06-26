<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ChildAchievementsView.vue -->

<template>
  <AppLayout>

    <div class="space-y-8">

      <!-- HEADER -->

      <div>

        <h1 class="text-3xl font-bold">
          Достижения 🏆
        </h1>

        <p class="text-slate-500 mt-2">
          Получайте награды за регулярное обучение
        </p>

      </div>

      <!-- OVERVIEW -->

      <div
        class="
          grid
          grid-cols-1
          md:grid-cols-3
          gap-6
        "
      >

        <!-- TOTAL -->

        <div class="bg-white border rounded-2xl p-6">

          <p class="text-slate-500">
            Всего достижений
          </p>

          <h2 class="text-4xl font-bold mt-3 text-blue-600">
            {{ achievements.length }}
          </h2>

        </div>

        <!-- UNLOCKED -->

        <div class="bg-white border rounded-2xl p-6">

          <p class="text-slate-500">
            Получено
          </p>

          <h2 class="text-4xl font-bold mt-3 text-green-600">
            {{ unlockedAchievements.length }}
          </h2>

        </div>

        <!-- XP -->

        <div class="bg-white border rounded-2xl p-6">

          <p class="text-slate-500">
            Всего опыта
          </p>

          <h2 class="text-4xl font-bold mt-3 text-purple-600">
            {{ totalXP }}
          </h2>

        </div>

      </div>

      <!-- ACHIEVEMENTS GRID -->

      <div
        class="
          grid
          grid-cols-1
          md:grid-cols-2
          xl:grid-cols-3
          gap-6
        "
      >

        <div
          v-for="achievement in achievements"
          :key="achievement.title"
          class="
            rounded-2xl
            border
            p-6
            transition-all
            hover:shadow-lg
          "
          :class="
            achievement.unlocked
              ? 'bg-white'
              : 'bg-slate-100 opacity-70'
          "
        >

          <!-- ICON -->

          <div class="text-5xl mb-5">
            {{ achievement.icon }}
          </div>

          <!-- TITLE -->

          <h2 class="text-xl font-bold">
            {{ achievement.title }}
          </h2>

          <!-- DESCRIPTION -->

          <p class="text-slate-500 mt-2">
            {{ achievement.description }}
          </p>

          <!-- PROGRESS -->

          <div class="mt-6">

            <div
              class="
                flex
                justify-between
                text-sm
                mb-2
              "
            >

              <span class="text-slate-500">
                Прогресс
              </span>

              <span class="font-medium">
                {{ achievement.progress }}
                /
                {{ achievement.goal }}
              </span>

            </div>

            <div
              class="
                w-full
                h-3
                bg-slate-200
                rounded-full
                overflow-hidden
              "
            >

              <div
                class="
                  h-full
                  rounded-full
                  transition-all
                "
                :class="
                  achievement.unlocked
                    ? 'bg-green-500'
                    : 'bg-blue-500'
                "
                :style="{
                  width: `${achievementPercent(achievement)}%`
                }"
              />

            </div>

          </div>

          <!-- FOOTER -->

          <div class="mt-6 flex items-center justify-between">

            <div
              class="
                text-sm
                font-medium
                px-3
                py-1
                rounded-full
              "
              :class="
                achievement.unlocked
                  ? 'bg-green-100 text-green-700'
                  : 'bg-slate-200 text-slate-600'
              "
            >

              {{
                achievement.unlocked
                  ? 'Получено'
                  : 'Заблокировано'
              }}

            </div>

            <div class="font-bold text-purple-600">
              +{{ achievement.xp }} XP
            </div>

          </div>

        </div>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import {
  computed,
  onMounted,
} from "vue"

import AppLayout from "@/layouts/AppLayout.vue"

import { useLessonsStore } from "@/stores/lessons"

const lessonsStore = useLessonsStore()

onMounted(async () => {
  await lessonsStore.fetchAllLessons()
})

/* LESSON STATS */

const completedLessons = computed(() => {

  return lessonsStore.lessons.filter(
    l => l.status === "completed"
  ).length
})

/* MOCK STREAK */

const streak = 5

/* ACHIEVEMENTS */

const achievements = computed(() => [

  {
    icon: "🚀",
    title: "Первое задание",
    description: "Завершите свое первое задание",
    progress: completedLessons.value,
    goal: 1,
    unlocked: completedLessons.value >= 1,
    xp: 50,
  },

  {
    icon: "📚",
    title: "Начинающий ученик",
    description: "Завершите 3 задания",
    progress: completedLessons.value,
    goal: 3,
    unlocked: completedLessons.value >= 3,
    xp: 100,
  },

  {
    icon: "🏆",
    title: "Мастер учебы",
    description: "Завершите 10 заданий",
    progress: completedLessons.value,
    goal: 10,
    unlocked: completedLessons.value >= 10,
    xp: 300,
  },

  {
    icon: "🔥",
    title: "Серия 3 дня",
    description: "Занимайтесь 3 дня подряд",
    progress: streak,
    goal: 3,
    unlocked: streak >= 3,
    xp: 120,
  },

  {
    icon: "⚡",
    title: "Серия 7 дней",
    description: "Занимайтесь 7 дней подряд",
    progress: streak,
    goal: 7,
    unlocked: streak >= 7,
    xp: 250,
  },

  {
    icon: "🎯",
    title: "На полпути",
    description: "Достигните 50% общего прогресса",
    progress: completedLessons.value,
    goal: 5,
    unlocked: completedLessons.value >= 5,
    xp: 200,
  },

])

/* UNLOCKED */

const unlockedAchievements = computed(() => {

  return achievements.value.filter(
    a => a.unlocked
  )
})

/* XP */

const totalXP = computed(() => {

  return unlockedAchievements.value.reduce(
    (sum, achievement) => sum + achievement.xp,
    0
  )
})

/* PROGRESS */

const achievementPercent = (achievement) => {

  return Math.min(
    Math.round(
      (achievement.progress / achievement.goal) * 100
    ),
    100
  )
}
</script>