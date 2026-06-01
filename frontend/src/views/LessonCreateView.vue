<template>
  <AppLayout>

    <div class="max-w-4xl mx-auto">

      <!-- HEADER -->
      <div class="mb-8">

        <h1 class="text-3xl font-bold">
          Create Lesson
        </h1>

        <p class="text-slate-500 mt-2">
          Create lesson for any child
        </p>

      </div>

      <!-- FORM -->
      <div class="bg-white border rounded-2xl p-6">

        <!-- CHILD -->
        <div class="mb-4">

          <label class="block text-sm font-medium mb-2">
            Child
          </label>

          <select
            v-model="form.child"
            class="w-full border rounded-xl px-4 py-3"
          >
            <option value="">
              Select child
            </option>

            <option
              v-for="child in children"
              :key="child.id"
              :value="child.id"
            >
              {{ child.first_name }}
            </option>

          </select>

        </div>

        <!-- SUBJECT -->
        <div class="mb-4">

          <label class="block text-sm font-medium mb-2">
            Subject
          </label>

          <select
            v-model="form.subject"
            class="w-full border rounded-xl px-4 py-3"
          >
            <option value="">
              Select subject
            </option>

            <option
              v-for="subject in subjects"
              :key="subject.id"
              :value="subject.id"
            >
              {{ subject.name }}
            </option>

          </select>

        </div>

        <!-- TOPIC -->
        <div class="mb-4">

          <label class="block text-sm font-medium mb-2">
            Topic
          </label>

          <select
            v-model="form.topic"
            class="w-full border rounded-xl px-4 py-3"
          >
            <option value="">
              Select topic
            </option>

            <option
              v-for="topic in topics"
              :key="topic.id"
              :value="topic.id"
            >
              {{ topic.name }}
            </option>

          </select>

        </div>

        <!-- TITLE -->
        <div class="mb-4">

          <label class="block text-sm font-medium mb-2">
            Lesson Title
          </label>

          <input
            v-model="form.title"
            class="w-full border rounded-xl px-4 py-3"
            placeholder="Lesson title"
          />

        </div>

        <!-- CONTENT -->
        <div class="mb-6">

          <label class="block text-sm font-medium mb-2">
            Content
          </label>

          <textarea
            v-model="form.content"
            rows="10"
            class="w-full border rounded-xl px-4 py-3"
            placeholder="Write lesson content..."
          />

        </div>

        <!-- ERROR -->
        <div
          v-if="error"
          class="mb-4 bg-red-50 border border-red-200 text-red-600 rounded-xl p-4"
        >
          {{ error }}
        </div>

        <!-- ACTIONS -->
        <div class="flex gap-3">

          <button
            @click="saveLesson"
            :disabled="loading"
            class="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl disabled:opacity-50"
          >
            {{ loading ? "Saving..." : "Create Lesson" }}
          </button>

          <button
            @click="router.push('/lessons')"
            class="border px-6 py-3 rounded-xl"
          >
            Cancel
          </button>

        </div>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { ref, onMounted, watch } from "vue"
import { useRouter } from "vue-router"

import AppLayout from "@/layouts/AppLayout.vue"
import api from "@/api/axios"

import { useLessonsStore } from "@/stores/lessons"
import { useChildrenStore } from "@/stores/children"

const router = useRouter()

const lessonsStore = useLessonsStore()
const childrenStore = useChildrenStore()

const children = ref([])
const subjects = ref([])
const topics = ref([])

const loading = ref(false)
const error = ref("")

const form = ref({
  child: "",
  subject: "",
  topic: "",
  title: "",
  content: "",
})

/* LOAD TOPICS */
watch(() => form.value.subject, async (val) => {

  if (!val) {
    topics.value = []
    return
  }

  try {

    const res = await api.get(
      `/lessons/topics/?subject=${val}`
    )

    topics.value = res.data

  } catch (e) {

    console.error(e)

  }

})

/* LOAD */
onMounted(async () => {

  try {

    await childrenStore.fetchChildren()

    children.value = childrenStore.children

    const subjectsRes = await api.get(
      "/lessons/subjects/"
    )

    subjects.value = subjectsRes.data

  } catch (e) {

    console.error(e)

  }

})

/* SAVE */
const saveLesson = async () => {

  error.value = ""

  if (!form.value.child) {
    error.value = "Select child"
    return
  }

  if (!form.value.title) {
    error.value = "Enter lesson title"
    return
  }

  try {

    loading.value = true

    await lessonsStore.addLesson(
      form.value.child,
      {
        title: form.value.title,
        content: form.value.content,
        subject: form.value.subject || null,
        topic: form.value.topic || null,
      }
    )

    router.push("/lessons")

  } catch (e) {

    console.error(e)

    error.value =
      e.response?.data?.detail ||
      "Failed to create lesson"

  } finally {

    loading.value = false

  }

}
</script>