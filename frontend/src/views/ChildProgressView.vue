<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ChildProgressView.vue -->

<template>
  <AppLayout>

    <div class="space-y-8">

      <!-- HEADER -->

      <div>

        <h1 class="text-3xl font-bold">
          Learning Analytics 📊
        </h1>

        <p class="text-slate-500 mt-2">
          Track your performance and consistency
        </p>

      </div>

      <!-- ANALYTICS -->

      <div
        class="
          grid
          grid-cols-1
          md:grid-cols-2
          xl:grid-cols-4
          gap-6
        "
      >

        <div class="bg-white border rounded-2xl p-6">

          <p class="text-slate-500">
            Total Lessons
          </p>

          <h2 class="text-4xl font-bold mt-3 text-blue-600">
            {{ totalLessons }}
          </h2>

        </div>

        <div class="bg-white border rounded-2xl p-6">

          <p class="text-slate-500">
            Completed
          </p>

          <h2 class="text-4xl font-bold mt-3 text-green-600">
            {{ completedLessons }}
          </h2>

        </div>

        <div class="bg-white border rounded-2xl p-6">

          <p class="text-slate-500">
            In Progress
          </p>

          <h2 class="text-4xl font-bold mt-3 text-orange-500">
            {{ inProgressLessons }}
          </h2>

        </div>

        <div class="bg-white border rounded-2xl p-6">

          <p class="text-slate-500">
            Completion Rate
          </p>

          <h2 class="text-4xl font-bold mt-3 text-purple-600">
            {{ completionRate }}%
          </h2>

        </div>

      </div>

      <!-- PROGRESS -->

      <div class="bg-white border rounded-2xl p-6">

        <div class="flex justify-between mb-3">

          <span class="font-medium">
            Overall Completion
          </span>

          <span class="text-slate-500">
            {{ completionRate }}%
          </span>

        </div>

        <div
          class="
            w-full
            h-4
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
            "
            :style="{
              width: `${completionRate}%`
            }"
          />

        </div>

      </div>

      <!-- RECENT ACTIVITY -->

      <div class="bg-white border rounded-2xl p-6">

        <h2 class="text-xl font-semibold mb-5">
          Recent Activity
        </h2>

        <div class="space-y-4">

          <div
            v-for="lesson in recentLessons"
            :key="lesson.id"
            class="
              border
              rounded-xl
              p-4
              flex
              items-center
              justify-between
            "
          >

            <div>

              <h3 class="font-semibold">
                {{ lesson.title }}
              </h3>

              <p class="text-sm text-slate-500 mt-1">
                {{ formatStatus(lesson.status) }}
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
              :class="statusClass(lesson.status)"
            >

              {{ lesson.progress }}%

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

const totalLessons = computed(() => {
  return lessonsStore.lessons.length
})

const completedLessons = computed(() => {

  return lessonsStore.lessons.filter(
    l => l.status === "completed"
  ).length
})

const inProgressLessons = computed(() => {

  return lessonsStore.lessons.filter(
    l => l.status === "in_progress"
  ).length
})

const completionRate = computed(() => {

  if (!totalLessons.value) {
    return 0
  }

  return Math.round(
    (completedLessons.value / totalLessons.value) * 100
  )
})

const recentLessons = computed(() => {

  return lessonsStore.lessons.slice(0, 8)
})

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

const statusClass = (status) => {

  switch (status) {

    case "completed":
      return "bg-green-100 text-green-700"

    case "in_progress":
      return "bg-blue-100 text-blue-700"

    default:
      return "bg-slate-100 text-slate-700"
  }
}
</script>