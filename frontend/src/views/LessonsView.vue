<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\LessonsView.vue-->
<template>
  <AppLayout>

    <!-- HEADER -->
    <div class="mb-8">

      <h1 class="text-3xl font-bold">
        All Lessons
      </h1>

      <p class="text-slate-500 mt-2">
        Lessons from all children
      </p>

      <div class="flex gap-3 mt-6">

          <button
            @click="activeTab = 'lessons'"
            class="px-4 py-2 rounded-xl border"
            :class="activeTab === 'lessons' ? 'bg-blue-600 text-white' : ''"
          >
            Lessons
          </button>

          <button
            @click="activeTab = 'subjects'"
            class="px-4 py-2 rounded-xl border"
            :class="activeTab === 'subjects' ? 'bg-blue-600 text-white' : ''"
          >
            Subjects & Topics
          </button>

        </div>

    </div>

    <!-- LESSONS TAB -->
    <div v-if="activeTab === 'lessons'">

      <!-- EMPTY -->
      <div
        v-if="!lessonsStore.lessons?.length"
        class="bg-white border rounded-2xl p-10 text-center"
      >
        <h2 class="text-2xl font-semibold">
          No lessons yet
        </h2>

        <p class="text-slate-500 mt-3">
          Generate first lesson for a child
        </p>
      </div>

      <!-- LESSONS -->
      <div
        v-else
        class="grid grid-cols-1 lg:grid-cols-2 gap-6"
      >

        <div
          v-for="lesson in lessonsStore.lessons"
          :key="lesson.id"
          class="
            bg-white
            border
            rounded-2xl
            p-6
            transition-all
            hover:shadow-lg
            hover:-translate-y-1
          "
        >

          <!-- TOP -->
          <div class="flex items-start justify-between">

            <div
              class="cursor-pointer"
              @click="openLesson(lesson.id)"
            >

              <h2 class="text-xl font-semibold">
                {{ lesson.title }}
              </h2>

              <p class="text-slate-500 mt-1">
                Child:
                {{ lesson.child_name || "Unknown" }}
              </p>

              <!-- SUBJECT / TOPIC -->
              <div class="flex gap-2 mt-3 flex-wrap">

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

            <!-- STATUS -->
            <div
              class="px-3 py-1 rounded-full text-sm font-medium"
              :class="statusClass(lesson.status)"
            >
              {{ formatStatus(lesson.status) }}
            </div>

          </div>

          <!-- CONTENT PREVIEW -->
          <div
            class="mt-5 cursor-pointer"
            @click="openLesson(lesson.id)"
          >

            <p class="text-slate-700 line-clamp-4">
              {{ formatContent(lesson.content) }}
            </p>

          </div>

          <!-- PROGRESS -->
          <div class="mt-6">

            <div class="flex items-center justify-between mb-2">

              <span class="text-sm text-slate-500">
                Progress
              </span>

              <span class="text-sm font-medium">
                {{ lesson.progress }}%
              </span>

            </div>

            <div class="w-full h-3 bg-slate-100 rounded-full overflow-hidden">

              <div
                class="h-full bg-blue-600 rounded-full transition-all"
                :style="{ width: `${lesson.progress}%` }"
              />

            </div>

          </div>

          <!-- ACTIONS -->
          <div
            v-if="!isChild"
            class="flex gap-3 mt-6"
          >

            <button
              class="px-4 py-2 rounded-xl bg-blue-600 text-white hover:bg-blue-700"
              @click.stop="editLesson(lesson.id)"
            >
              Edit
            </button>

            <button
              class="px-4 py-2 rounded-xl bg-red-600 text-white hover:bg-red-700"
              @click.stop="deleteLesson(lesson.id)"
            >
              Delete
            </button>

          </div>

        </div>

      </div>

    </div>

    <!-- SUBJECTS TAB -->
    <div
      v-if="activeTab === 'subjects'"
      class="max-w-4xl mx-auto p-6 space-y-6"
    >

      <!-- HEADER -->
      <div class="flex items-center justify-between">

        <h1 class="text-2xl font-bold">
          Subjects & Topics
        </h1>

        <button
          @click="creating = true"
          class="bg-blue-600 text-white px-4 py-2 rounded-xl"
        >
          + Add Subject
        </button>

      </div>

      <!-- CREATE SUBJECT -->
      <div
        v-if="creating"
        class="bg-white border rounded-xl p-4 space-y-3"
      >

        <input
          v-model="form.name"
          placeholder="Subject name"
          class="w-full border rounded-lg px-3 py-2"
        />

        <div class="flex gap-2">

          <button
            @click="createSubject"
            class="bg-green-600 text-white px-4 py-2 rounded-lg"
          >
            Save
          </button>

          <button
            @click="creating = false"
            class="text-gray-500"
          >
            Cancel
          </button>

        </div>

      </div>

      <!-- TREE -->
      <div class="bg-white border rounded-xl divide-y">

        <div
          v-for="subject in subjects"
          :key="subject.id"
          class="p-4"
        >

          <!-- SUBJECT ROW -->
          <div class="flex items-center justify-between group">

            <!-- EDIT -->
            <div
              v-if="editingId === subject.id"
              class="flex gap-2 w-full"
            >

              <input
                v-model="editForm.name"
                class="flex-1 border rounded px-3 py-2"
              />

              <button
                @click="saveEdit(subject.id)"
                class="bg-green-600 text-white px-3 py-2 rounded"
              >
                Save
              </button>

              <button
                @click="cancelEdit"
                class="text-gray-500"
              >
                Cancel
              </button>

            </div>

            <!-- VIEW -->
            <div
              v-else
              class="flex items-center justify-between w-full cursor-pointer"
              @click="toggle(subject.id)"
            >

              <div>

                <div class="font-semibold">
                  {{ subject.name }}
                </div>

                <div class="text-xs text-slate-400">
                  {{ subject.topics.length }} topics
                </div>

              </div>

              <div class="opacity-0 group-hover:opacity-100 flex gap-2">

                <button
                  @click.stop="startEdit(subject)"
                  class="text-blue-600"
                >
                  Edit
                </button>

                <button
                  @click.stop="deleteSubject(subject.id)"
                  class="text-red-500"
                >
                  Delete
                </button>

              </div>

            </div>

          </div>

          <!-- TOPICS -->
          <div
            v-if="openSubjects.includes(subject.id)"
            class="ml-4 mt-3 space-y-2"
          >

            <div
              v-for="topic in subject.topics"
              :key="topic.id"
              class="flex justify-between text-sm group"
            >

              <span class="text-slate-600">
                {{ topic.name }}
              </span>

              <button
                @click="deleteTopic(topic.id)"
                class="opacity-0 group-hover:opacity-100 text-red-400"
              >
                ✕
              </button>

            </div>

            <div
              v-if="addingTopicFor === subject.id"
              class="mt-2"
            >

              <input
                v-model="newTopic"
                placeholder="New topic"
                class="w-full border rounded px-3 py-2 text-sm"
              />

              <div class="flex gap-2 mt-2">

                <button
                  @click="saveTopic(subject.id)"
                  class="bg-green-600 text-white px-3 py-1 rounded text-sm"
                >
                  Add
                </button>

                <button
                  @click="cancelTopic"
                  class="text-gray-500 text-sm"
                >
                  Cancel
                </button>

              </div>

            </div>

            <button
              v-else
              @click="addingTopicFor = subject.id"
              class="text-blue-600 text-sm mt-2"
            >
              + Add topic
            </button>

          </div>

        </div>

      </div>

    </div>



   </AppLayout>
