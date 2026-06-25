<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ParentDashboard.vue -->
<template>

  <div>

    <div class="mb-8">

      <h1 class="text-2xl md:text-3xl font-bold">
        Добро пожаловать,
        {{ authStore.user?.first_name }}
      </h1>

      <p class="text-slate-500 mt-2">
        Обзор вашей образовательной платформы
      </p>

    </div>

    <!-- STATS -->

    <div class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">

      <!-- CHILDREN -->

      <BaseCard
        class="
          cursor-pointer
          transition-all
          hover:shadow-lg
          hover:-translate-y-1
        "
        @click="goToChildren"
      >

        <h3 class="text-lg font-semibold">
          Ученики
        </h3>

        <p class="text-4xl mt-4 font-bold text-blue-600">
          {{ childrenCount }}
        </p>

        <p class="text-slate-500 mt-2">
          Активных профилей учеников
        </p>

      </BaseCard>

      <!-- LESSONS -->

      <BaseCard
        class="
          cursor-pointer
          transition-all
          hover:shadow-lg
          hover:-translate-y-1
        "
        @click="goToLessons"
      >

        <h3 class="text-lg font-semibold">
          Задания
        </h3>

        <p class="text-4xl mt-4 font-bold text-green-600">
          {{ completedLessons }} / {{ totalLessons }}
        </p>

        <p class="text-slate-500 mt-2">
          Завершено / Всего уроков
        </p>

      </BaseCard>

<!--
<BaseCard
  class="
    cursor-pointer
    transition-all
    hover:shadow-lg
    hover:-translate-y-1
  "
  @click="goToBilling"
>

  <h3 class="text-lg font-semibold">
    Лимит ИИ
  </h3>

  <p class="text-4xl mt-4 font-bold text-purple-600">
    1200
  </p>

  <p class="text-slate-500 mt-2">
    Remaining monthly balance
  </p>

</BaseCard>
-->

    </div>

    <!-- RECENT CHILDREN -->

    <div class="mt-10">

      <h2 class="text-2xl font-bold mb-6">
        Мои ученики
      </h2>

      <div
        v-if="childrenStore.children.length"
        class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6"
      >

        <div
          v-for="child in recentChildren"
          :key="child.id"
          class="
            bg-white
            rounded-2xl
            border
            p-6
            cursor-pointer
            transition-all
            hover:shadow-lg
            hover:-translate-y-1
          "
          @click="openChild(child.id)"
        >

          <div class="flex items-center justify-between">

            <div>

              <h3 class="font-semibold text-lg">
                {{ child.first_name }}
              </h3>

              <p class="text-slate-500">
                {{ formatAge(child.age) }}
              </p>

            </div>

            <div
              class="
                w-12
                h-12
                rounded-full
                bg-blue-600
                text-white
                flex
                items-center
                justify-center
                font-bold
              "
            >
              {{ child.first_name.charAt(0) }}
            </div>

          </div>

        </div>

      </div>

      <div
          v-else
          class="bg-white border rounded-2xl p-6 md:p-10 text-center"
        >

        <h3 class="text-xl font-semibold">
          Пока нет учеников
        </h3>

        <p class="text-slate-500 mt-2">
          Создайте профиль ученика, чтобы начать обучение
        </p>

      </div>

    </div>

  </div>

</template>

<script setup>
import { computed, onMounted } from "vue"
import { useRouter } from "vue-router"

import BaseCard from "@/components/ui/BaseCard.vue"

import { useAuthStore } from "@/stores/auth"
import { useChildrenStore } from "@/stores/children"
import { useLessonsStore } from "@/stores/lessons"

const router = useRouter()

const authStore = useAuthStore()
const childrenStore = useChildrenStore()
const lessonsStore = useLessonsStore()

onMounted(() => {
  childrenStore.fetchChildren()
  lessonsStore.fetchAllLessons()
})

const childrenCount = computed(() => {
  return childrenStore.children.length
})

const recentChildren = computed(() => {
  return childrenStore.children.slice(0, 3)
})

const totalLessons = computed(() => {
  return lessonsStore.lessons.length
})

const completedLessons = computed(() => {
  return lessonsStore.lessons.filter(
    l => l.status === "completed"
  ).length
})

const goToChildren = () => {
  router.push("/children")
}

const goToLessons = () => {
  router.push("/lessons")
}

const goToBilling = () => {
  router.push("/billing")
}

const openChild = (id) => {
  router.push(`/children/${id}`)
}

const formatAge = (age) => {

  if (age % 100 >= 11 && age % 100 <= 14) {
    return `${age} лет`
  }

  switch (age % 10) {

    case 1:
      return `${age} год`

    case 2:
    case 3:
    case 4:
      return `${age} года`

    default:
      return `${age} лет`
  }
}

</script>