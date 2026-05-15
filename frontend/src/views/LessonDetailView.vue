<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\LessonDetailView.vue -->

<template>
  <AppLayout>

    <div v-if="lesson" class="max-w-4xl mx-auto space-y-6">

      <!-- HEADER -->
      <div class="bg-white border rounded-2xl p-8">

        <div class="flex items-center justify-between">

          <div>

            <!-- EDIT MODE -->
            <div v-if="editMode" class="space-y-3">

              <input
                v-model="form.title"
                class="w-full border rounded-xl px-4 py-3"
              />

              <textarea
                v-model="form.content"
                rows="6"
                class="w-full border rounded-xl px-4 py-3"
              />

            </div>

            <!-- VIEW MODE -->
            <div v-else>

              <h1 class="text-3xl font-bold">
                {{ lesson.title }}
              </h1>

              <p class="text-slate-500 mt-2">
                {{ lesson.child_name || "Child" }}
              </p>

            </div>

          </div>

          <!-- STATUS -->
          <div
            class="px-4 py-2 rounded-full text-sm font-medium"
            :class="statusClass"
          >
            {{ formatStatus(lesson.status) }}
          </div>

        </div>

      </div>

      <!-- CONTENT -->
      <div class="bg-white border rounded-2xl p-8">

        <h2 class="text-xl font-semibold mb-6">
          Lesson content
        </h2>

        <div
          v-if="!editMode"
          class="whitespace-pre-line text-slate-700"
        >
          {{ lesson.content }}
        </div>

      </div>

      <!-- PARENT ACTIONS -->
      <div
        v-if="authStore.user?.role === 'parent'"
        class="flex gap-3 flex-wrap"
      >

        <!-- EDIT -->
        <button
          class="
            bg-blue-600
            hover:bg-blue-700
            text-white
            px-5
            py-2
            rounded-xl
            transition
          "
          @click="toggleEdit"
        >
          {{ editMode ? "Cancel" : "Edit" }}
        </button>

        <!-- SAVE -->
        <button
          v-if="editMode"
          class="
            bg-green-600
            hover:bg-green-700
            text-white
            px-5
            py-2
            rounded-xl
            transition
          "
          @click="saveLesson"
        >
          Save
        </button>

        <!-- DELETE -->
        <button
          class="
            bg-red-600
            hover:bg-red-700
            text-white
            px-5
            py-2
            rounded-xl
            transition
          "
          @click="removeLesson"
        >
          Delete
        </button>

        <!-- COMPLETE -->
        <button
          v-if="lesson.status !== 'completed'"
          class="
            bg-emerald-600
            hover:bg-emerald-700
            text-white
            px-5
            py-2
            rounded-xl
            transition
          "
          @click="completeLesson"
        >
          Complete
        </button>

      </div>

      <!-- CHILD ACTIONS -->
      <div
        v-if="authStore.user?.role === 'child'"
        class="flex gap-3"
      >

        <button
          v-if="lesson.status !== 'completed'"
          class="
            bg-emerald-600
            hover:bg-emerald-700
            text-white
            px-6
            py-3
            rounded-xl
            transition
          "
          @click="completeLesson"
        >
          Mark as completed
        </button>

        <div
          v-else
          class="
            px-5
            py-3
            rounded-xl
            bg-green-100
            text-green-700
            font-medium
          "
        >
          Lesson completed 🎉
        </div>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRoute, useRouter } from "vue-router"

import AppLayout from "@/layouts/AppLayout.vue"

import { useLessonsStore } from "@/stores/lessons"
import { useAuthStore } from "@/stores/auth"

const route = useRoute()
const router = useRouter()

const lessonsStore = useLessonsStore()
const authStore = useAuthStore()

const lesson = ref(null)

const editMode = ref(false)

const form = ref({
  title: "",
  content: "",
})

/* LOAD */
onMounted(async () => {

  lesson.value = await lessonsStore.fetchLesson(
    route.params.id
  )

  form.value = {
    title: lesson.value.title,
    content: lesson.value.content,
  }
})

/* TOGGLE EDIT */
const toggleEdit = () => {

  editMode.value = !editMode.value

  if (!editMode.value) {

    form.value.title = lesson.value.title
    form.value.content = lesson.value.content
  }
}

/* SAVE */
const saveLesson = async () => {

  const updated = await lessonsStore.updateLesson(
    lesson.value.id,
    {
      title: form.value.title,
      content: form.value.content,
    }
  )

  lesson.value = updated

  editMode.value = false
}

/* DELETE */
const removeLesson = async () => {

  const confirmed = confirm(
    "Delete this lesson?"
  )

  if (!confirmed) return

  await lessonsStore.deleteLesson(
    lesson.value.id
  )

  router.push("/lessons")
}

/* COMPLETE */
const completeLesson = async () => {

  const updated = await lessonsStore.updateLesson(
    lesson.value.id,
    {
      status: "completed",
      progress: 100,
    }
  )

  lesson.value = updated
}

/* FORMAT STATUS */
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

/* STATUS STYLE */
const statusClass = computed(() => {

  if (!lesson.value) return ""

  switch (lesson.value.status) {

    case "completed":
      return "bg-green-100 text-green-700"

    case "in_progress":
      return "bg-blue-100 text-blue-700"

    default:
      return "bg-slate-100 text-slate-700"
  }
})
</script>