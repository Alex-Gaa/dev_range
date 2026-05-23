<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\SubjectsView.vue -->
<template>
  <AppLayout>

    <div class="max-w-4xl mx-auto p-6 space-y-6">

      <!-- HEADER -->
      <div class="flex items-center justify-between">
        <h1 class="text-2xl font-bold">Subjects & Topics</h1>

        <button
          @click="creating = true"
          class="bg-blue-600 text-white px-4 py-2 rounded-xl"
        >
          + Add Subject
        </button>
      </div>

      <!-- CREATE SUBJECT -->
      <div v-if="creating" class="bg-white border rounded-xl p-4 space-y-3">

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
            <div v-if="editingId === subject.id" class="flex gap-2 w-full">

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

            <!-- LIST -->
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

            <!-- ADD TOPIC -->
            <div v-if="addingTopicFor === subject.id" class="mt-2">

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
import { ref, onMounted } from "vue"
import api from "@/api/axios"
import AppLayout from "@/layouts/AppLayout.vue"

const subjects = ref([])

/* UI STATE */
const creating = ref(false)
const form = ref({ name: "" })

const editingId = ref(null)
const editForm = ref({ name: "" })

const openSubjects = ref([])

const addingTopicFor = ref(null)
const newTopic = ref("")

/* LOAD */
const load = async () => {
  const res = await api.get("/lessons/subjects/")

  const subjectsData = res.data

  const enriched = []

  for (const s of subjectsData) {
    try {
      const topicsRes = await api.get(`lessons/topics/?subject=${s.id}`)

      enriched.push({
        ...s,
        topics: topicsRes.data || []
      })

    } catch (e) {
      enriched.push({
        ...s,
        topics: []
      })
    }
  }

  subjects.value = enriched
}

onMounted(load)

/* SUBJECTS */
const createSubject = async () => {
  try {

    const res = await api.post("/lessons/subjects/", form.value)

    console.log(res.data)

    form.value.name = ""
    creating.value = false

    await load()

  } catch (e) {

    console.log(e.response.data)

  }
}

const deleteSubject = async (id) => {
  await api.delete(`lessons/subjects/${id}/`)
  await load()
}

const startEdit = (subject) => {
  editingId.value = subject.id
  editForm.value = { name: subject.name }
}

const cancelEdit = () => {
  editingId.value = null
}

const saveEdit = async (id) => {
  await api.patch(`lessons/subjects/${id}/`, editForm.value)

  editingId.value = null
  await load()
}

/* TOGGLE */
const toggle = (id) => {
  if (openSubjects.value.includes(id)) {
    openSubjects.value = openSubjects.value.filter(i => i !== id)
  } else {
    openSubjects.value.push(id)
  }
}

/* TOPICS */
const saveTopic = async (subjectId) => {

  if (!newTopic.value.trim()) return

  await api.post("lessons/topics/", {
    subject: subjectId,
    name: newTopic.value
  })

  newTopic.value = ""
  addingTopicFor.value = null

  await load()
}

const cancelTopic = () => {
  addingTopicFor.value = null
}

const deleteTopic = async (id) => {
  await api.delete(`lessons/topics/${id}/`)
  await load()
}
</script>