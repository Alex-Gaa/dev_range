<!-- LessonDetailView.vue -->
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

                <!-- SUBJECT / TOPIC -->
                <div class="flex gap-2 mt-4 flex-wrap">

                  <span
                    v-if="lesson.subject_name"
                    class="
                      bg-slate-100
                      text-slate-700
                      px-3
                      py-1
                      rounded-full
                      text-sm
                    "
                  >
                    {{ lesson.subject_name }}
                  </span>

                  <span
                    v-if="lesson.topic_name"
                    class="
                      bg-blue-100
                      text-blue-700
                      px-3
                      py-1
                      rounded-full
                      text-sm
                    "
                  >
                    {{ lesson.topic_name }}
                  </span>

                </div>

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
          {{ t.content }}
        </h2>

        <!-- TEXT LESSON -->
        <div
          v-if="!parsedContent"
          class="whitespace-pre-line text-slate-700"
        >
          {{ lesson.content }}
        </div>

        <!-- AI JSON LESSON -->
        <div v-else class="space-y-8">

          <!-- INTRO -->
          <div>
            <h3 class="text-2xl font-bold mb-3">
              {{ parsedContent.title }}
            </h3>

            <p class="text-slate-700 leading-8">
              {{ parsedContent.introduction }}
            </p>
          </div>

          <!-- THEORY -->
          <div>
            <h4 class="text-xl font-semibold mb-3">
              {{ t.theory }}
            </h4>

            <p class="text-slate-700 leading-8">
              {{ parsedContent.theory }}
            </p>
          </div>

          <!-- EXAMPLES -->
          <div v-if="parsedContent.examples?.length">

            <h4 class="text-xl font-semibold mb-4">
              {{ t.examples }}
            </h4>

            <div class="space-y-4">

              <div
                v-for="(example, index) in parsedContent.examples"
                :key="index"
                class="border rounded-2xl p-5 bg-slate-50"
              >

                <p class="font-medium">
                  {{ example.question }}
                </p>

                <p class="text-green-700 mt-3">
                  {{ example.answer }}
                </p>

              </div>

            </div>

          </div>

          <!-- ACTIVITY -->
          <div
            v-if="parsedContent.activity"
            class="bg-blue-50 border border-blue-100 rounded-2xl p-6"
          >

            <h4 class="text-xl font-semibold mb-3">
              {{ t.activity }}
            </h4>

            <p class="text-slate-700">
              {{ parsedContent.activity }}
            </p>

          </div>

          <!-- QUIZ -->
          <div v-if="parsedContent.quiz?.length">

            <h4 class="text-xl font-semibold mb-4">
              {{ t.quiz }}
            </h4>

            <div class="space-y-5">

              <div
                v-for="(quiz, index) in parsedContent.quiz"
                :key="index"
                class="border rounded-2xl p-5"
              >

                <p class="font-semibold mb-4">
                  {{ quiz.question }}
                </p>

                <div class="space-y-2">

                  <div
                    v-for="(option, optionIndex) in quiz.options"
                    :key="optionIndex"
                    class="bg-slate-50 rounded-xl px-4 py-3"
                  >
                    {{ option }}
                  </div>

                </div>

              </div>

            </div>

          </div>

          <!-- SUMMARY -->
          <div
            v-if="parsedContent.summary"
            class="bg-green-50 border border-green-100 rounded-2xl p-6"
          >

            <h4 class="text-xl font-semibold mb-3">
              {{ t.summary }}
            </h4>

            <p class="text-slate-700">
              {{ parsedContent.summary }}
            </p>

          </div>

        </div>

      </div>

      <!-- PARENT ACTIONS -->
      <div
        v-if="authStore.user?.role === 'parent'"
        class="flex gap-3 flex-wrap"
      >

        <button
          class="bg-blue-600 hover:bg-blue-700 text-white px-5 py-2 rounded-xl"
          @click="toggleEdit"
        >
          {{ editMode ? "Cancel" : "Edit" }}
        </button>

        <button
          v-if="editMode"
          class="bg-green-600 hover:bg-green-700 text-white px-5 py-2 rounded-xl"
          @click="saveLesson"
        >
          {{ t.save }}
        </button>

        <button
          class="bg-red-600 hover:bg-red-700 text-white px-5 py-2 rounded-xl"
          @click="removeLesson"
        >
          {{ t.delete }}
        </button>

        <button
          v-if="lesson.status !== 'completed'"
          class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2 rounded-xl"
          @click="completeLesson"
        >
          {{ t.complete }}
        </button>

      </div>

      <!-- CHILD ACTIONS -->
      <div
        v-if="authStore.user?.role === 'child'"
        class="flex gap-3"
      >

        <button
          v-if="lesson.status !== 'completed'"
          class="bg-emerald-600 hover:bg-emerald-700 text-white px-6 py-3 rounded-xl"
          @click="completeLesson"
        >
          {{ t.markCompleted }}
        </button>

        <div
          v-else
          class="px-5 py-3 rounded-xl bg-green-100 text-green-700 font-medium"
        >
          {{ t.completed }}
        </div>

      </div>

    </div>
    <ConfirmModal
      :show="showDeleteModal"
      title="Delete Lesson"
      message="Are you sure you want to delete this lesson?"
      @cancel="showDeleteModal = false"
      @confirm="confirmDeleteLesson"
    />

  </AppLayout>
