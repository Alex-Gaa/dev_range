<template>
  <div
    v-if="show"
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

    <div
      class="
        bg-white
        rounded-2xl
        p-6
        w-full
        max-w-md
      "
    >

      <h3 class="text-xl font-bold mb-3">
        {{ title }}
      </h3>

      <p class="text-slate-600 mb-5">
        {{ message }}
      </p>

      <div class="flex justify-end gap-3">

        <button
          @click="$emit('cancel')"
          class="
            border
            px-4
            py-2
            rounded-xl
          "
        >
          Cancel
        </button>

        <button
          @click="$emit('confirm')"
          class="
            bg-red-600
            hover:bg-red-700
            text-white
            px-4
            py-2
            rounded-xl
          "
        >
          Confirm
        </button>

      </div>

    </div>

  </div>
</template>

<script setup>
defineProps({
  show: Boolean,
  title: String,
  message: String,
})

defineEmits([
  "confirm",
  "cancel",
])
</script>