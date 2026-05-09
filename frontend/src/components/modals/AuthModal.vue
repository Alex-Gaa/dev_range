<script setup>
defineProps({
  isOpen: Boolean,
})

const emit = defineEmits(["close"])

const closeModal = () => {
  emit("close")
}
</script>

<template>
  <div
    v-if="isOpen"
    class="fixed inset-0 z-50 flex items-center justify-center"
  >

    <!-- BACKDROP -->
    <div
      class="absolute inset-0 bg-black/40 backdrop-blur-sm"
      @click="closeModal"
    />

    <!-- MODAL -->
    <div class="relative w-full max-w-md bg-white rounded-3xl shadow-2xl p-8">

      <button
        @click="closeModal"
        class="absolute top-4 right-4 text-slate-400 hover:text-black"
      >
        ✕
      </button>

      <slot />

    </div>

  </div>
</template>