</template>

<script setup>
import ConfirmModal from "@/components/common/ConfirmModal.vue"
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
const showDeleteModal = ref(false)

const errorMessage = ref("")
const successMessage = ref("")


/* LOAD */
onMounted(async () => {

  lesson.value = await lessonsStore.fetchLesson(
    route.params.id
  )

  form.value = {
    title: lesson.value.title,
    content:
      typeof lesson.value.content === "object"
        ? JSON.stringify(lesson.value.content, null, 2)
        : lesson.value.content,
  }
})

/* PARSE AI CONTENT */
const parsedContent = computed(() => {

  if (!lesson.value?.content) return null

  if (typeof lesson.value.content === "object") {
    return lesson.value.content
  }

  try {
    return JSON.parse(lesson.value.content)
  } catch {
    return null
  }
})

/* TOGGLE EDIT */
const toggleEdit = () => {

  editMode.value = !editMode.value

  if (!editMode.value) {

    form.value.title = lesson.value.title

    form.value.content =
      typeof lesson.value.content === "object"
        ? JSON.stringify(lesson.value.content, null, 2)
        : lesson.value.content
  }
}

/* SAVE */
const saveLesson = async () => {

  let parsed = form.value.content

  try {
    parsed = JSON.parse(form.value.content)
  } catch {
    // leave as string
  }

  const updated = await lessonsStore.updateLesson(
    lesson.value.id,
    {
      title: form.value.title,
      content: parsed,
    }
  )

  lesson.value = updated
  editMode.value = false
}

/* DELETE */
const removeLesson = () => {

  showDeleteModal.value = true
}
/*Confirm delete*/
const confirmDeleteLesson = async () => {

  errorMessage.value = ""

  try {

    await lessonsStore.deleteLesson(
      lesson.value.id
    )

    successMessage.value =
      "Lesson deleted successfully"

    router.push("/lessons")

  } catch (e) {

    errorMessage.value =
      e.response?.data?.detail ||
      "Failed to delete lesson"

  } finally {

    showDeleteModal.value = false
  }
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

/* STATUS */
const formatStatus = (status) => {
  switch (status) {
    case "completed": return t.status.completed
    case "in_progress": return t.status.in_progress
    default: return t.status.draft
  }

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
const t = {
  content: "Lesson content",
  theory: "Theory",
  examples: "Examples",
  activity: "Activity 🚀",
  quiz: "Quiz 🧠",
  summary: "Summary 🎉",

  cancel: "Cancel",
  edit: "Edit",
  save: "Save",
  delete: "Delete",
  complete: "Complete",
  markCompleted: "Mark as completed",
  completed: "Lesson completed 🎉",

  status: {
    draft: "Draft",
    in_progress: "In progress",
    completed: "Completed",
  }
}


</script>