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
            v-if="!isChild"
            @click="activeTab = 'lessons'"
            class="px-4 py-2 rounded-xl border"
            :class="activeTab === 'lessons' ? 'bg-blue-600 text-white' : ''"
          >
            Lessons
          </button>

          <button
            v-if="!isChild"
            @click="activeTab = 'subjects'"
            class="px-4 py-2 rounded-xl border"
            :class="activeTab === 'subjects' ? 'bg-blue-600 text-white' : ''"
          >
            Subjects & Topics
          </button>


          <button
            v-if="!isChild"
            @click="activeTab = 'create'"
            class="px-4 py-2 rounded-xl border"
            :class="activeTab === 'create'
              ? 'bg-blue-600 text-white'
              : ''"
          >
            Create Lesson
          </button>

      </div>


    </div>
    <!-- FILTERS -->
    <div
      class="
        bg-white
        border
        rounded-2xl
        p-5
        mb-6
      "
    >

      <div
      :class="[
        'grid grid-cols-1 md:grid-cols-2 gap-4',
        isChild ? 'lg:grid-cols-4' : 'lg:grid-cols-5'
      ]"
      >

        <!-- SEARCH -->
        <input
          v-model="filters.search"
          placeholder="Search lessons..."
          class="border rounded-xl px-4 py-3"
        />

        <!-- CHILD -->
        <select
          v-if="!isChild"
          v-model="filters.child"
          class="border rounded-xl px-4 py-3"
        >
          <option value="">
            All children
          </option>

          <option
            v-for="child in children"
            :key="child.id"
            :value="child.id"
          >
            {{ child.first_name }}
          </option>

        </select>

        <!-- STATUS -->
        <select
          v-model="filters.status"
          class="border rounded-xl px-4 py-3"
        >
          <option value="">
            All statuses
          </option>

          <option value="draft">
            Draft
          </option>

          <option value="in_progress">
            In Progress
          </option>

          <option value="completed">
            Completed
          </option>

        </select>

        <!-- SUBJECT -->
        <select
          v-model="filters.subject"
          class="border rounded-xl px-4 py-3"
        >
          <option value="">
            All subjects
          </option>

          <option
            v-for="subject in subjects"
            :key="subject.id"
            :value="subject.id"
          >
            {{ subject.name }}
          </option>

        </select>

        <!-- ORDER -->
        <select
          v-model="filters.ordering"
          class="border rounded-xl px-4 py-3"
        >
          <option value="-created_at">
            Newest
          </option>

          <option value="created_at">
            Oldest
          </option>

          <option value="title">
            Title A-Z
          </option>

          <option value="-title">
            Title Z-A
          </option>

          <option value="-progress">
            Progress ↓
          </option>

          <option value="progress">
            Progress ↑
          </option>

        </select>

      </div>

      <div class="flex gap-3 mt-4">

        <button
          @click="applyFilters"
          class="
            bg-blue-600
            text-white
            px-4
            py-2
            rounded-xl
          "
        >
          Apply
        </button>

        <button
          @click="resetFilters"
          class="
            border
            px-4
            py-2
            rounded-xl
          "
        >
          Reset
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





    <!-- CREATE LESSON TAB -->
    <div
      v-if="
        activeTab === 'create' &&
        !isChild
      "
      class="max-w-4xl mx-auto"
    >

      <div class="bg-white border rounded-2xl p-6">

        <h2 class="text-2xl font-semibold mb-6">
          Create Lesson
        </h2>

        <!-- CHILD -->
        <!-- CHILDREN -->
        <div class="mb-4">

          <label class="block text-sm font-medium mb-2">
            Children
          </label>

          <!-- DROPDOWN BUTTON -->
          <button
            type="button"
            @click="showChildren = !showChildren"
            class="
              w-full
              border
              rounded-xl
              px-4
              py-3
              bg-white
              flex
              items-center
              justify-between
              hover:border-blue-400
            "
          >
            <div class="text-left">

              <div
                v-if="lessonForm.children.length"
                class="font-medium"
              >
                {{ lessonForm.children.length }}
                selected
              </div>

              <div
                v-if="selectedChildrenNames"
                class="text-sm text-slate-500 truncate"
              >
                {{ selectedChildrenNames }}
              </div>

              <div
                v-else
                class="text-slate-400"
              >
                Select children
              </div>

            </div>

            <span>
              {{ showChildren ? "▲" : "▼" }}
            </span>

          </button>

          <!-- DROPDOWN CONTENT -->
          <div
            v-if="showChildren"
            class="
              mt-2
              border
              rounded-xl
              bg-white
              p-4
              shadow-lg
            "
          >

            <div
              class="
                flex
                justify-between
                mb-4
                text-sm
              "
            >

              <button
                type="button"
                @click="selectAllChildren"
                class="text-blue-600 hover:underline"
              >
                Select all
              </button>

              <button
                type="button"
                @click="clearChildren"
                class="text-red-500 hover:underline"
              >
                Clear
              </button>

            </div>

            <div
              class="
                max-h-60
                overflow-y-auto
                space-y-2
              "
            >

              <label
                v-for="child in children"
                :key="child.id"
                class="
                  flex
                  items-center
                  gap-3
                  p-2
                  rounded-lg
                  hover:bg-slate-50
                  cursor-pointer
                "
              >

                <input
                  type="checkbox"
                  :value="child.id"
                  v-model="lessonForm.children"
                />

                <span>
                  {{ child.first_name }}
                </span>

              </label>

            </div>

          </div>

        </div>
        <!-- SUBJECT -->
        <select
          v-model="lessonForm.subject"
          class="w-full border rounded-xl px-4 py-3 mb-4"
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

        <!-- TOPIC -->
        <select
          v-model="lessonForm.topic"
          class="w-full border rounded-xl px-4 py-3 mb-4"
        >
          <option value="">
            Select topic
          </option>

          <option
            v-for="topic in createTopics"
            :key="topic.id"
            :value="topic.id"
          >
            {{ topic.name }}
          </option>

        </select>

        <!-- TITLE -->
        <input
          v-model="lessonForm.title"
          placeholder="Lesson title"
          class="w-full border rounded-xl px-4 py-3 mb-4"
        />

        <!-- CONTENT -->
        <textarea
          v-model="lessonForm.content"
          rows="8"
          placeholder="Lesson content..."
          class="w-full border rounded-xl px-4 py-3 mb-4"
        />

        <button
          @click="createLesson"
          class="bg-green-600 text-white px-6 py-3 rounded-xl hover:bg-green-700"
        >
          Create Lesson
        </button>

      </div>

    </div>

    <!-- SUBJECTS TAB -->
    <div
      v-if="
        activeTab === 'subjects' &&
        !isChild
      "
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
            <div
              v-if="subjectSuccess"
              class="
                bg-green-50
                border
                border-green-200
                text-green-700
                p-3
                rounded-xl
                mb-3
              "
            >
              {{ subjectSuccess }}
            </div>
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
        <div
          v-if="subjectError"
          class="
            bg-red-50
            border
            border-red-200
            text-red-700
            p-3
            rounded-xl
            mb-3
          "
        >
          {{ subjectError }}
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
import { ref, computed, onMounted, watch } from "vue"
import { useRouter } from "vue-router"

