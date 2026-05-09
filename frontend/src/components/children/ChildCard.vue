<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\components\children\ChildCard.vue -->
<template>
  <div
    @click="openChild"
    class="
      bg-white
      rounded-2xl
      border
      p-6
      cursor-pointer
      transition-all
      hover:shadow-lg
      hover:-translate-y-1
    "
  >

    <div class="flex items-center justify-between">

      <div>

        <h3 class="text-xl font-semibold">
          {{ child.first_name }}
        </h3>

        <p class="text-slate-500">
          {{ child.age }} years old
        </p>

      </div>

      <div
        class="
          w-14
          h-14
          rounded-full
          bg-blue-600
          text-white
          flex
          items-center
          justify-center
          font-bold
          text-xl
        "
      >
        {{ child.first_name.charAt(0) }}
      </div>

    </div>

    <div class="mt-5 space-y-2">

      <p>
        <span class="font-medium">Grade:</span>
        {{ child.grade }}
      </p>

      <p>
        <span class="font-medium">Interests:</span>
        {{ child.interests || "—" }}
      </p>

    </div>

    <div
      v-if="child.has_account"
      class="mt-5 p-4 rounded-xl bg-green-50"
    >
      <p class="text-green-700 font-medium text-sm">
        Invite link generated
      </p>

      <p class="text-xs text-slate-500 break-all mt-2">
        {{ child.invite_link }}
      </p>
    </div>

  </div>
</template>

<script setup>
import { useRouter } from "vue-router"

const props = defineProps({
  child: Object,
})

const router = useRouter()

const openChild = () => {
  router.push(`/children/${props.child.id}`)
}
</script>