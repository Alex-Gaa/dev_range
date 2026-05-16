<template>

  <div>

    <!-- HEADER -->

    <div class="mb-8">

      <h1 class="text-3xl font-bold">
        Welcome back,
        {{ authStore.user?.first_name }}
      </h1>

      <p class="text-slate-500 mt-2">
        Continue your learning journey 🚀
      </p>

    </div>

    <!-- STATS -->

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

      <!-- TOTAL LESSONS -->

      <BaseCard>

        <h3 class="text-lg font-semibold">
          My Lessons
        </h3>

        <p class="text-4xl mt-4 font-bold text-blue-600">
          {{ totalLessons }}
        </p>

      </BaseCard>

      <!-- COMPLETED -->

      <BaseCard>

        <h3 class="text-lg font-semibold">
          Completed
        </h3>

        <p class="text-4xl mt-4 font-bold text-green-600">
          {{ completedLessons }}
        </p>

      </BaseCard>

      <!-- PROGRESS -->

      <BaseCard>

        <h3 class="text-lg font-semibold">
          Progress
        </h3>

        <p class="text-4xl mt-4 font-bold text-purple-600">
          {{ progressPercent }}%
        </p>

      </BaseCard>

    </div>

    <!-- RECENT LESSONS -->

    <div class="mt-10">

      <h2 class="text-2xl font-bold mb-6">
        Recent lessons
      </h2>

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

          <div class="flex items-center justify-between">

            <div>

              <h3 class="font-semibold text-lg">
                {{ lesson.title }}
              </h3>

              <p class="text-slate-500 mt-2">
                {{ lesson.content.slice(0, 100) }}...
              </p>

            </div>

            <div
              class="px-3 py-1 rounded-full text-sm font-medium"
              :class="
                lesson.status === 'completed'
                  ? 'bg-green-100 text-green-700'
                  : 'bg-blue-100 text-blue-700'
              "
            >
              {{ lesson.status }}
            </div>

          </div>

        </div>

      </div>

    </div>

  </div>

</template>

<script setup>
import { computed, onMounted } from "vue"
import { useRouter } from "vue-router"

import BaseCard from "@/components/ui/BaseCard.vue"

import { useAuthStore } from "@/stores/auth"
import { useLessonsStore } from "@/stores/lessons"

const router = useRouter()

const authStore = useAuthStore()
const lessonsStore = useLessonsStore()

onMounted(() => {
  lessonsStore.fetchAllLessons()
})

const totalLessons = computed(() => {
  return lessonsStore.lessons.length
})

const completedLessons = computed(() => {
  return lessonsStore.lessons.filter(
    l => l.status === "completed"
  ).length
})

const progressPercent = computed(() => {

  if (!lessonsStore.lessons.length) return 0

  const total = lessonsStore.lessons.reduce(
    (sum, lesson) => sum + lesson.progress,
    0
  )

  return Math.round(
    total / lessonsStore.lessons.length
  )
})

const recentLessons = computed(() => {
  return lessonsStore.lessons.slice(0, 5)
})

const openLesson = (id) => {
  router.push(`/lessons/${id}`)
}
</script>