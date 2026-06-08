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
          {{ child.first_name }} {{ child.last_name || "" }}
        </h3>

        <p class="text-slate-500">
          {{ child.age }} лет от роду
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

      <p v-if="child.email">
        <span class="font-medium">Email:</span>
        {{ child.email }}
      </p>

    </div>

    <!-- INVITE -->
    <div
      v-if="child.has_account"
      class="
        mt-5
        p-4
        rounded-xl
        bg-green-50
        border
        border-green-100
      "
    >

      <div class="flex items-center justify-between">

        <p class="text-green-700 font-medium text-sm">
          Invite link generated
        </p>

        <button
          @click.stop="copyInviteLink"
          class="
            text-xs
            bg-green-600
            hover:bg-green-700
            text-white
            px-3
            py-1
            rounded-lg
            transition
          "
        >
          Copy
        </button>

      </div>

      <a
        :href="fullInviteLink"
        target="_blank"
        class="
          text-xs
          text-blue-600
          break-all
          mt-3
          block
          hover:underline
        "
        @click.stop
      >
        {{ fullInviteLink }}
      </a>

    </div>
    <!-- COPY SUCCESS -->
    <div
      v-if="successMessage"
      class="
        mt-4
        bg-green-50
        border
        border-green-200
        text-green-700
        p-3
        rounded-xl
        text-sm
      "
    >
      {{ successMessage }}
    </div>

  </div>
</template>

<script setup>

import { useRouter } from "vue-router"

import { computed, ref } from "vue"

const successMessage = ref("")

const props = defineProps({
  child: Object,
})

const router = useRouter()

/* FULL INVITE LINK */
const fullInviteLink = computed(() => {

  if (!props.child?.invite_link) {
    return ""
  }

  return `${window.location.origin}${props.child.invite_link}`
})

/* COPY */
const copyInviteLink = async () => {

  try {

    await navigator.clipboard.writeText(
      fullInviteLink.value
    )

    successMessage.value =
      "Invite link copied"

    setTimeout(() => {
      successMessage.value = ""
    }, 3000)

  } catch {

    successMessage.value =
      "Failed to copy invite link"
  }
}

/* OPEN CHILD */
const openChild = () => {
  router.push(`/children/${props.child.id}`)
}
</script>