import AppLayout from "@/layouts/AppLayout.vue"
import api from "@/api/axios"
import { useLessonsStore } from "@/stores/lessons"
import { useAuthStore } from "@/stores/auth"



const activeTab = ref("lessons")

/* FILTERS */
const filters = ref({
  search: "",
  child: "",
  status: "",
  subject: "",
  ordering: "-created_at",
})

/* CREATE LESSON */
const children = ref([])

const lessonForm = ref({
  children: [],
  subject: "",
  topic: "",
  title: "",
  content: "",
})

const createTopics = ref([])
const filterTopics = ref([])
/* SUBJECTS */
const subjects = ref([])

const creating = ref(false)
const form = ref({ name: "" })
const subjectError = ref("")
const subjectSuccess = ref("")
const errorMessage = ref("")
const successMessage = ref("")

const showDeleteModal = ref(false)
const deleteSubjectId = ref(null)


const lessonToDelete = ref(null)
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

/* LOAD TOPICS FOR CREATE LESSON */
watch(
  () => lessonForm.value.subject,
  async (subjectId) => {

    if (!subjectId) {
      createTopics.value = []
      lessonForm.value.topic = ""
      return
    }

    try {

      const res = await api.get(
        `/lessons/topics/?subject=${subjectId}`
      )

      createTopics.value = res.data

    } catch (error) {

      console.error(error)

      createTopics.value = []

    }
  }
)
watch(
  () => filters.value.subject,
  async (subjectId) => {

    if (!subjectId) {

      filterTopics.value = []

      return
    }

    try {

      const res = await api.get(
        `/lessons/topics/?subject=${subjectId}`
      )

      filterTopics.value = res.data

    } catch (error) {

      console.error(error)

      filterTopics.value = []

    }

  }
)



/* LOAD */
onMounted(async () => {

  await lessonsStore.fetchAllLessons()

  await loadSubjects()

  const childrenRes = await api.get("/children/")

  children.value = childrenRes.data

})


