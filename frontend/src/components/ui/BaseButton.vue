<script setup>
defineProps({
  variant: {
    type: String,
    default: "primary",
  },
})
</script>

<template>

  <button
    :class="[
      'px-5 py-3 rounded-xl transition font-medium',

      variant === 'primary'
        ? 'bg-blue-600 hover:bg-blue-700 text-white'

      : variant === 'secondary'
        ? 'bg-white border hover:bg-slate-100'

      : variant === 'danger'
        ? 'bg-red-500 hover:bg-red-600 text-white'

      : '',
    ]"
  >

    <slot />

  </button>

</template>