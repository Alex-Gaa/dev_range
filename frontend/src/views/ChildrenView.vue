<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\ChildrenView.vue-->
<template>
  <AppLayout>

    <div class="flex items-center justify-between mb-8">

      <div>

        <h1 class="text-3xl font-bold">
          Children
        </h1>

        <p class="text-slate-500 mt-1">
          Manage your children
        </p>

      </div>

      <button
        @click="createError = ''; modalOpen = true"
        class="
          bg-blue-600
          hover:bg-blue-700
          text-white
          px-6
          py-3
          rounded-xl
        "
      >
        Add child
      </button>

    </div>

    <div
      v-if="childrenStore.loading"
      class="text-slate-500"
    >
      Loading...
    </div>

    <div
      v-else
      class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6"
    >

      <ChildCard
        v-for="child in childrenStore.children"
        :key="child.id"
        :child="child"
      />

    </div>

    <!-- MODAL -->

    <div
      v-if="modalOpen"
      class="
        fixed
        inset-0
        bg-black/40
        flex
        items-center
        justify-center
        z-50
      "
    >

    <AddChildModal
      :error="createError"
      @close="modalOpen = false"
      @submit="handleCreate"
    />

    </div>

  </AppLayout>
</template>

<script setup>
import { ref, onMounted } from "vue"

import AppLayout from "@/layouts/AppLayout.vue"
import { getErrorMessage } from "@/utils/errorHandler"

import ChildCard from "@/components/children/ChildCard.vue"
import AddChildModal from "@/components/children/AddChildModal.vue"

import { useChildrenStore } from "@/stores/children"

const childrenStore = useChildrenStore()

const modalOpen = ref(false)
const createError = ref("")

onMounted(() => {
  childrenStore.fetchChildren()
})

const handleCreate = async (data) => {

  createError.value = ""

  try {

    await childrenStore.addChild(data)

    modalOpen.value = false

  } catch (error) {

    console.log("HANDLE CREATE ERROR:", error)

    createError.value = getErrorMessage(error)

    console.log("CREATE ERROR VALUE:", createError.value)
  }
}
</script>