</template>

<script setup>
import { ref, computed, onMounted } from "vue"
import { useRouter } from "vue-router"

import AppLayout from "@/layouts/AppLayout.vue"
import api from "@/api/axios"
import { useLessonsStore } from "@/stores/lessons"
import { useAuthStore } from "@/stores/auth"

const activeTab = ref("lessons")
const subjects = ref([])

const creating = ref(false)
const form = ref({ name: "" })

const editingId = ref(null)
const editForm = ref({ name: "" })

const openSubjects = ref([])

const addingTopicFor = ref(null)
const newTopic = ref("")


const router = useRouter()

const lessonsStore = useLessonsStore()
const authStore = useAuthStore()

/* ROLE */
const isChild = computed(() => {
  return authStore.user?.role === "child"
})

onMounted(async () => {

  await lessonsStore.fetchAllLessons()

  await loadSubjects()

})

/* OPEN */
const openLesson = (id) => {
  router.push(`/lessons/${id}`)
}

/* EDIT */
const editLesson = (id) => {
  router.push(`/lessons/${id}?edit=true`)
}

/* DELETE */
const deleteLesson = async (id) => {

  if (!confirm("Delete this lesson?")) return

  await lessonsStore.deleteLesson(id)
}

/* FORMAT CONTENT (SAFE for AI JSON) */
const formatContent = (content) => {

  if (!content) return ""

  if (typeof content === "string") {

    try {
      const parsed = JSON.parse(content)

      return (
        parsed.introduction ||
        parsed.theory ||
        parsed.title ||
        JSON.stringify(parsed).slice(0, 200)
      )

    } catch {
      return content
    }
  }

  if (typeof content === "object") {
    return (
      content.introduction ||
      content.theory ||
      content.title ||
      ""
    )
  }

  return ""
}

/* STATUS */
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


/* LOAD SUBJECTS */
const loadSubjects = async () => {

  const res = await api.get("/lessons/subjects/")

  const subjectsData = res.data

  const enriched = []

  for (const s of subjectsData) {

    try {

      const topicsRes = await api.get(
        `/lessons/topics/?subject=${s.id}`
      )

      enriched.push({
        ...s,
        topics: topicsRes.data || []
      })

    } catch {

      enriched.push({
        ...s,
        topics: []
      })

    }

  }

  subjects.value = enriched
}

/* SUBJECTS */
const createSubject = async () => {

  await api.post(
    "/lessons/subjects/",
    form.value
  )

  form.value.name = ""
  creating.value = false

  await loadSubjects()
}

const deleteSubject = async (id) => {

  await api.delete(
    `/lessons/subjects/${id}/`
  )

  await loadSubjects()
}

const startEdit = (subject) => {

  editingId.value = subject.id

  editForm.value = {
    name: subject.name
  }
}

const cancelEdit = () => {
  editingId.value = null
}

const saveEdit = async (id) => {

  await api.patch(
    `/lessons/subjects/${id}/`,
    editForm.value
  )

  editingId.value = null

  await loadSubjects()
}

const toggle = (id) => {

  if (openSubjects.value.includes(id)) {

    openSubjects.value =
      openSubjects.value.filter(
        i => i !== id
      )

  } else {

    openSubjects.value.push(id)

  }
}

/* TOPICS */
const saveTopic = async (subjectId) => {

  if (!newTopic.value.trim()) return

  await api.post(
    "/lessons/topics/",
    {
      subject: subjectId,
      name: newTopic.value
    }
  )

  newTopic.value = ""

  addingTopicFor.value = null

  await loadSubjects()
}

const cancelTopic = () => {
  addingTopicFor.value = null
}

const deleteTopic = async (id) => {

  await api.delete(
    `/lessons/topics/${id}/`
  )

  await loadSubjects()
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