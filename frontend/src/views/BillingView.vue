<!-- C:\Users\Developer\PycharmProjects\devrange\frontend\src\views\BillingView.vue -->
<template>
  <AppLayout>

    <div class="max-w-3xl mx-auto space-y-6">

      <div class="bg-white border rounded-2xl p-8">

        <h1 class="text-3xl font-bold">
          Billing
        </h1>

        <p class="text-slate-500 mt-2">
          Manage your subscription
        </p>

      </div>

      <div
        v-if="billingStore.subscription"
        class="bg-white border rounded-2xl p-8 space-y-4"
      >

        <div class="flex justify-between">

          <span class="font-medium">
            Plan
          </span>

          <span>
            {{ billingStore.subscription.plan }}
          </span>

        </div>

        <div class="flex justify-between">

          <span class="font-medium">
            Status
          </span>

          <span>
            {{ billingStore.subscription.status }}
          </span>

        </div>

        <div class="flex justify-between">

          <span class="font-medium">
            Lessons Used
          </span>

          <span>
            {{
              billingStore.subscription.lessons_used
            }}
          </span>

        </div>

        <div class="flex justify-between">

          <span class="font-medium">
            Expires
          </span>

          <span>
            {{
              billingStore.subscription.expires_at
            }}
          </span>

        </div>

      </div>

      <div class="bg-white border rounded-2xl p-8">

        <h2 class="text-2xl font-semibold mb-4">
          Basic Plan
        </h2>

        <p class="text-slate-600 mb-6">
          50 AI lessons monthly
        </p>

        <button
          @click="activate"
          class="
            bg-blue-600
            hover:bg-blue-700
            text-white
            px-6
            py-3
            rounded-xl
          "
        >
          Activate Test Subscription
        </button>

      </div>

    </div>

  </AppLayout>
</template>

<script setup>
import { onMounted } from "vue"

import AppLayout from "@/layouts/AppLayout.vue"

import { useBillingStore } from "@/stores/billing"

const billingStore = useBillingStore()

onMounted(async () => {
  await billingStore.fetchSubscription()
})

const activate = async () => {

  await billingStore.activate(
    "basic"
  )
}
</script>