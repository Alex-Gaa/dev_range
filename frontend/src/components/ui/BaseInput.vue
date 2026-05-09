<script setup>
defineProps({
  modelValue: String,
  type: {
    type: String,
    default: "text",
  },
  placeholder: String,
})

const emit = defineEmits(["update:modelValue"])
</script>

<template>

  <input
    :value="modelValue"
    :type="type"
    :placeholder="placeholder"
    @input="emit('update:modelValue', $event.target.value)"
    class="
      w-full
      border
      rounded-xl
      p-3
      outline-none
      focus:ring-2
      focus:ring-blue-500
    "
  />

</template>