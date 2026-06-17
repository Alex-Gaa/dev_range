<template>
  <AppLayout>
    <div class="max-w-4xl mx-auto space-y-6">

      <!-- HEADER -->
      <div class="bg-white border rounded-2xl p-8">
        <h1 class="text-3xl font-bold">Billing</h1>
        <p class="text-slate-500 mt-2">
          Manage your subscription and billing settings
        </p>
      </div>

      <!-- CURRENT SUB -->
      <div
        v-if="billingStore.subscription"
        class="bg-white border rounded-2xl p-8 space-y-3"
      >
        <h2 class="text-xl font-semibold mb-2">Current subscription</h2>

        <div class="flex justify-between">
          <span>Plan</span>
          <span class="font-medium">{{ billingStore.subscription.plan }}</span>
        </div>

        <div class="flex justify-between">
          <span>Status</span>
          <span class="font-medium">{{ billingStore.subscription.status }}</span>
        </div>

        <div class="flex justify-between">
          <span>Lessons used</span>
          <span>{{ billingStore.subscription.lessons_used }}</span>
        </div>

        <div class="flex justify-between">
          <span>Expires</span>
          <span>{{ billingStore.subscription.expires_at }}</span>
        </div>

        <button
          v-if="billingStore.subscription.plan !== 'family'"
          @click="openCheckout('family')"
          class="mt-4 bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-xl"
        >
          Upgrade plan
        </button>
      </div>

      <!-- PLANS -->
      <div class="grid md:grid-cols-3 gap-4">

        <div
          v-for="plan in plans"
          :key="plan.id"
          class="bg-white border rounded-2xl p-6 space-y-3"
        >
          <h3 class="text-xl font-semibold">{{ plan.title }}</h3>
          <p class="text-slate-500">{{ plan.description }}</p>

          <div class="text-2xl font-bold">
            {{ plan.price }} ₽
          </div>

          <ul class="text-sm text-slate-600 space-y-1">
            <li>✔ {{ plan.lessons }} lessons</li>
            <li>✔ {{ plan.children }} children</li>
            <li>✔ AI learning access</li>
          </ul>

          <button
            @click="openCheckout(plan.id)"
            class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2 rounded-xl"
          >
            Choose plan
          </button>
        </div>

      </div>

      <!-- FAKE CHECKOUT MODAL -->
      <div
        v-if="checkoutPlan"
        class="fixed inset-0 bg-black/50 flex items-center justify-center"
      >
        <div class="bg-white rounded-2xl p-6 w-[420px] space-y-4">

          <h2 class="text-xl font-bold">
            Confirm payment
          </h2>

          <p>
            You selected <b>{{ checkoutPlan }}</b> plan
          </p>

          <div class="bg-slate-50 p-3 rounded-lg text-sm">
            This is a test payment. No real money will be charged.
          </div>

          <div class="flex gap-2 justify-end">

            <button
              @click="checkoutPlan = null"
              class="px-4 py-2 rounded-lg border"
            >
              Cancel
            </button>

            <button
              @click="pay"
              class="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg"
            >
              Pay now
            </button>

          </div>

        </div>
      </div>

    </div>
  </AppLayout>
</template>
<script setup>
import { onMounted, ref } from "vue"
import AppLayout from "@/layouts/AppLayout.vue"
import { useBillingStore } from "@/stores/billing"

const billingStore = useBillingStore()

const checkoutPlan = ref(null)

const plans = [
  {
    id: "free",
    title: "Free",
    description: "Basic access",
    price: 0,
    lessons: 5,
    children: 1
  },
  {
    id: "basic",
    title: "Basic",
    description: "For regular learning",
    price: 299,
    lessons: 50,
    children: 3
  },
  {
    id: "family",
    title: "Family",
    description: "Full access for family",
    price: 599,
    lessons: 200,
    children: 10
  }
]

onMounted(async () => {
  await billingStore.fetchSubscription()
})

const openCheckout = (planId) => {
  checkoutPlan.value = planId
}

const pay = async () => {
  const plan = checkoutPlan.value
  checkoutPlan.value = null

  // симуляция задержки оплаты
  await new Promise(r => setTimeout(r, 800))

  await billingStore.activate(plan)
  await billingStore.fetchSubscription()
}
</script>