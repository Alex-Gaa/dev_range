<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ChildDashboard.vue -->
<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ChildDashboard.vue -->

<template>

  <div>

    <!-- HEADER -->

    <div class="mb-8">

      <h1 class="text-3xl font-bold">
        Welcome back,
        {{ authStore.user?.first_name }} 🚀
      </h1>

      <p class="text-slate-500 mt-2">
        Ready to continue learning today?
      </p>

    </div>

    <!-- HERO -->

    <div
      v-if="continueLesson"
      class="
        bg-gradient-to-r
        from-blue-600
        to-indigo-600
        rounded-3xl
        p-8
        text-white
        mb-8
      "
    >

      <p class="uppercase text-sm opacity-80">
        Continue learning
      </p>

      <h2 class="text-3xl font-bold mt-3">
        {{ continueLesson.title }}
      </h2>

      <p class="mt-4 opacity-90">
        You are doing amazing. Keep going 🚀
      </p>

      <div class="mt-6">

        <div class="flex justify-between mb-2 text-sm">

          <span>
            Progress
          </span>

          <span>
            {{ continueLesson.progress }}%
          </span>

        </div>

        <div
          class="
            w-full
            h-3
            bg-white/20
            rounded-full
            overflow-hidden
          "
        >

          <div
            class="
              h-full
              bg-white
              rounded-full
            "
            :style="{
              width: `${continueLesson.progress}%`
            }"
          />

        </div>

      </div>

      <button
        @click="openContinueLesson"
        class="
          mt-8
          bg-white
          text-blue-600
          px-6
          py-3
          rounded-xl
          font-semibold
          hover:bg-slate-100
          transition
        "
      >
        Continue Lesson
      </button>

    </div>

    <!-- QUICK STATS -->

    <div
      class="
        grid
        grid-cols-1
        md:grid-cols-2
        xl:grid-cols-3
        gap-6
      "
    >

      <!-- DAILY GOAL -->

      <BaseCard>

        <div class="flex items-center justify-between">

          <div>

            <p class="text-slate-500">
              Daily Goal
            </p>

            <h3 class="text-4xl font-bold mt-2 text-green-600">
              {{ completedLessons }} / {{ dailyGoal }}
            </h3>

          </div>

          <div class="text-5xl">
            🎯
          </div>

        </div>

        <div class="mt-6">

          <div
            class="
              w-full
              h-3
              bg-slate-100
              rounded-full
              overflow-hidden
            "
          >

            <div
              class="
                h-full
                bg-green-600
                rounded-full
              "
              :style="{
                width: `${goalPercent}%`
              }"
            />

          </div>

        </div>

      </BaseCard>

      <!-- STREAK -->

      <BaseCard>

        <div class="flex items-center justify-between">

          <div>

            <p class="text-slate-500">
              Learning Streak
            </p>

            <h3 class="text-5xl font-bold mt-2 text-orange-500">
              🔥 {{ streak }}
            </h3>

          </div>

          <div class="text-5xl">
            🏆
          </div>

        </div>

        <p class="text-slate-500 mt-4">
          Keep learning every day!
        </p>

      </BaseCard>

      <!-- ACHIEVEMENTS -->

      <BaseCard>

        <div class="flex items-center justify-between">

          <div>

            <p class="text-slate-500">
              Latest Achievement
            </p>

            <h3 class="text-2xl font-bold mt-2">
              First Steps
            </h3>

          </div>

          <div class="text-5xl">
            ⭐
          </div>

        </div>

        <p class="text-slate-500 mt-4">
          Completed your first lesson
        </p>

      </BaseCard>

    </div>

    <!-- RECENT LESSONS -->

    <div class="mt-10">

      <div class="flex items-center justify-between mb-6">

        <h2 class="text-2xl font-bold">
          Recent Lessons
        </h2>

        <button
          @click="goToLessons"
          class="
            text-blue-600
            hover:text-blue-700
            font-medium
          "
        >
          View all
        </button>

      </div>

      <div
        v-if="recentLessons.length"
        class="space-y-4"
      >

        <div
          v-for="lesson in recentLessons"
          :key="lesson.id"
          class="
            bg-white
            border
            rounded-2xl
            p-6
            cursor-pointer
            transition-all
            hover:shadow-lg
          "
          @click="openLesson(lesson.id)"
        >

          <div class="flex items-start justify-between">

            <div>

              <h3 class="font-semibold text-lg">
                {{ lesson.title }}
              </h3>

              <p class="text-slate-500 mt-2">
                {{ lesson.content.slice(0, 100) }}...
              </p>

            </div>

            <div
              class="
                px-3
                py-1
                rounded-full
                text-sm
                font-medium
              "
              :class="
                lesson.status === 'completed'
                  ? 'bg-green-100 text-green-700'
                  : 'bg-blue-100 text-blue-700'
              "
            >

              {{ formatStatus(lesson.status) }}

            </div>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>

<script setup>
import {
  computed,
  onMounted,
} from "vue"

import { useRouter } from "vue-router"

import BaseCard from "@/components/ui/BaseCard.vue"

import { useAuthStore } from "@/stores/auth"
import { useLessonsStore } from "@/stores/lessons"

const router = useRouter()

const authStore = useAuthStore()
const lessonsStore = useLessonsStore()

onMounted(async () => {
  await lessonsStore.fetchAllLessons()
})

const dailyGoal = 3
const streak = 5

const completedLessons = computed(() => {

  return lessonsStore.lessons.filter(
    l => l.status === "completed"
  ).length
})

const goalPercent = computed(() => {

  return Math.min(
    Math.round(
      (completedLessons.value / dailyGoal) * 100
    ),
    100
  )
})

const continueLesson = computed(() => {

  return lessonsStore.lessons.find(
    lesson => lesson.status !== "completed"
  )
})

const recentLessons = computed(() => {

  return lessonsStore.lessons.slice(0, 3)
})

const openLesson = (id) => {
  router.push(`/lessons/${id}`)
}

const openContinueLesson = () => {

  if (!continueLesson.value) return

  router.push(
    `/lessons/${continueLesson.value.id}`
  )
}

const goToLessons = () => {
  router.push("/lessons")
}

const formatStatus = (status) => {

  switch (status) {

    case "completed":
      return "Completed"

    case "in_progress":
      return "In Progress"

    default:
      return "Draft"
  }
}
</script>