/* CREATE LESSON */
const createLesson = async () => {

  if (
    !lessonForm.value.children.length ||
    !lessonForm.value.title
  ) {
    errorMessage.value =
        "Select at least one child and enter title"
    return
  }

  try {

    for (const childId of lessonForm.value.children) {

      await lessonsStore.addLesson(
        childId,
        {
          subject: lessonForm.value.subject || null,
          topic: lessonForm.value.topic || null,
          title: lessonForm.value.title,
          content: lessonForm.value.content,
        }
      )

    }

    lessonForm.value = {
      children: [],
      subject: "",
      topic: "",
      title: "",
      content: "",
    }

    createTopics.value = []

    await lessonsStore.fetchAllLessons()

    activeTab.value = "lessons"

  } catch (error) {

    console.error(error)

    errorMessage.value =
      error.response?.data?.detail ||
      "Failed to create lesson"

  }
}
const showChildren = ref(false)

const selectAllChildren = () => {
  lessonForm.value.children =
    children.value.map(child => child.id)
}

const clearChildren = () => {
  lessonForm.value.children = []
}

/* LESSON FILTERS */
const applyFilters = async () => {

  try {

    const params = {}

    if (filters.value.search) {
      params.search = filters.value.search
    }

    if (filters.value.child) {
      params.child = filters.value.child
    }

    if (filters.value.status) {
      params.status = filters.value.status
    }

    if (filters.value.subject) {
      params.subject = filters.value.subject
    }

    if (filters.value.ordering) {
      params.ordering = filters.value.ordering
    }

    const res = await api.get(
      "/lessons/",
      {
        params
      }
    )

    lessonsStore.lessons = res.data

  } catch (error) {

    console.error(
      "Filter error:",
      error
    )

  }
}

const resetFilters = async () => {

  filters.value = {
    search: "",
    child: "",
    status: "",
    subject: "",
    ordering: "-created_at",
  }

  filterTopics.value = []

  await lessonsStore.fetchAllLessons()
}

/* OPEN */
const openLesson = (id) => {
  router.push(`/lessons/${id}`)
}

/* EDIT */
const editLesson = (id) => {
  router.push(`/lessons/${id}?edit=true`)
}

/* DELETE */
const deleteLesson = (id) => {

  lessonToDelete.value = id

  showDeleteModal.value = true
}
/*Confirm delete*/

const confirmDeleteLesson = async () => {

  if (!lessonToDelete.value) {
    return
  }

  try {

    await lessonsStore.deleteLesson(
      lessonToDelete.value
    )

    successMessage.value =
      "Lesson deleted successfully"

  } catch (e) {

    errorMessage.value =
      e.response?.data?.detail ||
      "Failed to delete lesson"

  } finally {

    showDeleteModal.value = false

    lessonToDelete.value = null
  }
}


/* FORMAT CONTENT */
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

/* SUBJECTS CRUD */
const createSubject = async () => {

  subjectError.value = ""
  subjectSuccess.value = ""

  try {

    await api.post(
      "/lessons/subjects/",
      form.value
    )

    form.value.name = ""

    creating.value = false

    subjectSuccess.value =
      "Subject created successfully"

    await loadSubjects()

  } catch (error) {

    console.error(
      "CREATE SUBJECT ERROR:",
      error
    )

    const data =
      error.response?.data

    if (data?.detail) {

      subjectError.value =
        data.detail

    } else if (data?.name?.length) {

      subjectError.value =
        data.name[0]

    } else {

      subjectError.value =
        "Failed to create subject"

    }
  }
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

  errorMessage.value = ""

  try {

    await api.patch(
      `/lessons/subjects/${id}/`,
      editForm.value
    )

    editingId.value = null

    successMessage.value =
      "Subject updated"

    await loadSubjects()

  } catch (e) {

    errorMessage.value =
      e.response?.data?.detail ||
      e.response?.data?.name?.[0] ||
      "Failed to update subject"
  }
}

/* TREE */
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

  errorMessage.value = ""

  try {

    await api.post(
      "/lessons/topics/",
      {
        subject: subjectId,
        name: newTopic.value
      }
    )

    newTopic.value = ""

    addingTopicFor.value = null

    successMessage.value =
      "Topic created"

    await loadSubjects()

  } catch (e) {

    errorMessage.value =
      e.response?.data?.detail ||
      e.response?.data?.name?.[0] ||
      "Failed to create topic"
  }
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

/* AUTO FILTER */
watch(
  filters,
  async () => {

    await applyFilters()

  },
  {
    deep: true
  }
)
</script>